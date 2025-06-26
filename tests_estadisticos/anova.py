"""
Script: anova.py
Descripción: Ejecuta un análisis ANOVA de un factor para comparar medias entre más de dos grupos.
Uso:
    from anova import anova_test
    grupo1 = [5.1, 5.5, 6.0]
    grupo2 = [6.3, 6.7, 6.9]
    grupo3 = [7.0, 7.5, 7.9]
    stat, pval = anova_test(grupo1, grupo2, grupo3)
"""

from scipy.stats import f_oneway

def anova_test(*grupos):
    stat, pval = f_oneway(*grupos)
    return stat, pval
