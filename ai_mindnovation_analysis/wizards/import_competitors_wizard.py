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
            xl = pd.ExcelFile(BytesIO(data))
        except Exception as e:
            raise UserError(f'Error leyendo el archivo: {e}')

        # Validar hojas requeridas
        required_sheets = {'importancia', 'desempeño'}
        if not required_sheets.issubset(set(xl.sheet_names)):
            raise UserError("El archivo debe tener las hojas 'importancia' y 'desempeño'.")

        df_imp = xl.parse('importancia')
        df_des = xl.parse('desempeño')

        # Obtener análisis activo desde contexto
        analysis_id = self.env.context.get('active_id')
        if not analysis_id:
            raise UserError('No se pudo determinar el análisis estratégico activo.')
        analysis = self.env['ai_mindnovation.strategic.analysis'].browse(analysis_id)

        # Mapear variables por palabras_clave (clave principal)
        variable_obj = self.env['ai_mindnovation.analysis.variable']
        variables = {v.palabras_clave.strip().lower(): v for v in analysis.analysis_variable_ids}
        if not variables:
            raise UserError('No hay variables cargadas en el análisis.')

        # --- Procesar hoja importancia ---
        for idx, row in df_imp.iterrows():
            palabras = str(row.get('palabras_clave', '')).strip().lower()
            variable = variables.get(palabras)
            if not variable:
                continue
            # Actualizar campos de variable
            variable.descripcion = row.get('descripcion', '')
            if hasattr(variable, 'tipo'):
                variable.tipo = row.get('tipo', '')
            # Importancias
            for i in range(1, 6):
                val = row.get(f'imp_{i}')
                if pd.notna(val):
                    setattr(variable, f'imp_{i}', float(val))

        # --- Procesar hoja desempeño ---
        # Detectar columnas de competidores (empiezan por 'comp_')
        comp_cols = [col for col in df_des.columns if str(col).lower().startswith('comp_')]
        empresa_col = 'empresa' if 'empresa' in [c.lower() for c in df_des.columns] else None
        dofa_col = 'dofa' if 'dofa' in [c.lower() for c in df_des.columns] else None

        competitor_obj = self.env['ai_mindnovation.competitor']
        value_obj = self.env['ai_mindnovation.competitor.value']

        # Crear competidores
        competitors = {}
        for comp_col in comp_cols:
            comp_name = str(comp_col).replace('comp_', 'Competidor ').strip()
            competitors[comp_col] = competitor_obj.create({
                'name': comp_name,
                'strategic_analysis_id': analysis.id
            })

        # Asignar valores de desempeño y dofa
        for idx, row in df_des.iterrows():
            palabras = str(row.get('palabras_clave', '')).strip().lower()
            variable = variables.get(palabras)
            if not variable:
                continue
            # DOFA
            if dofa_col and hasattr(variable, 'dofa'):
                variable.dofa = row.get(dofa_col, '')
            # Desempeño empresa
            if empresa_col and hasattr(variable, 'desemp_1'):
                val = row.get(empresa_col)
                if pd.notna(val):
                    variable.desemp_1 = float(val)
            # Valores de competidores
            for comp_col in comp_cols:
                val = row.get(comp_col)
                if pd.isna(val):
                    continue
                try:
                    val_float = float(val)
                except Exception:
                    raise UserError(f"Valor no numérico '{val}' en fila {idx+2}, columna {comp_col}.")
                value_obj.create({
                    'competitor_id': competitors[comp_col].id,
                    'variable_id': variable.id,
                    'value': val_float
                })
        return {'type': 'ir.actions.act_window_close'}
