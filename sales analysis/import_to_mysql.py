import pandas as pd
from sqlalchemy import create_engine, URL, String
from getpass import getpass

# MySQL credentials
password = getpass("Enter MySQL password: ")

# Connect to MySQL
url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password=password,
    host="localhost",
    database="sales_analysis"
)

engine = create_engine(url)

# Load CSV
df = pd.read_csv("sales_clean.csv")

# Keep date columns as text for now
df["Order Date"] = df["Order Date"].astype(str)
df["Ship Date"] = df["Ship Date"].astype(str)

# Import into MySQL
df.to_sql(
    name="superstore",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000
)

print("Import completed!")
print("Total rows:", len(df))

engine.dispose()