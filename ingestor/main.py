import json
import logging
from models import RoadEvent
from warehouse import PostgresWarehouse
from pydantic import ValidationError

# Setup logging to our Masterplan folder
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="logs/ingestor.log"
)

def run_pipeline():
    db = PostgresWarehouse()
    
    # Load our "Big Messy Data"
    try:
        with open('ingestor/mock_nzta_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: mock_nzta_data.json not found.")
        return

    print("--- Starting NZ Supply Chain Ingestion ---")
    
    for raw_row in data:
        try:
            # Step 1: Validate with Pydantic
            event = RoadEvent(**raw_row)
            
            # Step 2: Write to Warehouse
            db.insert_bronze_event(event)
            print(f"✅ Success: Event {event.event_id} loaded to Bronze.")
            
        except ValidationError as e:
            # Logs the specific Pydantic error details
            logging.warning(f"❌ Validation failed for Row {raw_row.get('event_id')}: {e.errors()}")
            print(f"❌ Rejected: Event {raw_row.get('event_id')} (Check logs for details)")
        except Exception as e:
            print(f"⚠️ System Error: {e}")

if __name__ == "__main__":
    run_pipeline()