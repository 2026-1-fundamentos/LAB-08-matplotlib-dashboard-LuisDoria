# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""


def pregunta_01():
    """
    Genera cuatro gráficas de los datos de envíos y crea un dashboard
    estático en la carpeta ``docs``.
    """

    import math
    from pathlib import Path

    import matplotlib

    # Backend no interactivo: permite ejecutar el código desde pytest.
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import pandas as pd
    from matplotlib.patches import Wedge

    # El enunciado actualizado ubica el CSV en data/. Se incluyen rutas
    # alternativas para que la solución también funcione con otras
    # estructuras usadas en el laboratorio.
    rutas_posibles = [
        Path("data/shipping-data.csv"),
        Path("files/shipping-data.csv"),
        Path("files/input/shipping-data.csv"),
    ]

    ruta_csv = next(
        (ruta for ruta in rutas_posibles if ruta.exists()),
        None,
    )

    if ruta_csv is None:
        raise FileNotFoundError(
            "No se encontró el archivo 'shipping-data.csv'. "
            "Ubíquelo en la carpeta 'data'."
        )

    carpeta_salida = Path("docs")
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    dataframe = pd.read_csv(ruta_csv)

    columnas_requeridas = [
        "Warehouse_block",
        "Mode_of_Shipment",
        "Customer_rating",
        "Weight_in_gms",
    ]

    columnas_faltantes = [
        columna for columna in columnas_requeridas if columna not in dataframe.columns
    ]

    if columnas_faltantes:
        raise ValueError(
            "Faltan las siguientes columnas en el CSV: " + ", ".join(columnas_faltantes)
        )

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "axes.titlesize": 15,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
        }
    )

    def guardar_figura(figura, nombre_archivo):
        """Guarda y cierra una figura de Matplotlib."""

        figura.tight_layout()

        figura.savefig(
            carpeta_salida / nombre_archivo,
            dpi=150,
            bbox_inches="tight",
            facecolor="white",
        )

        plt.close(figura)

    # ---------------------------------------------------------------
    # 1. Envíos por bloque de almacén: gráfico de barras.
    # ---------------------------------------------------------------
    envios_por_almacen = (
        dataframe["Warehouse_block"].dropna().astype(str).value_counts().sort_index()
    )

    figura, eje = plt.subplots(figsize=(8, 5))

    barras = eje.bar(
        envios_por_almacen.index,
        envios_por_almacen.values,
        color="#4C78A8",
        edgecolor="white",
        linewidth=0.8,
    )

    eje.set_title("Shipping per Warehouse")
    eje.set_xlabel("Warehouse block")
    eje.set_ylabel("Number of shipments")

    eje.spines["top"].set_visible(False)
    eje.spines["right"].set_visible(False)

    eje.grid(
        axis="y",
        linestyle="--",
        alpha=0.30,
    )

    for barra, valor in zip(
        barras,
        envios_por_almacen.values,
    ):
        eje.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height(),
            f"{valor:,}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    guardar_figura(
        figura,
        "shipping_per_warehouse.png",
    )

    # ---------------------------------------------------------------
    # 2. Distribución de los modos de envío: gráfico circular.
    # ---------------------------------------------------------------
    modos_envio = dataframe["Mode_of_Shipment"].dropna().astype(str).value_counts()

    figura, eje = plt.subplots(figsize=(8, 5))

    eje.pie(
        modos_envio.values,
        labels=modos_envio.index,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
        colors=[
            "#4C78A8",
            "#F58518",
            "#54A24B",
            "#E45756",
        ],
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 1.2,
        },
        textprops={
            "fontsize": 10,
        },
    )

    eje.set_title("Mode of Shipment")
    eje.axis("equal")

    guardar_figura(
        figura,
        "mode_of_shipment.png",
    )

    # ---------------------------------------------------------------
    # 3. Calificación promedio: indicador semicircular.
    # ---------------------------------------------------------------
    calificaciones = pd.to_numeric(
        dataframe["Customer_rating"],
        errors="coerce",
    ).dropna()

    promedio = float(calificaciones.mean())

    # Impide que la aguja salga de la escala de cero a cinco.
    valor_indicador = max(
        0.0,
        min(promedio, 5.0),
    )

    figura, eje = plt.subplots(figsize=(8, 5))

    zonas = [
        (0, 1, "#E45756"),
        (1, 2, "#F28E2B"),
        (2, 3, "#EDC948"),
        (3, 4, "#8CD17D"),
        (4, 5, "#59A14F"),
    ]

    for inicio, fin, color in zonas:
        angulo_inicial = 180 - (fin / 5) * 180
        angulo_final = 180 - (inicio / 5) * 180

        eje.add_patch(
            Wedge(
                center=(0, 0),
                r=1.0,
                theta1=angulo_inicial,
                theta2=angulo_final,
                width=0.28,
                facecolor=color,
                edgecolor="white",
                linewidth=1.2,
            )
        )

    # Ángulo y posición de la aguja.
    angulo_aguja = math.radians(180 - (valor_indicador / 5) * 180)

    extremo_x = 0.72 * math.cos(angulo_aguja)
    extremo_y = 0.72 * math.sin(angulo_aguja)

    eje.plot(
        [0, extremo_x],
        [0, extremo_y],
        color="#263238",
        linewidth=3,
        solid_capstyle="round",
    )

    eje.scatter(
        [0],
        [0],
        s=90,
        color="#263238",
        zorder=5,
    )

    # Etiquetas de cero a cinco.
    for valor in range(6):
        angulo_etiqueta = math.radians(180 - (valor / 5) * 180)

        posicion_x = 1.15 * math.cos(angulo_etiqueta)

        posicion_y = 1.15 * math.sin(angulo_etiqueta)

        eje.text(
            posicion_x,
            posicion_y,
            str(valor),
            ha="center",
            va="center",
            fontsize=10,
        )

    eje.text(
        0,
        -0.20,
        f"{promedio:.2f} / 5",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="#263238",
    )

    eje.text(
        0,
        -0.38,
        "Average rating",
        ha="center",
        va="center",
        fontsize=11,
        color="#607D8B",
    )

    eje.set_title(
        "Average Customer Rating",
        pad=15,
    )

    eje.set_xlim(-1.35, 1.35)
    eje.set_ylim(-0.55, 1.30)
    eje.set_aspect("equal")
    eje.axis("off")

    guardar_figura(
        figura,
        "average_customer_rating.png",
    )

    # ---------------------------------------------------------------
    # 4. Distribución del peso: histograma.
    # ---------------------------------------------------------------
    pesos = pd.to_numeric(
        dataframe["Weight_in_gms"],
        errors="coerce",
    ).dropna()

    peso_promedio = float(pesos.mean())

    figura, eje = plt.subplots(figsize=(8, 5))

    eje.hist(
        pesos,
        bins=30,
        color="#72B7B2",
        edgecolor="white",
        linewidth=0.7,
    )

    eje.axvline(
        peso_promedio,
        color="#E45756",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {peso_promedio:,.0f} g",
    )

    eje.set_title("Shipped Weight Distribution")
    eje.set_xlabel("Weight (g)")
    eje.set_ylabel("Frequency")

    eje.spines["top"].set_visible(False)
    eje.spines["right"].set_visible(False)

    eje.grid(
        axis="y",
        linestyle="--",
        alpha=0.30,
    )

    eje.legend(frameon=False)

    guardar_figura(
        figura,
        "weight_distribution.png",
    )

    # ---------------------------------------------------------------
    # 5. Dashboard HTML.
    # ---------------------------------------------------------------
    contenido_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Shipping Dashboard Example</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 32px;
            background: #f3f6f9;
            color: #263238;
            font-family: Arial, Helvetica, sans-serif;
        }

        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            margin-bottom: 24px;
        }

        h1 {
            margin: 0 0 8px;
            font-size: 32px;
        }

        .subtitle {
            margin: 0;
            color: #607d8b;
            font-size: 16px;
        }

        .grid {
            display: grid;
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
            gap: 22px;
        }

        .card {
            overflow: hidden;
            padding: 18px;
            background: white;
            border: 1px solid #e0e6eb;
            border-radius: 12px;
            box-shadow:
                0 6px 18px rgba(38, 50, 56, 0.08);
        }

        .card img {
            display: block;
            width: 100%;
            height: auto;
        }

        @media (max-width: 850px) {
            body {
                padding: 18px;
            }

            .grid {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 26px;
            }
        }
    </style>
</head>

<body>
    <main class="dashboard">
        <header class="header">
            <h1>Shipping Dashboard Example</h1>

            <p class="subtitle">
                Visually appealing representation
                of shipping data
            </p>
        </header>

        <section class="grid">
            <article class="card">
                <img
                    src="shipping_per_warehouse.png"
                    alt="Shipping per warehouse bar chart"
                >
            </article>

            <article class="card">
                <img
                    src="mode_of_shipment.png"
                    alt="Mode of shipment pie chart"
                >
            </article>

            <article class="card">
                <img
                    src="average_customer_rating.png"
                    alt="Average customer rating gauge"
                >
            </article>

            <article class="card">
                <img
                    src="weight_distribution.png"
                    alt="Weight distribution histogram"
                >
            </article>
        </section>
    </main>
</body>
</html>
"""

    (carpeta_salida / "index.html").write_text(
        contenido_html,
        encoding="utf-8",
    )
