import psycopg2
import logging

class PostgresWarehouse:
    def __init__(self):
        # Using Port 5433 to avoid local conflicts
        self.conn_params = {
            "host": '127.0.0.1',
            "port": 5433,
            "database": 'nz_supply_chain',
            "user": 'postgres',
            "password": 'postgres'
        }
        # This calls the hidden method below to set up DB automatically
        self._ensure_bronze_table_exists() 

    def _ensure_bronze_table_exists(self):
        """The Automation: Creates the table if it's not already there."""
        setup_query = """
        CREATE TABLE IF NOT EXISTS public.nzta_events_raw (
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_id INT,
            event_type TEXT,
            impact_score FLOAT,
            location TEXT,
            status TEXT
        );
        """
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(setup_query)
                    conn.commit()
        except Exception as e:
            logging.error(f"Automation failed to prepare table: {e}")

    def insert_bronze_event(self, event):
        """Accepts a validated RoadEvent object and pushes to SQL."""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cur:
                    query = """
                        INSERT INTO public.nzta_events_raw 
                        (event_id, event_type, impact_score, location, status)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cur.execute(query, (
                        event.event_id, 
                        event.event_type, 
                        event.impact_score, 
                        event.location, 
                        event.status
                    ))
                    conn.commit()
        except Exception as e:
            logging.error(f"Database write error: {e}")
            raise