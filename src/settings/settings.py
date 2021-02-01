"""
Contains all configurations for the projectself.
Should NOT contain any secrets.

"""
import os

# Folder paths
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_DIR = os.path.join(REPO_DIR, 'data')
MODEL_DIR = os.path.join(REPO_DIR, 'models')

# GCP project parameters
GCP_PROJECT_NAME = "marmitoph"
GCP_MODEL_PATH = "gs://marmitoph_bucket/model/model_finetuned.h5"
GCP_LABEL_DICT_PATH = "gs://marmitoph_bucket/model/label_dict.pickle"

# Local parameters for model
SAVED_MODEL = 'model_finetuned.h5'
LABEL_DICT_PATH = os.path.join(MODEL_DIR , 'label_dict.pickle')
MODEL_PATH = os.path.join(MODEL_DIR , SAVED_MODEL)

NORMALIZATION_BOOL = False
IMAGE_SIZE = 380

# Streamlit parameters
EXAMPLE_IMAGE = os.path.join(REPO_DIR , 'src/application/example_photo.jpg')
PAGE_ICON_IMAGE = os.path.join(REPO_DIR , 'src', 'interface','pantry.jpg')
NB_RECIPES = 5


HASH_FUNCS = {
    "_thread.RLock": lambda _: None,
    "_thread.lock": lambda _: None,
    "builtins.PyCapsule": lambda _: None,
    "_io.TextIOWrapper": lambda _: None,
    "builtins.weakref": lambda _: None,
    "builtins.dict": lambda _: None,}