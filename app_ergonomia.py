#!/usr/bin/env python
# coding: utf-8

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
        df = pd.DataFrame({
            "Segundos": list(range(len(historial_puntos))),
            "Usuario (cm)": historial_puntos,
            "Línea Referencia": [umbral_ideal] * len(historial_puntos)
        })
        st.line_chart(df.set_index("Segundos"))

# --- LÓGICA DE LA SIMULACIÓN DE 10 SEGUNDOS ---
if st.button("🚀 Iniciar Prueba de Biofeedback (10s)"):
    puntos_grafica = [10.0] * 20  
    
    for paso in range(101):
        if paso <= 20:
            dist_actual = 10.0 + np.random.normal(0, 0.2)
            placeholder_mensajes.success("Estado: Monitorización estable. Postura correcta.")
        elif 20 < paso <= 50:
            dist_actual = 10.0 + (paso - 20) * (16 / 30) 
            placeholder_mensajes.warning("Estado: Detectando pérdida de contacto con el respaldo...")
        elif 50 < paso <= 70:
            dist_actual = 26.0 + np.random.normal(0, 0.5)
            placeholder_mensajes.error("🚨 ALERTA ACTIVA: Corrige tu posición inmediatamente.")
        else:
            dist_actual = 26.0 - (paso - 70) * (16 / 30)
            placeholder_mensajes.info("Estado: Corrección en curso. Volviendo a zona segura.")

        puntos_grafica.append(dist_actual)
        actualizar_interfaz(dist_actual, True, puntos_grafica[-50:]) 
        time.sleep(0.1)
    
    placeholder_mensajes.success("✅ Prueba finalizada con éxito. El usuario ha recuperado la higiene postural.")

else:
    actualizar_interfaz(10.0, True, [10.0]*50)
    st.info("Pulsa el botón superior para realizar la prueba de estrés de 10 segundos.")

st.markdown("---")
st.markdown("""
**Nota Técnica:** Esta simulación permite evaluar el tiempo de respuesta del trabajador ante estímulos correctivos.
""")

# =================================================================
# NUEVA SECCIÓN: RESUMEN DE ACTIVIDAD DIARIA (MOCKUP DE DATOS)
# =================================================================
st.markdown("## 📊 Resumen Estadístico de la Jornada")
st.write("Datos acumulados del usuario durante las últimas 8 horas de trabajo.")

# Creamos 4 columnas para las métricas globales
col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)

with col_sum1:
    st.metric(label="Tiempo Total Sentado", value="6h 42m", help="Tiempo total detectado por el sensor IR")

with col_sum2:
    st.metric(label="Índice Postural", value="84%", delta="Optimizando", help="Porcentaje de tiempo con distancia < umbral")

with col_sum3:
    st.metric(label="Alertas Emitidas", value="12", delta="-3 vs ayer", delta_color="normal", help="Veces que saltó el aviso acústico/visual")

with col_sum4:
    st.metric(label="Pausas Activas", value="5", help="Sesiones en las que el usuario se levantó más de 5 min")

# Añadimos un pequeño análisis clínico descriptivo
st.info("""
**💡 Análisis del Sistema:** El usuario presenta una fatiga postural moderada a partir de la 4ª hora de jornada. 
Se recomienda configurar una alerta de pausa activa cada 50 minutos para reducir la carga estática sobre los discos intervertebrales.
""")

# Gráfico histórico de la jornada (simulado)
st.subheader("Evolución de la Fatiga Postural (Jornada de 8h)")
horas_dia = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
datos_dia = [8, 9, 11, 14, 10, 15, 18, 12] # Valores de distancia promedio por hora

df_dia = pd.DataFrame({
    "Hora": horas_dia,
    "Distancia Promedio (cm)": datos_dia,
    "Línea de Riesgo": [umbral_ideal] * len(horas_dia)
})

st.area_chart(df_dia.set_index("Hora"))
