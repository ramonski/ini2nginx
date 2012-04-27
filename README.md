# NGINX Config writer

## Anstract

This script helps you to generate various nginx configs with ease!

## Introduction

You have a lot of nginx configs to maintain, you probably copy&paste
an existing config to a new config to add a new VHM to NGINX.

Most of the time, the only values you have to change, is the rewrite path
and the server name.

## Usage

1. Customize the NGINX Template
2. Add a custom config writer, see `example_writer` in `ini2nginx.py`
3. Configure your custom site configuration in `nginx.ini`
4. Run `python ini2nginx.py`
5. Configs are saved by default under the `config` folder
6. For help, type `python ini2nginx.py --help`


##Links

NGINX Configuration:
    http://wiki.nginx.org/Configuration

..  vim: set ft=markdown tw=75 nocin nosi ai sw=4 ts=4 expandtab:
