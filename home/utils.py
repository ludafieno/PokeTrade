import requests

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"

def fetch_pokemon(poke_id):
    url = f"{POKEAPI_BASE}/{poke_id}/"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    # pull out a short flavor text too if you like…
    desc_url = data['species']['url']
    desc_data = requests.get(desc_url)
    desc_data.raise_for_status()
    desc = next(
        (x['flavor_text'] for x in desc_data.json()['flavor_text_entries']
         if x['language']['name']=='en'),
        ""
    ).replace("\n"," ")

    # build a lookup from stat name → base_stat
    stat_map = { s['stat']['name']: s['base_stat'] for s in data['stats'] }

    return {
        'poke_id':        data['id'],
        'name':           data['name'].capitalize(),
        'sprite':         data['sprites']['front_default'],
        'types':          [t['type']['name'].capitalize() for t in data['types']],
        'description':    desc,
        # now include each stat separately:
        'health':         stat_map.get('hp', 0),
        'attack':         stat_map.get('attack', 0),
        'defense':        stat_map.get('defense', 0),
        'special_attack': stat_map.get('special-attack', 0),
        'special_defense':stat_map.get('special-defense', 0),
        'speed':          stat_map.get('speed', 0),
    }