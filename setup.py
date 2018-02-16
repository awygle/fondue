import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="fondue",
    packages=['fondue',
              'fondue.tools',
              'fondue.provider'],
    use_scm_version={
        "relative_to": __file__,
        "write_to": "fondue/version.py",
    },
    author="Andrew Wygle",
    author_email="awygle@gmail.com",
    description=(
        "Fondue is a package manager and a set of build tools for HDL"
        "(Hardware Description Language) code."
        ),
    license="GPLv3",
    keywords=[
        "VHDL",
        "verilog",
        "hdl",
        "rtl",
        "synthesis",
        "FPGA",
        "simulation",
        "Xilinx",
        "Altera",
        "Lattice"
        ],
    url="https://github.com/awygle/fondue",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        'console_scripts': [
            'fondue = fondue.main:main'
        ]
    },
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'pyyaml',
    ],
)
