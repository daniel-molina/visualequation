# visualequation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# visualequation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import setuptools
import setuptools.command.build_py
import subprocess
import glob

from visualequation import commons

with open("README.md", "r") as fh:
    long_description = fh.read()

class BuildPyCommand(setuptools.command.build_py.build_py):
    def run(self):
        subprocess.call(['./populate_symbols.py'])
        setuptools.command.build_py.build_py.run(self)

setuptools.setup(
    name="visualequation",
    version=commons.VERSION,
    author="Daniel Molina",
    author_email="lluvia@autistici.org",
    description="An equation editor powered by LaTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniel-molina/visualequation",
    packages=setuptools.find_packages(exclude=['tests']),
    test_suite='tests',
    cmdclass={'build_py':BuildPyCommand},
    entry_points={
        'gui_scripts': ['visualequation = visualequation.__main__:main']
    },
    data_files=[
        ('share/applications', ['data/visualequation.desktop']),
        ('share/visualequation', ['data/eq_template.tex',
                                  'data/visualequation.png',
                                  'data/USAGE.html',]),
        ('share/visualequation/icons', glob.glob('data/icons/*.png')),
    ],
    #zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
    ],
    keywords='mathematics equation editor latex wysiwyg formulas'
)
