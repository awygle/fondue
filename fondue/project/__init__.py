import logging
import click
import os

from fondue.main import ComplexCLI

logger = logging.getLogger(__name__)

group = ComplexCLI(__file__, __name__)

def add_arguments(subparsers):
    # project operations
    parser_project = subparsers.add_parser(
        'project', help='Work with Fondue project files')
    project_subparsers = parser_project.add_subparsers()

    commands = project_command_collector.collect().items()

    for (command, function) in commands:
        logger.info(f"Topic 'project' adding arguments for command {command}")
        function(project_subparsers)
