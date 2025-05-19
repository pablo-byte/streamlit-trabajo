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
    default=["A", "B"],
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
    default=["Health and beauty", "Electronic accessories"],
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

st.header("Título principal del dashboard")

# #######################################################
# # SECCIÓN DE MÉTRICAS (PRIMERA FILA)
# #######################################################

# Mostramos métricas del último trimestre disponible
st.subheader("Graficos de torta")

# Obtenemos los datos del último trimestre
# ultimo = df_filtrado.iloc[-1]
# fecha_ultimo = f"Q{int(ultimo['Quarter'])} {int(ultimo['Year'])}"

# Creamos tres columnas para las métricas principales
col1, col2, col3 = st.columns(3)


#########################################################
# SECCIÓN DE GRÁFICOS (SEGUNDA FILA)
#########################################################

# Sección: Composición del PIB
# st.subheader("Composición del PIB")

c1_f1, c2_f1, c3_f1 = st.columns(3)

with c1_f1:
    if payment_type:
        # Filtrar por las sucursales seleccionadas
        df_filtered = df[df["Payment"].isin(payment_type)]

        # Calculamos la distribución de frecuencias
        pie_data = df_filtered["Payment"].value_counts()

        # Creamos el gráfico de torta
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            pie_data.values,
            labels=pie_data.index,
            autopct="%1.1f%%",
            colors=sns.color_palette("viridis", len(pie_data)),
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
        df_filtered = df[df["Branch"].isin(branches)]

        # Calculamos la distribución de frecuencias
        pie_data = df_filtered["Branch"].value_counts()

        # Creamos el gráfico de torta
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            pie_data.values,
            labels=pie_data.index,
            autopct="%1.1f%%",  # Mostrar porcentajes
            colors=sns.color_palette("viridis", len(pie_data)),
        )

        # Título del gráfico
        ax.set_title("Distribución por Sucursal")

        # Mostramos el gráfico en Streamlit
        st.pyplot(fig)
    else:
        st.info("Selecciona al menos una sucursal")


with c3_f1:
    if product_line:
        # Filtrar por las sucursales seleccionadas
        df_filtered = df[df["Product line"].isin(product_line)]

        # Calculamos la distribución de frecuencias
        pie_data = df_filtered["Product line"].value_counts()

        # Creamos el gráfico de torta
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            pie_data.values,
            labels=pie_data.index,
            autopct="%1.1f%%",  # Mostrar porcentajes
            colors=sns.color_palette("viridis", len(pie_data)),
        )

        # Título del gráfico
        ax.set_title("Distribución por Tipo de Producto")

        # Mostramos el gráfico en Streamlit
        st.pyplot(fig)
    else:
        st.info("Selecciona al menos un tipo de producto")

# Sección: Análisis de Tendencias Económicas
# st.subheader("Análisis Económico")
# st.write("Visualización de tendencias y relaciones")

#########################################################
# SECCIÓN DE ANÁLISIS DE INGRESOS
#########################################################

st.subheader("Análisis de Ingresos por Producto y Sucursal")

# Crear el gráfico de barras apiladas
pivot_data = df.pivot_table(
    values="gross income", index="Product line", columns="Branch", aggfunc="sum"
)

# Crear la figura con el tamaño especificado
fig, ax = plt.subplots(figsize=(12, 6))

# Crear el gráfico de barras apiladas
pivot_data.plot(kind="bar", stacked=True, ax=ax)

# Personalizar el gráfico
plt.title("Ingreso Bruto por Línea de Producto y Sucursal")
plt.xlabel("Línea de producto")
plt.ylabel("Ingreso bruto total")
plt.legend(title="Sucursal")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

#########################################################
# SECCIÓN DE ANÁLISIS DE SATISFACCIÓN
#########################################################

st.subheader("Distribución de Calificaciones de Clientes")

# Crear figura para el histograma
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el histograma con KDE
clientes = df["Rating"]
sns.histplot(data=clientes, bins=20, kde=True, ax=ax)

# Personalizar el gráfico
plt.title("Distribución de la Calificación de los Clientes")
plt.xlabel("Calificación")
plt.ylabel("Frecuencia")

# Ajustar el diseño
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

st.markdown("---")
st.caption("Trabajo Grupal | Datos: data.csv")
