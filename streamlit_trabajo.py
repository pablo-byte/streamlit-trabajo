# Importamos las bibliotecas necesarias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

##########################################################
# CONFIGURACIÓN DEL DASHBOARD
##########################################################

# Configuración básica de la página
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Configuración simple para los gráficos
sns.set_style("whitegrid")


# Función para convertir fecha de dd/mm/yyyy a datetime
def convert_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except:
        return None


##################################################
# CARGA DE DATOS
##################################################


# Función para cargar datos con cache para mejorar rendimiento
@st.cache_data
def cargar_datos():
    # Carga el archivo CSV con datos macroeconómicos
    df = pd.read_csv("data.csv")
    # Convertir la columna Date a datetime
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# Cargamos los datos
df = cargar_datos()

# Mostramos los primeros 5 registros del DataFrame
print(df.head(5))

##############################################
# CONFIGURACIÓN DE LA BARRA LATERAL
##############################################

# Simplificamos la barra lateral con solo lo esencial
st.sidebar.header("Filtros del Dashboard")

# Selector de fecha
fecha_seleccionada = st.sidebar.text_input(
    "Fecha (dd/mm/yyyy)",
    value="01/01/2019",
    help="Ingrese una fecha en formato dd/mm/yyyy",
)

# Convertir la fecha ingresada
try:
    fecha_dt = datetime.strptime(fecha_seleccionada, "%d/%m/%Y")
    fecha_valida = True
except ValueError:
    st.sidebar.error("Por favor ingrese una fecha válida en formato dd/mm/yyyy")
    fecha_valida = False

# Selector de branches
branches = st.sidebar.multiselect(
    "Branch",
    options=["A", "B", "C"],
    default=["A"],
    help="Selecciona la sucursal",
)

# Selector de customer type
customer_type = st.sidebar.multiselect(
    "Customer type",
    options=["Member", "Normal"],
    default=["Member"],
    help="Selecciona el tipo de cliente",
)

# Selector de gender
gender = st.sidebar.multiselect(
    "Gender",
    options=["Female", "Male"],
    help="Selecciona el genero",
)

product_line = st.sidebar.multiselect(
    "Product Line",
    options=[
        "Health and beauty",
        "Electronic accessories",
        "Home and lifestyle",
        "Sports and travel",
        "Food and beverages",
        "Fashion accessories",
    ],
    help="Selecciona la linea de productos",
)

payment_type = st.sidebar.multiselect(
    "Payment Type",
    options=["Cash", "Credit card", "Ewallet"],
    default=["Cash"],
    help="Selecciona forma de pago",
)
# ##################################################
# # FILTRADO DE DATOS
# ##################################################

# Filtramos los datos según el rango de años y la fecha seleccionada
# df_filtrado = df[(df["Year"] >= anio_inicio) & (df["Year"] <= anio_fin)]

# Aplicar filtro de fecha si es válida
"""if fecha_valida:
    df_filtrado = df_filtrado[df_filtrado["Date"].dt.date == fecha_dt.date()]
    if df_filtrado.empty:
        st.warning("No hay datos disponibles para la fecha seleccionada")

# Título principal del dashboard
st.title("📊 Dashboard Macroeconómico")
st.write(f"Datos económicos de EE.UU. ({anio_inicio}-{anio_fin})")"""

# #######################################################
# # SECCIÓN DE MÉTRICAS (PRIMERA FILA)
# #######################################################

# Mostramos métricas del último trimestre disponible
st.subheader("Último cuarter registrado")

# Obtenemos los datos del último trimestre
# ultimo = df_filtrado.iloc[-1]
# fecha_ultimo = f"Q{int(ultimo['Quarter'])} {int(ultimo['Year'])}"

# Creamos tres columnas para las métricas principales
col1, col2, col3 = st.columns(3)

# Mostramos las métricas con formato adecuado
"""col1.metric(
    "PIB (GDP)",
    f"${ultimo['gdp']:,.0f} Bill",
    help=f"Producto Interno Bruto en {fecha_ultimo}",
)
col2.metric(
    "Desempleo", f"{ultimo['unemp']:.1f}%", help=f"Tasa de desempleo en {fecha_ultimo}"
)
col3.metric(
    "Inflación",
    f"{ultimo['inflation']:.1f}%",
    help=f"Tasa de inflación en {fecha_ultimo}",
)"""

#########################################################
# SECCIÓN DE GRÁFICOS (SEGUNDA FILA)
#########################################################

# Sección: Composición del PIB
# st.subheader("Composición del PIB")

# Dividimos la pantalla en dos columnas (proporción 7:3)
c1_f1, c2_f1 = st.columns((4, 4))

with c1_f1:
    if payment_type:
        # Filtrar por las sucursales seleccionadas
        df_filtered = df[df['Payment'].isin(payment_type)]
        
        # Calculamos la distribución de frecuencias
        pie_data = df_filtered['Payment'].value_counts()

        # Creamos el gráfico de torta
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            pie_data.values,
            labels=pie_data.index,
            autopct="%1.1f%%",
            colors=sns.color_palette('viridis', len(pie_data))
        )

        # Título del gráfico
        ax.set_title("Distribución por Tipo de Pago")

        # Mostramos el gráfico en Streamlit
        st.pyplot(fig)
    else:
        st.info("Selecciona al menos un genero")

