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

## Datos

- **Temperatura mínima (Tmin)**: raster GeoTIFF disponible en Google Drive: https://drive.google.com/drive/folders/1kf8Kfuo3EkmcPfQMIyVKPug0FwnzTNHP
- **Límites administrativos**: GeoJSON de distritos, provincias y departamentos en `/data/vector/`

## Politicas publicas recomendadas en base a los resultados

### Diagnóstico
El análisis muestra que los distritos altoandinos (Puno, Cusco, Ayacucho, Huancavelica, Pasco) presentan valores de Tmin muy bajos y `cold_margin < 0`, indicando riesgo de heladas severas. En la Amazonía (Loreto, Ucayali, Madre de Dios), las bandas analizadas también muestran descensos bruscos de Tmin asociados a friajes.

### Medida 1 — Vivienda térmica (ISUR)
- **Objetivo:** reducir infecciones respiratorias agudas (IRAs) en escolares y adultos mayores.  
- **Población meta:** hogares en los 100 distritos más fríos (`cold_margin < 0`).  
- **Costo estimado:** S/ 3,500 por unidad mejorada.  
- **KPI:** −20% casos IRA (MINSA/ESSALUD), +15% asistencia escolar en invierno.

### Medida 2 — Kits anti-helada para pequeños productores
- **Objetivo:** disminuir pérdidas agrícolas y ganaderas.  
- **Intervención:** cobertores, microtúneles, sales minerales, refugios para alpacas.  
- **Población meta:** pequeños productores de zonas altoandinas con Tmin en p10 ≤ 0°C.  
- **Costo estimado:** S/ 800 por productor/ha.  
- **KPI:** −25% mortalidad de crías, −15% siniestros agro.

### Medida 3 — Calendario agro + alertas tempranas
- **Objetivo:** adaptar fechas de siembra/cosecha a percentiles locales de Tmin.  
- **Intervención:** envío de alertas (app/WhatsApp) y capacitación en manejo de friaje.  
- **Población meta:** agricultores en distritos amazónicos con descensos bruscos de Tmin.  
- **Costo estimado:** S/ 10 por agricultor/año.  
- **KPI:** ≥70% adopción de recomendaciones, −X% pérdidas por evento frío.

### Referencias del repositorio original
Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016. 
