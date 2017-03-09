import argparse
import os
import subprocess
import requests
import yaml
import shutil
from jinja2 import Environment, PackageLoader, select_autoescape

utility_dir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()
jinja_env = Environment(
    autoescape=select_autoescape(['html', 'xml']),
    loader=PackageLoader(__name__, '.')
)


def load_configuration():
    #pass
    configuration = {}
    project_config = None
    with open(utility_dir + "/default.config.yml", 'r') as stream:
        configuration = yaml.load(stream)

    try:
        with open(current_dir + "/documentation.config.yml", 'r') as stream:
            project_config = yaml.load(stream)
        if project_config is not None:
            configuration.update(project_config)
    except Exception as e:
        print(e)

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
            print("Node.js is installed. Will create JS API Reference.")
            is_node_installed = True
            return True
    except:
        print("Node.js is NOT installed. Will NOT create JS API Reference.")
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


def cleanup_rst_directory():
    for root, dirs, files in os.walk(utility_dir + '/generated_docs', topdown=False):
        for name in files:
            if name == 'conf.py' and root == utility_dir + '/generated_docs':
                continue
            else:
                os.remove(os.path.join(root, name))
        for name in dirs:
            if name not in ['documentation_static', 'documentation_templates']:
                os.rmdir(os.path.join(root, name))


def generate_jsdoc_rsts():
    print("Compiling JSDoc reference to RST,")
    print(current_dir)
    print(configuration.get('javascript_root_directory',''))
    result = subprocess.run([
        utility_dir + "/node_modules/.bin/jsdoc",
        "-t", utility_dir + "/jsdoc-sphinx-template",
        "-d", utility_dir + "/generated_docs/jsdoc",
        "-c", utility_dir + "/jsdoc.config.json",
        "-r",
        current_dir + "/" + configuration.get('javascript_root_directory','')])


def add_path_to_conf(python_dir):
    old = utility_dir + '/generated_docs/conf.py'
    new = utility_dir + '/generated_docs/tmp_conf.py'
    done = False
    # first check the file to see if it already has a sys.path.insert line
    with open(old, 'r') as o:
        for line in o:
            if line.startswith('sys.path.insert'):
                done = True
                break
                #if configuration.get('python_project_directory') in line:
                #    done = True
                #    break
    if not done:
        with open(old, 'r') as f:
            with open(new, 'w') as w:
                blank = False
                for line in f:
                    w.write(line)
                    if not line.startswith('#'):
                        if not blank:
                            #TODO : Change to this AND array of configuration.sys_inserts. See bin/pserve in fourfront repository.
                            comm = "import os\nimport sys\nsys.path.insert(0, '" + os.path.abspath(current_dir + '/' + configuration.get('python_project_directory','.') + '/..') + "')\n"
                            w.write(comm)
                            blank = True
        os.rename(new, old)


def generate_pydoc_rsts():
    print("Compiling PyDoc reference to RST, ")
    python_dir = os.path.abspath(current_dir + '/' + configuration.get('python_project_directory','.'))
    
    result = subprocess.run([
        'sphinx-apidoc', '-e', '-a', '--implicit-namespaces',
        "-H", "Python API Reference",
        "-V", str(configuration.get('project_version', "1")),
        "-A", configuration.get('project_author', "HMS-DBMI"),
        '-o', utility_dir + '/generated_docs/pydoc',
        python_dir
    ])
    add_path_to_conf(python_dir)

def copy_static_docs():
    sections_with_docs = []
    for section in configuration.get('sections', []):
        #print(section['path'])
        #print(os.path.abspath(utility_dir + "/generated_docs/" + section['saveAs']))
        if os.path.isfile(section['path']):
            sections_with_docs.append(section)
            shutil.copyfile(section['path'], os.path.abspath(utility_dir + "/generated_docs/" + section['saveAs']))
        else:
            print("Could not find '" + str(section['path']) + "' in current directory '" + str(current_dir) + "'.")
    return sections_with_docs

def generate_static_docs_index_rst():
    template = jinja_env.get_template("static_docs_index_template.rst")
    with open(utility_dir + "/generated_docs/static_documentation_contents.rst", 'w') as indexFile:
        indexFile.write(template.render(
            title = str(configuration.get("homepage_toc_sections_title", "Documents")),
            sections = [ s for s in sections if s['saveAs'][0:6].lower() != 'readme' ]
        ))

def generate_index_rst():
    template = jinja_env.get_template("index_template.rst")
    with open(utility_dir + "/generated_docs/index.rst", 'w') as indexFile:
        indexFile.write(template.render(
            title=str(configuration.get("homepage_toc_title", "Documentation")),
            js_is_documented=js_install_successfull,
            sections = sections,
            readme = os.path.abspath(utility_dir + '/generated_docs/' + readmePath)
        ))


def run_build():
    from datetime import date
    print("Running build")
    target_html_directory = os.path.abspath(current_dir + '/' + configuration.get('output_directory',"generated_documentation"))
    result = subprocess.run([
        "sphinx-build",
        "-b", "html",
        "-D", "project=" + configuration.get('project_name',"No Project Name Specified"),
        "-D", "author=" + configuration.get('project_author', "HMS-DBMI"),
        "-D", "copyright=" + str(date.today().year) + ", " + configuration.get('project_author', "HMS-DBMI"),
        utility_dir + "/generated_docs",
        target_html_directory
    ])
    if (result.returncode == 0):
        print("Successfully generated HTML documentation to '" + target_html_directory + "/index.html'.")
        print("Point your browser to that file ^.")
        #print("  Copy & paste it to gh-pages branch.\n  Upload it to an S3 bucket, or anywhere else, and point a subdomain to it.")
        return True
    else:
        print("Something somewhere went wrong.")
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

# Load config
configuration = load_configuration()

# Setup JSDoc if Node is available
js_install_successfull = install_node_js()

# Remove existing files/dirs from generated_docs except for conf.py
cleanup_rst_directory()

# If Node is available, doublecheck & install JS dependencies (JSDoc) and generate JS reference.
if js_install_successfull:
    js_dependencies_install_successfull = install_js_dependencies() # Make sure JSDoc and JSDoc-sphinx installed
    generate_jsdoc_rsts()

# Generate PyDoc reference.
pyapi_rst_success = generate_pydoc_rsts()  # generate rst files for specified python project

# Copy over static pages & docs.
sections = copy_static_docs()
readmePath = None

try:
    readmePath = [ s for s in sections if s.get('saveAs','').lower()[0:6] == 'readme' ][0]['saveAs']
except:
    pass

generate_static_docs_index_rst()

# Generate homepage with appropriate project name, etc.
generate_index_rst()

# Output to HTML
build_successful = run_build()

