import logging
import click
import os

from fondue.main import ComplexCLI

logger = logging.getLogger(__name__)

group = ComplexCLI(__file__, __name__, short_help="Work with project files.")
