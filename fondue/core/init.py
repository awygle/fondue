import os
import errno
import logging
import shutil
import collections
import distutils.dir_util
import copy
import pkg_resources
from os import listdir
from os.path import exists, isdir
from distutils.errors import DistutilsFileError
from tempfile import TemporaryDirectory

from fondue.templates import TemplateRepo

import click

logger = logging.getLogger(__name__)


def _validate_directory(directory):
    """Validate directory for new core.

    Directory must not exist OR must exist, be a directory, and be empty.
    """

    if exists(directory):
        if not isdir(directory):
            message = f"Cannot create directory '{directory}': not a directory"
            logger.error(message)
            raise FileExistsError(
                errno.EEXIST,
                message
            )
        elif listdir(directory):
            message = (
                f"Cannot create directory '{directory}': "
                "directory exists and is not empty"
            )
            logger.error(message)
            raise FileExistsError(
                errno.EEXIST,
                message
            )


def _render_templates(templates, arguments, directory):
    for (path, template) in templates.items():
        args = copy.copy(arguments)
        if template.parent:
            base = template.parent
        else:
            base = None

        file_name = os.path.splitext(path)[0]  # remove j2 suffix
        file_name = file_name.replace('name', args['name'])
        template.repo.render_template(
            template,
            os.path.join(directory, file_name),
            args,
            base=base
        )


def _commit_directory(source, dest):
    _validate_directory(dest)

    try:
        distutils.dir_util.copy_tree(source, dest)
    except DistutilsFileError as e:
        logger.error(
            f"Error committing to directory '{directory}' "
            f"(race condition): {e.args[0]}"
        )
        raise


def _update_templates(orig_templates, new_templates):
    for (name, template) in new_templates.items():
        if name in orig_templates:
            base_template = orig_templates[name]
            template.set_parent(base_template)
        orig_templates[name] = template


def _gather_templates(args):
    # default template
    template_repo = TemplateRepo('core_init/default')

    # default tool
    templates = template_repo.get_templates('default')

    # default sim templates
    if args['sim_tool']:
        sim_templates = template_repo.get_templates(args['sim_tool'])
        _update_templates(templates, sim_templates)

    # top-level template
    if args['template']:
        template_repo = TemplateRepo('core_init/' + args['template'])
        top_templates = template_repo.get_templates('default')
        _update_templates(templates, top_templates)

        # top-level sim templates
        if args['sim_tool']:
            sim_templates = template_repo.get_templates(args['sim_tool'])
            _update_templates(templates, sim_templates)

    return templates


@click.command('init',
               options_metavar="[<options>]",
               short_help='Initializes a core.')
@click.argument("name", metavar="<name>")
@click.option("--vendor", help="The vendor of the core (used in VLNV)")
@click.option("--library", help="The library of the core (used in VLNV)")
@click.option("--version", help="The version of the core (used in VLNV)")
@click.option("--template", help="The top-level template to use")
@click.option("--sim-tool", help="The sim tool template to use")
@click.option("--directory",
              help="The directory in which to create the core "
              "(defaults to <name>)",
              default=None, type=click.Path())
def cmd(**kwargs):
    run(kwargs)


def run(args):
    """ This command initializes a new fondue core file.

        The <name> argument is the name of the core to be created.
    """
    print(args)
    if args['directory']:
        directory = os.path.expanduser(args['directory'])
    else:
        directory = args['name']

    _validate_directory(directory)

    with TemporaryDirectory() as tmpdir:
        templates = _gather_templates(args)

        _render_templates(templates, args, tmpdir)

        _commit_directory(tmpdir, directory)
