#!/usr/bin/env python3
# START_STS
from __future__ import print_function

from random import random
import requests
import re
import json
import argparse
import sys
import os
import types
import urllib3
import importlib.machinery
import configparser
import builtins as __builtins__
import datetime

from datetime import date
from pprint import pprint

urllib3.disable_warnings()

CONSTANTS = {
    'url': 'https://stregsystem.fklub.dk',
    'room': '10',
    'exit_words': [':q', 'exit', 'quit', 'q'],
    'update_url': 'https://raw.githubusercontent.com/f-klubben/stregsystemet-cli/master/main.py',
    'debug': False,
}

if sys.argv[0] == './main.py':
    print('You are running the script in debug mode.')
    CONSTANTS['url'] = 'http://localhost:8000'
    CONSTANTS['room'] = '1'
    CONSTANTS['debug'] = True

is_windows = sys.platform == "win32"
referer_header = {'Referer': CONSTANTS['url']}
balance = float()
config = configparser.ConfigParser()
file_loaded = False

user_id = ''

if is_windows:
    os.system('color')

SHORTHANDS = {
    'abrikos': 1899,
    'ale16': 54,
    'alkofri': 1901,
    'alkoholfri': 1901,
    'cacao': 1882,
    'cider': 1831,
    'classic': 14,
    'cocio': 16,
    'fritfit': 1902,
    'fuzetea': 1879,
    'glaspant': 1848,
    'grøn': 14,
    'kaffe': 32,
    'kakao': 1882,
    'kildevand': 1839,
    'kinley': 1893,
    'monster': 1837,
    'monsterkaffe': 1900,
    'månedens': 1903,
    'noalc': 1901,
    'nordic': 1901,
    'nul': 1901,
    'panta': 1848,
    'pantb': 31,
    'pantc': 1849,
    'porter': 42,
    'redbull': 1895,
    'soda': 11,
    'sodapant': 31,
    'sodavand': 11,
    'sommersby': 1831,
    'specialøl': 1848,
    'sportcola': 1891,
    'sportscola': 1891,
    'storpant': 1849,
    'te': 1904,
    'the': 1904,
    'tuborgnul': 1901,
    'øl': 14,
}

try:
    if not os.path.exists(os.path.expanduser('~/.sts-wares')):
        SHORTHANDS = json.loads(requests.get(f'{CONSTANTS["url"]}/api/products/named_products').text)
        time = datetime.datetime.now()
        with open(os.path.expanduser('~/.sts-wares'), 'a') as f:
            f.writelines([str(time) + '\n', str(SHORTHANDS)])
    else:
        with open(os.path.expanduser('~/.sts-wares'), 'r') as f:
            date_ = datetime.datetime.fromisoformat(f.readline().strip())
            line = f.readline().replace("'", '"')
            SHORTHANDS = json.loads(line)
            if date_ + datetime.timedelta(days=7) < datetime.datetime.now():
                if CONSTANTS['debug']:
                    print('Updating SHORTHANDS')
                SHORTHANDS = json.loads(requests.get(f'{CONSTANTS["url"]}/api/products/named_products').text)
                date_ = datetime.datetime.now()
        with open(os.path.expanduser('~/.sts-wares'), 'w') as f:
            f.writelines([str(date_) + '\n', str(SHORTHANDS)])
        file_loaded = True
except Exception as e:
    if CONSTANTS['debug']:
        print(e)
    SHORTHANDS = {
        'abrikos': 1899,
        'ale16': 54,
        'alkofri': 1901,
        'alkoholfri': 1901,
        'cacao': 1882,
        'cider': 1831,
        'classic': 14,
        'cocio': 16,
        'fritfit': 1902,
        'fuzetea': 1879,
        'glaspant': 1848,
        'grøn': 14,
        'kaffe': 32,
        'kakao': 1882,
        'kildevand': 1839,
        'kinley': 1893,
        'monster': 1837,
        'monsterkaffe': 1900,
        'månedens': 1903,
        'noalc': 1901,
        'nordic': 1901,
        'nul': 1901,
        'panta': 1848,
        'pantb': 31,
        'pantc': 1849,
        'porter': 42,
        'redbull': 1895,
        'soda': 11,
        'sodapant': 31,
        'sodavand': 11,
        'sommersby': 1831,
        'specialøl': 1848,
        'sportcola': 1891,
        'sportscola': 1891,
        'storpant': 1849,
        'te': 1904,
        'the': 1904,
        'tuborgnul': 1901,
        'øl': 14,
    }
    with open(os.path.expanduser('~/.sts-wares'), 'w') as f:
        f.writelines([str(datetime.datetime.now()) + '\n', str(SHORTHANDS)])


