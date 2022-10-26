import argparse

# This block runs before the argument parser is created.
# It allows the user to create additional arguments.
def pre_argparse(parser: argparse.ArgumentParser, constants: dict) -> None:
    parser.add_argument('--recipe', action='store_true', help='Allows purchasing of custom recipes')
    pass


def print_recipes():
    print(
        '''
For at købe et recipe, skal navnet på recipe skrives som produkt, efter --recipe.
Eksempel: --recipe speedball

speedball: Halv kaffemonner og halv limfjordsporter.
           Køber 1 x 1900, 1 x 42
milktea: Te med et skud mælk (mandemælk)
              Køber 1 x 32, 1x 1904
'''
    )


# This block will run inside the code. This is where
# the user places their custom logic
def run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    # Make sure to check for the correct argument here. This block always runs
    if args.recipe and len(args.product) == 0:
        print_recipes()
        raise SystemExit

    if args.product and 'speedball' in args.product:
        args.product.remove('speedball')
        args.product.append('1900')
        args.product.append('42')

    if args.product and 'milktea' in args.product:
        args.product.remove('milktea')
        args.product.append('32')
        args.product.append('1904')

# This block runs at the very end of main and may not
# be reached, due to some 'raise systemExit'
def post_run(wares: list, args: list, arg_array: list, shorthands: dict, constants: dict) -> None:
    pass
