import requests

POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon"

def fetch_pokemon(poke_id):
    response = requests.get(f"{POKEAPI_BASE}/{poke_id}")
    response.raise_for_status()
    data = response.json()

    species = requests.get(data['species']['url']).json()
    desc = next(
        (entry['flavor_text'].replace('\n', ' ')
         for entry in species['flavor_text_entries']
         if entry['language']['name'] == 'en'),
        ""
    )

    return {
        'poke_id':     data['id'],
        'name':        data['name'].capitalize(),
        'sprite':      data['sprites']['front_default'],
        'types':       [t['type']['name'].capitalize() for t in data['types']],
        'description': desc,
        'health':      data['stats'][0]['base_stat'],  # HP stat
    }
