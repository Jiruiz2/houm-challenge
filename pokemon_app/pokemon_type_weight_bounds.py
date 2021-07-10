from .constants import CONNECTIONS, POKEMON_API_URL
import requests
import concurrent.futures


def type_pokemon_urls(pokemon_type):
    response = requests.get(f'{POKEMON_API_URL}/type/{pokemon_type}/')
    json_response = response.json()
    type_pokemons = json_response.get('pokemon')
    return [pokemon.get('pokemon').get('url') for pokemon in type_pokemons]


def weight_from_url(url):
    json_response = requests.get(url).json()
    return json_response.get('weight')


def pokemon_type_weight_bounds(pokemon_type):
    pokemon_urls = type_pokemon_urls(pokemon_type)
    pokemon_weights = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_requests = (executor.submit(weight_from_url, url) for url in pokemon_urls)
        for request in concurrent.futures.as_completed(future_requests):
            weight = request.result()
            pokemon_weights.append(weight)
    return [max(pokemon_weights), min(pokemon_weights)]
