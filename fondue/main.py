#!/usr/bin/env python
import argparse
import importlib
import os
import yaml

from fondue import __version__
from fondue.logging import init_logging
import fondue.core as core

import logging

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Global actions
    parser.add_argument('--version', help='Display the Fondue version', action='version', version=__version__)

    # Global options
    parser.add_argument('--verbose', help='More info messages', action='store_true')
    parser.add_argument('--monochrome', help='Don\'t use color for messages', action='store_true')

    # core operations
    parser_core = subparsers.add_parser('core', help='Work with Fondue core files')
    core_subparsers = parser_core.add_subparsers()
    parser_core_init = core_subparsers.add_parser('init', help='Create a new core file from a template')
    parser_core_init.add_argument('name', help='The name of the core')
    parser_core_init.add_argument('--vendor', help='The vendor of the core (used in VLNV)')
    parser_core_init.add_argument('--library', help='The library of the core (used in VLNV)')
    parser_core_init.add_argument('--version', help='The version of the core (used in VLNV)')
    parser_core_init.add_argument('--directory', help="The directory in which to create the core (defaults to 'name'")
    parser_core_init.set_defaults(func=core.init)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        return args
    else:
        parser.print_help()
        return None

def main():

    args = parse_args()
    if not args:
        exit(0)

    init_logging(args.verbose, args.monochrome)

    # Run the function
    args.func(args)

if __name__ == "__main__":
    main()
