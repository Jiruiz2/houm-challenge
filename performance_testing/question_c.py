import requests
import time
import concurrent.futures
import functools


CONNECTIONS = 100
POKEMON_API_URL = 'https://pokeapi.co/api/v2'


def get_type_pokemon_urls(pokemon_type):
    response = requests.get(f'{POKEMON_API_URL}/type/{pokemon_type}/')
    json_response = response.json()
    type_pokemons = json_response.get('pokemon')
    return [pokemon.get('pokemon').get('url') for pokemon in type_pokemons]


def get_weight_from_url(url):
    return requests.get(url).json().get('weight')


def get_type_pokemons_weight_bounds_v1(pokemon_type):
    pokemon_urls = get_type_pokemon_urls(pokemon_type)
    pokemon_weights = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(get_weight_from_url, url) for url in pokemon_urls)
        for future in concurrent.futures.as_completed(future_to_url):
            weight = future.result()
            pokemon_weights.append(weight)
    return [max(pokemon_weights), min(pokemon_weights)]


def get_type_pokemons_weight_bounds_v2(pokemon_type):
    pokemon_urls = get_type_pokemon_urls(pokemon_type)
    min_weight = 9999999999999999999999999999999999999999999999
    max_weight = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(get_weight_from_url, url) for url in pokemon_urls)
        for future in concurrent.futures.as_completed(future_to_url):
            weight = future.result()
            if weight > max_weight:
                max_weight = weight
            if weight < min_weight:
                min_weight = weight
    return [max_weight, min_weight]


def update_weght_bounds(weight_bounds, response):
    if not isinstance(weight_bounds, list):
        weight = weight_bounds.result()
        weight_bounds = [weight, weight]
    weight = response.result()
    if weight > weight_bounds[0]:
        weight_bounds[0] = weight
    if weight < weight_bounds[1]:
        weight_bounds[1] = weight
    return weight_bounds


def get_type_pokemons_weight_bounds_v3(pokemon_type):
    pokemon_urls = get_type_pokemon_urls(pokemon_type)
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(get_weight_from_url, url) for url in pokemon_urls)
        return functools.reduce(
            lambda weight_bounds, weight: update_weght_bounds(weight_bounds, weight),
            concurrent.futures.as_completed(future_to_url)
        )


weight_function_versions = [
    get_type_pokemons_weight_bounds_v1,
    get_type_pokemons_weight_bounds_v2,
    get_type_pokemons_weight_bounds_v3,
]
for weight_version in weight_function_versions:
    times = []
    for _ in range(50):
        t1 = time.time()
        resp = weight_version('fighting')
        times.append(time.time() - t1)
    print(f'{weight_version.__name__}: Se demoró {sum(times)/len(times)} segundos')
