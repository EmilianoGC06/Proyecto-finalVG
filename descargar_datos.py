import pandas as pd
import numpy as np

# ── 1. Cargar archivos ──────────────────────────────────────────────
print("Cargando datos...")
df = pd.read_csv("stations_daily.csv")
df_stations = pd.read_csv("stations_rsinaica.csv")

# ── 2. Unir con catálogo de estaciones ─────────────────────────────
df_stations_clean = df_stations[["station_id", "station_name", "network_name", "lat", "lon"]].copy()
df_stations_clean.rename(columns={"network_name": "ciudad"}, inplace=True)

df = df.merge(df_stations_clean, on="station_id", how="left")
print(f"Registros totales: {len(df)}")

# ── 3. Parsear fechas ──────────────────────────────────────────────
df["datetime"] = pd.to_datetime(df["datetime"])
df["year"]     = df["datetime"].dt.year
df["month"]    = df["datetime"].dt.month
df["day_of_week"] = df["datetime"].dt.dayofweek          # 0=Lunes
df["day_name"]    = df["datetime"].dt.day_name()

# ── 4. Filtrar ciudades principales y años recientes ──────────────
ciudades_principales = [
    "Valle de México", "Monterrey", "Guadalajara",
    "Municipio de Juárez", "Mexicali", "Puebla-Tlaxcala",
    "León", "Toluca", "Tijuana"
]
df = df[df["ciudad"].isin(ciudades_principales)]
df = df[df["year"] >= 2010]  # últimos ~11 años

# ── 5. Quedarse con columnas relevantes ───────────────────────────
cols = ["datetime", "year", "month", "day_of_week", "day_name",
        "station_id", "station_name", "ciudad",
        "PM2.5", "PM10", "O3", "NO2", "CO"]
df = df[cols]

# ── 6. Eliminar valores negativos (errores de sensor) ─────────────
for col in ["PM2.5", "PM10", "O3", "NO2", "CO"]:
    df[col] = df[col].where(df[col] >= 0, np.nan)

# ── 7. Guardar datos limpios ───────────────────────────────────────
df.to_csv("datos_limpios.csv", index=False)
print(f"✅ Datos limpios guardados: {len(df)} registros")
print(f"   Ciudades: {df['ciudad'].nunique()}")
print(f"   Período:  {df['datetime'].min().date()} a {df['datetime'].max().date()}")
print(f"\nRegistros por ciudad:")
print(df["ciudad"].value_counts())
print(f"\nValores disponibles (%):")
for col in ["PM2.5", "PM10", "O3", "NO2"]:
    pct = df[col].notna().mean() * 100
    print(f"  {col}: {pct:.1f}%")