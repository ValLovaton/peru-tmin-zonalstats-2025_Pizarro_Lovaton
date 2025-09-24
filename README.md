# Perú Tmin — Zonal Stats + Public Policy + Streamlit

## Propósito
Analizar datos de temperatura mínima (Tmin) a nivel territorial (distrito/provincia/departamento) usando un raster GeoTIFF. El objetivo es diagnosticar riesgos de heladas y friajes, y proponer políticas públicas basadas en evidencia. Además, se entrega una app interactiva en Streamlit.

## Estructura del repositorio
- `/app` → aplicación Streamlit 
- `/scripts` → utilidades de carga, zonal stats y gráficos.
- `/data` → raster y shapefiles/GeoJSON 
  - `raster/`
  - `vector/`
  - `outputs/`
- `/notebooks` → análisis exploratorio 
- `/app/assets` → imágenes o mapas estáticos.

## Requisitos
- Python 3.10+
- Instalar dependencias con:
  ```bash
  pip install -r requirements.txt

## Ejecución local
streamlit run app/streamlit_app.py

## Enlace publico
pendiente

### Referencias del repositorio original
Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016. 
