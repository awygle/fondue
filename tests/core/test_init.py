import pytest

import fondue.core as core

import tempfile
import errno
import os.path
import shutil
import logging
from argparse import Namespace

def test_empty_directory():
    with tempfile.TemporaryDirectory() as target_dir:
        args = Namespace()
        args.directory = target_dir
        args.name = 'test_core'
        
        core.init(args)
    
    # No exception indicates success

def test_nonempty_directory():
    with tempfile.TemporaryDirectory() as target_dir:
        with tempfile.TemporaryFile(mode="w+", dir=target_dir, delete=False) as f:
            f.write("nope")
        
        args = Namespace()
        args.directory = target_dir
        args.name = 'test_core'
        
        try:
            core.init(args)
        except FileExistsError as e:
            assert e.errno == errno.EEXIST
            assert "Failed to create directory '{}': directory exists and is not empty".format(args.directory) == e.strerror
        else:
            assert False

def test_file():
    with tempfile.NamedTemporaryFile(mode="w+") as f:
        f.write("nope")
    
        args = Namespace()
        args.directory = f.name
        args.name = 'test_core'
        
        try:
            core.init(args)
        except FileExistsError as e:
            assert e.errno == errno.EEXIST
            assert "Failed to create directory '{}': not a directory".format(args.directory) == e.strerror
        else:
            assert False

def test_creation():
    with tempfile.TemporaryDirectory() as target_dir:
        args = Namespace()
        args.directory = target_dir
        args.name = 'test_core'
        
        core.init(args)
        
        core_path = os.path.join(target_dir, "test_core.ffc")
        verilog_path = os.path.join(target_dir, "test_core.v")
        
        assert os.path.exists(core_path) and not os.path.isdir(core_path)
        assert os.path.exists(verilog_path) and not os.path.isdir(core_path)

def test_golden():
    with tempfile.TemporaryDirectory() as target_dir:
        args = Namespace()
        args.directory = target_dir
        args.name = 'test_core'
        
        core.init(args)
        
        core_path = os.path.join(target_dir, "test_core.ffc")
        verilog_path = os.path.join(target_dir, "test_core.v")
        
        assert os.path.exists(core_path) and not os.path.isdir(core_path)
        assert os.path.exists(verilog_path) and not os.path.isdir(core_path)
        
        cwd = os.path.dirname(__file__)
        golden_core = os.path.join(cwd, 'golden.ffc')
        golden_verilog = os.path.join(cwd, 'golden.v')
        with open(core_path) as fgen, open(golden_core) as fref:
            assert fref.read() == fgen.read()
        with open(verilog_path) as fgen, open(golden_verilog) as fref:
            assert fref.read() == fgen.read()
