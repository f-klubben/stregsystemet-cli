import argparse
import random

# This block runs before the argument parser is created.
# It allows the user to create additional arguments.
def pre_argparse(parser: argparse.ArgumentParser, constants: dict) -> None:
    parser.add_argument(
        '-md', '--monster_dice', action='store_true', help='Roll the dice for a random monster energy drink'
    )
    pass


# This block will run inside the code. This is where
# the user places their custom logic
def run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    if args.monster_dice:
        monsters = {
            'Grøn': 1837,
            'Blå (Zero)': 1837,
            'Monarch': 1837,
            'The Doctor': 1837,
            'Pacific Punch': 1837,
            'Ultra Paradise': 1837,
            'Ultra Fiesta': 1837,
            'Mango Loco': 1837,
            'Ultra Violet': 1837,
            'Ultra Zero': 1837,
            'Pipeline Punch': 1837,
            'Mule': 1837,
            'Monarch': 1837,
            'Espresso Milk': 1900,
            'Espresso Vanilla': 1900,
        }

        number = random.randrange(len(monsters))

        key = list(monsters)[number]

        args.product = monsters[key]
        print(f'Du fik en {key}!')
    pass


# This block runs at the very end of main and may not
# be reached, due to some 'raise systemExit'
def post_run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    pass
