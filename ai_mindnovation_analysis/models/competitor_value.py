from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CompetitorValue(models.Model):
    _name = 'ai_mindnovation.competitor.value'
    _description = 'Valor de Desempeño del Competidor por Variable'
    _rec_name = 'variable_id'
    _order = 'variable_id'

    competitor_id = fields.Many2one(
        'ai_mindnovation.competitor',
        string='Competidor',
        required=True,
        ondelete='cascade'
    )
    variable_id = fields.Many2one(
        'ai_mindnovation.analysis.variable',
        string='Variable de Análisis',
        required=True,
        ondelete='cascade'
    )
    value = fields.Float(
        string='Valor de Desempeño',
        required=True,
        digits=(12, 2),
        help='Valor de desempeño del competidor en esta variable (escala 1-5)'
    )
    
    # Campos relacionados para facilitar consultas
    strategic_analysis_id = fields.Many2one(
        related='competitor_id.strategic_analysis_id',
        string='Análisis Estratégico',
        store=True
    )
    variable_palabras_clave = fields.Char(
        related='variable_id.palabras_clave',
        string='Palabras Clave',
        store=True
    )
    variable_importancia = fields.Float(
        related='variable_id.media_importancia',
        string='Importancia de la Variable',
        store=True
    )
    
    @api.constrains('value')
    def _check_value_range(self):
        """Valida que el valor esté en el rango correcto"""
        for record in self:
            if record.value < 0 or record.value > 5:
                raise ValidationError('El valor de desempeño debe estar entre 0 y 5.')
    
    _sql_constraints = [
        ('competitor_variable_unique', 'unique(competitor_id, variable_id)',
         'No puede haber valores duplicados para la misma variable y competidor.')
    ]
