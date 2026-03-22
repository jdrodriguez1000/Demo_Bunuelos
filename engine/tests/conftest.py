"""
Configuración global de pytest para el engine.

Carga las variables de entorno desde .env antes de ejecutar cualquier test,
ya que pytest no carga .env automáticamente.
"""

from pathlib import Path

from dotenv import load_dotenv

# Raíz del proyecto (dos niveles arriba de engine/tests/)
ROOT = Path(__file__).parent.parent.parent
load_dotenv(ROOT / ".env")
