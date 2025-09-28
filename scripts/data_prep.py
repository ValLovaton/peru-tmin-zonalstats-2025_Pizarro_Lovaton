from pathlib import Path
import geopandas as gpd

# Directorios base
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
# VECTOR_DIR = DATA_DIR / "vector"
RASTER_DIR = DATA_DIR / "raster"


VECTOR_DIR = Path("data/vector")

def load_admin_level(level="district"):
    fname = {
        "district": "peru_districts.geojson",
        "province": "peru_provinces.geojson",
        "department": "peru_departments.geojson",
    }[level]

    gdf = gpd.read_file(VECTOR_DIR / fname).to_crs(4326)

    # Asignar UBIGEO y NAME según el nivel
    if level == "district":
        gdf["UBIGEO"] = gdf["IDDIST"].astype(str)
        gdf["NAME"] = gdf["NOMBDIST"].str.upper()
    elif level == "province":
        gdf["UBIGEO"] = gdf["IDPROV"].astype(str)
        gdf["NAME"] = gdf["NOMBPROV"].str.upper()
    else:  # department
        gdf["UBIGEO"] = gdf["IDDPTO"].astype(str)
        gdf["NAME"] = gdf["NOMBDEP"].str.upper()

    # Limpiar geometrías
    gdf = gdf[~gdf["geometry"].isna()].copy()
    gdf["geometry"] = gdf["geometry"].buffer(0)

    return gdf


def raster_path(name="tmin_peru.tif"):
    """Devuelve la ruta completa al raster."""
    return RASTER_DIR / name
