import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
import geopandas as gpd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import folium
from folium.features import GeoJsonTooltip
import branca.colormap as cm
from streamlit_folium import st_folium

#PREPROCESAMIENTO DE LOS DATOS



#Carga de los datos
df=pd.read_csv("https://raw.githubusercontent.com/Kalbam/Datos_DATAVIZ/refs/heads/main/deporte_eventos.csv")
mapa_col= gpd.read_file("COLOMBIA/COLOMBIA.shp",encoding="latin1")


#Limpieza de df para poder hacer un merge con mapa_col
df=df.drop(columns=["ID"])
df["Departamento"]=df["Departamento"].str.upper()
for i in range(len(df)):
    if df["Departamento"][i]=="ATLÁNTICO":
        df["Departamento"][i]="ATLANTICO"
    elif df["Departamento"][i]=="BOLÍVAR":
        df["Departamento"][i]="BOLIVAR"
    elif df["Departamento"][i]=="CÓRDOBA":
        df["Departamento"][i]="CORDOBA"
    elif df["Departamento"][i]=="BOGOTÁ D.C.":
        df["Departamento"][i]="BOGOTA D.C."
        
        
#Limpieza de mapa_col
mapa_col['DPTO_CNMBR'].replace({'NARI?O':'NARIÑO',},inplace=True)


#Groupby por departamento de la cantidad de eventos 
df_deportes=df.groupby("Departamento",as_index=False).agg(todos=("Evento","count"))
df_deportes["futbol"]=df.loc[df["Evento"]=="Fútbol"].groupby("Departamento",as_index=False).agg(futbol=("Evento","count"))["futbol"]
df_deportes["ciclismo"]=df.loc[df["Evento"]=="Ciclismo"].groupby("Departamento",as_index=False).agg(ciclismo=("Evento","count"))["ciclismo"]
df_deportes["atletismo"]=df.loc[df["Evento"]=="Atletismo"].groupby("Departamento",as_index=False).agg(atletismo=("Evento","count"))["atletismo"]
df_deportes["natacion"]=df.loc[df["Evento"]=="Natación"].groupby("Departamento",as_index=False).agg(natacion=("Evento","count"))["natacion"]


#Se agregan departamentos que no tienen eventos deportivos en el dataset
for dep in mapa_col["DPTO_CNMBR"]:
    if dep not in df_deportes["Departamento"].values:
        nuevo_registro = {"Departamento": dep, "todos":0,"futbol": 0, "ciclismo": 0, "atletismo": 0, "natacion": 0}
        df_deportes = pd.concat([df_deportes, pd.DataFrame([nuevo_registro])], ignore_index=True)
       
#Merge de los dos dataframes 
mapa_col = mapa_col.rename(columns={'DPTO_CNMBR': 'Departamento'})
data_deportes = pd.merge(mapa_col, df_deportes , on ='Departamento', how = 'outer')


#Groupby por departamento de la cantidad de participantes por evento 
df_participante=df.groupby("Departamento",as_index=False).agg(todos=("Participantes","mean")).round(1)
df_participante["futbol"]=df.loc[df["Evento"]=="Fútbol"].groupby("Departamento",as_index=False).agg(futbol=("Participantes","mean")).round(1)["futbol"]
df_participante["ciclismo"]=df.loc[df["Evento"]=="Ciclismo"].groupby("Departamento",as_index=False).agg(ciclismo=("Participantes","mean")).round(1)["ciclismo"]
df_participante["atletismo"]=df.loc[df["Evento"]=="Atletismo"].groupby("Departamento",as_index=False).agg(atletismo=("Participantes","mean")).round(1)["atletismo"]
df_participante["natacion"]=df.loc[df["Evento"]=="Natación"].groupby("Departamento",as_index=False).agg(natacion=("Participantes","mean")).round(1)["natacion"]


#Se agregan departamentos que no tienen eventos deportivos en el dataset
for dep in mapa_col["Departamento"]:
    if dep not in df_participante["Departamento"].values:
        nuevo_registro = {"Departamento": dep, "todos":0,"futbol": 0, "ciclismo": 0, "atletismo": 0, "natacion": 0}
        df_participante = pd.concat([df_participante, pd.DataFrame([nuevo_registro])], ignore_index=True)
       
       
#Merge de los dos dataframes 
data_participante = pd.merge(mapa_col, df_participante , on ='Departamento', how = 'outer')


