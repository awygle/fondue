#!/usr/bin/env python
import click
import importlib
import os
import yaml

from fondue import __version__
from fondue.logging import init_logging

import logging

logger = logging.getLogger(__name__)


class ComplexCLI(click.MultiCommand):
    def __init__(self, filename, module, *args, **kwargs):
        self._module_dir = os.path.dirname(filename)
        self._module_name = module
        self._cmds = {}
        super().__init__(*args, **kwargs)
        
        exclude_subdirs = ['static']
        exclude_files = []
        for root, dirs, files in os.walk(self._module_dir):
            root = os.path.relpath(root, self._module_dir)
            dirs = [x for x in dirs if not x.startswith('_') and not x.startswith('.') and x not in exclude_subdirs]
            files = [x for x in files if not x.startswith('_') and not x.startswith('.') and x not in exclude_files]
            for d in dirs:
                name = os.path.basename(d)
                try:
                    mod = importlib.import_module('fondue.'+name)
                    self._cmds[name] = mod.group
                except ImportError:
                    pass
                except AttributeError:
                    pass
            for f in files:
                name = f[:-3]
                try:
                    mod = importlib.import_module('.'+name, self._module_name)
                    self._cmds[name] = mod.run
                except ImportError:
                    pass
                except AttributeError:
                    pass
        
    def list_commands(self, ctx):
        return self._cmds.keys()
    
    def get_command(self, ctx, name):
        return self._cmds[name]

@click.command(cls=ComplexCLI, filename=__file__, module=__name__)
@click.option("--verbose", "-v", default=False, help='More verbose logging', is_flag=True)
@click.option("--monochrome", default=False, help="Don't use color for messages", is_flag=True)
@click.pass_context
def main(ctx, verbose, monochrome):

    init_logging(verbose, monochrome)

if __name__ == "__main__":
    main()
