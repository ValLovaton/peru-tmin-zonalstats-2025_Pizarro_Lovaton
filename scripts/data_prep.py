from pathlib import Path
import geopandas as gpd

# Directorios base
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
VECTOR_DIR = DATA_DIR / "vector"
RASTER_DIR = DATA_DIR / "raster"

def load_admin_level(level="district"):

    fname = {
        "district": "peru_districts.geojson",
        "province": "peru_provinces.geojson",
        "department": "peru_departments.geojson",
    }[level]

    gdf = gpd.read_file(VECTOR_DIR / fname).to_crs(4326)

    # Normalizar columnas
    gdf["UBIGEO"] = gdf["UBIGEO"].astype(str).str.upper()
    gdf["NAME"] = (
        gdf["NAME"]
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    # Arreglar geometrías inválidas
    gdf["geometry"] = gdf["geometry"].buffer(0)

    return gdf

def raster_path(name="tmin_peru.tif"):
    """Devuelve la ruta completa al raster."""
    return RASTER_DIR / name
