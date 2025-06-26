"""
Script: analisis.py (versión robusta)
Descripción: Analiza automáticamente un CSV y aplica:
- z-test de proporciones (2 grupos con conversiones/usuarios)
- chi-cuadrado (3+ grupos con conversiones/usuarios)
- t-test (2 grupos con datos continuos)
- ANOVA (3+ grupos con datos continuos)
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path

from limpieza.quitar_nulos import quitar_nulos
from limpieza.normalizar_columnas import normalizar_nombres
from tests_estadisticos.ztest_proporciones import z_test
from tests_estadisticos.chi_cuadrado import chi_test
from tests_estadisticos.ttest_medias import t_test
from tests_estadisticos.anova import anova_test
from visualizaciones.conversion_plot import plot_conversion
from reports.generador_html_resultado import generar_html
from reports.exportar_csv_resultados import exportar_resultados
from visualizaciones.plot_medias import plot_medias_boxplot

P_ACEPTABLE = 0.05  # Umbral de significancia estadística

# 1. Cargar archivo
DATA_DIR = Path("data")
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No se encontró ningún archivo .csv en la carpeta /data")

DATA_PATH = csv_files[0]
print(f"📄 Archivo seleccionado para análisis: {DATA_PATH.name}")

# Crear carpeta de salida
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_folder = Path(f"outputs/{timestamp}_analisis_ux")
output_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df = normalizar_nombres(df)
columnas = df.columns.tolist()
resultado = {}
conclusion = ""
descripcion_grafico = ""

# FUNCIONES
def generar_reflexion(resultado, columnas, p_aceptable):
    test = resultado.get("test", "").lower()
    pvalor = resultado.get("p_valor", 1.0)
    estadistico = resultado.get("estadistico", None)
    tipo_dato = "tasas de conversión entre variantes" if "conversiones" in columnas else "valores numéricos continuos entre grupos"
    interpretacion = (
        f"una diferencia estadísticamente significativa (p < {p_aceptable}) entre grupos"
        if pvalor < p_aceptable else
        f"que no se encontraron diferencias significativas con el umbral p < {p_aceptable}"
    )
    return (
        f"Este análisis automatizado utilizó un {test} para evaluar {tipo_dato}. "
        f"Se obtuvo un estadístico de prueba de {estadistico} y un valor p de {pvalor}. "
        f"Los resultados sugieren {interpretacion}. "
        f"Es importante considerar el tamaño muestral y la calidad de los datos al interpretar los resultados."
    )

def explicacion_del_test(test):
    test = test.lower()
    if "z-test" in test:
        return "El z-test compara tasas de conversión entre dos grupos. Sirve para saber si una versión convierte mejor que otra."
    elif "chi-cuadrado" in test:
        return "El test chi-cuadrado compara conversiones entre tres o más grupos. Ayuda a detectar si alguna variante destaca significativamente."
    elif "t-test" in test:
        return "El t-test compara promedios entre dos grupos. Sirve para saber si hay una diferencia real en valores como tiempo o puntajes."
    elif "anova" in test:
        return "ANOVA compara promedios entre tres o más grupos. Es útil para detectar si hay diferencias relevantes entre varias opciones."
    else:
        return "Este test estadístico permite comparar grupos para detectar diferencias con significancia matemática."

def generar_descripcion_grafico(variantes, tasas, resultado, p_aceptable):
    mayor = max(tasas)
    menor = min(tasas)
    diferencia = abs(mayor - menor)
    p = resultado.get("p_valor", 1.0)
    descripcion = (
        f"El gráfico de barras compara la tasa de conversión entre las variantes: "
        f"{', '.join(variantes)}. La diferencia observada es de aproximadamente {diferencia:.2%}. "
    )
    descripcion += (
        "Esta diferencia visual es consistente con el resultado estadístico, indicando significancia."
        if p < p_aceptable else
        f"Aunque puede observarse una diferencia visual, no es significativa estadísticamente (p ≥ {p_aceptable})."
    )
    return descripcion

# 2. Lógica principal
if all(col in columnas for col in ["conversiones", "usuarios"]):
    # Z-test o chi-cuadrado
    df = quitar_nulos(df, columnas=["variante", "conversiones", "usuarios"])
    variantes = df["variante"].tolist()
    conversiones = df["conversiones"].tolist()
    usuarios = df["usuarios"].tolist()
    tasas = [conv / usu for conv, usu in zip(conversiones, usuarios)]
    nombre_imagen = plot_conversion(variantes, tasas, output_folder)

    if len(variantes) == 2:
        z, p = z_test(conversiones, usuarios)
        resultado["test"] = "z-test de proporciones"
        resultado["estadistico"] = round(z, 4)
        resultado["p_valor"] = round(p, 4)
    else:
        tabla = [[conv, total - conv] for conv, total in zip(conversiones, usuarios)]
        chi2, p, _ = chi_test(tabla)
        resultado["test"] = "chi-cuadrado"
        resultado["estadistico"] = round(chi2, 4)
        resultado["p_valor"] = round(p, 4)

    conclusion = "Hay diferencia significativa" if resultado["p_valor"] < P_ACEPTABLE else "No hay diferencia significativa"
    descripcion_grafico = generar_descripcion_grafico(variantes, tasas, resultado, P_ACEPTABLE)

elif set(["variante", "valor"]).issubset(columnas):
    # Análisis de medias con gráfico
    df = quitar_nulos(df, columnas=["variante", "valor"])
    variantes = df["variante"].unique().tolist()
    grupos = [df[df["variante"] == v]["valor"].tolist() for v in variantes]

    if all(len(g) >= 2 for g in grupos):
        if len(grupos) == 2:
            t, p = t_test(*grupos)
            resultado["test"] = "t-test de medias"
            resultado["estadistico"] = round(t, 4)
            resultado["p_valor"] = round(p, 4)
        else:
            f, p = anova_test(*grupos)
            resultado["test"] = "ANOVA"
            resultado["estadistico"] = round(f, 4)
            resultado["p_valor"] = round(p, 4)

        conclusion = "Hay diferencia significativa" if resultado[
                                                           "p_valor"] < P_ACEPTABLE else "No hay diferencia significativa"

        # 🔥 NUEVO: generar gráfico de boxplot
        nombre_imagen = plot_medias_boxplot(df, output_folder)
        descripcion_grafico = "El gráfico muestra la distribución de valores por grupo. Ayuda a visualizar las diferencias que analiza el test estadístico."
    else:
        raise ValueError("Cada grupo debe tener al menos 2 valores para aplicar análisis de medias.")

# 3. Reportes
reflexion = generar_reflexion(resultado, columnas, P_ACEPTABLE)
explicacion_test = explicacion_del_test(resultado["test"])
generar_html(
    "Análisis automático de datos UX",
    f"{resultado['test']} = {resultado['estadistico']}",
    f"p = {resultado['p_valor']}",
    conclusion,
    output_folder,
    reflexion,
    descripcion_grafico,
    explicacion_test,
    nombre_imagen
)


resultado["conclusion"] = conclusion
exportar_resultados(output_folder / "resultado_estadistico.csv", {k: [v] for k, v in resultado.items()})

print("✅ Análisis completado. Reportes generados:")
print(" - reporte_resultado.html")
print(" - resultado_estadistico.csv")
