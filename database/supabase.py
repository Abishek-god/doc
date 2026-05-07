import os

from supabase import Client, create_client


_client: Client | None = None


def get_supabase_client() -> Client | None:
    global _client
    if _client:
        return _client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None

    _client = create_client(url, key)
    return _client
