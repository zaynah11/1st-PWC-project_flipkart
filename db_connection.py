from dotenv import load_dotenv
import os

load_dotenv()  # this loads variables from .env into os.environ

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")  # don't forget to encode this later
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

print(f"Loaded username: {username}")  # Add this to debug

# If password or username is None, connection string will fail!
from urllib.parse import quote_plus
from sqlalchemy import create_engine

password_encoded = quote_plus(password)

connection_url = (
    f"postgresql+psycopg2://{username}:{password_encoded}@{host}:{port}/{database}"
)

engine = create_engine(connection_url, connect_args={"sslmode": "require"})