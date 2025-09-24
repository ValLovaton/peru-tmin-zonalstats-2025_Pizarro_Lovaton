import matplotlib.pyplot as plt

def plot_distribution(gdf, col="mean", title="Distribución de Tmin (media)"):
    ax = gdf[col].hist(bins=40)
    ax.set_title(title)
    ax.set_xlabel("°C")
    ax.set_ylabel("Frecuencia")
    fig = ax.get_figure()
    fig.tight_layout()
    return fig

def top_bottom_ranking(gdf, col="mean", k=15):
    """
    Devuelve dos dataframes:
    - topk: los k distritos/provincias más fríos (menor Tmin promedio)
    - botk: los k distritos/provincias más cálidos (mayor Tmin promedio)
    """
    topk = gdf.nsmallest(k, col)
    botk = gdf.nlargest(k, col)
    return topk, botk

def plot_choropleth(gdf, col="cold_margin", title="Riesgo de helada (margen p10 vs 0°C)"):
    ax = gdf.plot(column=col, scheme="Quantiles", k=5, legend=True, figsize=(8, 8))
    ax.set_axis_off()
    ax.set_title(title)
    fig = ax.get_figure()
    fig.tight_layout()
    return fig
