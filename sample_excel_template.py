# crear_plantilla_excel.py
# Script para crear una plantilla de Excel de ejemplo para testing

import pandas as pd
import numpy as np

def crear_plantilla_excel():
    """
    Crea un archivo Excel de ejemplo para probar la aplicación
    """
    
    # Datos de ejemplo para hoja 'importancia'
    variables_ejemplo = [
        {'nro': 1, 'palabras_clave': 'Liderazgo tecnológico', 'descripcion': 'Capacidad de innovación tecnológica', 'dofa': 'Fortaleza', 'clasificacion': 'Competitiva'},
        {'nro': 2, 'palabras_clave': 'Flujo de caja', 'descripcion': 'Liquidez y capacidad financiera', 'dofa': 'Fortaleza', 'clasificacion': 'Financiera'},
        {'nro': 3, 'palabras_clave': 'Competencia intensa', 'descripcion': 'Rivalidad en el sector', 'dofa': 'Amenaza', 'clasificacion': 'Industria'},
        {'nro': 4, 'palabras_clave': 'Regulaciones ambientales', 'descripcion': 'Normativas ecológicas', 'dofa': 'Oportunidad', 'clasificacion': 'Entorno'},
        {'nro': 5, 'palabras_clave': 'Talento humano', 'descripcion': 'Calidad del personal', 'dofa': 'Fortaleza', 'clasificacion': 'Competitiva'},
        {'nro': 6, 'palabras_clave': 'Rentabilidad', 'descripcion': 'Márgenes de ganancia', 'dofa': 'Fortaleza', 'clasificacion': 'Financiera'},
        {'nro': 7, 'palabras_clave': 'Barreras de entrada', 'descripcion': 'Dificultad para nuevos competidores', 'dofa': 'Oportunidad', 'clasificacion': 'Industria'},
        {'nro': 8, 'palabras_clave': 'Tendencias del mercado', 'descripcion': 'Cambios en preferencias', 'dofa': 'Oportunidad', 'clasificacion': 'Entorno'},
        {'nro': 9, 'palabras_clave': 'Infraestructura IT', 'descripcion': 'Sistemas tecnológicos', 'dofa': 'Debilidad', 'clasificacion': 'Competitiva'},
        {'nro': 10, 'palabras_clave': 'Endeudamiento', 'descripcion': 'Nivel de deuda', 'dofa': 'Debilidad', 'clasificacion': 'Financiera'},
        {'nro': 11, 'palabras_clave': 'Poder de proveedores', 'descripcion': 'Dependencia de proveedores', 'dofa': 'Amenaza', 'clasificacion': 'Industria'},
        {'nro': 12, 'palabras_clave': 'Crisis económica', 'descripcion': 'Recesión económica', 'dofa': 'Amenaza', 'clasificacion': 'Entorno'},
        {'nro': 13, 'palabras_clave': 'Marca reconocida', 'descripcion': 'Posicionamiento de marca', 'dofa': 'Fortaleza', 'clasificacion': 'Competitiva'},
        {'nro': 14, 'palabras_clave': 'Acceso a crédito', 'descripcion': 'Facilidad de financiamiento', 'dofa': 'Fortaleza', 'clasificacion': 'Financiera'},
        {'nro': 15, 'palabras_clave': 'Crecimiento del sector', 'descripcion': 'Expansión de la industria', 'dofa': 'Oportunidad', 'clasificacion': 'Industria'},
        {'nro': 16, 'palabras_clave': 'Digitalización', 'descripcion': 'Transformación digital', 'dofa': 'Oportunidad', 'clasificacion': 'Entorno'},
        {'nro': 17, 'palabras_clave': 'Capacidad operativa', 'descripcion': 'Eficiencia en procesos', 'dofa': 'Debilidad', 'clasificacion': 'Competitiva'},
        {'nro': 18, 'palabras_clave': 'Control de costos', 'descripcion': 'Gestión financiera', 'dofa': 'Debilidad', 'clasificacion': 'Financiera'},
        {'nro': 19, 'palabras_clave': 'Poder de clientes', 'descripcion': 'Influencia de compradores', 'dofa': 'Amenaza', 'clasificacion': 'Industria'},
        {'nro': 20, 'palabras_clave': 'Políticas públicas', 'descripcion': 'Apoyo gubernamental', 'dofa': 'Oportunidad', 'clasificacion': 'Entorno'},
        {'nro': 21, 'palabras_clave': 'Innovación de productos', 'descripcion': 'Desarrollo de nuevos productos', 'dofa': 'Fortaleza', 'clasificacion': 'Competitiva'},
        {'nro': 22, 'palabras_clave': 'Estructura de capital', 'descripcion': 'Composición financiera', 'dofa': 'Fortaleza', 'clasificacion': 'Financiera'},
        {'nro': 23, 'palabras_clave': 'Productos sustitutos', 'descripcion': 'Amenaza de sustitución', 'dofa': 'Amenaza', 'clasificacion': 'Industria'},
        {'nro': 24, 'palabras_clave': 'Sostenibilidad', 'descripcion': 'Responsabilidad ambiental', 'dofa': 'Oportunidad', 'clasificacion': 'Entorno'},
        {'nro': 25, 'palabras_clave': 'Canales de distribución', 'descripcion': 'Red de distribución', 'dofa': 'Debilidad', 'clasificacion': 'Competitiva'},
        {'nro': 26, 'palabras_clave': 'Diversificación', 'descripcion': 'Portafolio de productos', 'dofa': 'Debilidad', 'clasificacion': 'Financiera'},
        {'nro': 27, 'palabras_clave': 'Economías de escala', 'descripcion': 'Ventajas por volumen', 'dofa': 'Oportunidad', 'clasificacion': 'Industria'},
        {'nro': 28, 'palabras_clave': 'Cambio climático', 'descripcion': 'Impacto ambiental', 'dofa': 'Amenaza', 'clasificacion': 'Entorno'},
        {'nro': 29, 'palabras_clave': 'Experiencia del equipo', 'descripcion': 'Know-how del personal', 'dofa': 'Fortaleza', 'clasificacion': 'Competitiva'},
        {'nro': 30, 'palabras_clave': 'Gestión de riesgos', 'descripcion': 'Control de riesgos financieros', 'dofa': 'Debilidad', 'clasificacion': 'Financiera'}
    ]
    
    # Crear DataFrame base
    df_base = pd.DataFrame(variables_ejemplo)
    
    # Generar calificaciones aleatorias pero realistas para importancia
    np.random.seed(42)  # Para reproducibilidad
    
    # Calificaciones de importancia (1-5) - 5 evaluadores
    imp_data = {
        'imp_1': np.random.normal(3.5, 0.8, 30).clip(1, 5).round(1),
        'imp_2': np.random.normal(3.7, 0.7, 30).clip(1, 5).round(1),
        'imp_3': np.random.normal(3.4, 0.9, 30).clip(1, 5).round(1),
        'imp_4': np.random.normal(3.6, 0.8, 30).clip(1, 5).round(1),
        'imp_5': np.random.normal(3.5, 0.8, 30).clip(1, 5).round(1)
    }
    
    # Calificaciones de desempeño (1-5) - 5 evaluadores
    desemp_data = {
        'desemp_1': np.random.normal(3.2, 0.9, 30).clip(1, 5).round(1),
        'desemp_2': np.random.normal(3.4, 0.8, 30).clip(1, 5).round(1),
        'desemp_3': np.random.normal(3.1, 1.0, 30).clip(1, 5).round(1),
        'desemp_4': np.random.normal(3.3, 0.9, 30).clip(1, 5).round(1),
        'desemp_5': np.random.normal(3.2, 0.8, 30).clip(1, 5).round(1)
    }
    
    # Crear DataFrames finales
    df_importancia = pd.concat([df_base, pd.DataFrame(imp_data)], axis=1)
    df_desemp = pd.DataFrame(desemp_data)
    
    # Crear archivo Excel
    filename = 'plantilla_analisis_estrategico.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_importancia.to_excel(writer, sheet_name='importancia', index=False)
        df_desemp.to_excel(writer, sheet_name='desempeño', index=False)
    
    print(f"✅ Archivo '{filename}' creado exitosamente!")
    print(f"📊 Contiene {len(df_importancia)} variables para análisis")
    print(f"🔢 Distribución por categoría SPACE:")
    print(df_importancia['clasificacion'].value_counts())
    print(f"🎯 Distribución DOFA:")
    print(df_importancia['dofa'].value_counts())
    
    return filename

# Ejecutar si se corre directamente
if __name__ == "__main__":
    crear_plantilla_excel()