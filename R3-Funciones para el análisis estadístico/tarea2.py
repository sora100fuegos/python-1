import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. GENERACIÓN DE DATOS
# ============================================================
np.random.seed(42)  # Para reproducibilidad
listaNumeros = np.random.normal(loc=5, scale=2, size=1000)

# ============================================================
# 2. FUNCIONES ESTADÍSTICAS
# ============================================================
def obtener_promedio(arr):
    """Retorna el promedio (media aritmética) del arreglo."""
    return np.mean(arr)

def obtener_mediana(arr):
    """Retorna la mediana del arreglo."""
    return np.median(arr)

def obtener_cuartiles(arr):
    """Retorna los cuartiles Q1, Q2 y Q3."""
    return np.percentile(arr, [25, 50, 75])

def obtener_deciles(arr):
    """Retorna los deciles D1 ... D9."""
    return np.percentile(arr, np.arange(10, 100, 10))

def obtener_percentil(arr, p):
    """Retorna el percentil 'p' (0 <= p <= 100) del arreglo."""
    if not 0 <= p <= 100:
        raise ValueError("El percentil debe estar entre 0 y 100")
    return np.percentile(arr, p)

def obtener_percentiles_extremos(arr):
    """Retorna los percentiles extremos: P2 y P98."""
    return np.percentile(arr, [2, 98])

# ============================================================
# 3. APP STREAMLIT
# ============================================================
st.set_page_config(page_title="Análisis Estadístico UVEG", layout="wide")
st.title("📈 Medidas Estadísticas de Distribución")
st.markdown("**Distribución Normal** — μ = 5, σ = 2, n = 1000")

# ---------- Histograma ----------
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(listaNumeros, bins=40, color="steelblue", edgecolor="white", alpha=0.85)
ax.set_title("Histograma de la muestra")
ax.set_xlabel("Valor")
ax.set_ylabel("Frecuencia")
st.pyplot(fig)

# ---------- Cálculos ----------
promedio  = obtener_promedio(listaNumeros)
mediana   = obtener_mediana(listaNumeros)
cuartiles = obtener_cuartiles(listaNumeros)
deciles   = obtener_deciles(listaNumeros)
extremos  = obtener_percentiles_extremos(listaNumeros)

# ---------- Promedio y Mediana ----------
c1, c2 = st.columns(2)
c1.metric("Promedio", f"{promedio:.4f}")
c2.metric("Mediana",  f"{mediana:.4f}")

# ---------- Cuartiles ----------
st.subheader("Cuartiles")
df_cuartiles = pd.DataFrame({
    "Cuartil": ["Q1 (25%)", "Q2 (50%)", "Q3 (75%)"],
    "Valor":   cuartiles
})
st.dataframe(df_cuartiles, hide_index=True, use_container_width=True)

# ---------- Deciles ----------
st.subheader("Deciles")
df_deciles = pd.DataFrame({
    "Decil": [f"D{i}" for i in range(1, 10)],
    "Valor": deciles
})
st.dataframe(df_deciles, hide_index=True, use_container_width=True)

# ---------- Percentil personalizado ----------
st.subheader("Percentil personalizado")
p = st.slider("Selecciona el percentil (0–100)", 0, 100, 50)
st.write(f"**Percentil {p}:** {obtener_percentil(listaNumeros, p):.4f}")

# ---------- Percentiles extremos ----------
st.subheader("Percentiles extremos")
c3, c4 = st.columns(2)
c3.metric("Percentil 2 (extremo inferior)", f"{extremos[0]:.4f}")
c4.metric("Percentil 98 (extremo superior)", f"{extremos[1]:.4f}")

st.info("💡 Los percentiles extremos P2 y P98 ayudan a detectar valores atípicos en los extremos de la distribución.")