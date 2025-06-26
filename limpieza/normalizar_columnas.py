"""
Script: normalizar_columnas.py
Descripción: Limpia y estandariza nombres de columnas: sin espacios, minúsculas, sin acentos.
Ideal para análisis automatizado o exportación limpia.
Uso:
    from normalizar_columnas import normalizar_nombres
    df = normalizar_nombres(df)
"""

import unicodedata

def normalizar_nombres(df):
    columnas = []
    for col in df.columns:
        col = col.strip().lower().replace(" ", "_")
        col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
        columnas.append(col)
    df.columns = columnas
    return df
