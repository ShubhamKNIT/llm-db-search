# utils/image_helpers.py

def make_entries_from_image_results(results: list) -> dict:
    entries = {}
    for result in results:
        category = result.get("category", "unknown")
        if category not in entries:
            entries[category] = []
        entry = {
            "id": result["id"],
            "distance": result["distance"]
        }
        entries[category].append(entry)
    print("🔗 Entries created from image results:", entries)  # Debugging line
    return entries

def merge_records_with_distances(records: list, entries: dict) -> list:
    # print("🔗 Merging records with distances:", records)  # Debugging line
    # print("🔗 Entries for merging:", entries)  # Debugging line
    merged = []

    # Step 1: Flatten entries into a map {id: distance}
    id_to_distance = {}
    for category_entries in entries.values():
        for entry in category_entries:
            id_to_distance[entry["id"]] = entry["distance"]

    # Step 2: Attach distance to matching records
    for record in records:
        record_id = record.get("id")
        if record_id in id_to_distance:
            record["distance"] = id_to_distance[record_id]
            merged.append(record)

    # Step 3: Sort by distance
    merged.sort(key=lambda x: x["distance"])
    print("🔗 Merged records with distances:", merged)
    return merged

