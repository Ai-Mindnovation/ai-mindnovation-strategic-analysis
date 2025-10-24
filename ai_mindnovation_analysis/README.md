# Módulo Odoo: AI Mindnovation Strategic Analysis

## 1. Levantamiento de requerimientos y alcance

Este módulo tiene como objetivo replicar la funcionalidad de la aplicación de análisis estratégico (DOFA, SPACE, McKinsey, Valor Percibido) dentro de Odoo, integrando completamente la gestión de usuarios, seguridad y visualización nativa.

### Alcance inicial:
- Carga y procesamiento de archivos Excel con hojas 'importancia' y 'desempeño'.
- Análisis estratégico: matrices DOFA, SPACE (tradicional y ponderada), McKinsey.
- Análisis de Valor Percibido vs competidores.
- Visualización de resultados con gráficos interactivos.
- Exportación de resultados.
- Integración total con usuarios y permisos de Odoo.
- Interfaz amigable y adaptable a cualquier instancia Odoo.

### Requerimientos funcionales:
1. El usuario debe autenticarse con credenciales Odoo.
2. El módulo debe permitir la carga de archivos Excel con el formato requerido.
3. Debe procesar los datos y mostrar resultados de los análisis estratégicos.
4. Debe generar gráficos y visualizaciones interactivas.
5. Debe permitir exportar resultados y configuraciones.
6. Debe respetar la seguridad y permisos definidos en Odoo.

### Requerimientos técnicos:
- Compatible con Odoo 15+ (ajustable según versión objetivo).
- Estructura estándar de módulos Odoo (`__manifest__.py`, `models/`, `views/`, `security/`, etc).
- Uso de librerías Python compatibles con Odoo para procesamiento y visualización.
- Documentación clara para instalación y uso.

---

## Avance actual

1. Estructura básica del módulo creada (carpetas, manifest, README).
2. Modelos principales definidos: StrategicAnalysis y AnalysisVariable.
3. Permisos configurados para el grupo administrador en ambos modelos.
4. Vistas básicas (formulario, lista, menú) implementadas para StrategicAnalysis.
5. Lógica inicial para carga y procesamiento de archivos Excel agregada.

### Siguiente paso:
- Probar la carga de datos y el funcionamiento de la interfaz.
- Implementar lógica de análisis estratégico (DOFA, SPACE, McKinsey, Valor Percibido).