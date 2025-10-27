# CI Pipeline Python Demo

Proyecto mínimo en Python diseñado para demostrar un pipeline multibranch en Jenkins.

## Características

- Aplicación de ejemplo (`app/calculator.py`).
- Pruebas unitarias con `pytest`.
- Análisis de calidad con `flake8`.
- Despliegue simulado en `C:\deploy\python_ci_app`.

## Requisitos locales

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
flake8 app tests
```