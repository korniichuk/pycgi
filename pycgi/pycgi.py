# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from os.path import dirname, exists, isfile, join
from sys import argv, exit

from configobj import ConfigObj

try:
    from fabric.api import local
except ImportError:
    print("Error: No module named 'fabric'. You can install it by typing:\n"
          "    sudo pip install fabric")
    exit(1)

module_location = dirname(__file__)
config_pycgi_abs_path = join(module_location, "config/pycgi.ini")
config = ConfigObj(config_pycgi_abs_path)

argparse = {} # Strings for -h --help
messages = {} # Strings for output

def create_dictionaries():
    """Create "argparse" and "messages" dictionaries"""

    config_argparse_rel_path = config["config_argparse_rel_path"]
    config_argparse_abs_path = join(module_location, config_argparse_rel_path)
    config_messages_rel_path = config["config_messages_rel_path"]
    config_messages_abs_path = join(module_location, config_messages_rel_path)
    with open(config_argparse_abs_path, 'r') as f:
        argparse_list = f.read().splitlines()
    for i in range(0, len(argparse_list), 2):
        argparse[argparse_list[i]] = argparse_list[i+1]
    with open(config_messages_abs_path, 'r') as f:
        messages_list = f.read().splitlines()
    for i in range(0, len(messages_list), 2):
        messages[messages_list[i]] = messages_list[i+1]

def install():
    """Install the Python CGI"""

    # Update the Package Index
    local("sudo apt-get update")
    # Check pip
    try:
        pip_version = check_output("pip -V", shell=True)
    except CalledProcessError:
        # Install pip
        downloads_path = expanduser("~/Downloads")
        local("cd %s; wget https://bootstrap.pypa.io/get-pip.py" %
                downloads_path)
        local("cd %s; sudo python get-pip.py" % downloads_path)
        pip_path = join(downloads_path, "get-pip.py")
        if exists(pip_path) and isfile(pip_path):
            remove(pip_path)
    pass # TODO
    print(messages["_installed"])

def main():
    """Main function"""

    create_dictionaries()
    args = parse_command_line_args()
    args.function_name()

def parse_command_line_args():
    """Parse command line arguments"""

    # Create top parser
    parser = ArgumentParser(prog="cgi", description=argparse["_parser"],
                            add_help=True)
    parser.add_argument("-v", "--version", action="version",
                        version="cgi 0.1a1")
    # Create subparsers for the top parser
    subparsers = parser.add_subparsers(title=argparse["_subparsers"])
    # Create the parser for the "install" subcommand
    parser_install = subparsers.add_parser("install",
            description=argparse["_parser_install"],
            help=argparse["_parser_install"])
    parser_install.set_defaults(function_name=install)    
    if len(argv) == 1:
        parser.print_help()
        exit(0) # Clean exit without any errors/problems
    return parser.parse_args()
