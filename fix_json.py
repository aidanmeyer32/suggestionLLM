import json

# Load the JSON file
file_path = "embeddings_with_metadata.json"
output_path = "corrected_embeddings.json"

try:
    with open(file_path, "r") as f:
        data = json.load(f)

    # Ensure data is a list
    if not isinstance(data, list):
        raise ValueError("The JSON file should contain a list of embeddings.")

    id_set = set()
    embedding_dim = None
    fixed_data = []
    errors = []

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"Item at index {idx} is not a dictionary.")
            continue

        # Fix ID
        item_id = item.get("id")
        if not isinstance(item_id, str):
            item_id = f"auto_id_{idx}"  # Generate a fallback ID
            errors.append(f"Missing or invalid 'id' at index {idx}. Assigned {item_id}.")
        if item_id in id_set:
            item_id += f"_{idx}"  # Ensure uniqueness
        id_set.add(item_id)
        item["id"] = item_id

        # Fix Embedding
        embedding = item.get("embedding")
        if not isinstance(embedding, list):
            errors.append(f"Missing or invalid 'embedding' at index {idx}. Skipping entry.")
            continue
        if embedding_dim is None:
            embedding_dim = len(embedding)
        elif len(embedding) != embedding_dim:
            errors.append(
                f"Inconsistent embedding dimension at index {idx}: Expected {embedding_dim}, got {len(embedding)}."
            )
            embedding = embedding[:embedding_dim]  # Trim or extend embeddings
        item["embedding"] = embedding

        # Fix Metadata
        if "metadata" not in item or not isinstance(item["metadata"], dict):
            item["metadata"] = {}
            errors.append(f"Missing or invalid 'metadata' at index {idx}. Assigned empty dict.")

        fixed_data.append(item)

    # Save the corrected JSON
    with open(output_path, "w") as f:
        json.dump(fixed_data, f, indent=4)

    print(f"Fixed JSON saved to {output_path}")
    print(f"Total errors fixed: {len(errors)}")

except json.JSONDecodeError as e:
    print(f"Invalid JSON format: {e}")
except Exception as e:
    print(f"Error: {e}")

