"""
Script: exportar_csv_resultados.py
Descripción: Exporta un diccionario de resultados a un archivo CSV.
Uso:
    from exportar_csv_resultados import exportar_resultados
    datos = {"variante": ["A", "B"], "conversiones": [72, 102], "usuarios": [512, 498]}
    exportar_resultados("resultados_ab_test.csv", datos)
"""

import pandas as pd

def exportar_resultados(nombre_archivo, datos):
    df = pd.DataFrame(datos)
    df.to_csv(nombre_archivo, index=False)
