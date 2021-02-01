import src.settings.settings as stg
import streamlit as st
import numpy as np
import io
import pickle
from urllib.error import URLError
import tensorflow as tf
from PIL import Image
from marmiton import Marmiton, RecipeNotFound
import pandas as pd

class ProductImage():
    """Product image uploaded by user in Streamlit Marmitoph app.

    Parameters
    ---------
    uploaded_file: UploadedFile object from Streamlit

    Attributes
    ----------
    uploaded_file : UploadedFile object from Streamlit
        File uploaded by user to streamlit 

    image : numpy array of shape based on uploaded_file
        Image coresponding to uploaded_file 

    resized_image : numpy array of shape (SIZE_IMAGE, SIZE_IMAGE, 3)

    Methods
    -------
    predict_ingredients : list of strings of length k
        Return a list with the k most probable ingredients based on uploaded image

    validate_ingredients : string
        Return an ingredient after validation by user through Streamlit widgets
    """

    def __init__(self, uploaded_file):
        self.uploaded_file = uploaded_file
        self.image = self._get_image()
        self.resized_image = self._resize_image()

    
    def predict_ingredients(self, model, dict_label, k=3, normalize=False):  
        """ Method returning a list of the k-most probable ingredient identified by the model from the uploaded image.

        Parameters
        ----------
        model : tf.Keras.Model
            Trained model

        dict_label : dict
            Label dictionnary associated to model giving the ingredient associated to target number

        k : int, default = 3
            Number of most probable ingredients to extract from prediction

        normalize : bool, default = False
            Wether to normalize data prior to prediction. Depends on the model that is used.

        Returns
        -------
        probable_ingredients : string list of length [k]
            Ingredients that have the largest prabability value at prediction (sorted from most to least probable)

        """
        image = self._preprocess_image(normalize)
        prediction = model.predict(image)[0]
        k_indices = np.argsort(-prediction)[:k]
        probable_ingredients = [dict_label[ind] for ind in k_indices]
        return probable_ingredients
        

    def _get_image(self):
        bytes_data = self.uploaded_file.read()
        img = Image.open(io.BytesIO(bytes_data))
        img = img.convert('RGB')
        return img

    def _resize_image(self):
        img = self.image
        img = np.array(img.resize((stg.IMAGE_SIZE,stg.IMAGE_SIZE)))
        return img


    def _preprocess_image(self, normalize = False):
        img = self.resized_image
        if normalize :
            img = tf.image.per_image_standardization(img)
        return np.array([img])




class Recipes():
    """ 
    Recipes obtained through Marmiton API based on ingredients list.

    Parameters
    ----------
    ingredients_to_include : list of strings
        Ingredients to include to recipe (in French)
    ingredients_to_exclude : list of strings
        Ingredients to exclude from recipe (in French)

    Attributes
    ----------
    included_ingredients : list of strings
        Ingredients to include to recipe (in French)
    excluded_ingredients :  list of strings
        Ingredients to exclude from recipe (in French)

    """

    def __init__(self, ingredients_to_include = [], ingredients_to_exclude = []):
        self.included_ingredients = ingredients_to_include 
        self.excluded_ingredients = ingredients_to_exclude

    
    @staticmethod
    def display(recipes_tab, nb_recipes = 3):
        """ 
        Method displaying in Streamit the nb_recipes first recipes found on Marmiton based on input ingredients list.

        Parameters
        ----------
        nb_recipes : int, default = 3
            Number of recipes to display

        Returns
        -------
        
            """

        recipes = recipes_tab.iloc[:nb_recipes]
        recipes_names = list(recipes.index)

        if len(recipes_names) > 0 :

            for recipe in recipes_names:

                image = recipes['image'].loc[recipe]
                ingredients = recipes['ingredients'].loc[recipe]
                steps = recipes['steps'].loc[recipe]

                col3, col4 = st.beta_columns([1,2])

                with col3:
                    try:
                        st.subheader("")
                        st.image(image, caption= recipe, use_column_width = True)
                    except:
                        pass
                   
                with col4:
                    st.subheader(recipe)
                    try :
                        st.write("Ingrédients : {}".format(", ".join(ingredients)))
                    except :
                        pass

                    try :
                        st.write("Etapes : {}".format(" ".join(steps)))
                    except:
                        pass
                
            st.header("Maintenant, à tes fourneaux !")
        
        else:
            st.warning("Désolés, aucune recette n'a été trouvée avec ces ingrédients :(")


    def get_recipes(self):
        """
        Method extracting recipes from Marmiton website based on ingredients list.
    
        Parameters
        ----------
        ingredients_to_include : list of strings
            Ingredients to include to recipe (in French)
        ingredients_to_exclude : list of strings
            Ingredients to exclude from recipe (in French)


        Returns
        -------
        DataFrame
            DataFrame containing all matching recipes with recipe name as index 
            and with recipe infos as columns :
            - ingredients: string list of the recipe ingredients (including quantities)
            - steps: string list of each step of the recipe
            - image: if exists, image of the recipe (url).
        """

        # Creation of query keywords based on ingredients
        ingredients_to_include = self.included_ingredients
        ingredients_to_exclude = self.excluded_ingredients

        query_keywords = " ".join(ingredients_to_include)
        if len(ingredients_to_exclude) > 0:
            query_keywords += " sans "
            query_keywords += " ".join(ingredients_to_exclude)

        # Search :
        query_options = {"aqt": query_keywords, "st": 1}

        query_result = []
        try: 
            query_result = Marmiton.search(query_options)
        except URLError:
            st.error('Vérifie ta connexion internet !')
            return query_result
        else :
            if len(query_result) == 0:
                st.error('Vérifie ta connexion internet !')
                return query_result
              
        # Recap on recipes and urls
        url_list = [recipe['url'] for recipe in query_result]
        recipes_list = [recipe['name'] for recipe in query_result]

        # Creation of tab with recipes infos
        recipes_keys = ['image', 'ingredients', 'steps']
        recipes_tab = pd.DataFrame(index = recipes_list, 
                                    columns = recipes_keys)

        for url in url_list:
            recipe = Marmiton.get(url)

            for key in recipes_keys:
                recipes_tab.loc[recipe['name'], key] = recipe[key]          
            
        return recipes_tab
