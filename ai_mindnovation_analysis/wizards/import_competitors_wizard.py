from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import pandas as pd
from io import BytesIO

class ImportCompetitorsWizard(models.TransientModel):
    _name = 'ai_mindnovation.import.competitors.wizard'
    _description = 'Importar Competidores desde Excel'

    file = fields.Binary('Archivo Excel', required=True, help="Archivo Excel con competidores y valores. Cada columna después de las variables debe ser un competidor.")
    filename = fields.Char('Nombre del Archivo')

    def action_import(self):
        self.ensure_one()
        if not self.file:
            raise UserError('Debes seleccionar un archivo Excel.')
        try:
            data = base64.b64decode(self.file)
            df = pd.read_excel(BytesIO(data), header=0)
        except Exception as e:
            raise UserError(f'Error leyendo el archivo: {e}')

        # Validar columnas mínimas
        required_cols = {'nro', 'palabras_clave', 'descripcion'}
        if not required_cols.issubset(set(df.columns.str.lower())):
            raise UserError('El archivo debe tener las columnas: nro, palabras_clave, descripcion y al menos un competidor.')

        # Detectar columnas de competidores
        competitor_cols = [col for col in df.columns if col.lower() not in required_cols]
        if not competitor_cols:
            raise UserError('No se detectaron columnas de competidores.')

        # Obtener análisis activo desde contexto
        analysis_id = self.env.context.get('active_id')
        if not analysis_id:
            raise UserError('No se pudo determinar el análisis estratégico activo.')
        analysis = self.env['ai_mindnovation.strategic.analysis'].browse(analysis_id)

        # Crear competidores y valores
        competitor_obj = self.env['ai_mindnovation.competitor']
        value_obj = self.env['ai_mindnovation.competitor.value']
        variable_obj = self.env['ai_mindnovation.analysis.variable']

        # Mapear variables por nro o palabras_clave
        variables = {str(v.nro): v for v in analysis.analysis_variable_ids}
        if not variables:
            raise UserError('No hay variables cargadas en el análisis.')

        for comp_col in competitor_cols:
            comp_name = str(comp_col).strip()
            competitor = competitor_obj.create({
                'name': comp_name,
                'strategic_analysis_id': analysis.id
            })
            for idx, row in df.iterrows():
                nro = str(row.get('nro'))
                variable = variables.get(nro)
                if not variable:
                    continue
                value = row.get(comp_col)
                if pd.isna(value):
                    continue
                value_obj.create({
                    'competitor_id': competitor.id,
                    'variable_id': variable.id,
                    'value': float(value)
                })
        return {'type': 'ir.actions.act_window_close'}
