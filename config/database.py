import os
from pathlib import Path
from typing import Optional

from supabase import Client, create_client
from supabase.lib.client_options import SyncClientOptions

_client_instance: Optional[Client] = None
_initialized: bool = False


def _load_local_env() -> None:
    """Carrega um arquivo .env na raiz do projeto sem depender de bibliotecas externas."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_supabase_client() -> Optional[Client]:
    """
    Retorna o cliente singleton do Supabase configurado por SUPABASE_URL e SUPABASE_KEY.
    Se não configurado, retorna None para permitir execução em modo offline/local.
    """
    global _client_instance, _initialized

    if _initialized:
        return _client_instance

    _load_local_env()
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_KEY", "").strip()

    if url and key:
        try:
            _client_instance = create_client(
                url,
                key,
                SyncClientOptions(persist_session=False),
            )
        except Exception as exc:
            print(f"[Supabase] Falha ao conectar ({exc}). Usando modo local.")
            _client_instance = None
    else:
        print("[Supabase] SUPABASE_URL/SUPABASE_KEY não definidas. Executando em modo local.")
        _client_instance = None

    _initialized = True
    return _client_instance