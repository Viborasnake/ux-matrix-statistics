"""
Script: ttest_medias.py
Descripción: Realiza un t-test para comparar medias entre dos grupos independientes (por ejemplo, tiempo promedio en tareas).
Uso:
    from ttest_medias import t_test
    grupo1 = [10.2, 9.8, 11.0]
    grupo2 = [8.5, 9.1, 7.9]
    stat, pval = t_test(grupo1, grupo2)
"""

from scipy.stats import ttest_ind

def t_test(grupo1, grupo2):
    stat, pval = ttest_ind(grupo1, grupo2, equal_var=False)
    return stat, pval
