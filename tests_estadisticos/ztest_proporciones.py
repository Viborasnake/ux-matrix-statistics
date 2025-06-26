"""
Script: ztest_proporciones.py
Descripción: Realiza un test z para comparar proporciones entre dos grupos (ideal para test A/B con tasas de conversión).
Uso:
    from ztest_proporciones import z_test
    clicks = [72, 102]
    muestras = [512, 498]
    stat, pval = z_test(clicks, muestras)
"""

from statsmodels.stats.proportion import proportions_ztest

def z_test(clicks, muestras):
    stat, pval = proportions_ztest(clicks, muestras)
    return stat, pval
