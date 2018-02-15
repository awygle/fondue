import os
import errno

import logging

logger = logging.getLogger(__name__)

from fondue.utils import render_template

def init(args):
    if args.directory:
        directory = os.path.expanduser(args.directory)
    else:
        directory = args.name
    
    try:
        os.makedirs(directory)
    except FileExistsError as e:
        if e.errno == errno.EEXIST:
            if os.path.isdir(directory):
                if os.listdir(directory):
                    logger.error("Failed to create directory '{}': directory exists and is not empty".format(directory))
                    exit(1)
            else:
                logger.error("Failed to create directory '{}': {}".format(directory, e.strerror))
                exit(1)
    
    core_file_name = os.path.join(directory, args.name + '.ffc')
    render_template('core_init/default.ffc.j2', core_file_name, vars(args))
    verilog_file_name = os.path.join(directory, args.name + '.v')
    render_template('core_init/default.v.j2', verilog_file_name, vars(args))
