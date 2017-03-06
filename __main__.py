import subprocess

# Install dependencies
def install_dependencies():
    print("Updating dependencies")
    result = subprocess.run(["pip3", "install", "-r", "./requirements.txt"])
    if (result.returncode == 0):
        print('...success!')
        return True
    else:
        result.check_returncode()
        return False

print("Running document static site generator...")
install_successful = install_dependencies()

if not install_successful:
    print("Shutting down")