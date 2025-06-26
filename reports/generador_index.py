from pathlib import Path

def generar_index_html(entrada_outputs="outputs"):
    outputs_path = Path(entrada_outputs)
    carpetas = [carpeta for carpeta in outputs_path.iterdir() if carpeta.is_dir()]

    enlaces_analisis = ""
    for carpeta in sorted(carpetas):
        nombre = carpeta.name
        enlace = carpeta / "reporte_resultado.html"
        if enlace.exists():
            enlaces_analisis += f'<li><a href="{enlace}" target="_blank">{nombre}</a></li>\n'

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel de Análisis UX</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f2f4f8;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
        }}
        .container {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-width: 700px;
            width: 90%;
            margin-top: 40px;
            margin-bottom: 60px;
        }}
        h2 {{
            text-align: center;
            color: #004080;
            margin-bottom: 20px;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            margin-bottom: 12px;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        footer {{
            margin-top: 40px;
            font-size: 0.9em;
            color: #777;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Panel de Análisis UX</h2>

        <h3>Comparativa general</h3>
        <ul>
            <li><a href="outputs/comparativa_resultados.html" target="_blank">📊 Tabla comparativa de resultados</a></li>
            <li><a href="outputs/evolucion_pvalores.png" target="_blank">📈 Gráfico evolución de p-valores</a></li>
        </ul>

        <h3>Informes individuales</h3>
        <ul>
            {enlaces_analisis}
        </ul>

        <footer>
            Desarrollado por Cristian Pizarro con asistencia IA
        </footer>
    </div>
</body>
</html>
"""

    index_path = outputs_path.parent / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Panel principal generado en: {index_path}")

if __name__ == "__main__":
    generar_index_html()
