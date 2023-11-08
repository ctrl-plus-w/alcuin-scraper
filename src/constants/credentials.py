from dotenv import load_dotenv

import os

load_dotenv()

USERNAME = os.getenv("ALCUIN_USERNAME")
PASSWORD = os.getenv("ALCUIN_PASSWORD")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SERVICE_ROLE_KEY")

assert USERNAME != "" and USERNAME != None, "Missing ALCUIN_USERNAME env variable"
assert PASSWORD != "" and PASSWORD != None, "Missing ALCUIN_PASSWORD env variable"
assert (
    SERVICE_ROLE_KEY != "" and SERVICE_ROLE_KEY != None
), "Missing SERVICE_ROLE_KEY env variable"
