import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from jinja2 import Template
from reports.generador_index import generar_index_html  # Asegurate de tener este módulo

def generar_tabla_comparativa(df, output_path):
    template_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Comparativa de Resultados UX</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f4f8;
                color: #333;
                display: flex;
                justify-content: center;
                margin: 0;
                padding: 0;
            }
            .container {
                background: white;
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                max-width: 900px;
                width: 95%;
                margin-top: 40px;
                margin-bottom: 60px;
            }
            h2 {
                text-align: center;
                color: #004080;
                margin-bottom: 24px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #e6f0ff;
                color: #004080;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            footer {
                margin-top: 40px;
                font-size: 0.9em;
                color: #777;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Comparativa de Resultados UX</h2>
            <table>
                <thead>
                    <tr>
                        {% for col in columnas %}
                        <th>{{ col }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for fila in filas %}
                    <tr>
                        {% for valor in fila %}
                        <td>{{ valor }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <footer>
                Desarrollado por Cristian Pizarro con asistencia IA
            </footer>
        </div>
    </body>
    </html>
    """
    template = Template(template_html)
    columnas = df.columns.tolist()
    filas = df.values.tolist()
    html = template.render(columnas=columnas, filas=filas)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def comparar_resultados(entrada_outputs="outputs", umbral_p=0.05):
    outputs_path = Path(entrada_outputs)
    resultados = []

    for carpeta in outputs_path.iterdir():
        if carpeta.is_dir():
            archivo_csv = carpeta / "resultado_estadistico.csv"
            if archivo_csv.exists():
                df = pd.read_csv(archivo_csv)
                df["carpeta"] = carpeta.name
                resultados.append(df)

    if not resultados:
        raise ValueError("No se encontraron archivos resultado_estadistico.csv dentro de las subcarpetas.")

    df_resultados = pd.concat(resultados, ignore_index=True)
    df_resultados["timestamp"] = pd.to_datetime(
        df_resultados["carpeta"].str.extract(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})")[0],
        format="%Y-%m-%d_%H-%M-%S"
    )
    df_resultados = df_resultados.sort_values("timestamp")

    # Guardar tabla HTML estilizada
    tabla_path = outputs_path / "comparativa_resultados.html"
    generar_tabla_comparativa(df_resultados, tabla_path)

    # Graficar evolución de p-valores
    plt.figure(figsize=(10, 6))
    plt.plot(df_resultados["timestamp"], df_resultados["p_valor"], marker="o", label="p-valor")
    plt.axhline(umbral_p, color="red", linestyle="--", label=f"p aceptable ({umbral_p})")
    plt.xticks(rotation=45)
    plt.ylabel("p-valor")
    plt.title("Evolución del p-valor en análisis UX")
    plt.legend()
    plt.tight_layout()
    grafico_path = outputs_path / "evolucion_pvalores.png"
    plt.savefig(grafico_path)

    print(f"✅ Comparativa generada: {tabla_path.name}, {grafico_path.name}")

    # Generar panel de navegación principal
    generar_index_html()
    print("📂 Navegador central index.html actualizado")

if __name__ == "__main__":
    comparar_resultados("outputs")
