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


def _validate_directory(directory, name):
    """Validate directory for new project.

    Directory must not exist, or must exist, be a directory, and not contain a
    file name which conflicts with the project file to be created.
    """

    if exists(directory):
        if not isdir(directory):
            message = f"Cannot create directory '{directory}': not a directory"
            logger.error(message)
            raise FileExistsError(
                errno.EEXIST,
                message
            )
        elif name in listdir(directory):
            message = (
                f"Cannot create project file '{name}' "
                "in directory '{directory}': "
                "directory already contains a file named '{name}'"
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


def _update_templates(orig_templates, new_templates):
    for (name, template) in new_templates.items():
        if name in orig_templates:
            base_template = orig_templates[name]
            template.set_parent(base_template)
        orig_templates[name] = template


def _gather_templates(args):
    # default template
    template_repo = TemplateRepo('project_init/default')

    # default tool
    templates = template_repo.get_templates('default')

    # default sim templates
    if args['sim_tool']:
        sim_templates = template_repo.get_templates(args['sim_tool'])
        _update_templates(templates, sim_templates)

    # top-level template
    if args['template']:
        template_repo = TemplateRepo('project_init/' + args['template'])
        top_templates = template_repo.get_templates('default')
        _update_templates(templates, top_templates)

        # top-level sim templates
        if args['sim_tool']:
            sim_templates = template_repo.get_templates(args['sim_tool'])
            _update_templates(templates, sim_templates)

    return templates


templates = pkg_resources.resource_listdir('fondue',
                                           'static/templates/project_init')


@click.command('init', short_help='Initializes a project')
@click.argument('name', metavar='<name>')
@click.option("--template", help="The top-level template to use")
@click.option("--sim-tool", help="The sim tool template to use")
@click.option("--template",
              help="The top-level template to use",
              type=click.Choice(templates))
@click.option("--sim-tool",
              help="The sim tool template to use",
              type=click.Choice(['verilator']))
@click.option("--directory",
              help="The directory in which to create the project "
              "(defaults to the current directory)",
              default=None, type=click.Path())
def cmd(**kwargs):
    run(kwargs)


def run(args):
    if args['directory']:
        directory = os.path.expanduser(args['directory'])
    else:
        directory = os.getcwd()

    _validate_directory(directory)

    templates = _gather_templates(args)

    _render_templates(templates, args, directory)
