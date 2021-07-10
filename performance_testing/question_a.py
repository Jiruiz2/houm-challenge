import requests
import time


POKEMON_API_URL = 'https://pokeapi.co/api/v2'
POKEMON_LIST_ENDPOINT = '/pokemon?limit=1118'


def get_pokemon_list():
    response = requests.get(f'{POKEMON_API_URL}{POKEMON_LIST_ENDPOINT}')
    json_response = response.json()
    return json_response.get('results')


def count_pokemon_with_at_and_double_a_v1(pokemon_list):
    pokemon_condition_count = len(list(filter(
        lambda x:
        x.get('name').count('at') >= 1 and x.get('name').count('a') == 2,
        pokemon_list
    )))
    return pokemon_condition_count


def count_pokemon_with_at_and_double_a_v2(pokemon_list):
    pokemon_count = 0
    for pokemon in pokemon_list:
        if pokemon.get('name').count('at') >= 1 and pokemon.get('name').count('a') == 2:
            pokemon_count += 1
    return pokemon_count


def count_pokemon_with_at_and_double_a_v3(pokemon_list):
    pokemon_count = 0
    for pokemon in pokemon_list:
        pokemon_count += int(pokemon.get('name').count('at') >=
                             1 and pokemon.get('name').count('a') == 2)
    return pokemon_count


def count_pokemon_with_at_and_double_a_v4(pokemon_list):
    pokemon_condition_count = [
        int(x.get('name').count('at') >= 1 and x.get('name').count('a') == 2)
        for x in pokemon_list
    ]
    return sum(pokemon_condition_count)


def count_pokemon_with_at_and_double_a_v5(pokemon_list):
    pokemon_condition_count = sum(1 for _ in filter(
        lambda x:
        x.get('name').count('at') >= 1 and x.get('name').count('a') == 2,
        pokemon_list
    ))
    return pokemon_condition_count


def count_pokemon_with_at_and_double_a_v6(pokemon_list):
    pokemon_count = 0
    for pokemon in pokemon_list:
        if pokemon.get('name').count('a') == 2 and pokemon.get('name').count('at') >= 1:
            pokemon_count += 1
    return pokemon_count


count_function_versions = [
    count_pokemon_with_at_and_double_a_v1,
    count_pokemon_with_at_and_double_a_v2,
    count_pokemon_with_at_and_double_a_v3,
    count_pokemon_with_at_and_double_a_v4,
    count_pokemon_with_at_and_double_a_v5,
    count_pokemon_with_at_and_double_a_v6
]
pokemon_data = get_pokemon_list()
for count_version in count_function_versions:
    times = []
    for _ in range(50):
        t1 = time.time()
        count_version(pokemon_data)
        times.append(time.time() - t1)

    print(f'{count_version.__name__}: Se demoró {sum(times)/len(times)} segundos')
