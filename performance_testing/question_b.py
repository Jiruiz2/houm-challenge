import requests
import time
import concurrent.futures


CONNECTIONS = 100
POKEMON_API_URL = 'https://pokeapi.co/api/v2'


def get_egg_groups_urls(pokemon_name):
    response = requests.get(f'{POKEMON_API_URL}/pokemon-species/{pokemon_name}/')
    json_response = response.json()
    egg_groups = json_response.get('egg_groups')
    return [egg_group.get('url') for egg_group in egg_groups]


def get_egg_group_pokemon_names(url):
    response = requests.get(url)
    json_response = response.json()
    pokemon_species = json_response.get('pokemon_species')
    return [pokemon.get('name') for pokemon in pokemon_species]


def get_pokemon_valid_couples_v1(pokemon_name):
    raichu_valid_couples = []
    raichu_egg_groups_url = get_egg_groups_urls(pokemon_name)
    for url in raichu_egg_groups_url:
        raichu_valid_couples += get_egg_group_pokemon_names(url)
    return len(set(raichu_valid_couples))


def get_pokemon_valid_couples_v2(pokemon_name):
    raichu_valid_couples = []
    raichu_egg_groups_url = get_egg_groups_urls(pokemon_name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = (executor.submit(get_egg_group_pokemon_names, url)
                         for url in raichu_egg_groups_url)
        for future in concurrent.futures.as_completed(future_to_url):
            raichu_valid_couples += future.result()
    return len(set(raichu_valid_couples))


couples_function_versions = [
    get_pokemon_valid_couples_v1,
    get_pokemon_valid_couples_v2
]
for couples_version in couples_function_versions:
    times = []
    for _ in range(50):
        t1 = time.time()
        couples_version('raichu')
        times.append(time.time() - t1)

    print(f'{couples_version.__name__}: Se demoró {sum(times)/len(times)} segundos')
