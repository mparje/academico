import streamlit as st
import scholarly
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

def buscar_articulos(palabras_clave, num_articulos):
    search_query = scholarly.search_pubs(palabras_clave)
    resultados = [next(search_query) for _ in range(num_articulos)]
    art_titulos = [articulo.bib['title'] for articulo in resultados]
    art_textos = []
    for articulo in resultados:
        try:
            texto = articulo.bib['abstract']
        except KeyError:
            texto = articulo.bib['title']
        art_textos.append(texto)
    return art_titulos, art_textos

def procesar_texto(texto):
    oraciones = sent_tokenize(texto)
    palabras = [word_tokenize(oracion) for oracion in oraciones]
    palabras_relevantes = [palabra.lower() for palabra in palabras if palabra.lower() not in stopwords.words('english')]
    ps = PorterStemmer()
    palabras_stem = [ps.stem(palabra) for palabra in palabras_relevantes]
    frecuencia_palabras = Counter(palabras_stem)
    return frecuencia_palabras

st.title("Generador de ensayos académicos")

palabras_clave = st.text_input("Ingrese las palabras clave del tema a investigar:")
num_articulos = st.slider("Cantidad de artículos a utilizar:", 1, 10, 5)
boton_generar = st.button("Generar ensayo")

if boton_generar:
    art_titulos, art_textos = buscar_articulos(palabras_clave, num_articulos)
    frecuencia_palabras = Counter()
    for texto in art_textos:
        frecuencia_palabras += procesar_texto(texto)
    palabras_importantes = frecuencia_palabras.most_common(10)
    st.write("Las palabras más relevantes encontradas en los artículos son:")
    for palabra, frecuencia in palabras_importantes:
        st.write("- " + palabra + " (" + str(frecuencia) + " veces)")
    st.write("Ensayo:")
    ensayo = ""
    for i in range(5):
        palabra = palabras_importantes[i][0]
        consulta = scholarly.search_pubs(palabra)
        resultado = next(consulta)
        texto = resultado.bib['abstract']
        oraciones = sent_tokenize(texto)
        ensayo += oraciones[0] + " "
    st.write(ensayo)
