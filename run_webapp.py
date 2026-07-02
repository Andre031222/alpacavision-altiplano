"""
AlpacaVision AI -- Servidor web principal.

Uso:
    venv/Scripts/python.exe run_webapp.py
    Abre: http://localhost:5050
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.webapp import create_app

app = create_app("development")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
