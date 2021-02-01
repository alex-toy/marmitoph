from src.domain.streamlit_classes import ProductImage, Recipes
import src.settings.settings as stg
import streamlit as st
import numpy as np
import io
import pickle
import tensorflow as tf
from PIL import Image

@st.cache(allow_output_mutation=True)
def load_model():
    """ Loads trained prediction model """
    model = tf.keras.models.load_model(stg.MODEL_PATH)
    return model

@st.cache(allow_output_mutation=True)
def load_dict():
    """ Loads dictionnary to retrieve ingredient labels """ 
    with open(stg.LABEL_DICT_PATH, 'rb') as handle:
        dict_to_label = pickle.load(handle)['dict_num_to_label']
    return dict_to_label

@st.cache(hash_funcs = stg.HASH_FUNCS, suppress_st_warning=True)
def extract_images_and_predictions(uploaded_images, 
                                    model , 
                                    dict_label, 
                                    k= 3, 
                                    normalize = False):

    """ 
        Function printing uploaded images and showing a Streamlit widget with the k-most probable 
        ingredients for user valiation. 
        If none of the probable ingredients is satisfying, the user can specify manually the nature 
        of the ingredient through a Streamlit input textbox.

        Returns
        ----------
        images : list
            Contains the list of uploaded images extracted

        probable_ingredients : dict of list
            The dict key correspond to each uploaded image.
            The dict values are a list of ingredients that have the largest probability value 
            at prediction (sorted from most to least probable)
    """

    images=[]
    probable_ingredients={}
    for i, uploaded_image in enumerate(uploaded_images):
        product = ProductImage(uploaded_image)
        images.append(product.image)
        probable_ingredients[i]= product.predict_ingredients(model, dict_label, k, normalize)    
    return images, probable_ingredients


def show_image_and_validate_predictions(images, probable_ingredients): 
    """ 
        Function printing uploaded images and showing a Streamlit widget with the k-most probable 
        ingredients for user valiation. 
        If none of the probable ingredients is satisfying, the user can specify manually the nature 
        of the ingredient through a Streamlit input textbox.

        Parameters
        ----------
        images : list
            Contains the list of uploaded images extracted

        probable_ingredients : dict of list
            The dict key correspond to each uploaded image.
            The dict values are a list of ingredients that have the largest probability value 
            at prediction (sorted from most to least probable)

        Returns
        -------
        picked_ingredients : dict of str
            The dict key correspond to each uploaded image.
            The dict value is the ingredient picked by used in streamlit radio button.

        replacement_ingredients : dict of str
            The dict key correspond to each uploaded image.
            The dict value is the potential replacement ingredient specfied by user in 
            the textbox if the predction is not satisfying.

        """       

    picked_ingredient = {}
    replacement_ingredient = {}
    for i, image in enumerate(images):
        st.sidebar.image(image, caption='Ingrédient {}'.format(i+1), width = 150)
        picked_ingredient[i] = st.sidebar.radio("Voilà ce que j'ai reconnu ! Peux-tu m'aider à confirmer ?",
                                        probable_ingredients[i], key = i) 
        replacement_ingredient[i] = st.sidebar.text_input("Oups, pas vraiment ! C'est plutôt :", key = i)
    return picked_ingredient, replacement_ingredient


@st.cache(allow_output_mutation=True)
def get_ingredients_list(picked_ingredient, replacement_ingredient):
    """
    Returns the final ingredients list for recipe search from the dictionnaries containing 
    the picked_ingredient and replacement_ingredient for each uploaded image.
    For each uploded image, the final ingredient is taken as the picked ingredient (with streamlit button) 
    or the replacement ingredient if specified.

    Parameters
    -------
    picked_ingredients : dict of str
        The dict key correspond to each uploaded image.
        The dict value is the ingredient picked by used in streamlit radio button.

    replacement_ingredients : dict of str
        The dict key correspond to each uploaded image.
        The dict value is the potential replacement ingredient specfied by user in 
        the textbox if the prediction is not satisfying.
    
    Returns
    -------
    ingredients_list : list of str
        Final list of ingredients 

    """
    ingredients_list = []
    for i in picked_ingredient.keys():
        if len(replacement_ingredient[i])>0:
            ingredients_list.append(replacement_ingredient[i])
        else:
            ingredients_list.append(picked_ingredient[i])
    return ingredients_list






