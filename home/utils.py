import requests

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"

def fetch_pokemon(poke_id):
    r = requests.get(f"{POKEAPI_BASE}/{poke_id}/")
    r.raise_for_status()
    data = r.json()

    # build the base_stat map
    stat_map = { s['stat']['name']: s['base_stat'] for s in data['stats'] }
    # pull out a flavor text…
    desc_data = requests.get(data['species']['url']).json()
    desc = next(
        (x['flavor_text'] for x in desc_data['flavor_text_entries']
         if x['language']['name']=='en'),
        ""
    ).replace("\n"," ")

    return {
        'poke_id':     data['id'],
        'name':        data['name'].capitalize(),
        'sprite':      data['sprites']['front_default'],
        'types':       [t['type']['name'].capitalize() for t in data['types']],
        'description': desc,
        # now include each stat explicitly:
        'hp':           stat_map.get('hp', 0),
        'attack':       stat_map.get('attack', 0),
        'defense':      stat_map.get('defense', 0),
        'sp_attack':    stat_map.get('special-attack', 0),
        'sp_defense':   stat_map.get('special-defense', 0),
        'speed':        stat_map.get('speed', 0),
    }