def is_int(value):
    if not value:
        return False
    try:
        int(value)
        return True
    except ValueError:
        return False


_date = date.today()
month = _date.month
bat_amount = _date.day
lines_counted = 0


def print(*args, **kwargs):
    global bat_amount, lines_counted
    msg = ' '.join(map(str, args))
    if _date.month == 10 and bat_amount > 0:
        # CPU Heater. Doesn't matter. Still faster than the actual stregsystem
        print_prob = (
            ((random() * 10) / (len(' '.join(map(str, args))) * random() + 0.1) * random())
            * ((_date.day / 100) + 1)
            * 0.7
            * (lines_counted * 0.15)
        )
        print_prob = print_prob / int(print_prob) if int(print_prob) >= 1 else print_prob

        batted = False
        for i in range(len(msg)):
            if print_prob > random() and random() > random() and bat_amount > 0 and not batted:
                if msg[i] == '-' or is_int(msg[i]):
                    if random() > 0.04:
                        print_prob += random()
                    continue
                msg = msg[:i] + '\U0001F987' + msg[i + 1 :]
                bat_amount -= 1
                batted = True
                print_prob = print_prob - random()
                if print_prob <= 0 or bat_amount == 0:
                    break
            else:
                batted = False
        __builtins__.print(msg, **kwargs)
    else:
        __builtins__.print(msg, **kwargs)
    lines_counted += 1


def format_triple(ware, index_0, index_1, index_2):
    r = ware[1]
    if re.match(r'<\w+?\d*?>', ware[1]):
        r = re.sub(r'<br>', ' - ', ware[1])
        r = re.sub(r'</?\w+?\d*?>', '', r)
        print('\u001B[31m{0:<{1}} {2:<{3}} {4:>{5}}\u001B[0m'.format(ware[0], index_0, r, index_1, ware[2], index_2))
    else:
        print('{0:<{1}} {2:<{3}} {4:>{5}}'.format(ware[0], index_0, r, index_1, ware[2], index_2))


def get_wares():
    try:
        session = requests.Session()
        r = session.get(f"{CONSTANTS['url']}/{CONSTANTS['room']}/", verify=False)
    except Exception:
        print('Could not fetch wares from Stregsystement...')
        raise SystemExit(1)

    body = r.text
    item_id_list = re.findall(r'<td>(\d+)</td>', body)
    item_name_list = re.findall(r'<td>(.+?)</td>', body)
    item_price_list = re.findall(r'<td align="right">(\d+\.\d+ kr)</td>', body)

    item_name_list = [x for x in item_name_list if not is_int(x)]

    session.close()
    wares = []
    for i in range(len(item_id_list)):
        wares.append((item_id_list[i], item_name_list[i], item_price_list[i]))

    return wares


wares = get_wares()


def print_wares(wares):
    print('{:<8} {:<50} {:>10}'.format('Id', 'Item', 'Price'))
    print('-' * 70)
    [format_triple(ware, 8, 50, 10) for ware in wares]


def print_no_user_help(user):
    print(
        f'Det var sært, {user}. \nDet lader ikke til, at du er registreret som aktivt medlem af F-klubben i TREOENs dat'
        f'abase. \nMåske tastede du forkert? \nHvis du ikke er medlem, kan du blive det ved at følge guiden på fklub.dk'
    )


def test_user(user):
    session = requests.Session()
    r = session.get(f"{CONSTANTS['url']}/{CONSTANTS['room']}/", verify=False)
    if r.status_code != 200:
        print('Noget gik galt', r.status_code)
        if CONSTANTS.get('debug', False):
            print(r.content)
        raise SystemExit(r.status_code)

    token = re.search('(?<=name="csrfmiddlewaretoken" value=")(.+?)"', r.text)
    json = {'quickbuy': f"{user}", 'csrfmiddlewaretoken': token.group(1)}
    # pprint(json)
    cookies = {'csrftoken': session.cookies.get_dict()['csrftoken'], 'djdt': 'show'}
    # pprint(cookies)
    sale = session.post(
        f"{CONSTANTS['url']}/{CONSTANTS['room']}/sale/",
        verify=False,
        data=json,
        cookies=cookies,
        headers=referer_header,
    )
    session.close()
    if sale.status_code != 200:
        print('Noget gik galt.', sale.status_code, sale.content)
        raise SystemExit
    if 'Det lader ikke til, at du er registreret som aktivt medlem af F-klubben' in sale.text:
        return False

    balance_regex = re.search(r'(\d+.\d+) kroner til gode!', sale.text)
    global balance
    balance = float(balance_regex.group(1))
    global user_id
    user_id = re.search(r'\<a href="/' + CONSTANTS['room'] + '/user/(\d+)"', sale.text).group(1)
    return True


