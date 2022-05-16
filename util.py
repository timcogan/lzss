import os
import subprocess
from typing import Final, Optional


def get_git_sha(cwd: str) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=cwd).decode("ascii").strip()
    except Exception:
        return "Unknown"


def write_version_info(package_name: str) -> str:
    build_version: Final[Optional[str]] = os.getenv(f"{package_name.upper()}_BUILD_VERSION")
    build_number: Final[Optional[str]] = os.getenv(f"{package_name.upper()}_BUILD_NUMBER")
    cwd: Final[str] = os.getcwd()

    version: str = open("version.txt", "r").read().strip()
    sha: str = get_git_sha(cwd)

    if build_version is not None:
        assert build_number is not None, "A build number must accompany a build version"
        if int(build_number) > 1:
            version += ".post" + build_number
        version = build_version
    elif sha != "Unknown":
        version += "+" + sha[:7]

    version_path = os.path.join(cwd, package_name, "version.py")
    with open(version_path, "w") as f:
        f.write("__version__ = '{}'\n".format(version))
        f.write("git_commit_hash = {}\n".format(repr(sha)))

    return version
