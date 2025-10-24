from odoo import models, fields, api
import base64
import pandas as pd
from io import BytesIO

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
    # Resultados principales
    dofa_result = fields.Text(string='Resultado DOFA')
    space_result = fields.Text(string='Resultado SPACE')
    mckinsey_result = fields.Text(string='Resultado McKinsey')
    valor_percibido_result = fields.Text(string='Resultado Valor Percibido')

    # Relación con variables de análisis
    analysis_variable_ids = fields.One2many(
        'ai_mindnovation.analysis.variable',
        'strategic_analysis_id',
        string='Variables de Análisis'
    )

    def process_analysis(self):
        """
        Procesa los archivos Excel, extrae variables y calcula los análisis estratégicos.
        """

        # Leer archivo 'importancia'
        if self.file_importancia:
            importancia_data = base64.b64decode(self.file_importancia)
            df_importancia = pd.read_excel(BytesIO(importancia_data), sheet_name='importancia', header=0)
        else:
            df_importancia = None

        # Leer archivo 'desempeño'
        if self.file_desempeno:
            desempeno_data = base64.b64decode(self.file_desempeno)
            df_desempeno = pd.read_excel(BytesIO(desempeno_data), sheet_name='desempeño', header=0)
        else:
            df_desempeno = None

        # Validar datos
        if df_importancia is not None and df_desempeno is not None:
            # Procesar y crear variables
            for idx, row in df_importancia.iterrows():
                # Buscar datos de desempeño por índice
                desempeno_row = df_desempeno.iloc[idx] if idx < len(df_desempeno) else None
                vals = {
                    'nro': row.get('nro'),
                    'palabras_clave': row.get('palabras_clave'),
                    'descripcion': row.get('descripcion'),
                    'dofa': row.get('dofa'),
                    'clasificacion': row.get('clasificacion'),
                    'imp_1': row.get('imp_1'),
                    'imp_2': row.get('imp_2'),
                    'imp_3': row.get('imp_3'),
                    'imp_4': row.get('imp_4'),
                    'imp_5': row.get('imp_5'),
                }
                if desempeno_row is not None:
                    vals.update({
                        'desemp_1': desempeno_row.get('desemp_1'),
                        'desemp_2': desempeno_row.get('desemp_2'),
                        'desemp_3': desempeno_row.get('desemp_3'),
                        'desemp_4': desempeno_row.get('desemp_4'),
                        'desemp_5': desempeno_row.get('desemp_5'),
                    })
                # Calcular medias
                imp_values = [row.get(f'imp_{i}') for i in range(1,6) if row.get(f'imp_{i}') is not None]
                desemp_values = [desempeno_row.get(f'desemp_{i}') for i in range(1,6) if desempeno_row is not None and desempeno_row.get(f'desemp_{i}') is not None]
                vals['media_importancia'] = sum(imp_values)/len(imp_values) if imp_values else 0
                vals['media_desemp'] = sum(desemp_values)/len(desemp_values) if desemp_values else 0

                self.env['ai_mindnovation.analysis.variable'].create({
                    **vals,
                    'strategic_analysis_id': self.id
                })
            # Aquí se puede continuar con el cálculo de análisis DOFA, SPACE, McKinsey, etc.
        else:
            # Manejar error de datos
            pass