def get_user_validated():
    input_split = [None]
    user = input('Hvad er dit brugernavn? ')
    if ' ' in user:
        input_split = user.split(' ')
        user = input_split[0]

    while not user or not test_user(user):
        if user.lower() in CONSTANTS['exit_words']:
            raise SystemExit
        print(f"'{user}' is not a valid user")
        user = input('Hvad er dit brugernavn? ')
        if ' ' in user:
            input_split = user.split(' ')
            user = input_split[0]

    return user, input_split[1:]


def print_history(wares):
    print('{:<29} {:<40} {:>10}'.format('Date', 'Item', 'Price'))
    print('-' * 81)
    [format_triple(ware, 29, 40, 10) for ware in wares]

    print('')
    print('')


def get_history(user_id):
    if not user_id:
        print('Den angivne bruger har ikke noget ID. Afslutter')
        raise SystemExit(1)

    try:
        session = requests.Session()
        r = session.get(f"{CONSTANTS['url']}/{CONSTANTS['room']}/user/{user_id}", verify=False)
    except Exception:
        print('Kunne ikke oprette forbindelse til Stregsystenet')
        raise SystemExit(1)

    body = r.text
    item_date_list = re.findall(r'<td>(\d+\.\s\w+\s\d+\s\d+:\d+)</td>', body)
    item_name_list = [x for x in re.findall(r'<td>(.+?)</td>', body) if x not in item_date_list][
        0 : len(item_date_list)
    ]
    item_price_list = re.findall(r'<td align="right">(\d+\.\d+)</td>', body)
    history = []
    for x in range(len(item_date_list)):
        history.append((item_date_list[x], item_name_list[x], f"{item_price_list[x]} kr"))

    print_history(history)


is_strandvejen = False


def print_coffee_amount(sale):
    if 'koffein i kroppen' in sale.text:
        in_body = re.search(r'Du har \d+mg koffein i kroppen\.', sale.text)
        cups = re.search(r'Det svarer til at drikke .+? kopper kaffe i streg!', sale.text)
        print(in_body.group(0), cups.group(0))


def print_blood_alcohol_ration(sale):
    if 'Din alkohol promille er ca. ' in sale.text:
        bac = re.search(r'<b>(\d+,\d+‰)</b>', sale.text).group(1)
        print(f'Din alkohol promille er ca. {bac}')


def parse_split_multibuy(itm):
    count = 1
    itm_arr = itm.split(':')
    if len(itm_arr) == 2:
        count = itm_arr[1]
        itm = itm_arr[0]
    elif len(itm_arr) > 2:
        print('Du har fejl i dit multibuy format. Brug kun et : for at adskille antal og vare')
        print('Din fejl er her:')
        print(itm)
        print(('-' * itm.index(':', itm.index(':') + 1)) + '^')
        return None, 0
    return itm, count


