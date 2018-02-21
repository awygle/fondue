import logging
import gather

from fondue.main import topic_collector

logger = logging.getLogger(__name__)

core_command_collector = gather.Collector()


@topic_collector.register()
def add_arguments(subparsers):
    # core operations
    parser_core = subparsers.add_parser(
        'core', help='Work with Fondue core files')
    core_subparsers = parser_core.add_subparsers()

    commands = core_command_collector.collect().items()

    for (command, function) in commands:
        logger.info(f"Topic 'core' adding arguments for command {command}")
        function(core_subparsers)
