"""
Conector Supabase para el motor de pronóstico.

Funciones públicas:
    get_client()          — crea y retorna instancia autenticada de Client.
    health_check(client)  — valida conectividad. Retorna True o lanza ERR_CONN_001.
    paginate_query(...)   — recupera todos los registros de una tabla con paginación.
"""

import os
from pathlib import Path

import yaml
from supabase import Client, create_client

# Carga config.yaml una sola vez al importar el módulo
_CONFIG_PATH = Path(__file__).parent.parent.parent / "config.yaml"
with open(_CONFIG_PATH, "r", encoding="utf-8") as _f:
    _CONFIG = yaml.safe_load(_f)

_TABLE_VENTAS: str = _CONFIG["database"]["supabase"]["tables"]["ventas"]


def get_client() -> Client:
    """
    Crea y retorna un cliente Supabase autenticado.

    Lee SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY del entorno (nunca hardcoding).

    Returns:
        supabase.Client: instancia lista para consultas.

    Raises:
        KeyError: si alguna variable de entorno requerida no está definida.
    """
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


def health_check(client: Client) -> bool:
    """
    Valida que el cliente puede conectarse a Supabase ejecutando una query mínima.

    Args:
        client: instancia de supabase.Client.

    Returns:
        True si la conexión responde correctamente.

    Raises:
        Exception: con código ERR_CONN_001 si la conexión falla por cualquier motivo.
    """
    try:
        client.table(_TABLE_VENTAS).select("id").limit(1).execute()
        return True
    except Exception as exc:
        raise Exception(f"ERR_CONN_001: conexión a Supabase fallida — {exc}") from exc


def paginate_query(
    client: Client,
    table: str,
    columns: str = "*",
    filters: dict | None = None,
) -> list:
    """
    Recupera todos los registros de una tabla usando paginación de 1.000 en 1.000.

    Itera con .range(offset, offset+999) en orden fecha ASC hasta respuesta vacía.
    Consolida y retorna la lista completa.

    Args:
        client:  instancia de supabase.Client.
        table:   nombre de la tabla en Supabase.
        columns: columnas a recuperar (default "*").
        filters: dict opcional de filtros {columna: valor}.

    Returns:
        list: todos los registros de la tabla (puede ser vacía).
    """
    PAGE_SIZE = 1000
    all_rows: list = []
    offset = 0

    while True:
        query = (
            client.table(table)
            .select(columns)
            .order("fecha", desc=False)
            .range(offset, offset + PAGE_SIZE - 1)
        )

        if filters:
            for column, value in filters.items():
                query = query.eq(column, value)

        response = query.execute()
        page = response.data

        if not page:
            break

        all_rows.extend(page)

        if len(page) < PAGE_SIZE:
            break

        offset += PAGE_SIZE

    return all_rows
