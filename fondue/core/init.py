import os
import errno
import logging
import shutil
import collections
import distutils.dir_util
from os import listdir
from os.path import exists, isdir
from distutils.errors import DistutilsFileError
from tempfile import TemporaryDirectory

from fondue.templates import TemplateRepo
from fondue.core import core_command_collector

logger = logging.getLogger(__name__)


init_template_repo = TemplateRepo('core_init')

Template = collections.namedtuple('Template', 'template_name file_name')


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
            message = (
                "Cannot create directory '{}': "
                "not a directory"
            ).format(directory)
            logger.error(message)
            raise FileExistsError(
                errno.EEXIST,
                message
            )
        elif listdir(directory):
            message = (
                "Cannot create directory '{}': "
                "directory exists and is not empty"
            ).format(directory)
            logger.error(message)
            raise FileExistsError(
                errno.EEXIST,
                message
            )


def _build_templates(template_sources, core_name):
    result = []
    for source in template_sources:
        for template_name in init_template_repo.get_templates(source):
            # remove j2 suffix
            file_name = os.path.splitext(os.path.basename(template_name))[0]
            file_name = file_name.replace(source, core_name)
            result.append(Template(template_name, file_name))
    return result


def _render_templates(templates, arguments, directory):
    for template in templates:
        init_template_repo.render_template(
            template.template_name,
            os.path.join(directory, template.file_name),
            arguments
        )


def _commit_directory(source, dest):
    _validate_directory(dest)

    try:
        distutils.dir_util.copy_tree(source, dest)
    except DistutilsFileError as e:
        logger.error("Error committing to directory '{}' (race condition): {}"
                     .format(dest, e.args[0]))
        raise


def run(args):
    if args.directory:
        directory = os.path.expanduser(args.directory)
    else:
        directory = args.name

    _validate_directory(directory)

    with TemporaryDirectory() as tmpdir:
        template_sources = [args.sim_tool, 'default']
        template_sources = [x for x in template_sources if x is not None]
        templates = _build_templates(template_sources, args.name)

        _render_templates(templates, vars(args), tmpdir)

        _commit_directory(tmpdir, directory)
