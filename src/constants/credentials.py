from dotenv import load_dotenv

import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
GH_TOKEN = os.getenv("GH_TOKEN")
GH_REPO = os.getenv("GH_REPO")

assert USERNAME != "" and USERNAME != None, "Missing USERNAME env variable"
assert PASSWORD != "" and PASSWORD != None, "Missing PASSWORD env variable"
assert GH_TOKEN != "" and GH_TOKEN != None, "Missing GH_TOKEN env variable"
assert GH_REPO != "" and GH_REPO != None, "Missing GH_REPO env variable"
