from dotenv import load_dotenv

import os

load_dotenv()

USERNAME = os.getenv("ALCUIN_USERNAME")
PASSWORD = os.getenv("ALCUIN_PASSWORD")
GH_TOKEN = os.getenv("GH_TOKEN")
GH_REPO = os.getenv("GH_REPO")

assert USERNAME != "" and USERNAME != None, "Missing ALCUIN_USERNAME env variable"
assert PASSWORD != "" and PASSWORD != None, "Missing ALCUIN_PASSWORD env variable"
assert GH_TOKEN != "" and GH_TOKEN != None, "Missing GH_TOKEN env variable"
assert GH_REPO != "" and GH_REPO != None, "Missing GH_REPO env variable"