#Groupby por departamento de la duración promedio de los eventos
df_duracion=df.groupby("Departamento",as_index=False).agg(todos=("Duración_Horas","mean")).round(1)
df_duracion["futbol"]=df.loc[df["Evento"]=="Fútbol"].groupby("Departamento",as_index=False).agg(futbol=("Duración_Horas","mean")).round(1)["futbol"]
df_duracion["ciclismo"]=df.loc[df["Evento"]=="Ciclismo"].groupby("Departamento",as_index=False).agg(ciclismo=("Duración_Horas","mean")).round(1)["ciclismo"]
df_duracion["atletismo"]=df.loc[df["Evento"]=="Atletismo"].groupby("Departamento",as_index=False).agg(atletismo=("Duración_Horas","mean")).round(1)["atletismo"]
df_duracion["natacion"]=df.loc[df["Evento"]=="Natación"].groupby("Departamento",as_index=False).agg(natacion=("Duración_Horas","mean")).round(1)["natacion"]


#Se agregan departamentos que no tienen eventos deportivos en el dataset
for dep in mapa_col["Departamento"]:
    if dep not in df_duracion["Departamento"].values:
        nuevo_registro = {"Departamento": dep, "todos":0,"futbol": 0, "ciclismo": 0, "atletismo": 0, "natacion": 0}
        df_duracion = pd.concat([df_duracion, pd.DataFrame([nuevo_registro])], ignore_index=True)
        
        
#Merge de los dos dataframes
data_duracion = pd.merge(mapa_col, df_duracion , on ='Departamento', how = 'outer')



#FIN PREPROCESAMIENTO DE LOS DATOS


# Menú de navegación en la barra lateral
with st.sidebar:
    seleccion = option_menu(
        "Actividad #3",
        ["Contexto", "Análisis", "Visualización", "Georreferenciación", "Conclusiones"],
        icons=["house", "bar-chart", "bar-chart", "map", "check2-circle"],
        menu_icon="cast", default_index=0
    )

# Contenido según la opción
if seleccion == "Contexto":
    st.title("Contextualización del dataset")
    st.markdown("""Este dataset fue escogido del GitHub de la profesora
                Keyla Alba, y puede acceder a el mediante el siguiente enlace:
                https://github.com/Kalbam/Datos_DATAVIZ/blob/main/deporte_eventos.csv .
                En este caso no se cuenta con un contexto como tal, pero este se
                puede inferir a partir de las variables que lo componen.
                """)
    st.image("https://fundaciondelcorazon.com/images/stories/iStock-949190756.jpg")

    st.markdown("""
                Se tiene información sobre 200 eventos deportivos
                realizados en Colombia. Esta información viene dada por características
                como: **el departamento donde se realizó**, **el tipo de evento(deporte)**,
                **la asistencia al evento**, y **la duración del mismo**.""")
    
    st.markdown("""Los departamentos que tienen registros de eventos deportivos en 
                este dataset son: **Antioquia, Atlántico, Bogotá D.C., Bolívar, Córdoba, Cundinamarca
                , Magdalena, Nariño, Santander y Valle del Cauca.**""")
elif seleccion == "Análisis":
    st.title("Breve análisis exploratorio")
    st.markdown("""Veamos un breve análisis exploratorio del dataset, sin entrar
                tanto en detalle en el preprocesamiento que se encuentra en el código
                para poder realizar los mapas correspondientes.""")
    st.markdown("""Echemos un vistazo a lo que se adelantó en la contextualización:
                **la estructura del dataset.**""")
    st.dataframe(df.head())
    st.markdown("""Además, los eventos deportivos con los que contamos son:""")
    st.dataframe(df["Evento"].unique())
    st.markdown("""Y el resúmen numérico:""")
    st.dataframe(df[["Participantes", "Duración_Horas"]].describe().round(1))
    st.markdown("""En la siguiente pestaña veremos una visualización de estos datos 
                de manera gráfica, antes de pasar con la georreferenciación.""")
elif seleccion == "Visualización":
    st.title("Visualización de las variables")
    variables = {
        "Cantidad de eventos": "data_deportes",
        "Participantes del evento": "data_participante",
        "Duración del evento en horas": "data_duracion"
    }
    
    deportes= {
        "Todos los deportes": "todos",
        "Fútbol": "futbol",
        "Ciclismo": "ciclismo",
        "Atletismo" : "atletismo",
        "Natación" : "natacion"
    }
    st.markdown("""En este apartado podemos apreciar de manera gráfica
                las distribuciones de las variables a georreferenciar.""")
    # Selectbox para variable
    var_select = st.selectbox("Selecciona la variable a graficar", list(variables.keys()))

    if var_select=="Cantidad de eventos":
        #Selectbox para el tipo de evento
        dep_select = st.selectbox("Selecciona el deporte", list(deportes.keys()))
        sport = deportes[dep_select]
        fig_bar = px.bar(data_deportes.loc[data_deportes["todos"]>0], x='Departamento', y=sport, color='Departamento', text=sport,
                 labels={sport: 'Cantidad de eventos deportivos realizados'})
        st.plotly_chart(fig_bar)
    elif var_select=="Participantes del evento":
        fig_box=px.box(df, x="Departamento", y="Participantes")
        st.plotly_chart(fig_box)
    elif var_select=="Duración del evento en horas":
        fig_box=px.box(df, x="Departamento", y="Duración_Horas")
        st.plotly_chart(fig_box)
