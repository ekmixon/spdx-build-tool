from __future__ import print_function
from __future__ import unicode_literals
import glob
import fnmatch
import os
# from analyser.parsers.pip import parse_pip_requirement_string
from colorama import init
from colorama import Fore, Back
from re import compile as compile_regex
import shutil
import socket

SCANCODE_DOWNLOAD_PATH = "https://github.com/nexB/scancode-toolkit/releases/download/v2.2.1/scancode-toolkit-2.2.1.zip"
REMOTE_SERVER = "www.google.com"
TEMP_DIR = 'build_tool_tmp_dir'
SCANCODE_DIR = 'scancode-toolkit-2.2.1'
SUPPORTED_BUILD_TOOLS = [
    'npm', 'pip'
]

FILES_TO_CHECK_PER_TOOL = {
    'npm': ['package.json'],
    'pip': ['requirements*.txt', 'setup.py']
}

FILES_TO_PARSE_PER_TOOL = {
    'npm': ['package.json'],
    'pip': ['requirements*.txt']
}

FILES_TO_CHECK_PER_BUILD = {
    'package.json': 'npm',
    'requirements*.txt': 'pip',
    'setup.py': 'pip'
}

HOME_PAGE_URL = {
    'npm': "https://www.npmjs.com/",
    'pip': "https://pip.pypa.io/"
}

PRIMARY_LANGUAGE = {
    'npm': "JavaScript",
    'pip': "Python"
}

COLORAMA_PRINT_TYPES = ["notification", "success", "failure", "information"]

COLORAMA_PRINT_COLOR = {
    "notification": Fore.BLUE,
    "success": Fore.GREEN,
    "failure": Fore.RED,
    "information": Fore.CYAN,
    "title": Back.BLUE,
}


def normalize_path(path):
    """
    Normalize ``path``.

    It returns ``path`` with leading and trailing slashes, and no multiple
    continuous slashes.

    """
    if path:
        if path[0] != "/":
            path = f"/{path}"

        if path[-1] != "/":
            path = f"{path}/"

        path = _MULTIPLE_PATHS.sub("/", path)
    else:
        path = "/"

    return path


def normalize_file_path(path):
    """
    Normalize ``file path``.

    It returns ``path`` with leading but no trailing slashes, and no multiple
    continuous slashes.

    """
    if path:
        if path[0] != "/":
            path = f"/{path}"

        path = _MULTIPLE_PATHS.sub("/", path)
    else:
        path = "/"

    return path


def check_file(project_dir, filename_to_check):
    """recursively check if file exists in directory"""
    matches = []
    for root, dirnames, filenames in os.walk(project_dir):
        matches.extend(
            os.path.join(root, filename)
            for filename in fnmatch.filter(filenames, filename_to_check)
        )

    return matches


def check_file_in_dir(project_dir, file_name_to_check):
    """Check if file exists in directory."""
    matches = list(
        glob.glob(
            '{0}/{1}'.format(project_dir, file_name_to_check), recursive=False
        )
    )

    return [normalize_file_path(item) for item in matches]


def print_to_command_line(msg, print_type):
    """Colorama wrapper to print output to the command line"""
    try:
        import colorama
        init(autoreset=True)
        print(COLORAMA_PRINT_COLOR[print_type] + msg + colorama.Fore.RESET)
    except ImportError:
        print(msg)
    return


_MULTIPLE_PATHS = compile_regex(r"/{2,}")


def create_tmp_dir(project_dir):
    temp_directory = '{0}{1}'.format(normalize_path(project_dir), TEMP_DIR)
    os.makedirs(temp_directory, exist_ok=True)
    return


def delete_tmp_dir(project_dir):
    temp_directory = '{0}{1}'.format(normalize_path(project_dir), TEMP_DIR)
    scancode_directory = '{0}{1}'.format(normalize_path(project_dir), SCANCODE_DIR)
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)
    if os.path.exists(scancode_directory):
        shutil.rmtree(scancode_directory)
    return


def determine_build_tool(project_directory_to_scan):
    """
    This method shall return the build tool(s) currently used by the software package being built
    """
    matching_file_list = []
    project_type_list = []
    for file_name_to_check in FILES_TO_CHECK_PER_BUILD.keys():
        matched_list = check_file_in_dir(
            project_directory_to_scan, file_name_to_check)
        matching_file_list.append(matched_list)
        if len(matched_list) != 0:
            project_type_list.append(
                FILES_TO_CHECK_PER_BUILD[file_name_to_check])
    print(project_type_list, matching_file_list)
    return (project_type_list, matching_file_list)


def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
