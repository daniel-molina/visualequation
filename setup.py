import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visualequation",
    version="0.2.0",
    author="Daniel Molina",
    author_email="lluvia@autistici.org",
    description="An equation editor powered by LaTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daniel-molina/visualequation",
    packages=setuptools.find_packages(exclude=['tests']),
    test_suite='tests',
    entry_points={
        'gui_scripts': ['visualequation = visualequation.__main__:main']
    },
    package_data={'visualequation': ['data/eq_template.tex', 'data/symbols/*']},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
    ],
    keywords='mathematics equation editor latex wysiwyg formulas'
)
