# 📊 Catálogo de Scripts UX Data — Documentación

Este repositorio contiene scripts en Python diseñados para facilitar análisis estadísticos comunes en investigación UX cuantitativa.

---

## 📁 Estructura del proyecto

```
catalogo_scripts_ux_data/
├── main.py                     ← Script principal que ejecuta el análisis automáticamente
├── data/                       ← Coloca aquí tu archivo CSV (ej. test_ab.csv)
├── limpieza/                   ← Scripts de limpieza de datos
├── reports/                    ← Scripts para generar reportes HTML y CSV
├── tests_estadisticos/        ← Pruebas estadísticas listas para usar
├── visualizaciones/           ← Visualizaciones con Matplotlib
├── templates/                 ← Plantillas de análisis y presentación
```

---

## ✅ ¿Qué hace `main.py`?

1. Carga el archivo `test_ab.csv` desde la carpeta `/data/`
2. Limpia y normaliza los datos
3. **Detecta automáticamente el tipo de prueba estadística a aplicar:**
   - **z-test de proporciones** (2 variantes + conversiones/usuarios)
   - **chi-cuadrado** (3 o más variantes + conversiones/usuarios)
   - `t-test` o `ANOVA` si detecta medias numéricas (implementado)

4. Ejecuta el test y muestra:
   - Resultado estadístico (z o chi²)
   - Valor p
   - Conclusión
5. Genera:
   - `reporte_resultado.html`
   - `resultados_ab_test.csv`
   - Gráfico de barras (si aplica)

---

## 📌 Estructura esperada del CSV (z-test o chi²)

| variante | conversiones | usuarios |
|----------|--------------|----------|
| A        | 72           | 512      |
| B        | 102          | 498      |

> Si tenés solo 2 filas → aplica z-test  
> Si tenés 3 o más → aplica chi-cuadrado

---

## 📌 Estructura esperada del CSV para ANOVA

| variante | valor1 | valor2 | valor3 | ... |
|----------|--------|--------|--------|
| A        | 10.2   | 9.8    | 11.0   |
| B        | 8.5    | 9.1    | 7.9    |
| C        | 9.9    | 10.3   | 9.7    |

> En este caso, cada fila representa un grupo y las columnas contienen los valores medidos (tiempos, puntuaciones, etc.)  
> Esto permite aplicar un **ANOVA de un factor** para determinar si hay diferencias significativas entre grupos.

---

## 📌 Estructura esperada para `t-test`

| grupo     | valores                    |
|-----------|----------------------------|
| control   | 10.2, 9.8, 11.0            |
| experimento | 8.5, 9.1, 7.9             |

> Este formato sirve para comparar **dos grupos de valores continuos** (como tiempos promedio) mediante un t-test.

---

## 🛠 Requisitos

- Python 3.x
- Bibliotecas:
  - `pandas`
  - `matplotlib`
  - `scipy`
  - `statsmodels`

Podés instalar todo con:

```bash
pip install pandas matplotlib scipy statsmodels
```

---

## 🧪 ¿Qué pruebas incluye el catálogo?

| Prueba            | Módulo                      | Uso típico                                   |
|-------------------|-----------------------------|----------------------------------------------|
| z-test            | `ztest_proporciones.py`     | Comparar tasas de conversión A/B             |
| chi-cuadrado      | `chi_cuadrado.py`           | Comparar frecuencias entre 3+ categorías     |
| t-test            | `ttest_medias.py`           | Comparar medias entre 2 grupos (continuo)    |
| ANOVA             | `anova.py`                  | Comparar medias entre 3+ grupos              |

---

## 🧠 Buenas prácticas

- Verificá siempre que tus columnas estén completas (`quitar_nulos` se encarga).
- Usá nombres de columnas entendibles y sin espacios (se normalizan automáticamente).
- Asegurate de tener muestras suficientemente grandes (ideal: ≥ 30 por grupo).
- Para z-test y chi² usá frecuencias. Para t-test y ANOVA, usá **valores reales** (tiempos, puntajes, etc.)

---

## 💡 Siguiente versión

La próxima evolución de `main.py` incluirá detección automática de:
- Comparaciones de medias (t-test, ANOVA)
- Columnas de valores continuos vs proporciones
- Gráficos y reportes adaptados al tipo de prueba

