from log_writer import collection
from pymongo.errors import PyMongoError
from tabulate import tabulate
from datetime import datetime, timedelta


def get_raw_logs(limit=5):
    try:
        pipeline = [
            {"$sort": {"timestamp": -1}},
            {"$limit": limit}
        ]
        results = list(collection.aggregate(pipeline))
        if results:
            table = []
            for log in results:
                timestamp = log.get("timestamp")
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S") if isinstance(timestamp, datetime) else str(timestamp)

                search_type = log.get("search_type", "")
                params = log.get("params", {})

                # Удалить offset из параметров при отображении
                params_display = {k: v for k, v in params.items() if k != "offset"}
                params_str = ", ".join(f"{k}: {v}" for k, v in params_display.items())

                results_count = log.get("results_count", 0)

                table.append([timestamp_str, search_type, params_str, results_count])

            headers = ["Date & time", "Request type", "Options", "Result"]
            print("\nRecent queries:")
            print(tabulate(table, headers=headers, tablefmt="grid", stralign="left"))
        else:
            print("No logs to display.")
    except PyMongoError as e:
        print(f"[MongoDB] Error while fetching logs: {e}")


def get_grouped_logs(limit=5):
    try:
        pipeline = [
            {"$sort": {"timestamp": -1}}
        ]
        logs = list(collection.aggregate(pipeline))

        if not logs:
            print("No logs to display.")
            return

        grouped = {}
        for log in logs:
            search_type = log.get("search_type")
            params = log.get("params", {})
            results_count = log.get("results_count", 0)
            timestamp = log.get("timestamp")

            params_without_offset = {k: v for k, v in params.items() if k != "offset"}

            # Группировка по типу и параметрам 
            group_key = (search_type, frozenset(params_without_offset.items()))

            if group_key in grouped:
                grouped[group_key]["results_count"] += results_count
                if timestamp > grouped[group_key]["timestamp"]:
                    grouped[group_key]["timestamp"] = timestamp
            else:
                grouped[group_key] = {
                    "search_type": search_type,
                    "params": params_without_offset,
                    "results_count": results_count,
                    "timestamp": timestamp
                }


        sorted_logs = sorted(grouped.values(), key=lambda x: x["timestamp"], reverse=True)[:limit]

        table = []
        for log in sorted_logs:
            timestamp_str = log["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(log["timestamp"], datetime) else str(log["timestamp"])
            search_type = log["search_type"]

            params_str = ", ".join(f"{k}: {v}" for k, v in log["params"].items())
            results_count = log["results_count"]
            table.append([timestamp_str, search_type, params_str, results_count])

        headers = ["Date & time", "Request type", "Options", "Result (total)"]
        print("\nRecent logical queries: ")
        print(tabulate(table, headers=headers, tablefmt="grid", stralign="left"))

    except PyMongoError as e:
        print(f"[MongoDB] Error while fetching logs:  {e}")



def get_most_frequent_logs(limit=5):
    try:
        pipeline = [
            {"$group": {"_id": "$search_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        results = list(collection.aggregate(pipeline))
        if results:
            table = [[entry["_id"], entry["count"]] for entry in results]
            headers = ["Query type", "Quantity"]
            print("\n Most frequent query:")
            print(tabulate(table, headers=headers, tablefmt="grid", stralign="left"))
        else:
            print("No data to display.")
    except PyMongoError as e:
        print(f"[MongoDB] Error while fetching logs: {e}")


def get_actor_stats():
    print("\n Top 5 actors by number of queries: ")
    pipeline = [
        {"$match": {"search_type": "actor"}},
        {"$group": {"_id": "$params.actor_name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    try:
        results = list(collection.aggregate(pipeline))
        if not results:
            print("No logs for actors.")
            return
        for i, entry in enumerate(results, 1):
            print(f"{i}. {entry['_id']} — {entry['count']} queries")
    except Exception as e:
        print(f"[MongoDB] Error while fetching statistics for actors: {e}")


def get_rating_stats():
    print("\n Statistics by ratings:")
    pipeline = [
        {"$match": {"search_type": "rating_year_range"}},
        {"$group": {"_id": "$params.rating", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    try:
        results = list(collection.aggregate(pipeline))
        if not results:
            print("No logs for rating.")
            return
        for i, entry in enumerate(results, 1):
            print(f"{i}. {entry['_id']} — {entry['count']} queries")
    except Exception as e:
        print(f"[MongoDB] Error while fetching statistics for ratings: {e}")