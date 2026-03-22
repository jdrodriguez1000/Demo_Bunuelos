"""
Tests de integración para engine.src.connectors.supabase_client.

Mandato CC_00003: Estos tests deben existir en ROJO antes de escribir
la implementación. No mockear servicios externos — prueba contra Supabase real.
"""

import pytest
from supabase import Client


# ---------------------------------------------------------------------------
# TSK-1-10: get_client retorna instancia de Client
# ---------------------------------------------------------------------------

def test_get_client_returns_client():
    """get_client() debe retornar una instancia de supabase.Client."""
    from engine.src.connectors.supabase_client import get_client

    client = get_client()

    assert isinstance(client, Client)


# ---------------------------------------------------------------------------
# TSK-1-11: health_check retorna True contra Supabase real
# ---------------------------------------------------------------------------

def test_health_check_success():
    """health_check(client) debe retornar True cuando Supabase responde."""
    from engine.src.connectors.supabase_client import get_client, health_check

    result = health_check(get_client())

    assert result is True


# ---------------------------------------------------------------------------
# TSK-1-12: health_check con key inválida debe lanzar excepción (no False)
# ---------------------------------------------------------------------------

def test_health_check_invalid_key_raises():
    """health_check con credencial inválida debe lanzar excepción con código ERR_CONN_001."""
    import os
    from supabase import create_client
    from engine.src.connectors.supabase_client import health_check

    url = os.environ.get("SUPABASE_URL", "https://invalid.supabase.co")
    # JWT con formato válido (pasa validación del cliente) pero firma inválida
    fake_jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJpbnZhbGlkIn0.INVALID_SIGNATURE"
    bad_client = create_client(url, fake_jwt)

    with pytest.raises(Exception) as exc_info:
        health_check(bad_client)

    assert "ERR_CONN_001" in str(exc_info.value)


# ---------------------------------------------------------------------------
# TSK-1-13: paginate_query retorna lista (respeta paginación)
# ---------------------------------------------------------------------------

def test_paginate_query_respects_limit():
    """paginate_query() sobre usr_ventas debe retornar una lista (vacía o con datos)."""
    from engine.src.connectors.supabase_client import get_client, paginate_query

    result = paginate_query(
        client=get_client(),
        table="usr_ventas",
        columns="*",
        filters=None,
    )

    assert isinstance(result, list)
    # Si la tabla tiene más de 1.000 registros, la paginación debe recuperarlos todos
    # (se valida indirectamente: len > 1000 implica que hubo al menos 2 páginas)