def sale(user, itm, count=1):
    if int(count) <= 0:
        print('Du kan ikke købe negative mængder af varer.')
        return

    itm, count = parse_split_multibuy(itm)
    # check for shorthand and replace
    if itm in SHORTHANDS:
        itm = str(SHORTHANDS[itm])

    session = requests.Session()
    r = session.get(f"{CONSTANTS['url']}/{CONSTANTS['room']}/", verify=False)
    if r.status_code != 200:
        print('Noget gik galt', r.status_code)
        if CONSTANTS.get('debug', False):
            print(r.content)
        raise SystemExit

    token = re.search('(?<=name="csrfmiddlewaretoken" value=")(.+?)"', r.text)
    json = {'quickbuy': f"{user} {itm}:{count}", 'csrfmiddlewaretoken': token.group(1)}
    sale = session.post(
        f"{CONSTANTS['url']}/{CONSTANTS['room']}/sale/",
        data=json,
        cookies={'csrftoken': session.cookies.get_dict()['csrftoken'], 'djdt': 'show'},
        headers=referer_header,
    )
    session.close()
    if sale.status_code != 200 and sale.status_code != 402:  # Stregforbud har 402, men no more inventory har ikke????
        print("Du har ikke købt din vare. Prøv igen", sale.status_code)
        raise SystemExit
    elif 'STREGFORBUD!' not in sale.text:
        if ':' in itm:
            if is_int(itm.split(':')[1]):
                count = itm.split(':')[1]
                if int(count) <= 0:
                    print('Du kan ikke købe negative mængder af varer.')
                    return
                itm = itm.split(':')[0]
            else:
                print('Du har angivet tekst hvor du skal angive en mængde')
                return

        ware = [x for x in wares if x[0] == itm]
        if not len(ware):
            print(f"Der findes ikke nogen varer med id {itm}.")
            return

        print(f'{user} har købt', count, ware[0][1], 'til', ware[0][2], 'stykket')
        global balance
        balance -= float(ware[0][2].replace('kr', '').strip()) * float(count)
        itm_unit_price = float(ware[0][2].replace("kr", "").strip())
        itm_units_left = f"{(balance / itm_unit_price):.2f}" if itm_unit_price > 0 else "∞"
        print(f'Der er {balance:.2f} stregdollars - eller {itm_units_left} ' f'x {ware[0][1]} - tilbage')
        print_coffee_amount(sale)
        print_blood_alcohol_ration(sale)

    else:
        ware = [x for x in wares if x[0] == itm]
        print(
            f'''STREGFORBUD!
Du kan ikke foretage køb, før du har foretaget en indbetaling!
Du kan foretage indbetaling via MobilePay. Du har {balance} stregdollars til gode. Den vare du prøvede at købe kostede {ware[0][2]}'''
        )
    global is_strandvejen
    if is_strandvejen:
        import time

        time.sleep(5)
        raise SystemExit


def pre_parse(args, parser: argparse.ArgumentParser):
    parser.add_argument('-z', '--noplugins', action='store_true', help='Disables the plugin loader')
    parser.add_argument(
        '-x', '--strandvejen', action='store_true', help='Flag used for the CRT terminal version running in strandvejen'
    )
    parser.add_argument('-a', '--update', action='store_true', help='Update the script and then exists')
    parser.add_argument('-v', '--verbose', action='store_true', help='Prints information about the running script')
    parser.add_argument('-s', '--setup', action='store_true', help='Runs the setup script')
    args, _ = parser.parse_known_args(args)
    return args


def parse(args, parser: argparse.ArgumentParser):

    parser.add_argument(
        '-u', '--user', default=None, nargs='?', dest='user', help='Specifies your Stregsystem username'
    )
    parser.add_argument('-i', '--item', default=None, nargs='?', dest='item', help='Specifies the item you wish to buy')
    parser.add_argument(
        '-c',
        '--count',
        default=1,
        nargs='?',
        dest='count',
        type=int,
        help='Specifies the amount of items you wish to buy',
    )
    parser.add_argument('-b', '--balance', action='store_true', help='Output only stregdollar balance')
    parser.add_argument('-l', '--history', action='store_true', help='Shows your recent purchases')
    parser.add_argument('-p', '--mobilepay', dest='money', help='Provides a QR code to insert money into your account')
    parser.add_argument('-a', '--update', action='store_true', help='Update the script and then exists')
    parser.add_argument('-o', '--shorthands', action='store_true', help='Shows shorthands')
    parser.add_argument('-z', '--noplugins', action='store_true', help='Disables the plugin loader')
    parser.add_argument(
        '-x', '--strandvejen', action='store_true', help='Flag used for the CRT terminal version running in strandvejen'
    )
    parser.add_argument(
        '-s', '--setup', action='store_true', help='Creates a .sts at /home/<user> storing your account username'
    )
    parser.add_argument('product', type=str, nargs='?', help="Specifies the product to buy")
    parser.add_argument('-v', '--verbose', action='store_true', help='Prints information about the running script')

    args = parser.parse_args(args)
    return args


