import requests

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"

def fetch_pokemon(poke_id):
    url = f"{POKEAPI_BASE}/{poke_id}/"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    # pull out a short flavor text too…
    desc_url  = data['species']['url']
    desc_data = requests.get(desc_url).json()
    desc = next(
        (x['flavor_text'] for x in desc_data['flavor_text_entries']
         if x['language']['name']=='en'),
        ""
    ).replace("\n"," ").replace("\f"," ")

    # build a map of stat_name -> base_stat
    stat_map = {
        s_block['stat']['name']: s_block['base_stat']
        for s_block in data['stats']
    }

    return {
        'poke_id':       data['id'],
        'name':          data['name'].capitalize(),
        'sprite':        data['sprites']['front_default'],
        'types':         [t['type']['name'].capitalize() for t in data['types']],
        'description':   desc,
        'stats':         data['stats'],               # ← leave this for admin
        'health':        stat_map.get('hp', 0),
        'attack':        stat_map.get('attack', 0),
        'defense':       stat_map.get('defense', 0),
        'special_attack':  stat_map.get('special-attack', 0),
        'special_defense': stat_map.get('special-defense', 0),
        'speed':         stat_map.get('speed', 0),
    }