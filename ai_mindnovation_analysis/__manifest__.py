{
    'name': 'AI Mindnovation Strategic Analysis',
    'version': '1.0.0',
    'summary': 'Análisis estratégico avanzado: DOFA, SPACE, McKinsey, Valor Percibido',
    'author': 'Ai-Mindnovation',
    'category': 'Tools',
    'website': 'https://ai-mindnovation.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/strategic_analysis_views.xml',
        'views/competitor_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'description': """
        Módulo nativo Odoo para análisis estratégico avanzado, replicando la funcionalidad de la app Streamlit.
        Incluye análisis DOFA, SPACE, McKinsey y Valor Percibido, con integración total a usuarios y seguridad Odoo.
    """
}
