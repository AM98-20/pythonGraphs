#instalar 
#pip install mysql-connector-python
#pip install --user matplotlib
#pip install numpy
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from collections import Counter 
from datetime import datetime
#from openai import OpenAI
#from textblob import TextBlob  # Para análisis de sentimiento básico

email =[]
fecha =[]
satisfeccion_general = []
conocia_empresa = []
recomendacion = []
comentario = []
SNG_Satisfaccion = 0
SNG_recomendacion = 0
avrg_recomendacion = 0
total_comentarios = 0
duracion = 0
pos = 0
neg = 0
satisfactorio = []
neutro = []
insatisfactorio = []
recomendaria = []
neutro_R = []
no_recomendaria = []

# Configuracion de conexion || informacion comunmente va en archivo secreto, por practica se agrega aca
connection = mysql.connector.connect(
    host="54.219.2.160",
    user="postulante",
    password="HB<tba!Sp6U2j5CN",
    database="prueba_postulantes"
)

# Verificar conexion y extraer datos
try:
    # print("Conexión exitosa a la base de datos")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM encuesta")
    results = cursor.fetchall()

    for row in results:
        c1, c2, c3, c4, c5, c6 = row
        #email.append(c1)
        fecha.append(c2)
        satisfeccion_general.append(c3)
        conocia_empresa.append(c4)
        recomendacion.append(c5)
        comentario.append(c6)

    # Cierre del cursor y la conexión
    cursor.close()
    connection.close()
    #print("Conexión cerrada")
except mysql.connector.Error as err:
    print("Ocurrio un error: {err}")

def Satisfaccion(resultados):
    for resultado in resultados:
        valor = resultado
        if valor > 5:
            satisfactorio.append(valor)
        elif valor < 5:
            insatisfactorio.append(valor)
        else:
            neutro.append(valor)
    SNG_Satisfaccion = round((len(satisfactorio)*100)/len(resultados)) - round((len(insatisfactorio)*100)/len(resultados))
    return SNG_Satisfaccion

def Conocian(respuestas):
    positivas = 0
    negativas = 0
    for resultado in respuestas:
        valor = resultado
        if valor == "Sí":
            positivas += 1
        else:
            negativas += 1
    return positivas, negativas

def Recomendarian(respuestas):
    avrg = 0
    total = 0
    for resultado in respuestas:
        total += resultado
        valor = resultado
        if valor > 5:
            recomendaria.append(valor)
        elif valor < 5:
            no_recomendaria.append(valor)
        else:
            neutro_R.append(valor)
    SNG_recomendacion = round((len(recomendaria)*100)/len(respuestas)) - round((len(no_recomendaria)*100)/len(respuestas))
    avrg = np.mean(respuestas)
    print(SNG_recomendacion)
    print(avrg)
    return SNG_recomendacion, avrg
    
def Comentarios(comentarios):
    total = len(list(filter(None, comentarios)))
    return total

def Comentarios_Fecha():
    total_comentarios = 0
    for respuesta in comentario:
        if respuesta is not None:
            total_comentarios += 1
    date_objects = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in fecha]
    latest_date = max(date_objects)
    earliest_date = min(date_objects)
    difference = latest_date - earliest_date
    return total_comentarios, difference

def Plot_Satisfaccion(satisfactorio, neutro, insatisfactorio):
    lista_larga = max(satisfactorio, neutro, insatisfactorio, key=len)
    muestras = list(range(1, len(lista_larga) + 1))
    longitud_deseada = len(lista_larga)
    #Adecuar tamaño de datos
    def extend_list_with_zeros(lista, longitud_deseada):
        if len(lista) < longitud_deseada:
            extension = [0] * (longitud_deseada - len(lista))
            lista.extend(extension)
        else:
            lista = lista[:longitud_deseada]
        return lista

    satisfactorio = extend_list_with_zeros(satisfactorio, longitud_deseada)
    neutro = extend_list_with_zeros(neutro, longitud_deseada)
    insatisfactorio = extend_list_with_zeros(insatisfactorio, longitud_deseada)
    
    # Configuracion de tabla lineal
    fig = plt.figure(figsize=(8, 6))
    plt.plot(muestras, satisfactorio, marker='o', linestyle='-', color='blue', label='Satisfactorio')
    plt.plot(muestras, insatisfactorio, marker='o', linestyle='--', color='green', label='Insatisfactorio')
    plt.plot(muestras, neutro, marker='o', linestyle='-.', color='orange', label='Neutro')
    plt.axhline(y=SNG_Satisfaccion, color='red', linestyle='--', label=f'SNG: {SNG_Satisfaccion:.2f}')
    plt.title('Distribución de valores de Satisfacción')
    plt.xlabel('Muestras')
    plt.ylabel('Valores')
    plt.legend()

    with PdfPages('grafico lineas.pdf') as pdf:
        pdf.savefig(fig)

    #plt.grid(True)
    #plt.tight_layout()
    #plt.show()

def Plot_Conocimiento():
    etiquetas = ['Sí', 'No']
    colores = ['lightblue', 'lightcoral']
    explode = (0.1, 0) 
    conteo = [pos, neg]
    fig = plt.figure(figsize=(6, 6))
    plt.pie(conteo, labels=etiquetas, colors=colores, explode=explode, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Distribución de Respuestas')

    with PdfPages('grafico pie.pdf') as pdf:
        pdf.savefig(fig)

    #plt.axis('equal')
    #plt.tight_layout()
    #plt.show()

def Plot_Recomendacion():
    etiquetas = list(range(1, 8))  

    conteo_elementos = Counter(recomendacion)

    muestra = []
    for etiqueta in etiquetas:
        muestra.append(conteo_elementos.get(etiqueta, 0))  # Si no existe, contar 0 veces

    avrg_recomendacion = sum(recomendacion) / len(recomendacion)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(etiquetas, muestra, color='skyblue', label='Datos columna 5')
    ax.axhline(y=avrg_recomendacion, color='b', linestyle='--', label=f'Promedio: {avrg_recomendacion:.2f}')
    ax.axhline(y=SNG_recomendacion, color='r', linestyle='-', label=f'SNG: {SNG_recomendacion:.2f}')

    # Etiquetas y título del gráfico
    ax.set_xlabel('Categorías')
    ax.set_ylabel('Valores')
    ax.set_title('Gráfico de Barras con Línea de Promedio')
    ax.legend()

    with PdfPages('grafico barras.pdf') as pdf:
        pdf.savefig(fig)

    #plt.grid(True)
    #plt.tight_layout()
    #plt.show()

total_comentarios, duracion = Comentarios_Fecha()

SNG_Satisfaccion = Satisfaccion(satisfeccion_general)
Plot_Satisfaccion(satisfactorio, neutro, insatisfactorio)
    
pos, neg = Conocian(conocia_empresa)
Plot_Conocimiento()
    
SNG_recomendacion, avrg_recomendacion = Recomendarian(recomendacion)
Plot_Recomendacion()