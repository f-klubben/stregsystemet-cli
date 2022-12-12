#!/usr/bin/env python3
# START_STS
from __future__ import print_function, annotations
import argparse
import builtins as __builtins__
from collections import Counter
import configparser
from dataclasses import dataclass
import datetime
from datetime import date
import importlib.machinery
import json
import os
from pprint import pprint
from random import random
import re
import sys
from time import sleep
import types
from typing import Callable

import requests

import urllib3

urllib3.disable_warnings()

CONSTANTS = {
    'url': 'https://stregsystem.fklub.dk',
    'room': '10',
    'exit_words': [':q', 'exit', 'quit', 'q'],
    'update_url': 'https://raw.githubusercontent.com/f-klubben/stregsystemet-cli/master/main.py',
    'plugin_url': 'https://raw.githubusercontent.com/f-klubben/stregsystemet-cli/master/community_plugins/$$REPLACEME$$.py',
    'debug': False,
    'printables': {
        4: '\U0001F414',  # Chicken emoji
        10: '\U0001F987',  # Bat emoji
        12: '\U00002744',  # Snowflake emoji
    },
}

if sys.argv[0] == './main.py':
    print('You are running the script in debug mode.')
    CONSTANTS['url'] = 'http://localhost:8000'
    CONSTANTS['room'] = '10'
    CONSTANTS['debug'] = True


_date = date.today()
month = _date.month
bat_amount = _date.day
lines_counted = 0

# Unicode characters for emojis
# https://apps.timwhitlock.info/emoji/tables/unicode
printables = {
    4: '\U0001F414',  # Chicken emoji
    10: '\U0001F987',  # Bat emoji
    12: '\U00002744',  # Snowflake emoji
}

special_months = [4, 10, 12]

if CONSTANTS['debug']:
    print(f'MONTH={_date.month}')
    print(f'PRINTABLE={printables.get(_date.month, "")}')


# Overwrite of print to write bats and stuff.
def print(*args, **kwargs):
    global bat_amount, lines_counted
    msg = ' '.join(map(str, args))
    if _date.month in special_months and bat_amount > 0 and config.getboolean('sts', 'emoji_support', fallback=True):
        # CPU Heater. Doesn't matter. Still faster than the actual stregsystem
        print_prob = (
            ((random() * 10) / (len(' '.join(map(str, args))) * random() + 0.1) * random())
            * ((_date.day / 31) + 1)
            * 0.4
            * (lines_counted * 0.15)
        )
        if CONSTANTS['debug']:
            __builtins__.print(f'PRINT_PROB={print_prob}')
        print_prob = print_prob / int(print_prob) if int(print_prob) >= 1 else print_prob

        batted = False
        for i in range(6, len(msg)):
            if print_prob > random() and random() > random() and bat_amount > 0 and not batted:
                if msg[i] == '-' or msg[i].isdigit():
                    if random() > 0.04:
                        print_prob += random()
                    continue
                msg = msg[:i] + printables[_date.month] + msg[i + 1 :]
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


class Configuration:
    user: str
    plugin_dir: str
    emoji_support: bool
    _dirs = [os.path.expanduser('~/.config/sts/.sts'), os.path.expanduser('~/.sts'), '.sts']

    def __init__(self):
        try:
            self.read()
        except Exception:
            self.user = ''
            self.plugin_dir = ''
            self.emoji_support = False

    def __str__(self):
        return f'user: {self.user}, plugin_dir: {self.plugin_dir}, emoji_support: {self.emoji_support}'

    def __dict__(self) -> dict:
        return {'user': self.user, 'plugin_dir': self.plugin_dir, 'emoji_support': self.emoji_support}

    def __repr__(self) -> str:
        return self.__str__()

    def write(self):
        paths = [path for path in self._dirs if os.path.exists(path)]
        config = configparser.ConfigParser()
        config['sts'] = self.__dict__()
        with open(paths[0], 'w') as configfile:
            config.write(configfile)

    def read(self):
        config = configparser.ConfigParser()
        config.read(self._dirs)
        self.user = config['sts']['user']
        self.plugin_dir = config['sts']['plugin_dir']
        self.emoji_support = config['sts']['emoji_support'] == 'True'

    def get_user(self):
        return self.user

    def get_plugin_dir(self):
        return self.plugin_dir

    def get_emoji_support(self):
        return self.emoji_support


