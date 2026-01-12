#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# Configuración de página
st.set_page_config(page_title="ErgoSmart - Simulación Biomecánica", layout="wide")

st.title("🛡️ Panel de Control Ergonómico: Simulación de Comportamiento")
st.markdown("---")

# --- PARÁMETROS DE CONFIGURACIÓN ---
st.sidebar.header("Ajustes Técnicos")
umbral_ideal = st.sidebar.slider("Umbral de Referencia (cm)", 5, 25, 12)

# --- INICIALIZACIÓN DE CONTENEDORES VACÍOS (Para actualización en vivo) ---
placeholder_metricas = st.empty()
placeholder_grafico = st.empty()
placeholder_mensajes = st.empty()

# Función para renderizar el estado actual en los contenedores
def actualizar_interfaz(dist, pres, historial_puntos):
    with placeholder_metricas.container():
        m1, m2, m3 = st.columns(3)
        m1.metric("Distancia (Ultrasonido)", f"{dist:.1f} cm")
        m2.metric("Presencia (IR)", "DETECTADA" if pres else "NULA")
        estado = "CORRECTA ✅" if dist < umbral_ideal else "MALA POSTURA ⚠️"
        m3.metric("Evaluación", estado, delta=f"{dist-umbral_ideal:.1f} cm", delta_color="inverse")

    with placeholder_grafico.container():
        # Generar DataFrame para el gráfico dinámico
        df = pd.DataFrame({
            "Segundos": list(range(len(historial_puntos))),
            "Usuario (cm)": historial_puntos,
            "Línea Referencia": [umbral_ideal] * len(historial_puntos)
        })
        st.line_chart(df.set_index("Segundos"))

# --- LÓGICA DE LA SIMULACIÓN DE 10 SEGUNDOS ---
if st.button("🚀 Iniciar Prueba de Biofeedback (10s)"):
    puntos_grafica = [10.0] * 20  # Iniciamos con base estable
    
    # Total 100 pasos de 0.1s = 10 segundos totales
    for paso in range(101):
        # 1. FASE INICIAL: Postura Correcta (Segundos 0-2)
        if paso <= 20:
            dist_actual = 10.0 + np.random.normal(0, 0.2)
            placeholder_mensajes.success("Estado: Monitorización estable. Postura correcta.")
        
        # 2. FASE DE DESAJUSTE: El usuario se inclina (Segundos 2-5)
        elif 20 < paso <= 50:
            # Incremento lineal de 10cm a 26cm
            dist_actual = 10.0 + (paso - 20) * (16 / 30) 
            placeholder_mensajes.warning("Estado: Detectando pérdida de contacto con el respaldo...")
        
        # 3. FASE DE ALERTA: Pico de mala postura (Segundos 5-7)
        elif 50 < paso <= 70:
            dist_actual = 26.0 + np.random.normal(0, 0.5)
            placeholder_mensajes.error("🚨 ALERTA ACTIVA: Corrige tu posición inmediatamente.")
        
        # 4. FASE DE CORRECCIÓN: El usuario recula (Segundos 7-10)
        else:
            # Descenso lineal de 26cm a 10cm
            dist_actual = 26.0 - (paso - 70) * (16 / 30)
            placeholder_mensajes.info("Estado: Corrección en curso. Volviendo a zona segura.")

        # Actualizar datos y visualización
        puntos_grafica.append(dist_actual)
        actualizar_interfaz(dist_actual, True, puntos_grafica[-50:]) # Mostramos los últimos 50 puntos
        time.sleep(0.1)
    
    placeholder_mensajes.success("✅ Prueba finalizada con éxito. El usuario ha recuperado la higiene postural.")

else:
    # Estado en reposo (antes de dar al botón)
    actualizar_interfaz(10.0, True, [10.0]*50)
    st.info("Pulsa el botón superior para realizar la prueba de estrés de 10 segundos.")

st.markdown("---")
st.markdown("""
**Nota Técnica:** Esta simulación permite evaluar el tiempo de respuesta del trabajador. La transición suave entre valores imita el comportamiento real del cuerpo humano al fatigarse (inclinación lenta) y al reaccionar al estímulo (corrección rápida).
""")

