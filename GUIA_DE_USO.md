# Guía de Uso - Módulo AI Mindnovation Strategic Analysis

## 📋 Descripción General

Este módulo de Odoo permite realizar **4 tipos de análisis estratégico** para evaluar la posición competitiva de tu empresa:

1. **Análisis DOFA** - Identifica Fortalezas, Oportunidades, Debilidades y Amenazas
2. **Matriz SPACE** - Determina la postura estratégica (Agresiva, Conservadora, Defensiva o Competitiva)
3. **Matriz McKinsey** - Evalúa el atractivo del mercado y la capacidad competitiva
4. **Análisis de Valor Percibido** - Compara tu desempeño contra competidores

---

## 📁 Archivos Excel Requeridos

El módulo necesita **DOS archivos Excel** con estructuras específicas:

### 1️⃣ `Formulario_datos_entrada_analisis_tipo_estrategia.xlsx`

Este archivo contiene las variables estratégicas que serán evaluadas. **Debe tener DOS hojas obligatorias:**

#### 📊 Hoja: `importancia`
Califica la **importancia** de cada variable para tu negocio (escala 1-5).

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| **Nro** | Número consecutivo de la variable | 1, 2, 3... |
| **Palabras Clave** | Identificador corto | "Innovación", "Calidad" |
| **Descripción** | Explicación detallada | "Capacidad de innovar productos" |
| **Usuario 1, Usuario 2...** | Calificaciones de importancia (1-5) | 5, 4, 5, 3 |

**Ejemplo:**
```
Nro | Palabras Clave    | Descripción                      | Usuario1 | Usuario2 | Usuario3
1   | Innovación        | Capacidad innovación productos   | 5        | 4        | 5
2   | Calidad           | Calidad del producto final       | 5        | 5        | 4
3   | Precio            | Competitividad en precios        | 3        | 4        | 3
```

#### 📊 Hoja: `desempeño`
Califica el **desempeño real** de tu empresa en cada variable (escala 1-5).

**Mismo formato que la hoja `importancia`, pero evaluando el desempeño actual:**
```
Nro | Palabras Clave    | Descripción                      | Usuario1 | Usuario2 | Usuario3
1   | Innovación        | Capacidad innovación productos   | 4        | 3        | 4
2   | Calidad           | Calidad del producto final       | 5        | 5        | 5
3   | Precio            | Competitividad en precios        | 2        | 3        | 2
```

---

### 2️⃣ `Formulario_datos_entrada_analisis_valor_percibido.xlsx`

Este archivo es **opcional** y se usa solo para el **Análisis de Valor Percibido** (comparación con competidores).

#### 📊 Estructura:
- **Mismas columnas** de variables (Nro, Palabras Clave, Descripción)
- **Columnas adicionales** para cada competidor

**Ejemplo:**
```
Nro | Palabras Clave    | Descripción                      | Competidor A | Competidor B | Competidor C
1   | Innovación        | Capacidad innovación productos   | 3            | 4            | 2
2   | Calidad           | Calidad del producto final       | 4            | 3            | 5
3   | Precio            | Competitividad en precios        | 4            | 5            | 4
```

**⚠️ Importante:** Las variables (Nro, Palabras Clave) deben coincidir con las del primer archivo.

---

## 🚀 Pasos para Usar el Módulo

### **Paso 1: Crear un Nuevo Análisis**

1. Ve a **Menú → AI Mindnovation → Análisis Estratégico**
2. Click en **"Crear"**
3. Completa los campos básicos:
   - **Nombre del Análisis**: Ej. "Análisis Q4 2025"
   - **Usuario**: Selecciona el responsable
   - **Fecha**: Se asigna automáticamente


### **Paso 2: Cargar los Archivos Excel**

1. En la sección **"Archivos"**, usa los botones de carga:
   - **📎 Archivo Importancia**: Sube `Formulario_datos_entrada_analisis_tipo_estrategia.xlsx`
   - **📎 Archivo Desempeño**: Sube el mismo archivo (tiene ambas hojas)

2. **IMPORTANTE:** Después de cargar los archivos, debes presionar el botón **"PROCESAR ANÁLISIS"** (arriba a la izquierda) para que el sistema lea los datos y cargue las variables.

3. El sistema procesará automáticamente:
   - Hoja `importancia` → Calcula promedios de importancia
   - Hoja `desempeño` → Calcula promedios de desempeño

### **Paso 3: Revisar Variables Cargadas**

1. Ve a la pestaña **"Variables"**
2. Verifica que se cargaron correctamente:
   - ✅ Nro, Palabras Clave, Descripción
   - ✅ Media Importancia (promedio de usuarios)
   - ✅ Media Desempeño (promedio de usuarios)
   - ✅ Clasificación DOFA (Fortaleza, Debilidad, Oportunidad, Amenaza)

**🔍 Clasificación Automática:**
- **Fortaleza** = Alta importancia + Alto desempeño (Interno)
- **Debilidad** = Alta importancia + Bajo desempeño (Interno)
- **Oportunidad** = Alta importancia + Alto desempeño (Externo)
- **Amenaza** = Alta importancia + Bajo desempeño (Externo)

### **Paso 4: Procesar los Análisis**

