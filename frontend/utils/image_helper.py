# utils/image_helpers.py

def make_entries_from_image_results(results: list):
    return [{"id": r["id"], "distance": r["distance"]} for r in results]

def merge_records_with_distances(records: list, entries: list):
    id_to_distance = {e["id"]: e["distance"] for e in entries}
    for record in records:
        record["distance"] = id_to_distance.get(record["id"], float("inf"))
    return sorted(records, key=lambda x: x["distance"])
