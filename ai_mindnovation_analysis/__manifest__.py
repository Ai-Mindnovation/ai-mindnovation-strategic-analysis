{
    'name': 'AI Mindnovation Strategic Analysis',
    'version': '1.0.0',
    'summary': 'Análisis estratégico avanzado: DOFA, SPACE, McKinsey, Valor Percibido',
    'author': 'Ai-Mindnovation',
    'category': 'Tools',
    'website': 'https://ai-mindnovation.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/import_competitors_wizard_view.xml',
        'views/competitor_views.xml',
        'views/strategic_analysis_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ai_mindnovation_analysis/static/src/lib/chart.min.js',
            'ai_mindnovation_analysis/static/src/js/chart_widgets.js',
            'ai_mindnovation_analysis/static/src/css/charts.css',
            'ai_mindnovation_analysis/static/src/xml/chart_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'description': """
        Módulo nativo Odoo para análisis estratégico avanzado, replicando la funcionalidad de la app Streamlit.
        Incluye análisis DOFA, SPACE, McKinsey y Valor Percibido, con integración total a usuarios y seguridad Odoo.
    """
}
