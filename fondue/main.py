#!/usr/bin/env python
import argparse
import importlib
import os
import yaml

import gather

from fondue import __version__
from fondue.logging import init_logging

import logging

logger = logging.getLogger(__name__)


topic_collector = gather.Collector()


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Global actions
    parser.add_argument('--version', help='Display the Fondue version',
                        action='version', version=__version__)

    # Global options
    parser.add_argument(
        '--verbose', '-v',
        help='More info messages',
        action='store_true'
    )
    parser.add_argument(
        '--monochrome',
        help='Don\'t use color for messages',
        action='store_true'
    )

    for (topic, function) in topic_collector.collect().items():
        logger.info(f"Adding arguments for topic '{topic}'")
        function(subparsers)

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
    try:
        args.func(args)
    except Exception as e:
        logger.debug(e)
        try:
            exit(e.errno)
        except Exception:
            exit(1)


if __name__ == "__main__":
    main()
