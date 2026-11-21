"""Run using the Python supplied by QGIS. Output is consumed by bench.py."""

import argparse
from pathlib import Path
from qgis.core import QgsApplication, QgsRasterLayer, QgsProject
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry


def main():
    parser = argparse.ArgumentParser()
    for field in ("first", "second", "output"):
        parser.add_argument(field)
    args = parser.parse_args()
    app = QgsApplication([], False)
    app.initQgis()
    try:
        calculate(args)
    finally:
        app.exitQgis()


def calculate(args):
    # Keep native layers scoped to this function so their destructors run before QGIS exits.
    layers = [
        QgsRasterLayer(path, name)
        for path, name in [(args.first, "A"), (args.second, "B")]
    ]
    a, b = layers
    if not all(l.isValid() for l in layers):
        raise ValueError("Unreadable raster")
    if (a.extent(), a.crs(), a.width(), a.height()) != (
        b.extent(),
        b.crs(),
        b.width(),
        b.height(),
    ):
        raise ValueError("Reference requires aligned full-scene inputs")
    entries = []
    expressions = []
    for layer in layers:
        entry = QgsRasterCalculatorEntry()
        entry.ref = layer.name() + "@1"
        entry.raster = layer
        entry.bandNumber = 1
        entries.append(entry)
        expressions.append(
            "(" + " OR ".join(f'("{entry.ref}" = {c})' for c in (4, 5, 6)) + ")"
        )
    calc = QgsRasterCalculator(
        " AND ".join(expressions),
        args.output,
        "GTiff",
        a.extent(),
        a.crs(),
        a.width(),
        a.height(),
        entries,
        QgsProject.instance().transformContext(),
    )
    if calc.processCalculation() != 0:
        raise RuntimeError(calc.lastError())


if __name__ == "__main__":
    main()