with c2_f1:
    if branches:
        # Filtrar por las sucursales seleccionadas
        df_filtered = df[df['Branch'].isin(branches)]
        
        # Calculamos la distribución de frecuencias
        pie_data = df_filtered['Branch'].value_counts()

        # Creamos el gráfico de torta
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            pie_data.values,
            labels=pie_data.index,
            autopct="%1.1f%%",  # Mostrar porcentajes
            colors=sns.color_palette('viridis', len(pie_data))
        )

        # Título del gráfico
        ax.set_title("Distribución por Sucursal")

        # Mostramos el gráfico en Streamlit
        st.pyplot(fig)
    else:
        st.info("Selecciona al menos una sucursal")


# Sección: Análisis de Tendencias Económicas
st.subheader("Análisis Económico")
st.write("Visualización de tendencias y relaciones entre indicadores económicos")

# Creamos una fila con dos gráficos: PIB y Variables Porcentuales
c1_f2, c2_f2 = st.columns(2)

# Diccionario para traducir nombres de variables
nombres = {"gdp": "PIB", "unemp": "Desempleo", "inflation": "Inflación"}

# Columna 1: Gráfico exclusivo para el PIB
"""with c1_f2:
    st.write("### Evolución del PIB")
    fig, ax = plt.subplots(figsize=(6, 3))

    # Graficamos el PIB agrupado por año
    df_anual_pib = df_filtrado.groupby("Year")["gdp"].mean().reset_index()
    sns.lineplot(data=df_anual_pib, x="Year", y="gdp", color="#1f77b4", ax=ax)

    # Configuración del gráfico
    ax.set_ylabel("Billones $")
    ax.set_title("Tendencia del Producto Interno Bruto")
    ax.grid(True, alpha=0.3)

    # Mostramos el gráfico
    st.pyplot(fig)
    st.write(
        "*El gráfico muestra la evolución del PIB a lo largo del tiempo, permitiendo identificar ciclos económicos y tendencias de crecimiento.*"
    )"""

# Columna 2: Gráfico para variables porcentuales (Desempleo e Inflación)
"""with c2_f2:
    st.write("### Desempleo e Inflación")
    fig, ax = plt.subplots(figsize=(6, 3))

    # Colores para cada variable
    colores = {"unemp": "#ff7f0e", "inflation": "#2ca02c"}

    # Graficamos las variables porcentuales agrupadas por año
    df_anual_vars = (
        df_filtrado.groupby("Year")[["unemp", "inflation"]].mean().reset_index()
    )
    for var in ["unemp", "inflation"]:
        sns.lineplot(
            data=df_anual_vars,
            x="Year",
            y=var,
            label=nombres.get(var),
            color=colores.get(var),
            ax=ax,
        )

    # Configuración del gráfico
    ax.set_ylabel("Porcentaje (%)")
    ax.set_title("Tendencias de Desempleo e Inflación")
    ax.legend()
    ax.grid(True, alpha=0)

    # Mostramos el gráfico
    st.pyplot(fig)
    st.write(
        "*Comparación entre tasas de desempleo e inflación, útil para analizar posibles compensaciones en política económica.*"
    )"""

########################################################
# SECCIÓN DE ANÁLISIS DE RELACIONES (CUARTA FILA)
########################################################

# Nueva fila: Gráfico de dispersión (Inflación vs Desempleo) e Histograma
c1_f3, c2_f3 = st.columns(2)

# Gráfico de dispersión: Desempleo vs Inflación (Curva de Phillips)
"""with c1_f3:
    st.write("### Relación Inflación-Desempleo")

    fig, ax = plt.subplots(figsize=(6, 3))

    # Crear gráfico de dispersión
    scatter = ax.scatter(
        df_filtrado["unemp"],
        df_filtrado["inflation"],
        alpha=0.7,
        c=df_filtrado["Year"],  # Colorear por año
        cmap="viridis",
    )

    # # Añadir línea de tendencia
    # z = np.polyfit(df_filtrado['unemp'], df_filtrado['inflation'], 1)
    # p = np.poly1d(z)
    # ax.plot(df_filtrado['unemp'], p(df_filtrado['unemp']), "r--", alpha=0.7)

    # Configuración del gráfico
    ax.set_xlabel("Tasa de Desempleo (%)")
    ax.set_ylabel("Tasa de Inflación (%)")
    ax.set_title("Curva de Phillips: Inflación vs Desempleo")
    ax.grid(True, alpha=0.3)

    # Mostrar gráfico
    st.pyplot(fig)
    st.write(
        "*Explora la relación entre inflación y desempleo. La teoría de la Curva de Phillips sugiere una relación inversa entre ambas variables.*"
    )"""

# Histograma de Inflación
"""with c2_f3:
    st.write("### Distribución de la Inflación")

    fig, ax = plt.subplots(figsize=(6, 3))

    # Crear histograma
    ax.hist(
        df_filtrado["inflation"], bins=15, color="#2ca02c", alpha=0.7, edgecolor="black"
    )

    # Configuración del gráfico
    ax.set_xlabel("Tasa de Inflación (%)")
    ax.set_ylabel("Frecuencia")
    ax.set_title("Distribución de la Inflación")
    ax.grid(True, alpha=0.3)

    # Mostrar línea vertical en la media
    media = df_filtrado["inflation"].mean()
    ax.axvline(
        media,
        color="red",
        linestyle="dashed",
        linewidth=1,
        label=f"Media: {media:.2f}%",
    )
    ax.legend()

    # Mostrar gráfico
    st.pyplot(fig)
    st.write(
        "*Visualiza la distribución de las tasas de inflación en el período seleccionado, mostrando su frecuencia y dispersión.*"
    )
"""
# Pie de página simple
st.markdown("---")
st.caption("Dashboard Macroeconómico Simple | Datos: USMacroG_v2.csv")
