"""
Script: chi_cuadrado.py
Descripción: Ejecuta una prueba chi-cuadrado para tablas de contingencia. Útil cuando se comparan distribuciones categóricas (como dispositivo vs error).
Uso:
    from chi_cuadrado import chi_test
    tabla = [[120, 30], [90, 10], [60, 15]]
    stat, p, expected = chi_test(tabla)
"""

from scipy.stats import chi2_contingency

def chi_test(tabla):
    stat, p, dof, expected = chi2_contingency(tabla)
    return stat, p, expected
