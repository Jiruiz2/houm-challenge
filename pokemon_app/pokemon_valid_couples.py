from .constants import CONNECTIONS, POKEMON_API_URL
import requests
import concurrent.futures


def egg_groups_urls(pokemon_name):
    response = requests.get(f'{POKEMON_API_URL}/pokemon-species/{pokemon_name}/')
    json_response = response.json()
    egg_groups = json_response.get('egg_groups')
    return [egg_group.get('url') for egg_group in egg_groups]


def egg_group_pokemon_names(url):
    response = requests.get(url)
    json_response = response.json()
    pokemon_species = json_response.get('pokemon_species')
    return [pokemon.get('name') for pokemon in pokemon_species]


def pokemon_valid_couples_count(pokemon_name):
    pokemon_valid_couples = []
    pokemon_egg_groups_url = egg_groups_urls(pokemon_name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_requests = (
            executor.submit(egg_group_pokemon_names, url)
            for url in pokemon_egg_groups_url
        )
        for request in concurrent.futures.as_completed(future_requests):
            pokemon_valid_couples += request.result()
    return len(set(pokemon_valid_couples))
