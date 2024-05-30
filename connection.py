import os
import psycopg2
from psycopg2 import OperationalError


def get_connection():
    try:
        # Database connection parameters
        db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST', 'postgres'),  # Read host from environment variable
            'port': 5432 # Default PostgreSQL port
        }

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Verify the connection
        if conn is None or cur is None:
            print("Connection or cursor is None.")
            return None, None

        #Executing an MYSQL function using the execute() method
        cur.execute("select version()")

        # Fetch a single row using fetchone() method.
        data = cur.fetchone()
        print("Connection established to: ",data)

        # Create schema if it doesn't exist
        cur.execute("CREATE SCHEMA IF NOT EXISTS \"EVN\"")

        # Create sequence and table within the schema if they don't exist
        setup_sequence = """
        DROP SEQUENCE IF EXISTS "EVN"."EVENT_MASTER_EventID_seq" CASCADE;

        CREATE SEQUENCE IF NOT EXISTS "EVN"."EVENT_MASTER_EventID_seq"
        INCREMENT 1
        START 1
        MINVALUE 1
        MAXVALUE 9223372036854775807
        CACHE 1;
        """
        
        setup_table = """
        DROP TABLE IF EXISTS "EVN"."EVENT_MASTER";
        
        CREATE TABLE IF NOT EXISTS "EVN"."EVENT_MASTER"
        (
            "EventID" integer NOT NULL DEFAULT nextval('"EVN"."EVENT_MASTER_EventID_seq"'::regclass),
            "EventName" text COLLATE pg_catalog."default" NOT NULL,
            "EventDateTime" timestamp without time zone NOT NULL,
            "EventLocation" text COLLATE pg_catalog."default" NOT NULL,
            "EventArtists" text COLLATE pg_catalog."default",
            "EventImageURL" text COLLATE pg_catalog."default",
            CONSTRAINT "EVENT_MASTER_pkey" PRIMARY KEY ("EventName", "EventLocation", "EventDateTime")
        )
        TABLESPACE pg_default;
        """
        
        cur.execute(setup_sequence)
        cur.execute(setup_table)

        # Optionally, add the owner and comment
        cur.execute("""
        ALTER TABLE IF EXISTS "EVN"."EVENT_MASTER"
        OWNER TO postgres;
        
        COMMENT ON TABLE "EVN"."EVENT_MASTER"
        IS 'Event Details';
        """)

        conn.commit()

        return conn, cur

    except OperationalError as e:
        print(f"dbConnect Error: {e}")
        return None, None

def close_connection(conn, cur):
    """Function to close Database Connection"""
    try:
        # Committing all the unsaved transactions in the database
        cur.commit()
        # Closing both Cursor and Connection objects
        conn.close()
    
    except Exception as e:
        print(f"dbClose Error: {e}")
        exit()