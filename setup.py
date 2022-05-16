from typing import Dict, Final, List

from setuptools import find_packages, setup

from util import write_version_info

package_name: Final[str] = "lz77"


requirements: Final[List[str]] = [
    "bitarray==0.8.1",
]

extras: Final[Dict[str, List[str]]] = {
    "dev": ["pytest", "flake8", "black", "autoflake", "autopep8", "isort", "coverage"],
    "doc": [],
}

setup(
    name=package_name,
    version=write_version_info(package_name),
    packages=find_packages(),
    install_requires=requirements,
    extras_require=extras,
    python_requires=">=3.10.0",
)
