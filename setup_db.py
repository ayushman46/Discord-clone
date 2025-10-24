import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass
import sys

def setup_database():
    # Get current user as default PostgreSQL user on macOS
    current_user = getpass.getuser()
    
    try:
        # Connect to PostgreSQL server
        print(f"Attempting to connect as user '{current_user}'...")
        conn = psycopg2.connect(
            dbname='postgres',
            user=current_user,  # Use current macOS username
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'discord_clone'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE discord_clone')
            print("Database 'discord_clone' created successfully!")
        else:
            print("Database 'discord_clone' already exists.")
            
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print("\nError: Could not connect to PostgreSQL server.")
        print("Please ensure that:")
        print("1. PostgreSQL is installed and running")
        print("2. Your user has the necessary permissions")
        print(f"\nDetailed error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
