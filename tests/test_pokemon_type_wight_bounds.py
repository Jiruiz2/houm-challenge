import responses
from pokemon_app.constants import POKEMON_API_URL
from pokemon_app.pokemon_type_weight_bounds import pokemon_type_weight_bounds


@responses.activate
def test_pokemon_type_weight_bounds():
    pokemon_type = 'fighting'
    pokemons_from_type = {
        'pokemon':
        [
            {'pokemon': {'url': f'{POKEMON_API_URL}/torchic'}},
            {'pokemon': {'url': f'{POKEMON_API_URL}/treecko'}},
            {'pokemon': {'url': f'{POKEMON_API_URL}/mudkip'}}
        ]
    }

    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}/type/{pokemon_type}/',
        json=pokemons_from_type,
        status=200
    )

    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}/torchic',
        json={'weight': 100},
        status=200
    )

    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}/treecko',
        json={'weight': 10},
        status=200
    )

    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}/mudkip',
        json={'weight': 1000},
        status=200
    )

    weight_bounds = pokemon_type_weight_bounds(pokemon_type)

    assert weight_bounds == [1000, 10]
