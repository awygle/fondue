import pytest

import fondue.core.init

import tempfile
import errno
import os.path
import shutil
import logging


def test_empty_directory():
    with tempfile.TemporaryDirectory() as target_dir:
        args = {}
        args['name'] = 'test_core'
        args['template'] = None
        args['sim_tool'] = None
        args['directory'] = target_dir

        fondue.core.init.run(args)

    # No exception indicates success


def test_nonempty_directory():
    with tempfile.TemporaryDirectory() as target_dir:
        with tempfile.NamedTemporaryFile(
                mode="w+",
                dir=target_dir,
                delete=False) as f:
            name = f.name
            f.write("nope")

        args = {}
        args['directory'] = target_dir
        args['name'] = 'test_core'
        args['sim_tool'] = None
        args['template'] = None

        try:
            fondue.core.init.run(args)
        except FileExistsError as e:
            assert e.errno == errno.EEXIST
            assert os.path.exists(target_dir) and os.path.isdir(target_dir)
            assert os.listdir(target_dir) == [os.path.basename(name)]
        else:
            assert False


def test_file():
    with tempfile.NamedTemporaryFile(mode="w+") as f:
        f.write("nope")

        args = {}
        args['directory'] = f.name
        args['name'] = 'test_core'
        args['sim_tool'] = None
        args['template'] = None

        try:
            fondue.core.init.run(args)
        except FileExistsError as e:
            assert e.errno == errno.EEXIST
            assert os.path.exists(f.name) and not os.path.isdir(f.name)
        else:
            assert False


def test_creation():
    with tempfile.TemporaryDirectory() as target_dir:
        args = {}
        args['directory'] = target_dir
        args['name'] = 'test_core'
        args['sim_tool'] = None
        args['template'] = None

        fondue.core.init.run(args)

        core_path = os.path.join(target_dir, "test_core.ffc")
        verilog_path = os.path.join(target_dir, "test_core.v")

        assert os.path.exists(core_path) and not os.path.isdir(core_path)
        assert os.path.exists(verilog_path) and not os.path.isdir(core_path)


def test_golden():
    with tempfile.TemporaryDirectory() as target_dir:
        args = {}
        args['directory'] = target_dir
        args['name'] = 'test_core'
        args['sim_tool'] = None
        args['template'] = None

        fondue.core.init.run(args)

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


def test_sim_tool():
    with tempfile.TemporaryDirectory() as target_dir:
        args = {}
        args['directory'] = target_dir
        args['name'] = 'test_core'
        args['sim_tool'] = 'verilator'
        args['template'] = None

        fondue.core.init.run(args)

        core_path = os.path.join(target_dir, "test_core.ffc")
        verilog_path = os.path.join(target_dir, "test_core.v")

        assert os.path.exists(core_path) and not os.path.isdir(core_path)
        assert os.path.exists(verilog_path) and not os.path.isdir(verilog_path)

        cpp_path = os.path.join(target_dir, "verilator-main.cpp")
        header_path = os.path.join(target_dir, "test_core.h")

        assert os.path.exists(cpp_path) and not os.path.isdir(cpp_path)
        assert os.path.exists(header_path) and not os.path.isdir(header_path)


def test_template():
    with tempfile.TemporaryDirectory() as target_dir:
        args = {}
        args['directory'] = target_dir
        args['name'] = 'test_core'
        args['sim_tool'] = None
        args['template'] = 'wb4-slave'

        fondue.core.init.run(args)

        core_path = os.path.join(target_dir, "test_core.ffc")
        verilog_path = os.path.join(target_dir, "test_core.v")

        assert os.path.exists(core_path) and not os.path.isdir(core_path)
        assert os.path.exists(verilog_path) and not os.path.isdir(verilog_path)

        with open(verilog_path) as fgen:
            assert 'wb_cyc_i' in fgen.read()
