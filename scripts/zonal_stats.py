import numpy as np
import geopandas as gpd
import rioxarray as rxr
from rasterstats import zonal_stats
from .data_prep import raster_path

# Métricas
STATS = ["count", "mean", "min", "max", "std", "percentile_10", "percentile_90"]

def compute_band_stats(gdf: gpd.GeoDataFrame, tif_name="tmin_peru.tif", band=1):

    tif = raster_path(tif_name)

    # Abrir raster con rioxarray para estimar escala
    xds = rxr.open_rasterio(tif, masked=True).sel(band=band)
    sample = xds.values
    scale_factor = 0.1 if np.nanmedian(sample) > 80 else 1.0

    zs = zonal_stats(
        vectors=gdf.to_crs(4326),
        raster=str(tif),
        stats=STATS,
        band=band,
        all_touched=True,
        nodata=None,
        geojson_out=False,
    )

    out = gdf.copy()
    for k in STATS:
        vals = np.array([d.get(k, np.nan) for d in zs], dtype=float)
        if k in {"mean", "min", "max", "std", "percentile_10", "percentile_90"}:
            vals *= scale_factor
        out[k] = vals

    # Métrica
    out["cold_margin"] = out["percentile_10"] - 0.0

    return out

def compute_multiband(gdf, tif_name="tmin_peru.tif", start_year=2020):
    """
    Itera sobre todas las bandas del raster y devuelve un dict {año: GeoDataFrame}.
    """
    tif = raster_path(tif_name)
    da = rxr.open_rasterio(tif, masked=True)

    results = {}
    for b in da.band.values:
        year = start_year + int(b) - 1
        results[year] = compute_band_stats(gdf, tif_name, band=int(b))
    return results
