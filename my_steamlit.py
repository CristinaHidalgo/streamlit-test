import streamlit as st
from PIL import Image
import pandas as pd


st.set_page_config(
    page_title="Mi primera APP Streamlit", #Nombre de la página
    page_icon="🧊",
    layout="wide", #todo el ancho de la pantalla
    initial_sidebar_state="expanded", #la barra laterial
)

options = st.sidebar.selectbox(label = "Selecciona una opción", options = ["Home", "Tabla", "Mapa", "Filtros"], index=0)
#index 0 es para que por defecto nos vaya siempre a home.
st.write(f"Has elegido {options} como opción") #st.write es como print en la web

#Cargamos datos:
data = pd.read_csv(r'data\red_recarga_acceso_publico_2021.csv', sep=';')
data.rename(columns={'longitud':'lon', 'latidtud': 'lat'}, inplace=True)

#Para que otra persona pueda subir un fichero 
uploaded_files = st.sidebar.file_uploader("Choose a CSV file",
                                accept_multiple_files=False,
                                type=["csv"])
if uploaded_files:
    data = pd.read_csv(uploaded_files, sep=';')
    #Celebramos que hemos cargado el archivo lanzando unos globos
    st.balloons()


if options == "Home":
    st.write("Esta es la página de Home")

    st.sidebar.write("Carga tu fichero aquí") #Lo mete en la barra lateral si ponemos st.sidebar

    image = Image.open('img\puntos-recarga-madrid.jpg')


    st.title('Mi first Streamlit APP')
    st.image(image, caption='Fotito', width=300) #width es para tamaño imagen

    with st.expander("Click for details"):
        st.write("Esta es una App construida en Streamlit que muestra puntos de recarga en Madrid")


elif options == "Tabla":
    st.write("Aquí se muestra la tabla")
    with st.echo(): #echo te muestra todo el código que quieras ponerle dentro del elemento.
        st.dataframe(data) #y además, esta linea te muestra lo que le hayas pedido.

elif options == "Mapa":
    st.write("Aquí se muestra el mapa :) ")

    #Creamos mapa
    st.map(data=data, zoom=11)
    # Agrupar los datos por distrito y contar el número de cargadores en cada distrito
    data_distrito = data.groupby("DISTRITO")["Nº CARGADORES"].count()

    # # Mostrar un gráfico de barras con los cargadores por distrito
    st.bar_chart(data_distrito)

    # # Agrupar los datos por operador y contar el número de cargadores para cada operador
    data_operador = data.groupby("OPERADOR")["Nº CARGADORES"].count()

    # # Mostrar un gráfico de barras con los cargadores por operador
    st.bar_chart(data_operador)

elif options == "Filtros":
    st.write("Aquí se muestran los filtros")

    # Crear un menú desplegable para seleccionar el distrito
    selected_district = st.sidebar.selectbox("Selecciona un distrito", options=data["DISTRITO"].unique())

    # Crear un menú desplegable para seleccionar el operador
    selected_operator = st.sidebar.selectbox("Selecciona un operador", options=data["OPERADOR"].unique())

    # Crear un control deslizante para seleccionar el número mínimo y máximo de cargadores
    min_chargers, max_chargers = st.sidebar.select_slider(
        "Selecciona el número mínimo y máximo de cargadores",
        options =range(data["Nº CARGADORES"].min(), data["Nº CARGADORES"].max() + 1),
        value=(data["Nº CARGADORES"].min(), data["Nº CARGADORES"].max())
    )

    # Crear una casilla de verificación para habilitar o deshabilitar el filtro de distrito
    use_district_filter = st.sidebar.checkbox("Usar filtro de distrito")

    # Crear una casilla de verificación para habilitar o deshabilitar el filtro de operador
    use_operator_filter = st.sidebar.checkbox("Usar filtro de operador")

    # Crear una casilla de verificación para habilitar o deshabilitar el filtro de número mínimo y máximo de cargadores
    use_chargers_filter = st.sidebar.checkbox("Usar filtro de número mínimo y máximo de cargadores")

    # Filtrar los datos según los filtros seleccionados por el usuario
    if use_district_filter:
        data = data[data["DISTRITO"] == selected_district]
    if use_operator_filter:
        data = data[data["OPERADOR"] == selected_operator]
    if use_chargers_filter:
        data = data[(data["Nº CARGADORES"] >= min_chargers) & (data["Nº CARGADORES"] <= max_chargers)]

    # Comprobar si el dataframe está vacío después de aplicar los filtros
    if data.empty:
        # Mostrar un aviso al usuario
        st.warning("No hay datos disponibles con los filtros seleccionados")
        
        # Detener la ejecución del código
        st.stop()

    # Mostrar un mapa con las ubicaciones de las estaciones
    st.map(data)

    # Comprobar si se ha aplicado el filtro de distrito
    if use_district_filter:
        # Mostrar un mapa con las ubicaciones de las estaciones y aumentar el zoom
        st.map(data, zoom=13)
    else:
        # Mostrar un mapa con las ubicaciones de las estaciones
        st.map(data)

    # Comprobar si se ha utilizado el filtro de distrito
    if not use_district_filter:
        # Agrupar los datos por distrito y contar el número de estaciones en cada distrito
        data_distrito = data.groupby("DISTRITO")["Nº CARGADORES"].count()
        
        # Mostrar un gráfico de barras con la distribución de las estaciones en los distritos
        st.bar_chart(data_distrito)
    # Comprobar si se ha utilizado el filtro de operador
    if not use_operator_filter:
        # Agrupar los datos por operador y contar el número de estaciones para cada operador
        data_operador = data.groupby("DISTRITO")["Nº CARGADORES"].count()
        
        # Mostrar un gráfico de barras con la distribución de las estaciones para cada operador
        st.bar_chart(data_operador)

    # Agrupar los datos por tamaño y contar el número de cargadores para cada tamaño
    data_tamaño = data.groupby("Tamaño")["Nº Cargadores"].sum()

    # Mostrar un gráfico de barras con el número de cargadores por tamaño
    st.bar_chart(data_tamaño)

    # Crear dos columnas con una proporción 3:2
    col1, col2 = st.columns((3, 2))

    # Mostrar contenido en la primera columna
    col1.write("Contenido en la primera columna")

    # Mostrar contenido en la segunda columna
    col2.write("Contenido en la segunda columna")