elif seleccion == "Georreferenciación":
    st.title("Mapa Coroplético Interactivo de Deportes")
    st.write("""En este apartado veremos los mapas coropléticos de
             tres variables distintas: la cantidad de eventos deportivos por departamento
             , la participación media de cada evento por departamento,
             y la duración media de los eventos por departamento.
             Además, cada una se puede filtrar ya sea contando a todos los deportes
             del dataset, o tomando un deporte en específico.""")
    data_deportes = data_deportes.to_crs(epsg=4326)
    data_participante = data_participante.to_crs(epsg=4326)
    data_duracion = data_duracion.to_crs(epsg=4326)
    
    variables = {
        "Cantidad de eventos": "data_deportes",
        "Participantes promedio del evento": "data_participante",
        "Duración media del evento en horas": "data_duracion"
    }
    
    deportes= {
        "Todos los deportes": "todos",
        "Fútbol": "futbol",
        "Ciclismo": "ciclismo",
        "Atletismo" : "atletismo",
        "Natación" : "natacion"
    }
    
    # Selectbox para variable
    var_select = st.selectbox("Selecciona la variable a graficar", list(variables.keys()))
    # Selectbox para deporte
    dep_select = st.selectbox("Selecciona el deporte", list(deportes.keys()))

    # Selecciona el dataframe y variable correspondientes
    df = eval(variables[var_select])
    sport = deportes[dep_select]
   
    # Crea columna auxiliar para el tooltip
    col_tooltip = f"{sport}_tooltip"
    if var_select == "Duración media del evento en horas":
        df[col_tooltip] = df[sport].apply(lambda x: "Sin datos" if x == 0 else round(x, 2))
    else:
        df[col_tooltip] = df[sport].apply(lambda x: "Sin datos" if x == 0 else int(x))
    # Crear el mapa centrado en Colombia
    m = folium.Map(location=[4.6, -74.1], zoom_start=5)

    # Crear el colormap
    vmin = df[sport].min()
    vmax = df[sport].max()
    colormap = cm.linear.YlOrRd_09.scale(vmin, vmax)
    colormap.caption = f"{var_select} en {sport}"
    colormap.position="bottomleft"

    # Crear GeoJson para el mapa coroplético
    folium.GeoJson(
        df,
        name="choropleth",
        style_function=lambda feature: {
            "fillColor": colormap(feature["properties"][sport]) if feature["properties"][sport] not in [0, None] else "#cccccc",
            "color": "black",
            "weight": 0.8,
            "fillOpacity": 0.7,
        },
        tooltip=GeoJsonTooltip(
            fields=["Departamento", col_tooltip],
            aliases=["Departamento", var_select],
            localize=True,
            sticky=True,
            labels=True,
            style=("background-color: white; color: #333333; font-family: Arial; font-size: 12px;"),
        ),
        highlight_function=lambda x: {"weight": 3, "color": "blue"},
    ).add_to(m)

    colormap.add_to(m)

    # Mostrar el mapa en Streamlit
    st_folium(m, width=700, height=600)
elif seleccion== "Conclusiones":
    st.title("Conclusiones")
    st.markdown("""Estos mapas corópleticos nos ofrecen información muy valiosa de 
                los departamentos de Colombia que están disponibles.""")
    st.markdown("""Primero que todo, georreferenciando la variable **Cantidad de eventos**
                podemos ver cuales son los departamentos con más eventos deportivos,
                lo cual puede ser usado para guiar a las personas interesadas en cierto
                tipo de deportes, como también para tratar de fomentar la práctica
                de estos mismos en lugares donde su cantidad sea baja.""")
    st.markdown("""Por otro lado, la georreferenciación de la variable 
                **Participantes promedio del evento** nos da un indicio de qué
                tan practicado es un deporte y qué tanto interesa este a los 
                habitantes de los departamentos en cuestión.""")
    st.markdown("""Y por último, con la variable **Duración media del evento en horas**
                , aunque un poco menos informativa, nos sirve para indicarle a las
                personas que no conozcan o no practiquen el deporte en cuestión,
                cuanto suele durar un evento de este mismo.""")
    

