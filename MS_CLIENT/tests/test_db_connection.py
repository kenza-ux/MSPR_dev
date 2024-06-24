from sqlalchemy import create_engine, text
from MS_CLIENT.config import Config

def test_connection():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    try:
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1')).fetchone()
            if result:
                print("Direct database connection successful")
            else:
                print("Failed to execute test query")
    except Exception as e:
        print(f"Failed direct database connection: {e}")

if __name__ == "__main__":
    test_connection()