def get_item(ware_ids):
    count = 1
    item_id = input('Id> ')
    if item_id.lower() in CONSTANTS['exit_words']:
        return 'exit', 0

    if ':' in item_id:
        item_id, count = parse_split_multibuy(item_id)
        if is_int(count):
            if int(count) <= 0:
                print('Du kan ikke købe negative mængder af varer.')
                return None, 0
        else:
            print('Du har angivet tekst hvor du skal angive en mængde')
            return None, 0

    if not (item_id in SHORTHANDS) and (not is_int(item_id) or item_id not in ware_ids):
        if item_id.lower() in CONSTANTS['exit_words']:
            return 'exit', 0

        print(f"'{item_id}' is not a valid item")
        return get_item(ware_ids)
    return item_id, count


def user_buy(user):
    if test_user(user):
        #        os.system('cls||clear')
        print('Hej,', user)
        print(f'Du har {balance:.2f} stregdollars')
        print('')
        print(
            "Hvad ønsker at købe i Stregsystemet? (Skriv en af",
            str(CONSTANTS['exit_words']),
            "for at komme ud af interfacet)",
        )
        print_wares(wares)
        print('')
        while True:
            item, count = get_item([x[0] for x in wares])
            if item in CONSTANTS['exit_words']:
                raise SystemExit
            elif item is None:
                continue
            sale(user, item, count)
    else:
        print_no_user_help(user)


def no_info_buy():
    print("Du kan skrive 'exit' for at annullere.")
    user, purchases = get_user_validated()
    # If wares exists make a sale on every ware
    if purchases:
        for ware in purchases:
            sale(user, ware[0])
    else:
        user_buy(user)


def get_qr(user, amount):
    if is_int(amount) and int(amount) < 50:
        print('Mindste indsætningsbeløb er 50. Alt under, håndteres ikke.')
        return

    print("Skan QR koden nedenfor, for at indsætte penge på din stregkonto")
    session = requests.Session()
    r = session.get(f"https://qrcode.show/mobilepay://send?phone=90601&comment={user}&amount={int(amount)}")
    if r.status_code != 200:
        print('Noget gik galt', r.status_code)
        if CONSTANTS.get('debug', False):
            print(r.content)
        raise SystemExit

    print(r.content.decode('UTF-8'))


def update_config_file(dirs):
    # This function iterates all config files and prepends "[sts]\n" to them.
    for path in dirs:
        if not os.path.exists(path):
            continue
        with open(path, 'r') as original:
            data = original.read()
        if not data.startswith('[sts]'):
            with open(path, 'w') as modified:
                modified.write('[sts]\n' + data)


def read_config():
    dirs = [os.path.expanduser('~/.config/sts/.sts'), os.path.expanduser('~/.sts'), '.sts']
    try:
        config.read(dirs)
    except configparser.MissingSectionHeaderError:
        # update the config to new format
        update_config_file(dirs)
        config.read(dirs)


def get_saved_user() -> str:
    return config.get('sts', 'user', fallback=None)


def get_plugin_dir() -> str:
    rawpath = config.get('sts', 'plugin_dir', fallback=None)
    if rawpath == None:
        return ""
    else:
        return os.path.expanduser(rawpath)


def calculate_sha256_binary(binary) -> str:
    import hashlib

    return hashlib.sha256(binary).hexdigest()


def has_version_difference():
    r = requests.get(CONSTANTS['update_url'])
    newest_file_hash = calculate_sha256_binary(r.content)
    with open(__file__, 'rb') as f:
        data = f.read()
    current_file_hash = calculate_sha256_binary(data)

    return newest_file_hash != current_file_hash


def update_script():
    if not os.access(__file__, os.W_OK):
        print('Stregsystemet-CLI er i læs-kun modus og kan derfor ikke opdateres. Er du på NIX operativsystem?')
        return

    if not has_version_difference():
        return

    # I perform open heart surgery on myself :)
    with open(__file__, 'w', encoding="utf-8") as f:
        r = requests.get(CONSTANTS['update_url'])
        if 'START_STS' in r.text and 'END_STS' in r.text:
            f.write(r.text)


def set_up_plugins(arg_array):
    if not get_plugin_dir() and not os.path.exists('plugins/') and '-z' not in arg_array:
        arg_array.insert(0, '-z')
    elif get_plugin_dir():
        pl_dir = get_plugin_dir()
        pl_dir = f'{pl_dir}/' if not pl_dir.endswith('/') or not pl_dir.endswith('\\') else pl_dir
        if not os.path.exists(f'{pl_dir}__init__.py'):
            with open(f'{pl_dir}__init__.py', 'w') as f:
                f.write('\x00')

    return arg_array


