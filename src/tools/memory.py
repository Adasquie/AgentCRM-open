import json, os

memory_file = "memory.json"
MAX_INTERACTIONS = 20

def load_memory() -> dict:
    if os.path.exists(memory_file):
        with open(memory_file) as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    return {"interactions": []}

def save_memory(data: dict):
    with open(memory_file, "w") as f:
        json.dump(data, f, indent=2)

def add_interaction(content: str, role: str = "user"):
    data = load_memory()
    interactions = data.get("interactions", [])

    interactions.append({"role": role, "content": content})
    if len(interactions) > MAX_INTERACTIONS:
        interactions = interactions[-MAX_INTERACTIONS:]

    data["interactions"] = interactions
    save_memory(data)

def get_last_interactions(n=20) -> list:
    data = load_memory()
    return data.get("interactions", [])[-n:]

def get_history_text(n=10) -> str:
    interactions = get_last_interactions(n)
    return "\n".join(
        f"{msg['role']}: {msg['content']}" 
        for msg in interactions 
        if isinstance(msg, dict) and 'role' in msg and 'content' in msg
    )

def clear_memory():
    save_memory({"interactions": []})