from db_connection import engine
import pandas as pd

with engine.connect() as conn:
    print("CONNECTED 🎉")

df = pd.read_sql(
    "SELECT * FROM flipkart_products LIMIT 10;",
    engine
)

print(df)