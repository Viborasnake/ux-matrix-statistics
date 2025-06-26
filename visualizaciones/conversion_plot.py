"""
Script: conversion_plot.py
Descripción: Grafica la tasa de conversión para distintas variantes en un test A/B.
Uso:
    from conversion_plot import plot_conversion
    variantes = ["A", "B"]
    tasas = [0.1406, 0.2048]
    plot_conversion(variantes, tasas)
"""

import matplotlib.pyplot as plt

def plot_conversion(variantes, tasas, output_folder):
    plt.bar(variantes, tasas)
    for i, rate in enumerate(tasas):
        plt.text(i, rate + 0.01, f"{rate:.2%}", ha='center')
    plt.ylabel("Tasa de conversión")
    plt.tight_layout()
    output_path = output_folder / "grafico.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path.name

    plt.title("Comparación A/B")
    plt.ylim(0, max(tasas) + 0.05)
    plt.show()
