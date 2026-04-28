# ¿Respiramos peor en lunes?
### Patrones de contaminación del aire en las principales ciudades de México (2010–2021)

**Autor:** Francisco Emiliano Guillén Calderón 
**Materia:** Visualización gráfica para IA  
**Universidad:** Universidad Iberoamericana León  
**Docente:** Dra. Dora Alvarado  

---

## Descripción del proyecto

Este proyecto es una narrativa visual interactiva que analiza los patrones de contaminación del aire en las principales zonas metropolitanas de México durante el período 2010–2021. A través de tres visualizaciones interactivas, se responde la pregunta: **¿importa qué día de la semana es para la calidad del aire que respiramos?**

El resultado funciona como un artículo de datos: el lector avanza por una historia donde cada gráfica aparece acompañada del contexto necesario para interpretarla, desde el panorama general por ciudad hasta los patrones semanales y la tendencia histórica.

---

## Fuente de datos

- **Dataset:** Mexico Hourly Air Pollution (2010-2021)
- **Origen:** SINAICA (Sistema Nacional de Información de la Calidad del Aire), publicado en Kaggle
- **URL:** https://www.kaggle.com/datasets/alizahidraza/mexico-hourly-air-pollution-2010-2021
- **Fecha de descarga:** Abril 2026
- **Licencia:** Datos públicos del gobierno mexicano (INECC/SINAICA)
- **Formato original:** CSV (`stations_daily.csv`, `stations_rsinaica.csv`)

---

## Estructura del repositorio

```
calidad-aire-mexico/
│
├── app.py                  # Aplicación principal de Streamlit
├── descargar_datos.py      # Script de obtención y limpieza de datos
├── datos_limpios.csv       # Dataset procesado y listo para visualizar
├── stations_rsinaica.csv   # Catálogo de estaciones de monitoreo
└── README.md               # Este archivo
```

---

## Instrucciones para ejecutar localmente

### 1. Requisitos previos
- Python 3.9 o superior
- pip

### 2. Instalar dependencias
```bash
pip install streamlit plotly pandas
```

### 3. Correr la aplicación
```bash
python -m streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.

### 4. (Opcional) Regenerar los datos limpios
Si quieres reproducir el proceso de limpieza desde cero, coloca los archivos `stations_daily.csv` y `stations_rsinaica.csv` en la misma carpeta y ejecuta:
```bash
python descargar_datos.py
```

---

## Visualizaciones

| # | Título | Pregunta que responde |
|---|--------|----------------------|
| 1 | El mapa de la contaminación | ¿Qué ciudades superan el límite de la OMS? |
| 2 | El ritmo semanal | ¿Qué día de la semana es el más contaminado? |
| 3 | La tendencia de una década | ¿Ha mejorado la calidad del aire entre 2010 y 2021? |

---

## Sitio desplegado

🔗 <!-- Agrega aquí el link de Streamlit Community Cloud una vez desplegado -->
