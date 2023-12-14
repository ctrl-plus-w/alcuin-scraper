"""Credenetials constants module"""
import os

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("ALCUIN_USERNAME")
PASSWORD = os.getenv("ALCUIN_PASSWORD")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SERVICE_ROLE_KEY")
RSA_PRIVATE_KEY = os.getenv("RSA_PRIVATE_KEY")

assert USERNAME != "" and USERNAME is not None, "Missing ALCUIN_USERNAME env variable"
assert PASSWORD != "" and PASSWORD is not None, "Missing ALCUIN_PASSWORD env variable"
assert SERVICE_ROLE_KEY != "" and SERVICE_ROLE_KEY is not None, "Missing SERVICE_ROLE_KEY env variable"
assert RSA_PRIVATE_KEY != "" and RSA_PRIVATE_KEY is not None, "Missing RSA_PRIVATE_KEY env variable"

RSA_PRIVATE_KEY = '\n'.join(RSA_PRIVATE_KEY.split('\n'))
