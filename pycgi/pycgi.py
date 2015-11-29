# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from errno import EACCES
from os import remove
from os.path import dirname, exists, isfile, join
from subprocess import check_output, CalledProcessError
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
    # Installing Apache 2
    local("echo \"Y\" | sudo apt-get install apache2")
    # Disable multithreading processes
    local("sudo a2dismod mpm_event")
    # Give Apache explicit permission to run scripts
    local("sudo a2enmod mpm_prefork cgi")
    # Configuration
    config_file_abs_path = "/etc/apache2/sites-enabled/000-default.conf"
    if exists(config_file_abs_path) and isfile(config_file_abs_path):
        try:
            with open(config_file_abs_path, 'r') as f:
                config_file_lines = f.readlines()
        except Exception as exception: # Python3 PermissionError
            error_code = exception.errno
            if error_code == EACCES: # 13
                print(messages["_error_NoRoot"])
                exit(1)
            else:
                print(messages["_error_Oops"] % strerror(error_code))
                exit(1)
    try:
        with open(config_file_abs_path, 'w') as f:
            for line in config_file_lines:
                f.write(line)
                line_strip = line.strip()
                if line_strip == "<VirtualHost *:80>":
                    f.write("\t<Directory /var/www/html>\n")
                    f.write("\t\tOptions +ExecCGI\n")
                    f.write("\t\tDirectoryIndex index.html\n")
                    f.write("\t</Directory>\n")
                    f.write("\tAddHandler cgi-script .py\n")
    except Exception as exception: # Python3 PermissionError
        error_code = exception.errno
        if error_code == EACCES: # 13
            print(messages["_error_NoRoot"])
            exit(1)
        else:
            print(messages["_error_Oops"] % strerror(error_code))
            exit(1)
    # Restart Apache
    local("sudo service apache2 restart")
    # Output
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
                        version="cgi 0.1a3")
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