1. Click en el botón verde **"Procesar Análisis"**
2. El sistema calculará automáticamente:
   - ✅ **Análisis DOFA** (conteos, proporciones, tipo de entorno)
   - ✅ **Matriz SPACE Tradicional** (posición competitiva tradicional)
   - ✅ **Matriz SPACE Ponderada** (posición competitiva ponderada)
   - ✅ **Matriz McKinsey** (estrategia recomendada)

3. Estado cambia a **"Procesado"** ✅


### **Paso 5: Agregar o Subir Competidores (Opcional)**

Para el **Análisis de Valor Percibido**, necesitas agregar competidores:

1. En la pestaña **"Valor Percibido"**
2. Click en **"Gestionar Competidores"** para agregarlos manualmente
3. O utiliza el botón **"Subir Competidores"** para importar desde Excel
   - **Nombre del Competidor**
   - Para cada variable, ingresa su **desempeño** (1-5)

**💡 Tip:** Puedes importar desde Excel usando el archivo `Formulario_datos_entrada_analisis_valor_percibido.xlsx`

> **NOTA IMPORTANTE:**
> La función de importación de competidores desde Excel está en construcción. Actualmente, el sistema procesa las hojas `importancia` y `desempeño` y mapea los campos automáticamente, pero puede presentar errores o comportamientos inesperados. Si tienes problemas, agrega los competidores manualmente mientras se estabiliza esta función.

4. Regresa al análisis y presiona **"Procesar Análisis"** nuevamente
5. Se calculará automáticamente:
   - Desempeño ponderado de tu empresa
   - Desempeño promedio del mercado (competidores)
   - Fortalezas vs mercado
   - Oportunidades de mejora
   - Posición competitiva

---

## 📊 Visualizaciones Disponibles

Cada análisis incluye **gráficos interactivos** (Chart.js):

### 🥧 **1. Gráfico Circular DOFA**
- Muestra la distribución de variables: Fortalezas, Debilidades, Oportunidades, Amenazas

### 📡 **2. Radar SPACE Tradicional**
- Visualiza 4 dimensiones: Competitiva, Financiera, Industria, Entorno

### 📡 **3. Radar SPACE Ponderado**
- Versión ponderada por importancia de variables

### 📈 **4. Matriz McKinsey (Scatter)**
- Gráfico de dispersión: Capacidad Interna vs Atractivo Externo
- Recomendación estratégica según posición

### 🎯 **5. Radar Valor Percibido**
- Compara tu empresa vs promedio de competidores en todas las variables

---

## 📥 Exportar Resultados a Excel

1. Después de procesar el análisis, aparece el botón **"Exportar a Excel"** ✅
2. Click en el botón verde con ícono 📥
3. Se genera un archivo Excel con **3 hojas:**

### 📄 **Hoja 1: Variables_Analisis**
Todas las variables con:
- Nro, Palabras Clave, Descripción
- DOFA, Clasificación
- Media Importancia, Media Desempeño

### 📄 **Hoja 2: Resultados**
Resumen de todos los análisis:
- **DOFA**: Conteos y proporciones
- **SPACE Tradicional**: Ejes X/Y y recomendación
- **SPACE Ponderado**: Ejes X/Y y recomendación
- **McKinsey**: Promedios y estrategia
- **Valor Percibido**: Desempeños y posición

### 📄 **Hoja 3: Competidores** (opcional)
Lista de competidores con sus desempeños por variable

**📌 Formato:** `analisis_<usuario>_YYYYMMDD_HHMMSS.xlsx`

---

## 🎓 Interpretación de Resultados

### **Análisis DOFA**
- **Tipo de Entorno**: Indica si tu situación es:
  - ✅ **Optimista** (más positivas)
  - ⚠️ **Realista** (equilibrado)
  - ❌ **Pesimista** (más negativas)

### **Matriz SPACE**
- **Recomendación Estratégica:**
  - 🎯 **Agresiva**: Expansión y crecimiento
  - 🛡️ **Conservadora**: Consolidación
  - ⚔️ **Defensiva**: Protección de posición
  - 💪 **Competitiva**: Diferenciación

### **Matriz McKinsey**
- **Estrategia Recomendada** según posición 3x3:
  - **Alto-Alto**: Invertir para crecer
  - **Medio**: Selectividad
  - **Bajo-Bajo**: Cosechar o desinvertir

### **Valor Percibido**
- **Fortalezas**: Variables donde superas al mercado
- **Debilidades**: Variables donde estás por debajo
- **Posición Competitiva**: Líder, Competitivo, o Necesita Mejora

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo editar las variables después de cargarlas?**
R: Sí, en la pestaña "Variables" puedes editar directamente en la tabla.

**P: ¿Qué pasa si proceso el análisis sin competidores?**
R: El Análisis de Valor Percibido no se calculará, pero los otros 3 sí funcionarán.

**P: ¿Puedo procesar nuevamente después de cambios?**
R: Sí, solo presiona "Procesar Análisis" nuevamente y se recalculará todo.

**P: ¿Los gráficos se actualizan automáticamente?**
R: Sí, al procesar el análisis, todas las visualizaciones se regeneran.

**P: ¿Puedo hacer múltiples análisis para diferentes períodos?**
R: Sí, crea un nuevo registro para cada análisis (mensual, trimestral, anual).

---

## 📞 Soporte

Para dudas o problemas técnicos, contacta al equipo de **AI Mindnovation**:
- 📧 Email: soporte@ai-mindnovation.com
- 🌐 Web: https://ai-mindnovation.com

---

**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025
