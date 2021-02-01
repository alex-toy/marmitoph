import openfoodfacts
import pandas as pd

def export_openfoodfacts_data_to_csv(country, filepath, max_products = 50000):

    category_list = []
    product_list=[]
    image_list=[]
    barcode_list=[]

    i = 0
    for product in openfoodfacts.products.get_all_by_country(country):
        if ('product_name' in product.keys()) & \
        ('image_small_url' in product.keys()) & \
        ('categories_old' in product.keys()) & \
        ('code' in product.keys()):

            i+=1
            image_list.append(product['image_small_url'])
            product_list.append(product['product_name'])
            category_list.append(product['categories_old'])
            barcode_list.append(product['code'])
            if i%1000 == 0:
                print("{} products".format(i))

            if i%max_products == 0:
                break
    
    results = pd.DataFrame({'image_url' : image_list,
                            'barcode' : barcode_list,
                            'product_name': product_list,
                            'product_category': category_list})
    
    results.to_csv(filepath, index = False)


country = "France"
filepath = "data/products.csv"
max_products = 1000
export_openfoodfacts_data_to_csv(country, filepath, max_products)