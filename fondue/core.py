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
        os.makedirs(directory, exist_ok=True)
    except FileExistsError as e:
        raise FileExistsError(e.errno, "Failed to create directory '{}': not a directory".format(directory))
    except Exception as e:
        raise type(e)("Failed to create directory '{}': {}".format(directory, e.args[0]))
    
    if os.listdir(directory):
        raise FileExistsError(errno.EEXIST, "Failed to create directory '{}': directory exists and is not empty".format(directory))
    
    core_file_name = os.path.join(directory, args.name + '.ffc')
    render_template('core_init/default.ffc.j2', core_file_name, vars(args))
    verilog_file_name = os.path.join(directory, args.name + '.v')
    render_template('core_init/default.v.j2', verilog_file_name, vars(args))