def main():
    arg_array = sys.argv[1::]

    read_config()
    purchases = None

    parser = argparse.ArgumentParser()
    _parser = argparse.ArgumentParser(add_help=False)
    _args = pre_parse(arg_array, _parser)
    if not _args.setup:
        arg_array = set_up_plugins(arg_array)
    if _args.verbose:
        __builtins__.print(
            f'PLUGIN FOLDER={get_plugin_dir()}',
            f'RUNNING FROM={__file__}',
            f'CURRENT USER={get_saved_user()}',
            f'CONFIG LOCATION={"".join([p for p in [os.path.expanduser("~/.config/sts/.sts"), os.path.expanduser("~/.sts")] if os.path.exists(p)])}',
            sep='\n',
        )

    if os.path.exists(get_plugin_dir() or 'plugins'):
        try:
            plugins = []
            for item in [
                f'{get_plugin_dir()}{item}'
                for item in os.listdir(get_plugin_dir() or 'plugins')
                if item.endswith('.py') and item != '__init__.py'
            ]:

                loader = importlib.machinery.SourceFileLoader(item.replace('.py', ''), item)
                mod = types.ModuleType(loader.name)
                loader.exec_module(mod)
                plugins.append(mod)
        except Exception as e:
            if not _args.strandvejen:
                print('STS now supports plugins. Add "plugin_dir=~/.sts_plugins/" to your .sts file')
                if _args.verbose:
                    print(e)
            plugins = []
    else:
        if not _args.strandvejen:
            print('STS now supports plugins. Add "plugin_dir=~/.sts_plugins/" to your .sts file')
        plugins = []

    if not _args.noplugins:
        for plugin in plugins:
            try:
                plugin.pre_argparse(parser, CONSTANTS)
            except (AttributeError, TypeError) as e:
                print(e)
            except Exception:
                pass

    if has_version_difference():
        print("Der er en opdatering til STS. Hent den fra GitHub eller kør sts med --update.", file=sys.stderr)

    args = parse(arg_array, parser)

    if args.user is None:
        args.user = get_saved_user()

    if not args.noplugins:
        for plugin in plugins:
            try:
                plugin.run(wares, args, arg_array, SHORTHANDS, CONSTANTS)
            except (AttributeError, TypeError) as e:
                print(e)
            except Exception:
                pass

    global is_strandvejen
    is_strandvejen = args.strandvejen

    if args.update is True:
        update_script()
        return

    if args.shorthands:
        print("You can use the following shorthand for purchasing")
        pprint(SHORTHANDS)
        if args.verbose:
            print(f'file_loaded={file_loaded}')
        return

    if args.user is None:
        args.user = get_saved_user()

    if args.setup:
        if args.user is None:
            args.user, purchases = get_user_validated()

        if test_user(args.user):
            home = os.path.expanduser('~')
            if not os.path.isfile(f"{home}/.sts"):
                with open(f"{home}/.sts", "w") as f:
                    print(f"Your .sts file has been created at location {home}/.sts")
                    f.write("[sts]\n")
                    f.write(f"user={args.user}\n")
                    f.write('plugin_dir=')

    if args.user and args.product:
        if test_user(args.user):
            sale(args.user, args.item if args.item else str(args.product), args.count)
        else:
            print_no_user_help(args.user)

        return

    if args.balance and args.user:
        test_user(args.user)
        print(f'{balance:.2f}')
        return

    if args.history and args.user:
        global user_id
        test_user(args.user)
        get_history(user_id)

    if args.user is None or args.item is None:
        if args.user is None:
            args.user, purchases = get_user_validated()
            if args.verbose:
                print(f'USER={args.user}')
                print(f'PURCHASES={purchases}')

        if args.user is not None:
            if args.money:
                get_qr(args.user, args.money)
            elif purchases:
                for ware in purchases:
                    sale(args.user, ware)
            else:
                user_buy(args.user)
        else:
            no_info_buy()

    else:
        if test_user(args.user):
            if args.money:
                get_qr(args.user, args.money)
            else:
                sale(args.user, args.item, args.count)
        else:
            print_no_user_help(args.user)

    if not args.noplugins:
        for plugin in plugins:
            try:
                plugin.post_run(wares, args, arg_array, SHORTHANDS, CONSTANTS)
            except (AttributeError, TypeError) as e:
                print(e)
            except Exception:
                pass


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(0)

# END_STS
