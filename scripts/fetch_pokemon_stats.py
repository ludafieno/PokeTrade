import requests
from home.models import Pokemon

def fetch_and_update_stats():
    for p in Pokemon.objects.all():
        url = f"https://pokeapi.co/api/v2/pokemon/{p.name.lower()}/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # 👇 Step 2: Extract stats
            stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
            p.health = stats.get("hp", 0)
            p.attack = stats.get("attack", 0)
            p.defense = stats.get("defense", 0)
            p.special_attack = stats.get("special-attack", 0)
            p.special_defense = stats.get("special-defense", 0)
            p.speed = stats.get("speed", 0)

            # ✅ Step 2: Extract types
            types = [t["type"]["name"].capitalize() for t in data["types"]]
            p.types = types

            p.save()
            print(f"✅ Updated stats and types for {p.name}")
        else:
            print(f"❌ Failed to fetch stats for {p.name} (poke_id={p.poke_id})")