class History:
    def __init__(self, date, name, price):
        self.date = date
        self.name = name
        self.price = price

    def __str__(self):
        return f'{self.date} - {self.name} - {self.price}'

    def __repr__(self):
        return self.__str__()

    def format_str(self, date_width, name_width, price_width):
        return f'{self.date:<{date_width}} {self.name:<{name_width}} {self.price:>{price_width}}'


class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.special = re.match(r'<\w+\d*>', name)
        self.price = price

    def __repr__(self):

        return f'{self.id} - {self.name} - {self.price}'

    def __str__(self):
        return f'{self.id} - {self.name} - {self.price}'

    def format_str(self, id_width, name_width, price_width):
        if re.match(r'<\w+\d*>', self.name):
            self.name = re.sub(r'</?\w+?\d*?>', '', self.name)
            return (
                f'\u001B[31m{self.id:<{id_width}} {self.name:<{name_width}} {self.price:>{price_width}.2f} kr.\u001B[0m'
            )

        return f'{self.id:<{id_width}} {self.name:<{name_width}} {self.price:>{price_width}.2f} kr.'

    def __getitem__(self, indicies):
        if indicies == 0:
            return self.id
        if indicies == 1:
            return self.name
        if indicies == 2:
            return self.price


@dataclass
class User:
    username: str
    balance: float
    user_id: int


@dataclass
class Plugin:
    pre_argparse: Callable
    run: Callable
    post_run: Callable


def parse_split_multibuy(product: str) -> tuple[str, int]:
    itm: str = product
    count: str = '1'
    itm_arr: list[str] = product.split(':')
    if len(itm_arr) == 2:
        count = itm_arr[1]
        itm = itm_arr[0]
    elif len(itm_arr) > 2:
        raise SystemExit(
            f'''Du har fejl i dit multibuy format. Brug kun et : for at adskille antal og vare
Din fejl er her:
{product}
{'~' * (product.index(':', product.index(':') + 1)) + '^'}
'''
        )
    if not re.match(r'\d+', str(count)):
        raise SystemExit(
            f'''Du har fejl i dit multibuy format. Antal skal være et tal
Din fejl er her:
{product}
{('~' * (product.index(':') + 1)) + ('^'*len(str(count)))}
'''
        )
    return itm, int(count)


