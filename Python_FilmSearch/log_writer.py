from local_settings import MONGODB_URL_WRITE
from pymongo import MongoClient, errors
from datetime import datetime

try:
    client = MongoClient(MONGODB_URL_WRITE, serverSelectionTimeoutMS=3000)
    client.server_info()
    db = client.ich_edit
    group = "final_project_030325"
    full_name = "Vesna_Kostrewa"
    collection_name = f"{group}_{full_name}"
    collection = db[collection_name]
    mongo_available = True
except errors.ServerSelectionTimeoutError as e:
    print(f"[MongoDB] Connection failure: {e}")
    mongo_available = False
except Exception as e:
    print(f"[MongoDB] Unexpected error during connection: {e}")
    mongo_available = False


def log_query(search_type, params, results_count):
    if not mongo_available:
        return 

    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }

    try:
        collection.insert_one(log)
    except Exception as e:
        print(f"[MongoDB] Failed to write log: {e}")

def close():
    global client
    if 'client' in globals() and client:
        client.close()