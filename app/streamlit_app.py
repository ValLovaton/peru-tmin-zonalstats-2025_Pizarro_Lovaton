import streamlit as st
import pandas as pd
import geopandas as gpd
from scripts.plotting import plot_distribution, top_bottom_ranking, plot_choropleth

st.set_page_config(page_title="Perú Tmin – Zonal Stats", layout="wide")

st.title("Perú Tmin – Zonal Statistics & Public Policy")

st.markdown("""
Esta app permitira explorar estadísticas de temperatura mínima (Tmin) 
por distritos/provincias/departamentos en el Perú, y conectar los resultados 
con propuestas de política pública.
""")

# Datos de ejemplo
data = {
    "UBIGEO": ["001", "002", "003"],
    "NAME": ["Distrito A", "Distrito B", "Distrito C"],
    "mean": [5.2, 12.3, 8.7],
    "min": [1.0, 8.5, 3.2],
    "max": [10.2, 15.6, 12.9],
    "std": [2.1, 1.3, 1.7],
    "percentile_10": [2.0, 9.0, 4.0],
    "percentile_90": [9.0, 14.0, 11.5],
    "cold_margin": [2.0 - 0.0, 9.0 - 0.0, 4.0 - 0.0],
}
gdf = pd.DataFrame(data)

st.subheader("Resultados (tabla)")
st.dataframe(gdf)

# Distribución
st.subheader("Distribución de temperaturas promedio")
fig_dist = plot_distribution(gdf, col="mean")
st.pyplot(fig_dist)

# Ranking
st.subheader("Ranking de distritos")
topk, botk = top_bottom_ranking(gdf, col="mean")
col1, col2 = st.columns(2)
with col1:
    st.write("**Más fríos**")
    st.dataframe(topk)
with col2:
    st.write("**Más cálidos**")
    st.dataframe(botk)

# Mapa estático
st.subheader("Mapa estático (ejemplo)")
gdf_geo = gpd.GeoDataFrame(gdf)  
fig_map = plot_choropleth(gdf_geo, col="cold_margin")
st.pyplot(fig_map)

st.header("Propuestas de política pública (borrador)")
st.markdown("""
- **Medida 1:** Vivienda térmica (ISUR).  
- **Medida 2:** Kits anti-helada para pequeños productores.  
- **Medida 3:** Calendario agro + alertas tempranas.
""")
