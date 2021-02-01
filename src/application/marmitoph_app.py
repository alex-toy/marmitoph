from src.domain.streamlit_classes import Recipes
import src.settings.settings as stg
from src.domain.streamlit_app_functions import load_model, load_dict 
from src.domain.streamlit_app_functions import extract_images_and_predictions, show_image_and_validate_predictions, get_ingredients_list
import streamlit as st
from PIL import Image
import time

### Load model
MODEL = load_model()
DICT_LABEL = load_dict()

### Header
st.title("Marmitoph")
st.header("Des recettes inspirées par les photos de ton garde-manger")

### Sidebar Header
st.sidebar.subheader("Qu'as-tu dans ton garde manger ?")

### Example
st.sidebar.info("Essaie de cadrer tes photos comme celle-ci") 
ex_image = Image.open(stg.EXAMPLE_IMAGE)
st.sidebar.image(ex_image, width=150)

### Image uploading
uploaded_images = st.sidebar.file_uploader("", accept_multiple_files=True)
time.sleep(5)


### Extract images and predict k most probable ingredients
images, probable_ingredients = extract_images_and_predictions(uploaded_images, 
																model = MODEL, 
																dict_label = DICT_LABEL, 
																k= 3, 
																normalize = stg.NORMALIZATION_BOOL)

### Show images and validate predictions
picked_ingredient, replacement_ingredient = show_image_and_validate_predictions(images, 
																				probable_ingredients)



 ### Recipes search
NB_RECIPES = st.sidebar.slider("Nombre de recettes", min_value=1, max_value=10, value = 5)
launch_find_recipe_button = st.sidebar.button("Trouve moi des recettes !")


if launch_find_recipe_button:

	ingredients_list = get_ingredients_list(picked_ingredient, replacement_ingredient)

	st.write("Mes propositions de recettes avec : {}".format(", ".join(ingredients_list)))
																	  
	recipes = Recipes(ingredients_list)
	recipes_tab = recipes.get_recipes()
	recipes.display(recipes_tab, nb_recipes = NB_RECIPES)





    