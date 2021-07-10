import responses
from pokemon_app.constants import POKEMON_API_URL, POKEMON_LIST_ENDPOINT
from pokemon_app.pokemon_name_filter import count_pokemons_with_at_and_double_a


@responses.activate
def test_count_pokemons_with_at_and_double_a():
    data = {
        'results':
        [
            {'name': 'ratatta'},
            {'name': 'raticate'},
            {'name': 'raticate-alola'},
            {'name': 'umbreon'},
            {'name': 'atila'},
        ]
    }
    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}{POKEMON_LIST_ENDPOINT}',
        json=data,
        status=200
    )

    pokemon_filter_count = count_pokemons_with_at_and_double_a()

    # only raticate and atila are valid
    assert pokemon_filter_count == 2
