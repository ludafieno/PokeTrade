import requests

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"

def fetch_pokemon(poke_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}/"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()

    # pull out a short flavor text too if you like…
    desc_url = data['species']['url']
    desc_data = requests.get(desc_url).json()
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
        # base_stat list for all stats:
        'stats':       data['stats'],
    }
