from dotenv import load_dotenv
import os

load_dotenv()
STORAGE_CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING")
SECRET_KEY = os.getenv("SECRET_KEY")
CONTAINER_NAME = "container01"
