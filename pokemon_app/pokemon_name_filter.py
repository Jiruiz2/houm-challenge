import requests
from .constants import POKEMON_API_URL, POKEMON_LIST_ENDPOINT


def pokemons_list():
    response = requests.get(f'{POKEMON_API_URL}{POKEMON_LIST_ENDPOINT}')
    json_response = response.json()
    return json_response.get('results')


def count_pokemons_with_at_and_double_a():
    pokemon_count = 0
    for pokemon in pokemons_list():
        pokemon_name = pokemon.get('name')
        if pokemon_name.count('at') >= 1 and pokemon_name.count('a') == 2:
            pokemon_count += 1
    return pokemon_count
