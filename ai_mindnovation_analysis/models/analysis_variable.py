from odoo import models, fields, api

class AnalysisVariable(models.Model):
    _name = 'ai_mindnovation.analysis.variable'
    _description = 'Variable de Análisis Estratégico'
    _rec_name = 'palabras_clave'

    strategic_analysis_id = fields.Many2one('ai_mindnovation.strategic.analysis', string='Análisis Estratégico', required=True, ondelete='cascade')
    nro = fields.Integer(string='Nro')
    palabras_clave = fields.Char(string='Palabras Clave', required=True)
    descripcion = fields.Char(string='Descripción')
    dofa = fields.Selection([
        ('Fortaleza', 'Fortaleza'),
        ('Debilidad', 'Debilidad'),
        ('Oportunidad', 'Oportunidad'),
        ('Amenaza', 'Amenaza')
    ], string='DOFA')
    clasificacion = fields.Selection([
        ('Competitiva', 'Competitiva'),
        ('Financiera', 'Financiera'),
        ('Industria', 'Industria'),
        ('Entorno', 'Entorno')
    ], string='Clasificación SPACE')
    imp_1 = fields.Float(string='Importancia 1')
    imp_2 = fields.Float(string='Importancia 2')
    imp_3 = fields.Float(string='Importancia 3')
    imp_4 = fields.Float(string='Importancia 4')
    imp_5 = fields.Float(string='Importancia 5')
    desemp_1 = fields.Float(string='Desempeño 1')
    desemp_2 = fields.Float(string='Desempeño 2')
    desemp_3 = fields.Float(string='Desempeño 3')
    desemp_4 = fields.Float(string='Desempeño 4')
    desemp_5 = fields.Float(string='Desempeño 5')
    media_importancia = fields.Float(string='Media Importancia')
    media_desemp = fields.Float(string='Media Desempeño')
    # Otros campos según necesidad
