import argparse
import os
import subprocess
import requests
import yaml

utility_dir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()


def load_configuration():
    #pass
    configuration = {}
    with open(utility_dir + "/default.config.yml", 'r') as stream:
        configuration = yaml.load(stream)
    
    print(configuration)
    #configuration.update(yaml.load(os.getcwd() + './documentation.config.yaml'))
    return configuration

# Install dependencies
def install_dependencies():
    print("Updating dependencies")
    result = subprocess.run(["pip3", "install", "-r", utility_dir + "/requirements.txt"])
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
        return False

        # TODO: Keep below or not? Lets not install node for users and if no node installed, pretend we don't do JSdoc.
        result_download = subprocess.run(["curl", "http://nodejs.org/dist/node-latest.tar.gz", "-o", utility_dir + "/node-latest.tar.gz"])
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
    os.chdir(utility_dir)
    result_install_jsdoc_sphinx = subprocess.run(["npm", "install", "jsdoc", "jsdoc-sphinx"])
    os.chdir(current_dir)
    if result_install_jsdoc_sphinx.returncode == 0:
        return True
    else:
        return False


def generate_jsdoc_rsts():
    print("Compiling JSDoc reference to RST,")
    print(current_dir)
    print(configuration.get('javascript_root_directory',''))
    result = subprocess.run([
        utility_dir + "/node_modules/.bin/jsdoc",
        "-t", utility_dir + "/node_modules/jsdoc-sphinx/template",
        "-d", utility_dir + "/docs/jsdoc",
        "-c", utility_dir + "/jsdoc.config.json",
        "-r",
        current_dir + "/" + configuration.get('javascript_root_directory','')])

def run_build():
    print("Running build")
    result = subprocess.run(["sphinx-build", "-b", "html", utility_dir + "/docs", utility_dir + "/docs/documentation_build"])
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

configuration = load_configuration()
js_install_successfull = install_node_js()

if js_install_successfull:
    js_dependencies_install_successfull = install_js_dependencies() # Make sure JSDoc and JSDoc-sphinx installed
    generate_jsdoc_rsts()

build_successful = run_build()

print("Finished successfully. Shutting down.")