def generar_html(titulo, estadistico, pvalor, conclusion, output_folder, reflexion, descripcion_grafico, explicacion_test, nombre_imagen):


    html = f"""<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
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
                text-align: center;
            }}
            h2 {{
                color: #004080;
                margin-bottom: 20px;
            }}
            p {{
                font-size: 1.1em;
                margin: 12px 0;
            }}
            img {{
                margin-top: 20px;
                max-width: 100%;
                border: 1px solid #ddd;
                border-radius: 8px;
            }}
            footer {{
                margin-top: 40px;
                font-size: 0.9em;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{titulo}</h2>
            <p><strong>Estadístico:</strong> {estadistico}</p>
            <p><strong>Valor p:</strong> {pvalor}</p>
            <p><strong>Conclusión:</strong> {conclusion}</p>
            <hr>
            <h3>Reflexión automatizada del análisis</h3>
            <p style="font-style: italic;">{reflexion}</p>
            <hr>
            <h3>¿Qué significa este test?</h3>
            <p>{explicacion_test}</p>
            <hr>
            <h3>Descripción del gráfico</h3>
            <p>{descripcion_grafico}</p>
            <img src="{nombre_imagen}" alt="Gráfico del análisis estadístico">"""




    html += """
            <footer>
                Desarrollado por Cristian Pizarro con asistencia IA
            </footer>
        </div>
    </body>
    </html>
    """

    output_path = output_folder / "reporte_resultado.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
