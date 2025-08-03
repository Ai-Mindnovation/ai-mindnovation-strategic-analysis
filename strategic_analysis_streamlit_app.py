# app.py - Aplicación Principal de Análisis Estratégico
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
from datetime import datetime
import os
import hashlib
import yaml
from pathlib import Path
from auth_database import get_auth_manager
from valor_percibido_streamlit import analisis_valor_percibido

# Configuración de la página
st.set_page_config(
    page_title="AI-Mindnovation | Análisis Estratégico",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado con colores de AI-Mindnovation
def load_css():
    st.markdown("""
    <style>
    /* Colores principales */
    :root {
        --primary-blue: #1F4A90;
        --secondary-blue: #1E5A73;
        --accent-green: #B2FFDA;
        --text-dark: #2c3e50;
        --background-light: #f8f9fa;
    }
    
    /* Header personalizado */
    .main-header {
        background: linear-gradient(135deg, #1F4A90 0%, #1E5A73 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(45deg, #1F4A90, #1E5A73);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #1E5A73, #1F4A90);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 74, 144, 0.3);
    }
    
    /* Cards de resultados */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1F4A90;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #B2FFDA 0%, #E8FFF5 100%);
        border-left: 4px solid #00C851;
    }
    
    /* Métricas personalizadas */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #B2FFDA;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1F4A90;
    }
    
    .metric-label {
        color: #1E5A73;
        font-weight: 500;
    }
    
    /* Sidebar personalizado */
    .css-1d391kg {
        background: linear-gradient(180deg, #1F4A90 0%, #1E5A73 100%);
    }
    
    /* Upload zone */
    .uploadedFile {
        background: #B2FFDA;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #1E5A73;
        border-top: 1px solid #e0e0e0;
        margin-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)



# Clase principal para el análisis estratégico
class StrategicAnalysis:
    def __init__(self):
        self.data = None
        self.results = {}
    
    def load_excel_data(self, uploaded_file):
        """Carga los datos desde el archivo Excel subido"""
        try:
            # Leer ambas hojas
            df_importancia = pd.read_excel(uploaded_file, sheet_name='importancia', header=0)
            df_desemp = pd.read_excel(uploaded_file, sheet_name='desempeño', header=0)
            
            # Procesar datos como en tu script original
            desemp = df_desemp[['desemp_1', 'desemp_2', 'desemp_3', 'desemp_4', 'desemp_5']]
            df = df_importancia.join(desemp)
            
            # Calcular medias
            df['media_importancia'] = df[['imp_1', 'imp_2', 'imp_3', 'imp_4', 'imp_5']].mean(axis=1)
            df['media_desemp'] = df[['desemp_1', 'desemp_2', 'desemp_3', 'desemp_4', 'desemp_5']].mean(axis=1)
            
            # Ordenar por importancia
            df = df.sort_values(by='media_importancia', ascending=False, na_position='last')
            
            self.data = df
            return True, "Datos cargados exitosamente"
            
        except Exception as e:
            return False, f"Error al cargar datos: {str(e)}"
    
    def prepare_analysis_data(self):
        """Prepara los datos para análisis - selecciona top 25 y completa categorías SPACE"""
        if self.data is None:
            return False, "No hay datos cargados"
        
        try:
            # Filtrando las 25 primeras variables
            data = self.data.iloc[0:25].copy()
            alt_data = self.data.iloc[25:].copy()
            
            # Contar variables por categoría SPACE
            cant_competitiva = len(data[data['clasificacion'] == 'Competitiva'])
            cant_financiera = len(data[data['clasificacion'] == 'Financiera'])
            cant_industria = len(data[data['clasificacion'] == 'Industria'])
            cant_entorno = len(data[data['clasificacion'] == 'Entorno'])
            
            # Calcular faltantes
            falt_competitivas = max(0, 3 - cant_competitiva)
            falt_financieras = max(0, 3 - cant_financiera)
            falt_industria = max(0, 3 - cant_industria)
            falt_entorno = max(0, 3 - cant_entorno)
            
            # Añadir variables faltantes (versión corregida)
            for categoria, faltantes in [('Competitiva', falt_competitivas), 
                                       ('Financiera', falt_financieras),
                                       ('Industria', falt_industria), 
                                       ('Entorno', falt_entorno)]:
                if faltantes > 0:
                    variables_encontradas = alt_data[alt_data['clasificacion'] == categoria].head(faltantes)
                    if not variables_encontradas.empty:
                        data = pd.concat([data, variables_encontradas], ignore_index=True)
            
            # Convertir tipos de datos
            columnas_numericas = ['imp_1', 'imp_2', 'imp_3', 'imp_4', 'imp_5',
                                'desemp_1', 'desemp_2', 'desemp_3', 'desemp_4', 'desemp_5',
                                'media_importancia', 'media_desemp']
            
            columnas_existentes = [col for col in columnas_numericas if col in data.columns]
            data[columnas_existentes] = data[columnas_existentes].apply(pd.to_numeric, errors='coerce')
            
            self.analysis_data = data
            return True, f"Datos preparados: {len(data)} variables para análisis"
            
        except Exception as e:
            return False, f"Error en preparación: {str(e)}"
    
    def perform_dofa_analysis(self):
        """Análisis DOFA del entorno organizacional"""
        try:
            variables_dofa = self.analysis_data['dofa'].value_counts().sort_index(ascending=True)
            
            # Calcular métricas
            total_vars = variables_dofa.sum()
            dofa_internas = variables_dofa.get('Debilidad', 0) + variables_dofa.get('Fortaleza', 0)
            dofa_externas = variables_dofa.get('Amenaza', 0) + variables_dofa.get('Oportunidad', 0)
            dofa_positivas = variables_dofa.get('Fortaleza', 0) + variables_dofa.get('Oportunidad', 0)
            dofa_negativas = variables_dofa.get('Amenaza', 0) + variables_dofa.get('Debilidad', 0)
            
            # Clasificar entorno
            prop_internas = dofa_internas / total_vars
            prop_positivas = dofa_positivas / total_vars
            
            if prop_internas >= 0.6:
                tipo_int_ext = 'Interno'
            elif prop_internas <= 0.4:
                tipo_int_ext = 'Externo'
            else:
                tipo_int_ext = 'Equilibrado'
            
            if prop_positivas >= 0.6:
                tipo_pos_neg = 'Positivo'
            elif prop_positivas <= 0.4:
                tipo_pos_neg = 'Negativo'
            else:
                tipo_pos_neg = 'Neutro'
            
            self.results['dofa'] = {
                'variables_dofa': variables_dofa,
                'tipo_entorno': f"{tipo_int_ext} - {tipo_pos_neg}",
                'metricas': {
                    'total': total_vars,
                    'internas': dofa_internas,
                    'externas': dofa_externas,
                    'positivas': dofa_positivas,
                    'negativas': dofa_negativas
                }
            }
            
            return True, "Análisis DOFA completado"
            
        except Exception as e:
            return False, f"Error en análisis DOFA: {str(e)}"
    
    def perform_space_analysis(self):
        """Análisis de matriz SPACE tradicional y ponderada"""
        try:
            # Crear subgrupos SPACE
            data = self.analysis_data
            
            df_competitiva = data[data['clasificacion'] == 'Competitiva'].copy()
            df_financiera = data[data['clasificacion'] == 'Financiera'].copy()
            df_industria = data[data['clasificacion'] == 'Industria'].copy()
            df_entorno = data[data['clasificacion'] == 'Entorno'].copy()
            
            # Calcular pesos relativos para análisis ponderado
            for df_group in [df_competitiva, df_financiera, df_industria, df_entorno]:
                if not df_group.empty:
                    df_group['imp_relativa'] = df_group['media_importancia'] / df_group['media_importancia'].sum()
            
            # SPACE Tradicional
            prom_competitiva = df_competitiva['media_desemp'].mean() - 5
            prom_financiera = df_financiera['media_desemp'].mean()
            prom_industria = df_industria['media_desemp'].mean()
            prom_entorno = df_entorno['media_desemp'].mean() - 5
            
            eje_x_trad = prom_industria + prom_competitiva
            eje_y_trad = prom_financiera + prom_entorno
            
            # SPACE Ponderado
            prom_competitiva_pond = sum(df_competitiva['imp_relativa'] * df_competitiva['media_desemp']) - 5 if not df_competitiva.empty else 0
            prom_financiera_pond = sum(df_financiera['imp_relativa'] * df_financiera['media_desemp']) if not df_financiera.empty else 0
            prom_industria_pond = sum(df_industria['imp_relativa'] * df_industria['media_desemp']) if not df_industria.empty else 0
            prom_entorno_pond = sum(df_entorno['imp_relativa'] * df_entorno['media_desemp']) - 5 if not df_entorno.empty else 0
            
            eje_x_pond = prom_industria_pond + prom_competitiva_pond
            eje_y_pond = prom_financiera_pond + prom_entorno_pond
            
            # Determinar recomendaciones
            def get_space_recommendation(x, y):
                if x > 0 and y > 0: return 'Agresiva'
                elif x < 0 and y > 0: return 'Conservadora'
                elif x > 0 and y < 0: return 'Competitiva'
                else: return 'Defensiva'
            
            recomend_trad = get_space_recommendation(eje_x_trad, eje_y_trad)
            recomend_pond = get_space_recommendation(eje_x_pond, eje_y_pond)
            
            self.results['space'] = {
                'tradicional': {
                    'eje_x': eje_x_trad,
                    'eje_y': eje_y_trad,
                    'recomendacion': recomend_trad,
                    'valores': {
                        'competitiva': round(prom_competitiva, 2),
                        'financiera': round(prom_financiera, 2),
                        'industria': round(prom_industria, 2),
                        'entorno': round(prom_entorno, 2)
                    }
                },
                'ponderado': {
                    'eje_x': eje_x_pond,
                    'eje_y': eje_y_pond,
                    'recomendacion': recomend_pond,
                    'valores': {
                        'competitiva': round(prom_competitiva_pond, 2),
                        'financiera': round(prom_financiera_pond, 2),
                        'industria': round(prom_industria_pond, 2),
                        'entorno': round(prom_entorno_pond, 2)
                    }
                }
            }
            
            return True, "Análisis SPACE completado"
            
        except Exception as e:
            return False, f"Error en análisis SPACE: {str(e)}"
    
    def perform_mckinsey_analysis(self):
        """Análisis de matriz McKinsey/Interna-Externa"""
        try:
            data = self.analysis_data
            
            # Crear grupos interno y externo
            df_internas = pd.concat([
                data[data['clasificacion'] == 'Competitiva'],
                data[data['clasificacion'] == 'Financiera']
            ])
            
            df_externas = pd.concat([
                data[data['clasificacion'] == 'Industria'],
                data[data['clasificacion'] == 'Entorno']
            ])
            
            # Calcular pesos relativos
            if not df_internas.empty:
                df_internas['imp_relativa'] = df_internas['media_importancia'] / df_internas['media_importancia'].sum()
                prom_internas = sum(df_internas['imp_relativa'] * df_internas['media_desemp'])
            else:
                prom_internas = 2.5
            
            if not df_externas.empty:
                df_externas['imp_relativa'] = df_externas['media_importancia'] / df_externas['media_importancia'].sum()
                prom_externas = sum(df_externas['imp_relativa'] * df_externas['media_desemp'])
            else:
                prom_externas = 2.5
            
            # Determinar recomendación McKinsey
            if prom_internas > 3 and prom_externas > 3:
                recomendacion = 'Crecer'
            elif prom_internas > 3 and prom_externas < 3:
                recomendacion = 'Crecer Selectivamente Portafolios'
            elif prom_internas < 3 and prom_externas > 3:
                recomendacion = 'Crecer Selectivamente Mercados'
            elif prom_internas < 3 and prom_externas < 3:
                recomendacion = 'Mantener'
            elif prom_internas < 2 and prom_externas < 2:
                recomendacion = 'Reducir'
            else:
                recomendacion = 'Mantener Selectivamente'
            
            self.results['mckinsey'] = {
                'prom_internas': round(prom_internas, 2),
                'prom_externas': round(prom_externas, 2),
                'recomendacion': recomendacion
            }
            
            return True, "Análisis McKinsey completado"
            
        except Exception as e:
            return False, f"Error en análisis McKinsey: {str(e)}"
    
    def generate_visualizations(self):
        """Genera las visualizaciones de los análisis"""
        visualizations = {}
        
        try:
            # Gráfico SPACE Tradicional
            space_trad = self.results['space']['tradicional']
            fig_space_trad = go.Figure()
            
            fig_space_trad.add_trace(go.Scatter(
                x=[0, space_trad['eje_x']], 
                y=[0, space_trad['eje_y']],
                mode='lines+markers',
                line=dict(color='#1F4A90', width=4),
                marker=dict(size=[8, 12], color=['#1F4A90', '#B2FFDA']),
                name='Vector SPACE'
            ))
            
            fig_space_trad.add_hline(y=0, line_dash="dash", line_color="black")
            fig_space_trad.add_vline(x=0, line_dash="dash", line_color="black")
            
            # Agregar etiquetas de cuadrantes para SPACE Tradicional
            fig_space_trad.add_annotation(x=1.5, y=1.5, text="AGRESIVA", showarrow=False, 
                                         font=dict(size=12, color="green"))
            fig_space_trad.add_annotation(x=-1.5, y=1.5, text="CONSERVADORA", showarrow=False, 
                                         font=dict(size=12, color="blue"))
            fig_space_trad.add_annotation(x=1.5, y=-1.5, text="COMPETITIVA", showarrow=False, 
                                         font=dict(size=12, color="orange"))
            fig_space_trad.add_annotation(x=-1.5, y=-1.5, text="DEFENSIVA", showarrow=False, 
                             font=dict(size=12, color="red"))
            
            fig_space_trad.update_layout(
                title="Matriz SPACE Tradicional",
                xaxis_title="Industria + Competitiva",
                yaxis_title="Financiera + Entorno",
                xaxis=dict(range=[-3, 3], zeroline=True, zerolinecolor="black", zerolinewidth=2),
                yaxis=dict(range=[-3, 3], zeroline=True, zerolinecolor="black", zerolinewidth=2),
                showlegend=True,
                template="plotly_white",
                font=dict(color="#1E5A73"),
                height=500,
                width=500
            )
            
            visualizations['space_tradicional'] = fig_space_trad
            
            # Gráfico SPACE Ponderado
            space_pond = self.results['space']['ponderado']
            fig_space_pond = go.Figure()
            
            fig_space_pond.add_trace(go.Scatter(
                x=[0, space_pond['eje_x']], 
                y=[0, space_pond['eje_y']],
                mode='lines+markers',
                line=dict(color='#1E5A73', width=4),
                marker=dict(size=[8, 12], color=['#1E5A73', '#B2FFDA']),
                name='Vector SPACE Ponderado'
            ))
            
            fig_space_pond.add_hline(y=0, line_dash="dash", line_color="black")
            fig_space_pond.add_vline(x=0, line_dash="dash", line_color="black")
            
            # Agregar etiquetas de cuadrantes para SPACE Ponderado
            fig_space_pond.add_annotation(x=1.5, y=1.5, text="AGRESIVA", showarrow=False, 
                                         font=dict(size=12, color="green"))
            fig_space_pond.add_annotation(x=-1.5, y=1.5, text="CONSERVADORA", showarrow=False, 
                                         font=dict(size=12, color="blue"))
            fig_space_pond.add_annotation(x=1.5, y=-1.5, text="COMPETITIVA", showarrow=False, 
                                         font=dict(size=12, color="orange"))
            fig_space_pond.add_annotation(x=-1.5, y=-1.5, text="DEFENSIVA", showarrow=False, 
                                         font=dict(size=12, color="red"))
            
            fig_space_pond.update_layout(
                title="Matriz SPACE Ponderada",
                xaxis_title="Industria + Competitiva (Ponderado)",
                yaxis_title="Financiera + Entorno (Ponderado)",
                xaxis=dict(range=[-3, 3], zeroline=True, zerolinecolor="black", zerolinewidth=2),
                yaxis=dict(range=[-3, 3], zeroline=True, zerolinecolor="black", zerolinewidth=2),
                showlegend=True,
                template="plotly_white",
                font=dict(color="#1E5A73"),
                height=500,
                width=500
            )
            
            visualizations['space_ponderado'] = fig_space_pond
            
            # Gráfico McKinsey
            mckinsey = self.results['mckinsey']
            fig_mckinsey = go.Figure()
            
            fig_mckinsey.add_trace(go.Scatter(
                x=[mckinsey['prom_internas']], 
                y=[mckinsey['prom_externas']],
                mode='markers',
                marker=dict(size=30, color='#1F4A90', symbol='circle'),
                name='Posición Estratégica'
            ))
            
            # Líneas de división McKinsey
            fig_mckinsey.add_hline(y=2, line_dash="solid", line_color="black")
            fig_mckinsey.add_hline(y=3, line_dash="solid", line_color="black")
            fig_mckinsey.add_vline(x=2, line_dash="solid", line_color="black")
            fig_mckinsey.add_vline(x=3, line_dash="solid", line_color="black")
            
            fig_mckinsey.update_layout(
                title="Matriz McKinsey/Interna-Externa",
                xaxis_title="Factores Internos",
                yaxis_title="Factores Externos",
                xaxis=dict(range=[1, 4]),
                yaxis=dict(range=[1, 4]),
                showlegend=True,
                template="plotly_white",
                font=dict(color="#1E5A73")
            )
            
            visualizations['mckinsey'] = fig_mckinsey
            
            # Gráfico DOFA
            dofa_data = self.results['dofa']['variables_dofa']
            fig_dofa = px.pie(
                values=dofa_data.values,
                names=dofa_data.index,
                title="Distribución de Variables DOFA",
                color_discrete_sequence=['#1F4A90', '#1E5A73', '#B2FFDA', '#7FB3D3']
            )
            
            visualizations['dofa'] = fig_dofa
            
            return visualizations
            
        except Exception as e:
            st.error(f"Error generando visualizaciones: {str(e)}")
            return {}

# Función principal de la aplicación
def main():
    load_css()
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AI-Mindnovation</h1>
        <p>Plataforma de Análisis Estratégico Avanzado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    auth = get_auth_manager()
    
    # Sistema de autenticación
    if not st.session_state.authenticated:
        st.markdown("### 🔐 Acceso a la Plataforma")
        
        tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Usuario")
                password = st.text_input("Contraseña", type="password")
                submit = st.form_submit_button("Iniciar Sesión")
                
                if submit:
                    if auth.authenticate(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("¡Bienvenido!")
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("Nuevo Usuario")
                new_email = st.text_input("Email")
                new_password = st.text_input("Contraseña", type="password")
                confirm_password = st.text_input("Confirmar Contraseña", type="password")
                register = st.form_submit_button("Registrarse")
                
                if register:
                    if new_password != confirm_password:
                        st.error("Las contraseñas no coinciden")
                    elif len(new_password) < 6:
                        st.error("La contraseña debe tener al menos 6 caracteres")
                    else:
                        success, message = auth.register_user(new_username, new_password, new_email)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
    
    else:
        # Aplicación principal para usuarios autenticados
        user_info = auth.get_user_info(st.session_state.username)
        
        # Sidebar con información del usuario
        with st.sidebar:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #B2FFDA 0%, #E8FFF5 100%); 
                        padding: 1rem; border-radius: 10px; text-align: center;">
                <h3>👋 Hola, {st.session_state.username}!</h3>
                <p>Análisis realizados: {user_info.get('analyses_count', 0)}</p>
                <p><small>Último acceso: {user_info.get('last_login', 'N/A')[:10] if user_info.get('last_login') else 'N/A'}</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Cerrar Sesión"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.rerun()
        
        # ===== SELECTOR DE ANÁLISIS (NUEVO) =====
        st.markdown("### 🔬 Selecciona tu Análisis")
        
        # Opciones de análisis disponibles
        analysis_options = [
            "📈 Análisis Estratégico (Matrices DOFA, SPACE, McKinsey)",
            "📊 Análisis de Valor Percibido (Comparación vs Competidores)"
        ]
        
        selected_analysis = st.selectbox(
            "¿Qué análisis deseas realizar?",
            analysis_options,
            help="Selecciona el tipo de análisis que mejor se adapte a tus necesidades"
        )
        
        st.markdown("---")
        


# ===== CÓDIGO COMPLETO PARA REEMPLAZAR =====
# (Copia esto y reemplaza desde "# Interfaz principal de análisis" hasta antes del Footer)

        
        # ===== ANÁLISIS ESTRATÉGICO =====
        if selected_analysis == analysis_options[0]:
            st.markdown("### 📊 Análisis Estratégico")
            
            # Upload de archivo
            uploaded_file = st.file_uploader(
                "Sube tu archivo Excel con datos de análisis estratégico",
                type=['xlsx', 'xls'],
                help="El archivo debe contener las hojas 'importancia' y 'desempeño'"
            )
            
            if uploaded_file is not None:
                analysis = StrategicAnalysis()
                
                # Cargar datos
                success, message = analysis.load_excel_data(uploaded_file)
                
                if success:
                    st.success(message)
                    
                    # Botón para ejecutar análisis
                    if st.button("🚀 Ejecutar Análisis Completo", key="analyze_btn"):
                        with st.spinner("Procesando análisis estratégico..."):
                            
                            # Preparar datos
                            success, msg = analysis.prepare_analysis_data()
                            if not success:
                                st.error(msg)
                                return
                            
                            # Ejecutar análisis
                            analysis.perform_dofa_analysis()
                            analysis.perform_space_analysis()
                            analysis.perform_mckinsey_analysis()
                            
                            # Actualizar contador de análisis
                            auth.increment_analysis_count(st.session_state.username)
                            
                            st.success("¡Análisis completado exitosamente!")
                            
                            # Mostrar resultados
                            st.markdown("## 📈 Resultados del Análisis")
                            
                            # Métricas principales
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{analysis.results['dofa']['tipo_entorno']}</div>
                                    <div class="metric-label">Tipo de Entorno</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{analysis.results['space']['tradicional']['recomendacion']}</div>
                                    <div class="metric-label">SPACE Tradicional</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col3:
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{analysis.results['space']['ponderado']['recomendacion']}</div>
                                    <div class="metric-label">SPACE Ponderado</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col4:
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{analysis.results['mckinsey']['recomendacion']}</div>
                                    <div class="metric-label">Recomendación McKinsey</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                            # Recomendación final destacada
                            space_rec = analysis.results['space']['ponderado']['recomendacion']
                            mckinsey_rec = analysis.results['mckinsey']['recomendacion']
                            
                            st.markdown(f"""
                            <div class="success-card">
                                <h2>🎯 Recomendación Estratégica Final</h2>
                                <h3>{mckinsey_rec} de forma {space_rec}</h3>
                                <p>Basado en el análisis integrado de matrices SPACE ponderada y McKinsey</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Tabs con análisis detallados
                            tab1, tab2, tab3, tab4 = st.tabs(["📊 DOFA", "🎯 SPACE", "📈 McKinsey", "📋 Datos"])
                            
                            with tab1:
                                st.markdown("### Análisis DOFA del Entorno Organizacional")
                                
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    # Generar visualizaciones
                                    visualizations = analysis.generate_visualizations()
                                    if 'dofa' in visualizations:
                                        st.plotly_chart(visualizations['dofa'], use_container_width=True)
                                
                                with col2:
                                    dofa_results = analysis.results['dofa']
                                    st.markdown("#### Distribución de Variables:")
                                    for categoria, cantidad in dofa_results['variables_dofa'].items():
                                        st.write(f"**{categoria}:** {cantidad} variables")
                                    
                                    st.markdown("#### Clasificación del Entorno:")
                                    st.info(f"**{dofa_results['tipo_entorno']}**")
                            
                            with tab2:
                                st.markdown("### Análisis de Matriz SPACE")
                                
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    st.markdown("#### SPACE Tradicional")
                                    if 'space_tradicional' in visualizations:
                                        st.plotly_chart(visualizations['space_tradicional'], use_container_width=True)
                                    
                                    space_trad = analysis.results['space']['tradicional']
                                    st.markdown("**Valores por dimensión:**")
                                    for dim, valor in space_trad['valores'].items():
                                        st.write(f"**{dim.title()}:** {valor}")
                                    st.success(f"**Recomendación:** {space_trad['recomendacion']}")
                                
                                with col2:
                                    st.markdown("#### SPACE Ponderado")
                                    if 'space_ponderado' in visualizations:
                                        st.plotly_chart(visualizations['space_ponderado'], use_container_width=True)
                                    
                                    space_pond = analysis.results['space']['ponderado']
                                    st.markdown("**Valores ponderados por dimensión:**")
                                    for dim, valor in space_pond['valores'].items():
                                        st.write(f"**{dim.title()}:** {valor}")
                                    st.success(f"**Recomendación:** {space_pond['recomendacion']}")
                            
                            with tab3:
                                st.markdown("### Análisis de Matriz McKinsey/Interna-Externa")
                                
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    if 'mckinsey' in visualizations:
                                        st.plotly_chart(visualizations['mckinsey'], use_container_width=True)
                                
                                with col2:
                                    mckinsey_results = analysis.results['mckinsey']
                                    
                                    st.markdown("#### Puntuaciones:")
                                    st.metric("Factores Internos", mckinsey_results['prom_internas'])
                                    st.metric("Factores Externos", mckinsey_results['prom_externas'])
                                    
                                    st.markdown("#### Interpretación:")
                                    st.info(f"**{mckinsey_results['recomendacion']}**")
                                    
                                    # Explicación de la recomendación
                                    recom_explicacion = {
                                        'Crecer': '🚀 Posición fuerte en mercado atractivo. Invertir para maximizar crecimiento.',
                                        'Crecer Selectivamente Portafolios': '📊 Fortalezas internas con mercado moderado. Enfocar recursos en áreas clave.',
                                        'Crecer Selectivamente Mercados': '🎯 Mercado atractivo pero capacidades limitadas. Desarrollar competencias.',
                                        'Mantener': '⚖️ Posición equilibrada. Mantener posición actual y mejorar eficiencias.',
                                        'Reducir': '📉 Posición débil en mercado poco atractivo. Considerar desinversión.'
                                    }
                                    
                                    st.markdown("#### Estrategia Recomendada:")
                                    st.write(recom_explicacion.get(mckinsey_results['recomendacion'], 'Evaluar opciones estratégicas'))
                            
                            with tab4:
                                st.markdown("### Datos del Análisis")
                                
                                # Mostrar resumen de datos procesados
                                st.markdown("#### Variables Utilizadas en el Análisis:")
                                
                                # Crear tabla resumen
                                summary_data = analysis.analysis_data[['palabras_clave', 'clasificacion', 'dofa', 
                                                                      'media_importancia', 'media_desemp']].copy()
                                summary_data = summary_data.round(2)
                                summary_data.columns = ['Variable', 'Clasificación SPACE', 'DOFA', 'Importancia', 'Desempeño']
                                
                                st.dataframe(summary_data, use_container_width=True)
                                
                                # Estadísticas por categoría
                                st.markdown("#### Estadísticas por Categoría SPACE:")
                                for categoria in ['Competitiva', 'Financiera', 'Industria', 'Entorno']:
                                    subset = analysis.analysis_data[analysis.analysis_data['clasificacion'] == categoria]
                                    if not subset.empty:
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric(f"{categoria} - Variables", len(subset))
                                        with col2:
                                            st.metric(f"{categoria} - Importancia Promedio", round(subset['media_importancia'].mean(), 2))
                                        with col3:
                                            st.metric(f"{categoria} - Desempeño Promedio", round(subset['media_desemp'].mean(), 2))
                            
                            # Botón de descarga de resultados
                            st.markdown("---")
                            st.markdown("### 💾 Descargar Resultados")
                            
                            # Crear Excel con resultados
                            output = io.BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                # Hoja con variables utilizadas
                                summary_data.to_excel(writer, sheet_name='Variables_Analisis', index=False)
                                
                                # Hoja con resultados
                                results_df = pd.DataFrame({
                                    'Análisis': ['DOFA - Tipo Entorno', 'SPACE Tradicional', 'SPACE Ponderado', 'McKinsey', 'Recomendación Final'],
                                    'Resultado': [
                                        analysis.results['dofa']['tipo_entorno'],
                                        analysis.results['space']['tradicional']['recomendacion'],
                                        analysis.results['space']['ponderado']['recomendacion'],
                                        analysis.results['mckinsey']['recomendacion'],
                                        f"{mckinsey_rec} de forma {space_rec}"
                                    ]
                                })
                                results_df.to_excel(writer, sheet_name='Resultados', index=False)
                            
                            excel_data = output.getvalue()
                            
                            st.download_button(
                                label="📊 Descargar Resultados en Excel",
                                data=excel_data,
                                file_name=f"analisis_estrategico_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                else:
                    st.error(message)
         
        elif selected_analysis == analysis_options[1]:  # Valor Percibido
            st.info("🆕 **Nueva funcionalidad** - Compara el desempeño de tu empresa vs competidores en atributos valorados por los clientes")
            analisis_valor_percibido()
    
       
               
        # Footer
        st.markdown("""
        <div class="footer">
            <p>🧠 <strong>AI-Mindnovation</strong> | Plataforma de Análisis Estratégico</p>
            <p>Desarrollado para optimizar la toma de decisiones estratégicas</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()