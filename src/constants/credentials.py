from dotenv import load_dotenv

import os

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

assert USERNAME != "" and USERNAME != None, "Missing USERNAME env variable"
assert PASSWORD != "" and PASSWORD != None, "Missing PASSWORD env variable"
