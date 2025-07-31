import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
import json
from datetime import datetime

def analisis_valor_percibido():
    """
    Módulo de Análisis de Valor Percibido para Streamlit
    """
    st.header("📊 Análisis de Valor Percibido")
    st.markdown("---")
    
    # Sidebar para configuración
    with st.sidebar:
        st.subheader("⚙️ Configuración del Análisis")
        
        # Número de atributos a mostrar
        num_atributos = st.slider(
            "Número de atributos principales a mostrar",
            min_value=5, max_value=20, value=10
        )
        
        # Configuración de colores
        st.subheader("🎨 Colores del Gráfico")
        color_empresa = st.color_picker("Color Empresa", "#1f77b4")
        color_mercado = st.color_picker("Color Mercado", "#ff7f0e")
    
    # Instrucciones para el usuario
    with st.expander("📋 Instrucciones de Uso", expanded=False):
        st.markdown("""
        **Formato del archivo Excel requerido:**
        
        **Hoja 'importancia':**
        - palabras_clave: Atributos a evaluar
        - imp_1, imp_2, imp_3, imp_4, imp_5: Evaluaciones de importancia (1-10)
        
        **Hoja 'desempeño':**
        - empresa: Evaluación de tu empresa
        - [Nombre_Competidor_1]: Evaluación del primer competidor
        - [Nombre_Competidor_2]: Evaluación del segundo competidor
        - [Más competidores...]: Puedes agregar más columnas con nombres de competidores
        
        **Nota:** Ahora puedes usar nombres reales de competidores en lugar de 'compet_1', 'compet_2'
        """)
        st.markdown("""
        **⚠️ IMPORTANTE - Formato del archivo:**
        - Las hojas deben llamarse exactamente 'importancia' y 'desempeño'
        - NO debe haber columnas duplicadas en el archivo
        - Ambas hojas deben tener el mismo número de filas
        - La primera fila debe contener los nombres de las columnas
        """)
    
    # Upload del archivo
    uploaded_file = st.file_uploader(
        "📁 Sube tu archivo de datos",
        type=['xlsx', 'xls'],
        help="Archivo Excel con las hojas 'importancia' y 'desempeño'"
    )
    
    if uploaded_file is not None:
        try:
            # Leer los datos
            with st.spinner("📖 Leyendo datos..."):
                df_importancia = pd.read_excel(uploaded_file, sheet_name='importancia', header=0)
                df_desemp = pd.read_excel(uploaded_file, sheet_name='desempeño', header=0)
            
            # Mostrar vista previa de los datos
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Vista previa - Importancia")
                st.dataframe(df_importancia.head(), use_container_width=True)
            
            with col2:
                st.subheader("Vista previa - Desempeño")
                st.dataframe(df_desemp.head(), use_container_width=True)
            
            # Identificar columnas de competidores automáticamente
            competidor_cols = [col for col in df_desemp.columns if col not in ['empresa']]
            
            st.success(f"✅ Se encontraron {len(competidor_cols)} competidores: {', '.join(competidor_cols)}")
            
            # Selección de competidores a incluir en el análisis
            st.subheader("🏢 Selecciona los competidores a comparar")
            competidores_seleccionados = st.multiselect(
                "Competidores:",
                competidor_cols,
                default=competidor_cols[:2] if len(competidor_cols) >= 2 else competidor_cols,
                help="Selecciona los competidores que quieres incluir en el gráfico radar"
            )
            
            if len(competidores_seleccionados) > 0:
                # Procesamiento de datos
                with st.spinner("🔄 Procesando datos..."):
                    # Crear dataset consolidado
                    cols_desemp = ['empresa'] + competidores_seleccionados
                    desemp = df_desemp[cols_desemp]
                    
                    # Verificar y evitar conflictos de columnas
                    if any(col in df_importancia.columns for col in desemp.columns):
                        df = pd.concat([df_importancia.reset_index(drop=True), 
                                        desemp.reset_index(drop=True)], axis=1)
                    else:
                        df = df_importancia.join(desemp)
                    
                    # Calcular medias
                    df['media_importancia'] = df[['imp_1', 'imp_2', 'imp_3', 'imp_4', 'imp_5']].mean(axis=1)
                    df['media_desemp'] = df[cols_desemp].mean(axis=1)
                    
                    # Ordenar por importancia
                    df = df.sort_values(by='media_importancia', ascending=False, na_position='last')
                    
                    # Filtrar top atributos
                    data = df.iloc[0:num_atributos, :]
                    
                    # Calcular importancia relativa
                    data['imp_relativa'] = data['media_importancia'] / data['media_importancia'].sum()
                    
                    # Calcular desempeño ponderado
                    data['desmp_empresa'] = data['imp_relativa'] * data['empresa']
                    data['desmp_mercado'] = data['imp_relativa'] * data['media_desemp']
                    
                    # Calcular desempeño ponderado para competidores seleccionados
                    for comp in competidores_seleccionados:
                        data[f'desmp_{comp}'] = data['imp_relativa'] * data[comp]
                
                # Mostrar tabla de resultados
                st.subheader(f"📈 Top {num_atributos} Atributos por Importancia")
                resultado_cols = ['palabras_clave', 'media_importancia', 'desmp_empresa', 'desmp_mercado'] + [f'desmp_{comp}' for comp in competidores_seleccionados]
                resultado_df = data[resultado_cols].copy()
                resultado_df = resultado_df.round(4)
                st.dataframe(resultado_df, use_container_width=True)
                
                # Crear gráfico radar
                st.subheader("🎯 Gráfico Radar - Valor Percibido")
                
                # Opciones de personalización del gráfico
                col1, col2 = st.columns(2)
                with col1:
                    incluir_mercado = st.checkbox("Incluir línea de Mercado", value=True)
                with col2:
                    mostrar_valores = st.checkbox("Mostrar valores en el gráfico", value=False)
                
                # Crear el gráfico
                atributos = list(data['palabras_clave'])
                fig = go.Figure()
                
                # Añadir empresa
                fig.add_trace(go.Scatterpolar(
                    r=data['desmp_empresa'],
                    theta=atributos,
                    fill='toself',
                    name='Tu Empresa',
                    line_color=color_empresa,
                    opacity=0.7
                ))
                
                # Añadir competidores seleccionados
                colors = ['#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
                for i, comp in enumerate(competidores_seleccionados):
                    fig.add_trace(go.Scatterpolar(
                        r=data[f'desmp_{comp}'],
                        theta=atributos,
                        fill='toself',
                        name=comp,
                        line_color=colors[i % len(colors)],
                        opacity=0.6
                    ))
                
                # Añadir mercado si está seleccionado
                if incluir_mercado:
                    fig.add_trace(go.Scatterpolar(
                        r=data['desmp_mercado'],
                        theta=atributos,
                        fill='toself',
                        name='Promedio Mercado',
                        line_color=color_mercado,
                        line_dash='dash',
                        opacity=0.5
                    ))
                
                # Configurar layout del gráfico
                max_value = data[['desmp_empresa'] + [f'desmp_{comp}' for comp in competidores_seleccionados] + (['desmp_mercado'] if incluir_mercado else [])].max().max()
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max_value + 0.01],
                            showticklabels=mostrar_valores,
                            ticks="outside",
                            tickfont=dict(size=10)
                        ),
                        angularaxis=dict(
                            tickfont=dict(size=10)
                        )
                    ),
                    showlegend=True,
                    title={
                        'text': f"Análisis de Valor Percibido - Top {num_atributos} Atributos",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 16}
                    },
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    ),
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Insights automáticos
                st.subheader("💡 Insights Automáticos")
                
                # Encontrar fortalezas y debilidades
                empresa_scores = data['desmp_empresa'].values
                mercado_scores = data['desmp_mercado'].values
                
                fortalezas = data[empresa_scores > mercado_scores]['palabras_clave'].tolist()
                debilidades = data[empresa_scores < mercado_scores]['palabras_clave'].tolist()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success("**🏆 Fortalezas vs Mercado:**")
                    for fortaleza in fortalezas[:5]:
                        st.write(f"• {fortaleza}")
                
                with col2:
                    st.warning("**⚠️ Oportunidades de Mejora:**")
                    for debilidad in debilidades[:5]:
                        st.write(f"• {debilidad}")
                
                # Comparación con competidores
                st.subheader("🥊 Comparación Competitiva")
                for comp in competidores_seleccionados:
                    comp_scores = data[f'desmp_{comp}'].values
                    ventajas = data[empresa_scores > comp_scores]['palabras_clave'].tolist()
                    desventajas = data[empresa_scores < comp_scores]['palabras_clave'].tolist()
                    
                    with st.expander(f"📊 vs {comp}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.success(f"**Ventajas vs {comp}:**")
                            for ventaja in ventajas[:3]:
                                st.write(f"• {ventaja}")
                        with col2:
                            st.error(f"**Desventajas vs {comp}:**")
                            for desventaja in desventajas[:3]:
                                st.write(f"• {desventaja}")
                
                # Exportar resultados
                st.subheader("💾 Exportar Resultados")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Exportar datos a Excel
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        resultado_df.to_excel(writer, sheet_name='Resultados_Valor_Percibido', index=False)
                        data[['palabras_clave', 'media_importancia', 'imp_relativa'] + cols_desemp].to_excel(
                            writer, sheet_name='Datos_Procesados', index=False
                        )
                    
                    st.download_button(
                        label="📊 Descargar Excel",
                        data=buffer.getvalue(),
                        file_name=f"analisis_valor_percibido_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with col2:
                    # Exportar configuración del gráfico
                    config_data = {
                        "competidores_seleccionados": competidores_seleccionados,
                        "num_atributos": num_atributos,
                        "incluir_mercado": incluir_mercado,
                        "color_empresa": color_empresa,
                        "color_mercado": color_mercado,
                        "fecha_analisis": datetime.now().isoformat()
                    }
                    
                    st.download_button(
                        label="⚙️ Descargar Configuración",
                        data=json.dumps(config_data, indent=2),
                        file_name=f"config_valor_percibido_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                        mime="application/json"
                    )
                
                # Log de actividad (si tienes sistema de usuarios)
                if 'user_email' in st.session_state:
                    log_activity(
                        user_email=st.session_state.user_email,
                        activity_type="analisis_valor_percibido",
                        details={
                            "competidores": competidores_seleccionados,
                            "num_atributos": num_atributos,
                            "timestamp": datetime.now().isoformat()
                        }
                    )
            
            else:
                st.warning("⚠️ Por favor selecciona al menos un competidor para realizar el análisis.")
                
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")
            st.info("Verifica que el archivo tenga las hojas 'importancia' y 'desempeño' con el formato correcto.")
    
    else:
        st.info("👆 Sube un archivo Excel para comenzar el análisis")

def log_activity(user_email, activity_type, details):
    """
    Función para registrar actividad del usuario
    (Implementar según tu sistema de logs)
    """
    # Aquí puedes implementar el logging a tu base de datos o archivo
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_email,
        "activity": activity_type,
        "details": details
    }
    # Ejemplo: guardar en session_state para el panel admin
    if 'activity_logs' not in st.session_state:
        st.session_state.activity_logs = []
    st.session_state.activity_logs.append(log_entry)

# Ejemplo de cómo integrar en tu app principal
if __name__ == "__main__":
    st.set_page_config(
        page_title="Análisis de Valor Percibido",
        page_icon="📊",
        layout="wide"
    )
    analisis_valor_percibido()