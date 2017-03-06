import argparse
import subprocess
import yaml

# TODO: Load configs from command-line args and YAML into here. Replace like "./docs" w/ entries from YAML config.
configuration = {}

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

def load_configuration():
    pass
    # TODO: Load YAML
    #yaml.load()

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
build_successful = run_build()

print("Finished successfully. Shutting down.")