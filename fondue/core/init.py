import os
import errno
import logging
import shutil
import collections
import distutils.dir_util
import copy
from os import listdir
from os.path import exists, isdir
from distutils.errors import DistutilsFileError
from tempfile import TemporaryDirectory

from fondue.templates import TemplateRepo
from fondue.core import core_command_collector

logger = logging.getLogger(__name__)


@core_command_collector.register()
def add_arguments(subparsers):
    parser_core_init = subparsers.add_parser(
        'init', help='Create a new core file from a template')
    parser_core_init.add_argument('name', help='The name of the core')
    parser_core_init.add_argument(
        '--vendor', help='The vendor of the core (used in VLNV)')
    parser_core_init.add_argument(
        '--library', help='The library of the core (used in VLNV)')
    parser_core_init.add_argument(
        '--version', help='The version of the core (used in VLNV)')
    parser_core_init.add_argument(
        '--sim-tool', help='The sim tool template to use',
        choices=['verilator'])
    parser_core_init.add_argument(
        '--directory',
        help="The directory in which to create the core (defaults to 'name'"
    )
    parser_core_init.set_defaults(func=run)


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
        file_name = file_name.replace('name', args.name)
        template.repo.render_template(
            template,
            os.path.join(directory, file_name),
            vars(args),
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


def _gather_templates(args):
    # default template
    template_repo = TemplateRepo('core_init/default')

    # default tool
    templates = template_repo.get_templates('default')

    if args.sim_tool:
        sim_templates = template_repo.get_templates(args.sim_tool)
        for (name, template) in sim_templates.items():
            if name in templates:
                base_template = templates[name]
                template.set_parent(base_template)
            templates[name] = template

    return templates


def run(args):
    if args.directory:
        directory = os.path.expanduser(args.directory)
    else:
        directory = args.name

    _validate_directory(directory)

    with TemporaryDirectory() as tmpdir:
        templates = _gather_templates(args)

        _render_templates(templates, args, tmpdir)

        _commit_directory(tmpdir, directory)
