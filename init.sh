# exit on error
#set -e

echo "Starting project initialization. This sould only be run once per machine!"
echo "Creating a local python environment in .venv and activating it"

function init_venv() {
    { # try to create a .venv with the standard python3
        python3 -m venv .venv
    } || { # if it fails: warn the user (clean the .venv if it was partially created)
        rm -rf .venv && echo "ERROR: failed to create the .venv : do it yourself!" && exit 1
    }
}

init_venv && (
    echo "*********************************************************"
    echo "Successfully created the virtual environment! it is located at:"
    echo "$(pwd)/.venv"
    echo "*********************************************************"
)

echo "Activating this venv:"
source activate.sh

echo "Installing requirements"
source install_packages.sh

echo "you should now have a local python3 version:"
python3 --version
which python3
