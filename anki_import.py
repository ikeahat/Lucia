import json
import requests
import sys
from pathlib import Path

ANKI_CONNECT_URL = "http://localhost:8765"

DEFAULT_DECK = "Auto Imported Deck"

DEFAULT_JSON = "cards.json"

def read_json(path):
    p = Path(path)
    if not p.exists():
        print(f"Error: {path} does not exist.")
        sys.exit(1)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def add_ankis(deck_name, ankis):
    payload = {
        "action": "addNotes",
        "version": 6,
        
        "params": {
            "notes": [
            ]
        }
    }

    for n in ankis:
        tags = n.get("tags", [])

        anki = {
            "deckName": deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": n["front"],
                "Back": n["back"]
            },
        "options": {"allowDuplicate": True},
        "tags": tags
        }
        payload["params"]["notes"].append(anki)

    try: 
        r = requests.post(ANKI_CONNECT_URL, json=payload)
        r.raise_for_status()
        result = r.json()
        print("AnkiConnect response:", result)
    except requests.exceptions.RequestException as e:
        print("Network or AnkiConnect Error:", e)
        sys.exit(1)
    
def main():
    json_file = "cards.json"

    if len(sys.argv) >= 2:
        deck = sys.argv[1]
    else:
        deck = DEFAULT_DECK

    ankis = read_json(Path(json_file))
    if not isinstance(ankis, list):
        print("Error: JSON not a list of card objects")
        sys.exit(1)

    for i, card in enumerate(ankis):
        if "front" not in card or "back" not in card:
            print(f"""Error: card at index {1} is missing "front" or "back".""")
            sys.exit(1)

    add_ankis(deck, ankis)

if __name__ == "__main__":
    main()