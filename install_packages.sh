function install_packages() {
    { # try to install with poetry
        poetry install --no-dev
    } || { # if it fails, try with requirements.txt
        pip install --upgrade pip && pip install -r requirements.txt
    } || { # if it fails: warn the user and exit
        echo ""; echo "ERROR: failed to install package dependencies"; return 1
    }
}

install_packages && (
    echo ""
    echo "************************************************************************************"
    echo "Successfuly installed package dependencies"
    echo "************************************************************************************"
    echo ""
)
