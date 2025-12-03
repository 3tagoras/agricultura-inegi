# Impacto del riego en la productividad agrícola en México (2021–2022)

Este artículo explica, paso a paso y de forma replicable, cómo se desarrolló un proyecto de análisis de datos para responder una sola pregunta aplicada:

**¿Cómo influye el acceso al riego en la productividad agrícola a cielo abierto en México durante 2021–2022?**

El proceso sigue el enfoque **CRISP-DM** y utiliza datasets oficiales del sector agropecuario.  
Todo está narrado para que puedas reproducirlo desde cero: obtención de datos, integración, análisis y conclusiones.

---

# 1. Definición del problema

La productividad agrícola mexicana varía ampliamente entre regiones. Un factor clave es el riego.  
El objetivo es cuantificar su impacto comparando:

- producción en toneladas  
- superficie sembrada  
- rendimientos  
- modalidades hídricas (riego, temporal, mixto)  
- ciclos agrícolas (OI y PV)  
- cultivos anuales y perennes  
- adopción tecnológica  

El análisis busca estimar **cuánto aumenta el rendimiento cuando existe riego**, controlando por cultivo y entidad.

---

# 2. Datos utilizados (máximo 10 datasets)

Los datos provienen de estadísticas agropecuarias recientes:

1. Unidades de producción y porcentaje que usan riego (entidad, municipio)  
2. Agricultura a cielo abierto y protegida: superficie y producción (entidad, cultivo)  
3. Agricultura a cielo abierto por modalidad hídrica (entidad, cultivo, estrato)  
4. Cultivos anuales OI por modalidad hídrica  
5. Cultivos anuales PV por modalidad hídrica  
6. Cultivos perennes a cielo abierto (superficie por edad)  
7. Superficie total y uso agropecuario (entidad)  
8. Instalaciones agrícolas utilizadas (entidad, municipio)  
9. Unidades agropecuarias activas por uso del suelo  
10. Uso de tecnologías agrícolas en agricultura a cielo abierto (entidad, municipio)

Estos datasets permiten una vista completa: riego, producción, suelo, tecnología y ciclos.

---

# 3. Preparación del entorno

Se usaron:

- Python 3.11  
- Pandas, Numpy, Geopandas  
- SQL (PostgreSQL)  
- Matplotlib  
- Jupyter Notebook  

Estructura recomendada:

```

project/
├── data_raw/
├── data_clean/
├── notebooks/
├── sql/
├── src/
└── outputs/

```

---

# 4. ETL: extracción, limpieza y transformación

## 4.1 Extracción
- Descargar cada dataset en CSV o Excel.  
- Convertir a UTF-8.  
- Normalizar nombres de columnas.  
- Agregar identificadores clave (entidad_id, municipio_id, cultivo_id).

## 4.2 Limpieza
Acciones comunes:

- Eliminar filas vacías.  
- Homologar unidades:
  - superficie → hectáreas  
  - producción → toneladas  
- Estandarizar nombres de cultivos.  
- Corregir valores “ND”, “NR”, “999999”, etc.

## 4.3 Transformación
Variables derivadas creadas:

- **rendimiento = producción / superficie**  
- **riego_binario = 1 si modalidad_hidrica = riego, 0 si temporal**  
- **tecnología_index = Σ(% uso de cada tecnología)**  
- **modalidad_simplificada (riego, temporal, mixto)**

Se generaron tablas finales:

```

fact_produccion
dim_entidad
dim_municipio
dim_cultivo
fact_tecnologia
fact_superficie

```

Finalmente, todos los datos limpios se cargaron en PostgreSQL.

---

# 5. Análisis exploratorio (EDA)

El análisis se organiza en cinco bloques. Cada uno puede reproducirse creando vistas SQL y visualizaciones simples.

## 5.1 Cobertura de riego por entidad
Se calcula:

```

porcentaje_riego = upa_con_riego / total_upa

```

Resultados clave:

- Se detectan entidades con alta dependencia del riego.  
- Otras dependen casi totalmente del temporal.  

## 5.2 Rendimiento por modalidad hídrica  
Se construyen dos series:

- rendimiento_riego  
- rendimiento_temporal  

Comparaciones hechas:

- Por cultivo  
- Por entidad  
- A nivel nacional  

El patrón general es consistente: **el riego incrementa el rendimiento**, pero varía entre cultivos.

## 5.3 Ciclos agrícolas OI y PV (anuales)  
Se analizaron ambos ciclos:

- Superficie sembrada  
- Producción  
- Rendimientos por modalidad hídrica  

Esto permite ver cómo cambia la ventaja del riego entre estaciones.

## 5.4 Cultivos perennes  
Los datos incluyen edad de plantaciones.  
Se evalúa:

- rendimiento por riego vs temporal  
- impacto de plantaciones jóvenes vs maduras  

Los perennes muestran brechas diferentes a los anuales.

## 5.5 Infraestructura y tecnología  
Se relaciona:

- porcentaje_riego  
- tecnología_index  
- instalaciones agrícolas

Análisis base:

```

correl(riego_binario, tecnologia_index)

```

Permite ver si la tecnología complementa el riego o lo sustituye.

---

# 6. Modelado (opcional, reproducible en pocas líneas)

Modelo lineal general:

```

rendimiento ~ riego_binario + superficie + tecnologia_index + C(cultivo) + C(entidad)

```

Los coeficientes clave:

- **riego_binario** → estima el impacto marginal del riego  
- **superficie** → controla eficiencia por escala  
- **tecnología** → mide efectos adicionales  

También se ajustó un modelo individual por cultivo (ej. maíz) para interpretación más limpia.

---

# 7. Resultados principales

Los resultados dependen de cada ejecución pero la estructura replicable produce salidas comparables:

- El riego incrementa el rendimiento en la mayoría de los cultivos.  
- La brecha riego–temporal cambia según entidad.  
- En cultivos anuales, el impacto del riego es mayor en OI que en PV.  
- En perennes, la edad de plantación influye más que la modalidad hídrica en algunos casos.  
- La adopción tecnológica se asocia a mayor eficiencia, incluso en temporal.

---

# 8. Conclusiones

El proyecto permite responder la pregunta inicial con evidencia cuantitativa:

- El riego mejora el rendimiento agrícola, pero no de forma uniforme.  
- Las diferencias entre entidades permiten identificar zonas prioritarias para inversión.  
- La tecnología puede reducir la dependencia del riego en ciertas regiones.  
- El análisis por ciclos muestra que el efecto del riego no es constante durante el año.

La metodología es totalmente replicable. Cualquier persona puede rehacer el proyecto siguiendo los pasos: obtener los 10 datasets, aplicar las transformaciones, cargar en SQL, realizar EDA y, si desea, ajustar modelos.

---

# 9. Archivos sugeridos en un repositorio

```

/notebooks/01_ETL.ipynb
/notebooks/02_EDA.ipynb
/notebooks/03_Modelos.ipynb
/sql/schema.sql
/sql/cleaning.sql
/src/utils.py
/src/etl.py
/outputs/figures/

```
