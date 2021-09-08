# Stregsystemet-CLI

This repository is the UNOFFICIAL Stregsystemet CLI, to buy things in Stregsystemet, at AAU.

## Requirements

The CLI is a python script that relies on no external dependendencies. The script is tested with python 3.9

## Usage

```bash
$ ./main.py -h
usage: ./main.py [-h] [-u [USER]] [-i [ITEM]] [-c [COUNT]]

optional arguments:
  -h, --help            show this help message and exit
  -u [USER], --user [USER]
                        Specifies your Stregsystem username
  -i [ITEM], --item [ITEM]
                        Specifies the item you wish to buy
  -c [COUNT], --count [COUNT]
                        Specifies the amount of items you wish to buy
  ```

  If either the user or item arguments or no arguments at all are specified the CLI will enter interactive mode.

  The script also keeps track of your balance and what items are available in Stregsystemet.
