from odoo import models, fields, api

class Competitor(models.Model):
    _name = 'ai_mindnovation.competitor'
    _description = 'Competidor para Análisis de Valor Percibido'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Nombre del Competidor', required=True)
    strategic_analysis_id = fields.Many2one(
        'ai_mindnovation.strategic.analysis',
        string='Análisis Estratégico',
        required=True,
        ondelete='cascade'
    )
    competitor_value_ids = fields.One2many(
        'ai_mindnovation.competitor.value',
        'competitor_id',
        string='Valores del Competidor'
    )
    
    # Campos computed para métricas agregadas
    promedio_desempeno = fields.Float(
        string='Promedio de Desempeño',
        compute='_compute_promedio_desempeno',
        store=True,
        digits=(12, 2)
    )
    num_variables = fields.Integer(
        string='Número de Variables',
        compute='_compute_num_variables',
        store=True
    )
    
    @api.depends('competitor_value_ids', 'competitor_value_ids.value')
    def _compute_promedio_desempeno(self):
        """Calcula el promedio de desempeño del competidor"""
        for record in self:
            if record.competitor_value_ids:
                values = record.competitor_value_ids.mapped('value')
                record.promedio_desempeno = sum(values) / len(values) if values else 0.0
            else:
                record.promedio_desempeno = 0.0
    
    @api.depends('competitor_value_ids')
    def _compute_num_variables(self):
        """Cuenta el número de variables evaluadas"""
        for record in self:
            record.num_variables = len(record.competitor_value_ids)
    
    _sql_constraints = [
        ('name_analysis_unique', 'unique(name, strategic_analysis_id)', 
         'El nombre del competidor debe ser único dentro del análisis.')
    ]
