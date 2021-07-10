import responses
from pokemon_app.constants import POKEMON_API_URL
from pokemon_app.pokemon_valid_couples import pokemon_valid_couples_count


@responses.activate
def test_pokemon_valid_couples_count():
    pokemon_name = 'raichu'
    pokemon_egg_groups = {
        'egg_groups':
        [
            {'url': f'{POKEMON_API_URL}/field'},
            {'url': f'{POKEMON_API_URL}/fairy'},
        ]
    }
    pokemon_species_in_field_egg_group = {
        'pokemon_species': [
            {'name': 'Sandshrew'},
            {'name': 'Ninetales'}
        ]
    }
    pokemon_species_in_fairy_egg_group = {
        'pokemon_species': [
            {'name': 'Clefairy'},
            {'name': 'Ninetales'}
        ]
    }

    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}/pokemon-species/{pokemon_name}/',
        json=pokemon_egg_groups,
        status=200
    )

    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}/field',
        json=pokemon_species_in_field_egg_group,
        status=200
    )

    responses.add(
        responses.GET,
        f'{POKEMON_API_URL}/fairy',
        json=pokemon_species_in_fairy_egg_group,
        status=200
    )

    valid_couples_count = pokemon_valid_couples_count(pokemon_name)

    # Ninetales is duplicated in the responses
    assert valid_couples_count == 3
