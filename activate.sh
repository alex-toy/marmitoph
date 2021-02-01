function activate_venv() {
    { # try: activate with poetry:
        poetry shell
    } || { # try: activate from the "python -m venv" created environment:
        source .venv/bin/activate
    } || { # catch: error
        echo ""; echo "ERROR: failed to activate virtual environment .venv! do it yourself"; return 1
    }
}

activate_venv && (
    echo ""
    echo "************************************************************************************"
    echo "Successfuly activated the virtual environment; you are now using this python:"
    echo "$ which python"
    echo "$(which python)"
    echo "************************************************************************************"
    echo ""
)
export PYTHONPATH="$(pwd):$PYTHONPATH"
export JUPYTER_PATH="$(pwd):$JUPYTER_PATH"