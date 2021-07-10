from pokemon_app.pokemon_name_filter import count_pokemons_with_at_and_double_a
from pokemon_app.pokemon_valid_couples import pokemon_valid_couples_count
from pokemon_app.pokemon_type_weight_bounds import pokemon_type_weight_bounds


if __name__ == '__main__':
    print(
        'N° de pokemones con \'at\' y dos a\'s en el nombre: '
        f'{count_pokemons_with_at_and_double_a()}'
    )
    print(
        'N° especies con que puede procrear Raichu: '
        f'{pokemon_valid_couples_count("raichu")}'
    )
    print(
        'Máximo y mínimo peso de pokemones tipo fighting: '
        f'{pokemon_type_weight_bounds("fighting")}'
    )
