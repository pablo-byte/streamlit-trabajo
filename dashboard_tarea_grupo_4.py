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
    st.sidebar.error("Ingresar una fecha válida en formato dd/mm/yyyy")
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

rating_ini, rating_fin = st.sidebar.slider("Rango de Rating", 1, 10, (1, 10))

# ##################################################
# # FILTRADO DE DATOS
# ##################################################


st.header("Título principal del dashboard")

# #######################################################
# # SECCIÓN DE MÉTRICAS (PRIMERA FILA)
# #######################################################

st.subheader("Graficos de torta")

# Creamos tres columnas para las métricas principales
col1, col2, col3 = st.columns(3)


#########################################################
# SECCIÓN DE GRÁFICOS (SEGUNDA FILA)
#########################################################


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

# Crear figura para el histograma con espacio para colorbar
fig, (ax, cax) = plt.subplots(
    1, 2, figsize=(12, 6), gridspec_kw={"width_ratios": [20, 1]}
)

# Preparar datos para el histograma coloreado
clientes = df["Rating"]
n, bins, patches = ax.hist(clientes, bins=20, alpha=0.7)

# Crear escala de colores
fracs = n / n.max()
norm = plt.Normalize(fracs.min(), fracs.max())

# Aplicar colores a las barras
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.viridis(norm(thisfrac))
    thispatch.set_facecolor(color)

# Agregar KDE
sns.kdeplot(data=clientes, color="red", ax=ax, linewidth=2)

# Agregar colorbar
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=norm)
sm.set_array([])
fig.colorbar(sm, cax=cax, label="Frecuencia Relativa")

# Personalizar el gráfico
plt.title("Distribución de la Calificación de los Clientes")
plt.xlabel("Calificación")
plt.ylabel("Frecuencia")

# Ajustar el diseño
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

#########################################################
# SECCIÓN DE ANÁLISIS 3D DE RELACIONES
#########################################################

st.subheader("Análisis 3D: Ingresos, Cantidad y Satisfacción")

# Filtrar datos según el rango de rating seleccionado
df_filtered = df[(df["Rating"] >= rating_ini) & (df["Rating"] <= rating_fin)]

# Seleccionamos las 3 variables del DataFrame filtrado
gross_income = df_filtered["gross income"]
quantity = df_filtered["Quantity"]
rating = df_filtered["Rating"]

# Crear figura 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

# Scatter plot 3D con colores basados en Gross Income
scatter = ax.scatter(
    quantity,
    rating,
    gross_income,
    c=gross_income,
    cmap=sns.color_palette("viridis", as_cmap=True),
    s=60,
    alpha=0.7,
    edgecolors="w",
    linewidth=0.5,
)

# Etiquetas de los ejes
ax.set_xlabel("Cantidad", fontsize=12, labelpad=10)
ax.set_ylabel("Rating (1-10)", fontsize=12, labelpad=10)
ax.set_zlabel("Ingresos Brutos ($)", fontsize=12, labelpad=10)
ax.set_title("Relación entre Ingresos Brutos, Cantidad y Rating", fontsize=14, pad=20)

# Barra de color
cbar = plt.colorbar(scatter)
cbar.set_label("Ingresos Brutos ($)", fontsize=12, rotation=270, labelpad=15)

# Ajustar el diseño
plt.tight_layout()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Agregar explicación
st.markdown(
    """
Este gráfico 3D muestra la relación entre tres variables importantes:
- **Cantidad** de productos vendidos
- **Rating** dado por los clientes (1-10)
- **Ingresos Brutos** generados

El color de cada punto representa el nivel de ingresos brutos
, donde los colores más claros indican mayores ingresos.
"""
)

st.markdown("---")


st.caption("Trabajo Grupal | Datos: data.csv")
