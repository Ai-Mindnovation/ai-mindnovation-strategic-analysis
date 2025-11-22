from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64
import pandas as pd
from io import BytesIO
import json
import logging

_logger = logging.getLogger(__name__)

class StrategicAnalysis(models.Model):
    _name = 'ai_mindnovation.strategic.analysis'
    _description = 'Análisis Estratégico AI Mindnovation'
    _rec_name = 'name'

    name = fields.Char(string='Nombre del Análisis', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', required=True, default=lambda self: self.env.user)
    file_importancia = fields.Binary(string='Archivo Importancia')
    file_desempeno = fields.Binary(string='Archivo Desempeño')
    date = fields.Datetime(string='Fecha de Análisis', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('processed', 'Procesado'),
        ('done', 'Finalizado')
    ], string='Estado', default='draft')
    
    # Resultados principales (texto legacy)
    dofa_result = fields.Text(string='Resultado DOFA')
    space_result = fields.Text(string='Resultado SPACE')
    mckinsey_result = fields.Text(string='Resultado McKinsey')
    valor_percibido_result = fields.Text(string='Resultado Valor Percibido')

    # ===== CAMPOS DOFA =====
    dofa_fortalezas = fields.Integer(
        string='Fortalezas',
        compute='_compute_dofa_analysis',
        store=True,
        help='Número de variables clasificadas como Fortaleza'
    )
    dofa_debilidades = fields.Integer(
        string='Debilidades',
        compute='_compute_dofa_analysis',
        store=True,
        help='Número de variables clasificadas como Debilidad'
    )
    dofa_oportunidades = fields.Integer(
        string='Oportunidades',
        compute='_compute_dofa_analysis',
        store=True,
        help='Número de variables clasificadas como Oportunidad'
    )
    dofa_amenazas = fields.Integer(
        string='Amenazas',
        compute='_compute_dofa_analysis',
        store=True,
        help='Número de variables clasificadas como Amenaza'
    )
    dofa_total = fields.Integer(
        string='Total Variables DOFA',
        compute='_compute_dofa_analysis',
        store=True
    )
    dofa_internas = fields.Integer(
        string='Variables Internas',
        compute='_compute_dofa_analysis',
        store=True,
        help='Fortalezas + Debilidades'
    )
    dofa_externas = fields.Integer(
        string='Variables Externas',
        compute='_compute_dofa_analysis',
        store=True,
        help='Oportunidades + Amenazas'
    )
    dofa_positivas = fields.Integer(
        string='Variables Positivas',
        compute='_compute_dofa_analysis',
        store=True,
        help='Fortalezas + Oportunidades'
    )
    dofa_negativas = fields.Integer(
        string='Variables Negativas',
        compute='_compute_dofa_analysis',
        store=True,
        help='Debilidades + Amenazas'
    )
    dofa_prop_internas = fields.Float(
        string='% Internas',
        compute='_compute_dofa_analysis',
        store=True,
        digits=(5, 2)
    )
    dofa_prop_externas = fields.Float(
        string='% Externas',
        compute='_compute_dofa_analysis',
        store=True,
        digits=(5, 2)
    )
    dofa_prop_positivas = fields.Float(
        string='% Positivas',
        compute='_compute_dofa_analysis',
        store=True,
        digits=(5, 2)
    )
    dofa_prop_negativas = fields.Float(
        string='% Negativas',
        compute='_compute_dofa_analysis',
        store=True,
        digits=(5, 2)
    )
    dofa_tipo_int_ext = fields.Selection([
        ('interno', 'Interno'),
        ('externo', 'Externo'),
        ('equilibrado', 'Equilibrado')
    ], string='Tipo Interno/Externo', compute='_compute_dofa_analysis', store=True)
    
    dofa_tipo_pos_neg = fields.Selection([
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
        ('neutro', 'Neutro')
    ], string='Tipo Positivo/Negativo', compute='_compute_dofa_analysis', store=True)
    
    dofa_tipo_entorno = fields.Char(
        string='Tipo de Entorno',
        compute='_compute_dofa_analysis',
        store=True,
        help='Clasificación completa del entorno organizacional'
    )

    # ===== CAMPOS SPACE TRADICIONAL =====
    space_trad_competitiva = fields.Float(
        string='Competitiva (Trad)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio de desempeño en variables Competitivas - 5'
    )
    space_trad_financiera = fields.Float(
        string='Financiera (Trad)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio de desempeño en variables Financieras'
    )
    space_trad_industria = fields.Float(
        string='Industria (Trad)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio de desempeño en variables de Industria'
    )
    space_trad_entorno = fields.Float(
        string='Entorno (Trad)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio de desempeño en variables de Entorno - 5'
    )
    space_trad_eje_x = fields.Float(
        string='Eje X (Trad)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Industria + Competitiva'
    )
    space_trad_eje_y = fields.Float(
        string='Eje Y (Trad)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Financiera + Entorno'
    )
    space_trad_recomendacion = fields.Selection([
        ('agresiva', 'Agresiva'),
        ('conservadora', 'Conservadora'),
        ('competitiva', 'Competitiva'),
        ('defensiva', 'Defensiva')
    ], string='Recomendación SPACE Tradicional', compute='_compute_space_analysis', store=True)

    # ===== CAMPOS SPACE PONDERADO =====
    space_pond_competitiva = fields.Float(
        string='Competitiva (Pond)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio ponderado por importancia en variables Competitivas - 5'
    )
    space_pond_financiera = fields.Float(
        string='Financiera (Pond)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio ponderado por importancia en variables Financieras'
    )
    space_pond_industria = fields.Float(
        string='Industria (Pond)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio ponderado por importancia en variables de Industria'
    )
    space_pond_entorno = fields.Float(
        string='Entorno (Pond)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio ponderado por importancia en variables de Entorno - 5'
    )
    space_pond_eje_x = fields.Float(
        string='Eje X (Pond)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Industria + Competitiva (ponderado)'
    )
    space_pond_eje_y = fields.Float(
        string='Eje Y (Pond)',
        compute='_compute_space_analysis',
        store=True,
        digits=(12, 2),
        help='Financiera + Entorno (ponderado)'
    )
    space_pond_recomendacion = fields.Selection([
        ('agresiva', 'Agresiva'),
        ('conservadora', 'Conservadora'),
        ('competitiva', 'Competitiva'),
        ('defensiva', 'Defensiva')
    ], string='Recomendación SPACE Ponderado', compute='_compute_space_analysis', store=True)

    # ===== CAMPOS MCKINSEY/INTERNA-EXTERNA =====
    mckinsey_prom_internas = fields.Float(
        string='Promedio Interno',
        compute='_compute_mckinsey_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio ponderado de variables Competitivas y Financieras'
    )
    mckinsey_prom_externas = fields.Float(
        string='Promedio Externo',
        compute='_compute_mckinsey_analysis',
        store=True,
        digits=(12, 2),
        help='Promedio ponderado de variables de Industria y Entorno'
    )
    mckinsey_recomendacion = fields.Selection([
        ('crecer', 'Crecer'),
        ('mantener', 'Mantener'),
        ('reducir', 'Reducir'),
        ('crecer_selectivamente_portafolios', 'Crecer Selectivamente Portafolios'),
        ('crecer_selectivamente_mercados', 'Crecer Selectivamente Mercados'),
        ('mantener_selectivamente', 'Mantener Selectivamente')
    ], string='Recomendación McKinsey', compute='_compute_mckinsey_analysis', store=True,
       help='Estrategia recomendada según posición en matriz McKinsey')

    # Relación con variables de análisis
    analysis_variable_ids = fields.One2many(
        'ai_mindnovation.analysis.variable',
        'strategic_analysis_id',
        string='Variables de Análisis'
    )

    @api.depends('analysis_variable_ids', 'analysis_variable_ids.dofa')
    def _compute_dofa_analysis(self):
        """
        Calcula el análisis DOFA completo basado en las variables cargadas.
        Replica la funcionalidad de strategic_analysis_streamlit_app.py líneas 184-227
        """
        for record in self:
            if not record.analysis_variable_ids:
                # Inicializar campos en cero si no hay variables
                record.dofa_fortalezas = 0
                record.dofa_debilidades = 0
                record.dofa_oportunidades = 0
                record.dofa_amenazas = 0
                record.dofa_total = 0
                record.dofa_internas = 0
                record.dofa_externas = 0
                record.dofa_positivas = 0
                record.dofa_negativas = 0
                record.dofa_prop_internas = 0.0
                record.dofa_prop_externas = 0.0
                record.dofa_prop_positivas = 0.0
                record.dofa_prop_negativas = 0.0
                record.dofa_tipo_int_ext = False
                record.dofa_tipo_pos_neg = False
                record.dofa_tipo_entorno = ''
                continue
            
            # Contar variables por categoría DOFA
            variables = record.analysis_variable_ids
            fortalezas = len(variables.filtered(lambda v: v.dofa == 'Fortaleza'))
            debilidades = len(variables.filtered(lambda v: v.dofa == 'Debilidad'))
            oportunidades = len(variables.filtered(lambda v: v.dofa == 'Oportunidad'))
            amenazas = len(variables.filtered(lambda v: v.dofa == 'Amenaza'))
            
            total_vars = fortalezas + debilidades + oportunidades + amenazas
            
            # Calcular agrupaciones
            internas = fortalezas + debilidades
            externas = oportunidades + amenazas
            positivas = fortalezas + oportunidades
            negativas = debilidades + amenazas
            
            # Asignar contadores
            record.dofa_fortalezas = fortalezas
            record.dofa_debilidades = debilidades
            record.dofa_oportunidades = oportunidades
            record.dofa_amenazas = amenazas
            record.dofa_total = total_vars
            record.dofa_internas = internas
            record.dofa_externas = externas
            record.dofa_positivas = positivas
            record.dofa_negativas = negativas
            
            # Calcular proporciones
            if total_vars > 0:
                prop_internas = internas / total_vars
                prop_externas = externas / total_vars
                prop_positivas = positivas / total_vars
                prop_negativas = negativas / total_vars
                
                record.dofa_prop_internas = prop_internas * 100
                record.dofa_prop_externas = prop_externas * 100
                record.dofa_prop_positivas = prop_positivas * 100
                record.dofa_prop_negativas = prop_negativas * 100
                
                # Clasificar entorno (Interno/Externo/Equilibrado)
                if prop_internas >= 0.6:
                    tipo_int_ext = 'interno'
                elif prop_internas <= 0.4:
                    tipo_int_ext = 'externo'
                else:
                    tipo_int_ext = 'equilibrado'
                
                # Clasificar entorno (Positivo/Negativo/Neutro)
                if prop_positivas >= 0.6:
                    tipo_pos_neg = 'positivo'
                elif prop_positivas <= 0.4:
                    tipo_pos_neg = 'negativo'
                else:
                    tipo_pos_neg = 'neutro'
                
                record.dofa_tipo_int_ext = tipo_int_ext
                record.dofa_tipo_pos_neg = tipo_pos_neg
                
                # Tipo de entorno completo
                tipo_int_ext_label = dict(record._fields['dofa_tipo_int_ext'].selection).get(tipo_int_ext, '')
                tipo_pos_neg_label = dict(record._fields['dofa_tipo_pos_neg'].selection).get(tipo_pos_neg, '')
                record.dofa_tipo_entorno = f"{tipo_int_ext_label} - {tipo_pos_neg_label}"
                
                # Actualizar campo de resultado legacy (JSON)
                dofa_data = {
                    'fortalezas': fortalezas,
                    'debilidades': debilidades,
                    'oportunidades': oportunidades,
                    'amenazas': amenazas,
                    'total': total_vars,
                    'internas': internas,
                    'externas': externas,
                    'positivas': positivas,
                    'negativas': negativas,
                    'prop_internas': round(prop_internas * 100, 2),
                    'prop_externas': round(prop_externas * 100, 2),
                    'prop_positivas': round(prop_positivas * 100, 2),
                    'prop_negativas': round(prop_negativas * 100, 2),
                    'tipo_entorno': record.dofa_tipo_entorno
                }
                record.dofa_result = json.dumps(dofa_data, indent=2, ensure_ascii=False)
            else:
                record.dofa_prop_internas = 0.0
                record.dofa_prop_externas = 0.0
                record.dofa_prop_positivas = 0.0
                record.dofa_prop_negativas = 0.0
                record.dofa_tipo_int_ext = False
                record.dofa_tipo_pos_neg = False
                record.dofa_tipo_entorno = ''
                record.dofa_result = json.dumps({'error': 'No hay variables DOFA para analizar'})

    @api.depends('analysis_variable_ids', 'analysis_variable_ids.clasificacion',
                 'analysis_variable_ids.media_importancia', 'analysis_variable_ids.media_desemp')
    def _compute_space_analysis(self):
        """
        Calcula el análisis SPACE tradicional y ponderado.
        Replica la funcionalidad de strategic_analysis_streamlit_app.py líneas 229-294
        """
        for record in self:
            if not record.analysis_variable_ids:
                # Inicializar campos en cero si no hay variables
                record.space_trad_competitiva = 0.0
                record.space_trad_financiera = 0.0
                record.space_trad_industria = 0.0
                record.space_trad_entorno = 0.0
                record.space_trad_eje_x = 0.0
                record.space_trad_eje_y = 0.0
                record.space_trad_recomendacion = False
                record.space_pond_competitiva = 0.0
                record.space_pond_financiera = 0.0
                record.space_pond_industria = 0.0
                record.space_pond_entorno = 0.0
                record.space_pond_eje_x = 0.0
                record.space_pond_eje_y = 0.0
                record.space_pond_recomendacion = False
                record.space_result = json.dumps({'error': 'No hay variables para análisis SPACE'})
                continue
            
            variables = record.analysis_variable_ids
            
            # Filtrar variables por clasificación SPACE
            df_competitiva = variables.filtered(lambda v: v.clasificacion == 'Competitiva')
            df_financiera = variables.filtered(lambda v: v.clasificacion == 'Financiera')
            df_industria = variables.filtered(lambda v: v.clasificacion == 'Industria')
            df_entorno = variables.filtered(lambda v: v.clasificacion == 'Entorno')
            
            # ===== SPACE TRADICIONAL =====
            # Calcular promedios simples (restar 5 para Competitiva y Entorno según lógica de Streamlit)
            prom_competitiva = (sum(df_competitiva.mapped('media_desemp')) / len(df_competitiva) - 5) if df_competitiva else 0.0
            prom_financiera = (sum(df_financiera.mapped('media_desemp')) / len(df_financiera)) if df_financiera else 0.0
            prom_industria = (sum(df_industria.mapped('media_desemp')) / len(df_industria)) if df_industria else 0.0
            prom_entorno = (sum(df_entorno.mapped('media_desemp')) / len(df_entorno) - 5) if df_entorno else 0.0
            
            # Calcular ejes
            eje_x_trad = prom_industria + prom_competitiva
            eje_y_trad = prom_financiera + prom_entorno
            
            # Determinar cuadrante tradicional
            if eje_x_trad > 0 and eje_y_trad > 0:
                recomend_trad = 'agresiva'
            elif eje_x_trad < 0 and eje_y_trad > 0:
                recomend_trad = 'conservadora'
            elif eje_x_trad > 0 and eje_y_trad < 0:
                recomend_trad = 'competitiva'
            else:
                recomend_trad = 'defensiva'
            
            # ===== SPACE PONDERADO =====
            # Función auxiliar para calcular promedio ponderado
            def calc_ponderado(df_group, restar_5=False):
                if not df_group:
                    return 0.0
                total_imp = sum(df_group.mapped('media_importancia'))
                if total_imp == 0:
                    return 0.0
                suma_ponderada = sum(
                    (v.media_importancia / total_imp) * v.media_desemp
                    for v in df_group
                )
                return suma_ponderada - 5 if restar_5 else suma_ponderada
            
            prom_competitiva_pond = calc_ponderado(df_competitiva, restar_5=True)
            prom_financiera_pond = calc_ponderado(df_financiera, restar_5=False)
            prom_industria_pond = calc_ponderado(df_industria, restar_5=False)
            prom_entorno_pond = calc_ponderado(df_entorno, restar_5=True)
            
            # Calcular ejes ponderados
            eje_x_pond = prom_industria_pond + prom_competitiva_pond
            eje_y_pond = prom_financiera_pond + prom_entorno_pond
            
            # Determinar cuadrante ponderado
            if eje_x_pond > 0 and eje_y_pond > 0:
                recomend_pond = 'agresiva'
            elif eje_x_pond < 0 and eje_y_pond > 0:
                recomend_pond = 'conservadora'
            elif eje_x_pond > 0 and eje_y_pond < 0:
                recomend_pond = 'competitiva'
            else:
                recomend_pond = 'defensiva'
            
            # Asignar valores tradicionales
            record.space_trad_competitiva = round(prom_competitiva, 2)
            record.space_trad_financiera = round(prom_financiera, 2)
            record.space_trad_industria = round(prom_industria, 2)
            record.space_trad_entorno = round(prom_entorno, 2)
            record.space_trad_eje_x = round(eje_x_trad, 2)
            record.space_trad_eje_y = round(eje_y_trad, 2)
            record.space_trad_recomendacion = recomend_trad
            
            # Asignar valores ponderados
            record.space_pond_competitiva = round(prom_competitiva_pond, 2)
            record.space_pond_financiera = round(prom_financiera_pond, 2)
            record.space_pond_industria = round(prom_industria_pond, 2)
            record.space_pond_entorno = round(prom_entorno_pond, 2)
            record.space_pond_eje_x = round(eje_x_pond, 2)
            record.space_pond_eje_y = round(eje_y_pond, 2)
            record.space_pond_recomendacion = recomend_pond
            
            # Actualizar campo legacy (JSON)
            space_data = {
                'tradicional': {
                    'competitiva': record.space_trad_competitiva,
                    'financiera': record.space_trad_financiera,
                    'industria': record.space_trad_industria,
                    'entorno': record.space_trad_entorno,
                    'eje_x': record.space_trad_eje_x,
                    'eje_y': record.space_trad_eje_y,
                    'recomendacion': recomend_trad.title()
                },
                'ponderado': {
                    'competitiva': record.space_pond_competitiva,
                    'financiera': record.space_pond_financiera,
                    'industria': record.space_pond_industria,
                    'entorno': record.space_pond_entorno,
                    'eje_x': record.space_pond_eje_x,
                    'eje_y': record.space_pond_eje_y,
                    'recomendacion': recomend_pond.title()
                }
            }
            record.space_result = json.dumps(space_data, indent=2, ensure_ascii=False)

    @api.depends('analysis_variable_ids', 'analysis_variable_ids.clasificacion',
                 'analysis_variable_ids.media_importancia', 'analysis_variable_ids.media_desemp')
    def _compute_mckinsey_analysis(self):
        """
        Calcula el análisis McKinsey/Interna-Externa.
        Variables internas: Competitiva + Financiera
        Variables externas: Industria + Entorno
        Replica la funcionalidad de strategic_analysis_streamlit_app.py líneas 296-351
        """
        for record in self:
            if not record.analysis_variable_ids:
                # Inicializar campos en cero si no hay variables
                record.mckinsey_prom_internas = 0.0
                record.mckinsey_prom_externas = 0.0
                record.mckinsey_recomendacion = False
                record.mckinsey_result = json.dumps({'error': 'No hay variables para análisis McKinsey'})
                continue
            
            variables = record.analysis_variable_ids
            
            # Filtrar variables internas (Competitiva + Financiera)
            df_internas = variables.filtered(lambda v: v.clasificacion in ['Competitiva', 'Financiera'])
            
            # Filtrar variables externas (Industria + Entorno)
            df_externas = variables.filtered(lambda v: v.clasificacion in ['Industria', 'Entorno'])
            
            # Calcular promedio ponderado para internas
            if df_internas:
                total_imp_internas = sum(df_internas.mapped('media_importancia'))
                if total_imp_internas > 0:
                    # Calcular importancia relativa
                    suma_ponderada_internas = sum(
                        (v.media_importancia / total_imp_internas) * v.media_desemp
                        for v in df_internas
                    )
                    prom_internas = suma_ponderada_internas
                else:
                    prom_internas = sum(df_internas.mapped('media_desemp')) / len(df_internas)
            else:
                prom_internas = 0.0
            
            # Calcular promedio ponderado para externas
            if df_externas:
                total_imp_externas = sum(df_externas.mapped('media_importancia'))
                if total_imp_externas > 0:
                    # Calcular importancia relativa
                    suma_ponderada_externas = sum(
                        (v.media_importancia / total_imp_externas) * v.media_desemp
                        for v in df_externas
                    )
                    prom_externas = suma_ponderada_externas
                else:
                    prom_externas = sum(df_externas.mapped('media_desemp')) / len(df_externas)
            else:
                prom_externas = 0.0
            
            # Determinar recomendación según rangos de la matriz McKinsey
            # Matriz 3x3:
            # Alto (>3), Medio (2-3), Bajo (<2) para ambos ejes
            if prom_internas > 3 and prom_externas > 3:
                recomendacion = 'crecer'
            elif prom_internas < 2 and prom_externas < 2:
                recomendacion = 'reducir'
            elif prom_internas > 3 and 2 <= prom_externas <= 3:
                recomendacion = 'crecer_selectivamente_mercados'
            elif 2 <= prom_internas <= 3 and prom_externas > 3:
                recomendacion = 'crecer_selectivamente_portafolios'
            elif 2 <= prom_internas <= 3 and 2 <= prom_externas <= 3:
                recomendacion = 'mantener_selectivamente'
            else:
                recomendacion = 'mantener'
            
            # Asignar valores
            record.mckinsey_prom_internas = round(prom_internas, 2)
            record.mckinsey_prom_externas = round(prom_externas, 2)
            record.mckinsey_recomendacion = recomendacion
            
            # Actualizar campo legacy (JSON)
            mckinsey_data = {
                'prom_internas': record.mckinsey_prom_internas,
                'prom_externas': record.mckinsey_prom_externas,
                'recomendacion': recomendacion.replace('_', ' ').title(),
                'matriz_posicion': {
                    'interno': 'Alto' if prom_internas > 3 else ('Medio' if prom_internas >= 2 else 'Bajo'),
                    'externo': 'Alto' if prom_externas > 3 else ('Medio' if prom_externas >= 2 else 'Bajo')
                }
            }
            record.mckinsey_result = json.dumps(mckinsey_data, indent=2, ensure_ascii=False)

    def process_analysis(self):
        """
        Procesa los archivos Excel, extrae variables y calcula los análisis estratégicos.
        """
        try:
            # Leer archivo 'importancia'
            if self.file_importancia:
                importancia_data = base64.b64decode(self.file_importancia)
                df_importancia = pd.read_excel(BytesIO(importancia_data), sheet_name='importancia', header=0)
            else:
                raise ValidationError("Falta el archivo de importancia")

            # Leer archivo 'desempeño'
            if self.file_desempeno:
                desempeno_data = base64.b64decode(self.file_desempeno)
                df_desempeno = pd.read_excel(BytesIO(desempeno_data), sheet_name='desempeño', header=0)
            else:
                raise ValidationError("Falta el archivo de desempeño")

            # Limpiar variables existentes
            self.analysis_variable_ids.unlink()

            # Procesar y crear variables
            for idx, row in df_importancia.iterrows():
                # Buscar datos de desempeño por índice
                desempeno_row = df_desempeno.iloc[idx] if idx < len(df_desempeno) else None
                
                vals = {
                    'nro': int(row.get('nro')) if pd.notna(row.get('nro')) else idx + 1,
                    'palabras_clave': str(row.get('palabras_clave', '')),
                    'descripcion': str(row.get('descripcion', '')),
                    'dofa': row.get('dofa'),
                    'clasificacion': row.get('clasificacion'),
                    'imp_1': float(row.get('imp_1', 0)) if pd.notna(row.get('imp_1')) else 0,
                    'imp_2': float(row.get('imp_2', 0)) if pd.notna(row.get('imp_2')) else 0,
                    'imp_3': float(row.get('imp_3', 0)) if pd.notna(row.get('imp_3')) else 0,
                    'imp_4': float(row.get('imp_4', 0)) if pd.notna(row.get('imp_4')) else 0,
                    'imp_5': float(row.get('imp_5', 0)) if pd.notna(row.get('imp_5')) else 0,
                }
                
                if desempeno_row is not None:
                    vals.update({
                        'desemp_1': float(desempeno_row.get('desemp_1', 0)) if pd.notna(desempeno_row.get('desemp_1')) else 0,
                        'desemp_2': float(desempeno_row.get('desemp_2', 0)) if pd.notna(desempeno_row.get('desemp_2')) else 0,
                        'desemp_3': float(desempeno_row.get('desemp_3', 0)) if pd.notna(desempeno_row.get('desemp_3')) else 0,
                        'desemp_4': float(desempeno_row.get('desemp_4', 0)) if pd.notna(desempeno_row.get('desemp_4')) else 0,
                        'desemp_5': float(desempeno_row.get('desemp_5', 0)) if pd.notna(desempeno_row.get('desemp_5')) else 0,
                    })
                
                # Calcular medias
                imp_values = [vals[f'imp_{i}'] for i in range(1, 6) if vals.get(f'imp_{i}', 0) > 0]
                desemp_values = [vals[f'desemp_{i}'] for i in range(1, 6) if vals.get(f'desemp_{i}', 0) > 0]
                
                vals['media_importancia'] = sum(imp_values) / len(imp_values) if imp_values else 0
                vals['media_desemp'] = sum(desemp_values) / len(desemp_values) if desemp_values else 0
                
                self.env['ai_mindnovation.analysis.variable'].create({
                    **vals,
                    'strategic_analysis_id': self.id
                })
            
            # Cambiar estado
            self.state = 'processed'
            
            _logger.info(f"Análisis {self.name} procesado correctamente con {len(self.analysis_variable_ids)} variables")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Éxito',
                    'message': f'Análisis procesado correctamente. {len(self.analysis_variable_ids)} variables cargadas.',
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except ValidationError as e:
            _logger.error(f"Error de validación en análisis {self.name}: {str(e)}")
            raise
        except Exception as e:
            _logger.error(f"Error procesando análisis {self.name}: {str(e)}")
            raise UserError(f"Error al procesar el archivo: {str(e)}")