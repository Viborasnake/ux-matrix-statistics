
import matplotlib.pyplot as plt
import seaborn as sns

def plot_medias_boxplot(df, output_folder):
    """
    Genera un boxplot para visualización de medias entre grupos.
    - df: DataFrame con columnas 'variante' y 'valor'
    - output_folder: carpeta donde se guarda el gráfico
    """
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='variante', y='valor', hue='variante', data=df, palette='Set2', legend=False)
    plt.title("Distribución de valores por grupo")
    plt.ylabel("Valor observado")
    plt.xlabel("Grupo / Variante")
    plt.tight_layout()

    output_path = output_folder / "boxplot_medias.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path.name
