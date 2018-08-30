import logging
import click
import os

logger = logging.getLogger(__name__)

class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        fondue_dir = os.path.dirname(__file__)
        exclude_subdirs = ['static']
        rv = []
        for root, dirs, files in os.walk(fondue_dir):
            root = os.path.relpath(root, fondue_dir)
            dirs = [x for x in dirs if not x.startswith('_') and os.path.join(root, x)[2:] not in exclude_subdirs]
            if root == ".":
                continue
            if any(not filename.startswith('_') and filename.endswith('.py') for filename in files):
                rv.append(os.path.basename(root))
        rv.sort()
        return rv
    
    def get_command(self, ctx, name):
        print(name)
        try:
            mod = importlib.import_module('fondue.'+name)
        except ImportError as e:
            print(e)
            print('oops')
            return
        if "run" in mod.__dict__:
            return mod.run
        else:
            return mod.group
        
group = ComplexCLI()

def add_arguments(subparsers):
    # core operations
    parser_core = subparsers.add_parser(
        'core', help='Work with Fondue core files')
    core_subparsers = parser_core.add_subparsers()

    commands = core_command_collector.collect().items()

    for (command, function) in commands:
        logger.info(f"Topic 'core' adding arguments for command {command}")
        function(core_subparsers)