class Stregsystem:
    class ArgumentHandler:
        args: argparse.Namespace

        def __init__(self, args: argparse.Namespace, shorthands: dict[str, int], products: dict[int, Product]):
            self.args: argparse.Namespace = args
            self.shorthands: dict[str, int] = shorthands

        def handle_stopping(self, sts: Stregsystem, user_manager, request_handler) -> None:
            if self.args.update:
                update_script()
                raise SystemExit(0)
            sts.determine_user()
            if self.args.money:
                self.mobilepay(self.args.money, user_manager, request_handler)
                raise SystemExit(0)
            if self.args.history:
                self.history(user_manager, request_handler)
                raise SystemExit(0)
            if self.args.shorthands:
                self.show_shorthands()
                raise SystemExit(0)
            if self.args.balance:
                self.balance(user_manager, request_handler)
                raise SystemExit(0)
            if self.args.setup:
                self.setup_sts(user_manager, request_handler, Configuration())
                raise SystemExit(0)
            if self.args.rank:
                self.ranking(user_manager, request_handler)
                raise SystemExit(0)
            if self.args.pluginstall:
                self.install_plugin(self.args.pluginstall, Configuration(), request_handler)
                raise SystemExit(0)
            if self.args.pluguninstall:
                self.uninstall_plugin(self.args.pluguninstall, Configuration())
                raise SystemExit(0)

        def get_plugin_dir(self, config: Configuration):
            if config.plugin_dir and os.path.exists(config.plugin_dir):
                return config.plugin_dir

            # Prompt for setup of plugins. The user wants to install anyways
            __builtins__.print('You do not have a plugin directory set up.')
            dirr = input('Please enter a valid plugin directory')
            while not os.path.exists(dirr):
                __builtins__.print('You do not have a plugin directory set up.')
                dirr = input('Please enter a valid plugin directory')

            config.plugin_dir = dirr
            config.write()
            return dirr

        def install_plugin(self, plugin_name: str, configuration: Configuration, request_handler: RequestHandler):
            def test_for_plugin_online(plugin_name: str, request_handler: RequestHandler):
                req = request_handler.get(CONSTANTS['plugin_url'].replace('$$REPLACEME$$', plugin_name))
                return req.status_code == 200

            def download_plugin(plugin: str, dirr: str, req_handler: RequestHandler):
                req = req_handler.get(CONSTANTS['plugin_url'].replace('$$REPLACEME$$', plugin))
                with open(f'{dirr}{plugin}.py', 'w') as plg:
                    plg.write(req.text)

            dirr = self.get_plugin_dir(configuration)
            if test_for_plugin_online(plugin_name, request_handler):
                existed = os.path.exists(f'{dirr}{plugin_name}.py')
                download_plugin(plugin_name, dirr, request_handler)
                print('Plugin', ('installed' if not existed else 'reinstalled'))
            else:
                print(f'The plugin "{plugin_name}" does not exist as a community plugin.')

        def uninstall_plugin(self, plugin_name: str, configuration: Configuration):
            dirr = self.get_plugin_dir(configuration)
            if os.path.exists(f'{dirr}{plugin_name}.py'):
                os.remove(f'{dirr}{plugin_name}.py')
                print('Plugin removed')
            else:
                print(plugin_name, 'is not an installed plugin')

        def has_products(self) -> bool:
            return self.args.product is not None and len(self.args.product) > 0

        def history(self, user_manager, request_handler) -> None:
            hist = user_manager.get_history(request_handler)
            print('{:<29} {:<40} {:>10}'.format('Date', 'Item', 'Price'))
            print('-' * 81)
            for h in hist:
                print(h.format_str(29, 40, 10))

        def get_products(self) -> dict[str, int]:
            products = {}
            for product in self.args.product:
                itm, count = parse_split_multibuy(product)
                products[itm] = int(count)

            return products

        def mobilepay(self, amount, user_manager, request_handler) -> None:
            request_handler.add_funds(amount, user_manager)

        def show_shorthands(self) -> None:
            sorted_shorthands = {}
            for i in sorted(self.shorthands):
                sorted_shorthands[i] = self.shorthands[i]
            pprint(sorted_shorthands)

        def setup_sts(self, user_manager: UserManager, request_handler: RequestHandler, configuration: Configuration):
            user = user_manager.get_username()
            if user is None or not user_manager.check_user_exists(user, request_handler):
                user = user_manager.prompt_user(request_handler)

            answer = 'a'
            while answer.lower() not in ['y', 'n']:
                __builtins__.print('Please check if you are able to see the emojis between the <> symbols below')
                __builtins__.print(
                    f'<{CONSTANTS["printables"][4]}><{CONSTANTS["printables"][10]}><{CONSTANTS["printables"][12]}>'
                )
                try:
                    answer = input('Does your terminal support emojis? (y/n) ')
                except (EOFError, KeyboardInterrupt):
                    raise SystemExit()
            emoji_support = answer.lower() == 'y'
            configuration.user = user
            configuration.emoji_support = emoji_support
            configuration.plugin_dir = ''
            configuration.write()

        def balance(self, user_manager: UserManager, request_handler: RequestHandler) -> None:
            user = user_manager.get_username()
            if user is None or not user_manager.check_user_exists(user, request_handler):
                __builtins__.print('You need to provide a user to check the balance of')
                raise SystemExit(0)
            print(user_manager.get_balance())

        def ranking(self, user_manager: UserManager, request_handler: RequestHandler) -> None:
            user = user_manager.get_username()
            if user is None or not user_manager.check_user_exists(user, request_handler):
                __builtins__.print('Ypu need to provide a user to check the ranking of')
                raise SystemExit()
            print(user_manager.get_ranking(request_handler))

        def get_user(self):
            return self.args.user

    class RequestHandler:
        cookies: dict

        def __init__(self):
            self.session = requests.Session()
            self.session.headers.update(
                {'User-Agent': 'STS - Stregsystem CLI - https://github.com/f-klubben/stregsystemet-cli'}
            )
            self.session.headers.update({'Referer': CONSTANTS['url']})
            self.session.verify = False

        def get(self, url, params=None) -> requests.Response:
            return self.session.get(url, params=params)

        def get_clean_body(self, response) -> str:
            return re.sub(r'\s{2,}', '', response.text)

        def set_cookies(self) -> None:
            response = self.get(f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/')
            self.cookies = {'csrftoken': response.cookies.get_dict()['csrftoken'], 'djdt': 'show'}

        def get_token(self, get_response) -> str:
            token = re.search('(?<=name="csrfmiddlewaretoken" value=")(.+?)"', get_response.text)
            if token:
                return token.group(1)
            else:
                raise Exception('Could not find token in GET request from ' + get_response.url)

        def post(self, url, data=None) -> requests.Response:
            token = self.get_token(self.get(f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/'))
            data.update({'csrfmiddlewaretoken': token})
            return self.session.post(url, data=data)

        def add_funds(self, amount, user_manager) -> None:
            try:
                amount = float(amount)
            except ValueError:
                raise SystemExit('Det indtastede beløb er ikke et tal')
            if amount < 50:
                print('Mindste indsætningsbeløb er 50. Alt under, håndteres ikke.')
                raise SystemExit(0)

            user = user_manager.get_username()
            if not user:
                user = user_manager.prompt_user(self)
            if not user:
                raise SystemExit(1)

            print("Skan QR koden nedenfor, for at indsætte penge på din stregkonto")
            # Start a new session to not leak information about STS to outside host
            session = requests.Session()
            r = session.get(f"https://qrcode.show/mobilepay://send?phone=90601&comment={user}&amount={int(amount)}")
            if r.status_code != 200:
                print('Noget gik galt', r.status_code)
                if CONSTANTS.get('debug', False):
                    __builtins__.print(r.content)
                raise SystemExit

            print(r.content.decode('UTF-8'))

    class UserManager:
        user: User

        def __init__(self, user) -> None:
            self.user = user

        def get_user(self) -> User:
            return self.user

        def update_balance(self, request_handler: RequestHandler) -> None:
            user_response = request_handler.post(
                f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/sale/', data={'quickbuy': self.user.username}
            )

            balance_regex = re.search(r'(\d+.\d+) kroner til gode!', user_response.text)
            if not balance_regex:
                raise SystemExit(f'Could not get user information from stregsystemet, could not find balance')

            self.user.balance = float(balance_regex.group(1))

        def get_balance(self) -> float:
            return self.user.balance

        def get_user_id(self) -> int:
            return self.user.user_id

        def get_username(self) -> str:
            return self.user.username

        def set_user(self, username, request_handler) -> None:
            user_response = request_handler.post(
                f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/sale/', data={'quickbuy': username}
            )
            if user_response.status_code != 200:
                raise SystemExit(
                    f'Could not get user information from stregsystemet, status {user_response.status_code}'
                )

            balance_regex = re.search(r'(\d+.\d+) kroner til gode!', user_response.text)
            if not balance_regex:
                raise SystemExit(f'Could not get user information from stregsystemet, could not find balance')

            balance = float(balance_regex.group(1))
            user_id_regex = re.search(r'\<a href="/' + CONSTANTS['room'] + '/user/(\d+)"', user_response.text)
            if not user_id_regex:
                raise SystemExit(f'Could not get user information from stregsystemet, could not find user id')

            user_id = int(user_id_regex.group(1))
            self.user = User(username, balance, user_id)

        def update_user(self, request_handler) -> None:
            if not self.user:
                raise SystemExit('No user set')
            self.set_user(self.user.username, request_handler)

        def get_history(self, request_handler: RequestHandler) -> list[History]:
            if not self.user.user_id:
                print('Den angivne bruger har ikke noget ID. Afslutter')
                raise SystemExit(1)

            body = request_handler.get_clean_body(
                request_handler.get(f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/user/{self.user.user_id}/')
            )
            item_date_list = re.findall(r'<td>(\d+\.\s\w+\s\d+\s\d+:\d+)</td>', body)
            item_name_list = [
                x for x in re.findall(r'<td>(.+?)</td>', body) if x not in item_date_list and '<center>' not in x
            ][0 : len(item_date_list)]
            item_price_list = re.findall(r'<td align="right">(\d+\.\d+)</td>', body)
            history: list[History] = []
            for x in range(len(item_date_list)):
                history.append(History(item_date_list[x], item_name_list[x][0:40], f"{item_price_list[x]} kr"))

            return history

        def check_user_exists(self, username: str, request_handler: RequestHandler) -> bool:
            if username == '' or username is None:
                return False
            user_response = request_handler.post(
                f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/sale/', data={'quickbuy': username}
            )
            return (
                user_response.status_code == 200
                and 'Det lader ikke til, at du er registreret som aktivt medlem af F-klubben' not in user_response.text
            )

        def prompt_user(self, request_handler: RequestHandler) -> tuple[str, list[str]]:
            try:
                response = input('Indtast dit brugernavn: ')
                while not self.check_user_exists(response.split(' ')[0], request_handler):
                    self.print_no_user_help(response.split(' ')[0])
                    response = input('Indtast dit brugernavn: ')
            except (EOFError, KeyboardInterrupt):
                raise SystemExit()
            username = response.split(' ')[0]
            wares = response.split(' ')[1:]
            return username, wares

        def print_no_user_help(self, user):
            print(
                f'Det var sært, {user}. \nDet lader ikke til, at du er registreret som aktivt medlem af F-klubben i TREOENs dat'
                f'abase. \nMåske tastede du forkert? \nHvis du ikke er medlem, kan du blive det ved at følge guiden på fklub.dk'
            )

        def get_ranking(self, request_handler: RequestHandler):
            ret_val = f'Ranking for {self.user.username}\n\n'
            if not self.user.user_id:
                ret_val += 'den angivne bruger har ikke noget ID. Afslutter\n'
                raise SystemExit(1)
            r = request_handler.get(f"{CONSTANTS['url']}/{CONSTANTS['room']}/user/{self.get_user_id()}/rank")
            if r.status_code != 200:
                __builtins__.print('Noget gik galt.', r.status_code, r.url)
                raise SystemExit(r.status_code)
            items = self.parse_scoreboard(r.text)
            ret_val += '{:<20} {:>10} {:>10}'.format('Navn', 'Gennemsnit', 'Rank') + '\n'
            ret_val += ('-' * 42) + '\n'
            for i in range(len(items[0])):
                ret_val += self.format_scoreboard((items[0][i], items[1][i], items[2][i])) + '\n'
            return ret_val

        def parse_scoreboard(self, content):
            content = (
                re.search(r'<table class="ranking">(.+?)</table>', content, re.DOTALL)
                .group(1)
                .replace('  ', '')
                .replace('\n', '')
            )
            headers = re.findall(r'<th class="ranking">(.+?)</th>', content)
            fields = re.findall(r'<td class="ranking">(.+?)</td>', content)
            return headers, fields[len(headers) :], fields[: len(headers)]

        def format_scoreboard(self, triple) -> str:
            return '{:<20} {:>10} {:>10}'.format(*triple)

    products: dict[int, Product] = {}
    shorthands: dict[str, int] = {}
    _request_handler: RequestHandler = RequestHandler()
    _user_manager: UserManager = UserManager(User(username='', balance=0, user_id=0))
    _argument_handler: ArgumentHandler
    plugins: list[Plugin] = []
    kiosk_mode: bool = False
    disable_plugins: bool = False
    _args: argparse.Namespace
    args: argparse.Namespace
    raw_args: list = []

    config: Configuration

    def __init__(self, config: Configuration, _args: argparse.Namespace, args: list) -> None:
        if sys.platform == 'win32':
            os.system('color')
        self.raw_args = args
        self.kiosk_mode = _args.strandvejen if _args else False
        self.disable_plugins = _args.noplugins or self.kiosk_mode if _args else False
        self._args = _args
        self.config = config

    def load(self) -> None:

        self.load_plugins()
        self.update_products()
        self.update_shorthands()

        parser = argparse.ArgumentParser()
        if not self.disable_plugins:
            for plugin in self.plugins:
                if plugin.pre_argparse:
                    plugin.pre_argparse(parser, CONSTANTS)
        self.args = parse(self.raw_args, parser)
        self._argument_handler = self.ArgumentHandler(self.args, self.shorthands, self.products)
        self._argument_handler.handle_stopping(self, self._user_manager, self._request_handler)

    def check_user_exists(self, username) -> bool:
        return self._user_manager.check_user_exists(username, self._request_handler)

    def load_plugins(self) -> None:
        self.set_plugins(self.get_plugins(self.config))

    def set_plugins(self, plugins: list[Plugin]) -> None:
        self.plugins = plugins

    def get_plugins(self, config: Configuration) -> list[Plugin]:
        plugins = []
        if self.disable_plugins:
            return plugins

        if config.get_plugin_dir() and os.path.exists(config.get_plugin_dir()):
            try:
                for item in [
                    f'{config.get_plugin_dir()}{item}'
                    for item in os.listdir(config.get_plugin_dir())
                    if os.path.isfile(f'{config.get_plugin_dir()}{item}')
                    and item.endswith('.py')
                    and item != '__init__.py'
                ]:
                    loader = importlib.machinery.SourceFileLoader(item.replace('.py', ''), item)
                    mod = types.ModuleType(loader.name)
                    loader.exec_module(mod)
                    plugins.append(Plugin(mod.pre_argparse, mod.run, mod.post_run))
            except Exception as e:
                if e and CONSTANTS['debug']:
                    print(e)
                elif not self.kiosk_mode:
                    print('Der opstod en fejl under indlæsning af plugins. Ingen plugins er blevet indlæst.')
                plugins = []

        return plugins

    def prompt_user(self) -> tuple[str, list[str]]:
        return self._user_manager.prompt_user(self._request_handler)

    def make_purchase(self, products: dict[str, int]) -> tuple[bool, str]:
        # key is item ID, value is quantity
        output = ''
        if not self.products:
            raise SystemExit('Unable to make purchase. No products loaded.')

        sale_output_template = """{0} har købt {1} {2} til {3} kr. stykket.
Der er {4:.2f} stregdollar - eller {5} x {2} tilbage.
"""
        buy_string = f'{self._user_manager.get_username()} '
        self._user_manager.update_user(self._request_handler)
        temp_balance = self._user_manager.get_balance()
        for product_id, quantity in products.items():
            if quantity < 1:
                output = f'Du kan ikke købe 0 eller færre varer.\nDu forsøgte at købe {quantity} x {product_id}'
                return False, output

            if not re.match(r'\d+', product_id):
                if product_id == '':
                    continue
                if product_id in self.shorthands:
                    product_id = self.shorthands[product_id]
                else:
                    raise SystemExit(f'Product {product_id} not found.')

            product_id = int(product_id)
            if product_id not in self.products:

                raise SystemExit(f'Product {product_id} not found.')

            temp_balance -= self.products[product_id].price * quantity
            itm_units_left = (
                f"{(temp_balance / self.products[product_id].price):.2f}"
                if self.products[product_id].price > 0
                else "∞"
            )
            output += sale_output_template.format(
                self._user_manager.get_username(),
                quantity,
                self.products[product_id].name,
                self.products[product_id].price,
                temp_balance,
                itm_units_left,
            )
            buy_string += f'{product_id}:{quantity} '

        response = self._request_handler.post(
            f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/sale/', data={'quickbuy': buy_string}
        )

        if 'STREGFORBUD!' in response.text:
            output = f'''STREGFORBUD!
Du kan ikke foretage køb, før du har foretaget en indbetaling!
Du kan foretage indbetaling via MobilePay. Du har {self._user_manager.get_balance()} stregdollars til gode.'''

            return False, output

        self._user_manager.update_user(self._request_handler)

        return response.status_code == 200, output

    def set_user(self, username: str) -> None:
        self._user_manager.set_user(username, self._request_handler)

    def add_product(self, id, name, price) -> None:
        self.products[int(id)] = Product(id, name, price)

    def add_shorthand(self, id, shorthand) -> None:
        self.shorthands[shorthand] = id

    def write_shorthand_file(self, file_path, date) -> None:
        with open(file_path, 'w') as f:
            f.writelines([str(date) + '\n', str(self.shorthands)])

    def read_shorthand_file(self, file_path) -> tuple[datetime.datetime, dict]:
        with open(file_path, 'r') as f:
            date = datetime.datetime.fromisoformat(f.readline().strip())
            self.shorthands = json.loads(f.readline().replace('\'', '"'))
            return date, self.shorthands

    def determine_user(self):
        if self._argument_handler.get_user():
            self._user_manager.set_user(self._argument_handler.get_user(), self._request_handler)
        elif not sts.check_user_exists(configuration.get_user()):
            username, wares = sts.prompt_user()
            sts.set_user(username)
            if wares:
                sts.buy_multiple_items(wares)
                sts.handle_kiosk()
                raise SystemExit
        else:
            sts.set_user(configuration.get_user())

    def get_greeting(self, user: User) -> str:
        return (
            f'''
Hej, {user.username}
Du har {user.balance} stregdollar.
        '''.strip()
            + '\n'
        )

    def get_catalogue(self) -> str:
        if not self.products:
            raise SystemExit('No products loaded.')
        output = '{:<8} {:<50} {:>10}'.format('Id', 'Navn', 'Pris')
        output += '\n' + ('-' * 74) + '\n'
        output += '\n'.join([product.format_str(8, 50, 10) for product in self.products.values()])
        return output

    def update_shorthands(self) -> None:
        try:
            if not os.path.exists(os.path.expanduser('~/.sts-wares')):
                self.shorthands.update(
                    json.loads(self._request_handler.get(f'{CONSTANTS["url"]}/api/products/named_products').text)
                )
                time = datetime.datetime.now()
                self.write_shorthand_file(os.path.expanduser('~/.sts-wares'), time)
            else:
                last_update, _ = self.read_shorthand_file(os.path.expanduser('~/.sts-wares'))
                if last_update + datetime.timedelta(days=7) < datetime.datetime.now():
                    if CONSTANTS['debug']:
                        print('Updating SHORTHANDS')
                    self.shorthands.update(
                        json.loads(self._request_handler.get(f'{CONSTANTS["url"]}/api/products/named_products').text)
                    )
                    date_ = datetime.datetime.now()
                    self.write_shorthand_file(os.path.expanduser('~/.sts-wares'), date_)
        except Exception as e:
            if CONSTANTS['debug']:
                __builtins__.print(e)
            __builtins__.print('FATAL ERROR: Could not fetch shorthands. Shorthands will be disabled for this session')

    def update_products(self) -> None:
        response = self._request_handler.get(f'{CONSTANTS["url"]}/{CONSTANTS["room"]}/')
        clean_body = self._request_handler.get_clean_body(response)
        item_id_list = re.findall(r'<td>(\d+)( / \w+)?</td>', clean_body)
        item_name_list = re.findall(r'<td>(.+?)</td>', clean_body)
        item_price_list = re.findall(r'<td align="right">(\d+\.\d+) kr</td>', clean_body)

        exclusion_set = set([f'{y[0]}{y[1]}' for y in item_id_list])
        item_name_list = [
            x.replace('<br>', ' - ')
            for x in item_name_list
            if x not in exclusion_set and (re.match(r'<\w+\d+>', x) is not None or not x.startswith('<'))
        ]

        for i in range(len(item_id_list)):
            self.add_product(item_id_list[i][0], item_name_list[i], float(item_price_list[i]))

    def quickbuy(self, items=None) -> None:
        if not self.disable_plugins:
            for plugin in self.plugins:
                if plugin.pre_argparse:
                    plugin.run(
                        self.products,
                        self._argument_handler.args,
                        self.raw_args,
                        self.shorthands,
                        CONSTANTS,
                    )

        if items is None:
            success, output = self.make_purchase(self._argument_handler.get_products())
        else:
            success, output = self.make_purchase(items)

        if not self.disable_plugins:
            for plugin in self.plugins:
                if plugin.post_run:
                    plugin.post_run(
                        list(self.products.values()),
                        self._argument_handler.args,
                        self.raw_args,
                        self.shorthands,
                        CONSTANTS,
                    )

        print(output)
        self.handle_kiosk()
        if success:
            raise SystemExit(0)
        else:
            raise SystemExit(1)

    def buy_multiple_items(self, items) -> None:
        for item in items:
            itm, qnty = parse_split_multibuy(item)
            if itm in self.shorthands:
                itm = self.shorthands[itm]
            itm = int(itm)
            if itm in self.products:
                success, output = self.make_purchase({str(itm): int(qnty)})
                print(output)
                if not success:
                    raise SystemExit(1)

    def handle_kiosk(self) -> None:
        if self.kiosk_mode:
            sleep(5)
            raise SystemExit()

    def enter_shop_loop(self) -> None:
        global _date, bat_amount
        if CONSTANTS['debug']:
            __builtins__.print('Bats printed:', (_date.day - bat_amount))
        while True:
            try:
                items = input('Id> ').strip()
            except (EOFError, KeyboardInterrupt):
                raise SystemExit()

            if items in CONSTANTS['exit_words']:
                raise SystemExit(0)

            if ' ' in items:
                items = re.split(r'\s+', items)
                self.buy_multiple_items(items)
            else:
                itm, qnty = parse_split_multibuy(items)
                if not itm.isdigit() and itm in self.shorthands:
                    itm = self.shorthands[itm]

                if type(itm) is str and not itm.isdigit():
                    print(f'Varen \'{itm}\' findes ikke.')
                    continue
                itm = int(itm)
                if itm in self.products:
                    success, output = self.make_purchase({str(itm): int(qnty)})
                    print(output)
                    if not success:
                        raise SystemExit(1)
                    if not self.disable_plugins:
                        for plugin in self.plugins:
                            if plugin.post_run:
                                plugin.post_run(
                                    list(self.products.values()),
                                    self._argument_handler.args,
                                    self.raw_args,
                                    self.shorthands,
                                    CONSTANTS,
                                )

                    self.handle_kiosk()

    def shop(self) -> None:
        if not self.disable_plugins:
            for plugin in self.plugins:
                if plugin.pre_argparse:
                    plugin.run(
                        list(self.products.values()),
                        self._argument_handler.args,
                        self.raw_args,
                        self.shorthands,
                        CONSTANTS,
                    )

                    if self._argument_handler.args.product:
                        self._argument_handler.args.product = [str(self._argument_handler.args.product)]
                        self.quickbuy()

        print(self.get_greeting(self._user_manager.get_user()))
        print(
            "Hvad ønsker at købe i Stregsystemet? (Skriv en af [':q', 'exit', 'quit', 'q'] for at komme ud af interfacet)"
        )
        [print(line) for line in self.get_catalogue().split('\n')]
        print('')
        self.enter_shop_loop()

    def start_shop(self) -> None:

        if self._argument_handler.has_products():
            self.quickbuy()
        else:
            self.shop()


is_windows = sys.platform == "win32"
referer_header = {'Referer': CONSTANTS['url']}
balance = float()
config = configparser.ConfigParser()

user_id = ''

if is_windows:
    os.system('color')


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
    parser.add_argument('product', type=str, nargs='*', help="Specifies the product to buy")
    parser.add_argument('-v', '--verbose', action='store_true', help='Prints information about the running script')
    parser.add_argument('-r', '--rank', action='store_true', help='Shows your rank in different categories')
    parser.add_argument(
        '-pi',
        '--pluginstall',
        default=None,
        nargs='?',
        dest='pluginstall',
        help='Install a plugin from the community plugins. https://github.com/f-klubben/stregsystemet-cli/tree/master/community_plugins',
    )
    parser.add_argument(
        '-pu',
        '--pluguninstall',
        default=None,
        nargs='?',
        dest='pluguninstall',
        help='Remove a plugin from your installation of STS.',
    )

    args = parser.parse_args(args)
    return args


if __name__ == '__main__':
    configuration = Configuration()

    arg_array = sys.argv[1::]
    _parser = argparse.ArgumentParser(add_help=False)
    _args = pre_parse(arg_array, _parser)
    if has_version_difference():
        __builtins__.print(
            "Der er en opdatering til STS. Hent den fra GitHub eller kør sts med --update.", file=sys.stderr
        )

    sts = Stregsystem(configuration, _args, arg_array)
    sts.load()
    sts.start_shop()

# END_STS
