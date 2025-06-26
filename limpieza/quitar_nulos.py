"""
Script: quitar_nulos.py
Descripción: Elimina filas con valores nulos en columnas específicas de un DataFrame.
Ideal para limpiar resultados de encuestas o eventos incompletos.
Uso:
    from quitar_nulos import quitar_nulos
    df_limpio = quitar_nulos(df, columnas=["email", "evento"])
"""

import pandas as pd

def quitar_nulos(df, columnas):
    return df.dropna(subset=columnas)
