import os

from supabase import create_client, Client


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SERVICE_ROLE_KEY")

client: Client = create_client(url, key)
