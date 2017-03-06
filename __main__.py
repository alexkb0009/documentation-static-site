import argparse
import os
import subprocess
import requests
import yaml

# TODO: Load configs from command-line args and YAML into here. Replace like "./docs" w/ entries from YAML config.
configuration = {}

is_node_installed = False

def load_configuration():
    pass
    # TODO: Load YAML (PSUEDOCODE BELOW)
    #configuration = yaml.load(os.dirname(os.realpath(__file__)) + './default.config.yaml')
    #configuration.update(yaml.load(os.getcwd() + './documentation.config.yaml'))
    #yaml.load(os.getcwd() + './documentation.config.yaml')

# Install dependencies
def install_dependencies():
    print("Updating dependencies")
    result = subprocess.run(["pip3", "install", "-r", "./requirements.txt"])
    if (result.returncode == 0):
        print('Successfully installed dependencies!')
        return True
    else:
        result.check_returncode()
        return False

def install_node_js():

    try:
        result = subprocess.run(["node", "-v"])
        if result.returncode == 0:
            print("Node.js is installed.")
            is_node_installed = True
            return True
    except:
        # Not installed.
        is_node_installed = False
        return
        
        # TODO: Keep below or not? Lets not install node for users and if no node installed, pretend we don't do JSdoc.
        result_download = subprocess.run(["curl", "http://nodejs.org/dist/node-latest.tar.gz", "-o", "node-latest.tar.gz"])
        print(result_download)
        result_unpack = subprocess.run(["tar", "xvzf", "node-latest.tar.gz"])
        result_remove = subprocess.run(["rm", "node-latest.tar.gz"])
        current_dir = os.getcwd()
        child_dirs = os.listdir(current_dir)
        valid_child_dirs = [ d for d in child_dirs if 'node-v' in d ]
        if len(valid_child_dirs) < 1:
            raise Exception("No node installation available")
        #os.chdir(valid_child_dirs[0])
        result_config = subprocess.run(["./" + valid_child_dirs[0] + "/configure", "--prefix", current_dir + '/node-installation', '--with-intl', 'none'])
        result_install = subprocess.run(["make", "-C", valid_child_dirs[0]])
        # TODO: clean this up(?)

        if result_install.returncode == 0:
            return True
        else:
            return False
        
        print(os.getcwd())

def install_js_dependencies():
    result_install_jsdoc = subprocess.run(["npm", "install", "jsdoc"])
    result_install_jsdoc_sphinx = subprocess.run(["npm", "install", "jsdoc-sphinx"])
    if result_install_jsdoc_sphinx.returncode == 0:
        return True
    else:
        return False


def run_build():
    print("Running build")
    result = subprocess.run(["sphinx-build", "-b", "html", "./docs", "./docs/documentation_build"])
    if (result.returncode == 0):
        print('Successfully generated HTML files!')
        return True
    else:
        result.check_returncode()
        return False





print("Running document static site generator...")
install_successful = install_dependencies()

parser = argparse.ArgumentParser(description="Process options.")
args = parser.parse_args()
pass

if not install_successful:
    print("Shutting down")

# TODO: Figure out what's needed for RST files and /documentation/ dir.
# TODO: Generate /documentation/ dir full of required RST files.
#   TODO: Sphinx autodoc for PyDoc -> RST files
#   TODO: JSDoc-> RST Files


# TODO : Sphinx-build -> HTML
js_install_successfull = install_node_js()
js_dependencies_install_successfull = install_js_dependencies()
#build_successful = run_build()

print("Finished successfully. Shutting down.")