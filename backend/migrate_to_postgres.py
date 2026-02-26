import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)
load_dotenv()

SQLITE_DB = os.getenv('DATABASE_PATH', 'parsehub.db')
POSTGRES_URL = os.getenv('DATABASE_URL')

if not POSTGRES_URL:
    print("❌ Error: DATABASE_URL not found in environment.")
    exit(1)

# Ensure absolute path for SQLite
if not os.path.isabs(SQLITE_DB):
    SQLITE_DB = str(Path(__file__).parent / SQLITE_DB)

print(f"🔄 Starting Migration...")
print(f"📂 Source (SQLite): {SQLITE_DB}")
print(f"🌐 Target (Postgres): {POSTGRES_URL.split('@')[-1]}")

def migrate():
    try:
        # Connect to databases
        sqlite_conn = sqlite3.connect(SQLITE_DB)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()

        pg_conn = psycopg2.connect(POSTGRES_URL)
        pg_conn.autocommit = True
        pg_cursor = pg_conn.cursor()

        # Define tables in order of migration (parent tables first)
        tables = [
            'projects',
            'import_batches',
            'metadata',
            'project_metadata',
            'runs',
            'scraped_data',
            'metrics',
            'recovery_operations',
            'data_lineage',
            'run_checkpoints',
            'monitoring_sessions',
            'scraped_records',
            'analytics_cache',
            'csv_exports',
            'analytics_records',
            'scraping_sessions',
            'iteration_runs',
            'combined_scraped_data',
            'url_patterns',
            'product_data'
        ]

        for table in tables:
            print(f"--- Migrating table: {table} ---")
            
            # Check if table exists in SQLite
            sqlite_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not sqlite_cursor.fetchone():
                print(f"⚠️  Table {table} does not exist in SQLite skipping...")
                continue

            # Fetch data from SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"ℹ️  Table {table} is empty.")
                continue

            print(f"📦 Found {len(rows)} records. Transferring...")

            # Prepare Postgres column names
            columns = rows[0].keys()
            col_names = ",".join(columns)
            placeholders = ",".join(["%s"] * len(columns))
            
            # Prepare data
            data = [tuple(row) for row in rows]

            # Clear existing data in Postgres to avoid duplicates (optional, but safer for re-runs)
            pg_cursor.execute(f"TRUNCATE TABLE {table} CASCADE")

            # Insert into Postgres
            query = f"INSERT INTO {table} ({col_names}) VALUES %s"
            execute_values(pg_cursor, query, data)
            
            # Update sequences for SERIAL columns
            pg_cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='{table}' AND column_name='id')")
            if pg_cursor.fetchone()[0]:
                pg_cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE(MAX(id), 1)) FROM {table}")

            print(f"✅ Table {table} migrated successfully.")

        print("\n🎉 Migration Complete!")
        
        sqlite_conn.close()
        pg_conn.close()

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate()
