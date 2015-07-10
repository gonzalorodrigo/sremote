"""
Installer for remoting lib
"""

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
# added command classes

# Do the setup
setup(
    name="sremote",
    packages=find_packages(),
    version="0.13",
    # install_requires=[s.strip() for s in open("requirements.txt")],
    extras_require={},
    package_data={"sremote": ["res/*.*"]},
    author="Gonzalo Rodrigo",
    author_email="GPRodrigoAlvarez@lbl.gov",
    maintainer="Gonzalo Rodrigo",
    url="https://github.com/gonzalorodrigo/qdo_interpreter",
    license="BSD 3-clause",
    description="Simple Remote",
    long_description="A Simple Remote layer to execute Python code remotely. "+
        "It only supports package calls to methods with serializable "
        +"arguments and return types.",
    keywords=["remoting"],
    #py_modules = ['sremote', 'sremote.api', 'sremote.tools'],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Distributed systems",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    ext_modules=[],
    #cmdclass = {
    #    "doc": BuildDocumentation,
    #},
)
