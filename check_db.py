from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Connect to the exact same database file
engine = create_engine("sqlite:///./recycling.db")
Session = sessionmaker(bind=engine)
session = Session()

print("--- CHECKING DATABASE ---")

try:
    result = session.execute(text("SELECT * FROM companies"))
    rows = result.fetchall()

    if not rows:
        print("The table is empty.")
    else:
        for row in rows:
            print(f"Found Company: {row}")

except Exception as e:
    print(f"Error: {e}")
    print("Does the table 'companies' exist?")

session.close()