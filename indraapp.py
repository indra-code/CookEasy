import google.generativeai as genai
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import base64
import os
import mysql.connector
import streamlit as st


load_dotenv()
key = os.getenv("GOOGLE_API_KEY")
pwd = os.getenv("SQL_PASSWORD")
genai.configure(api_key = key)
model = ChatGoogleGenerativeAI(model = 'models/gemini-1.5-flash-latest',temperature = 0)
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = pwd,
    database = "sqproj"
)
mycursor = db.cursor()
def get_base64(img):
    return base64.b64encode(img.read()).decode()
#base64_img = get_base64('download1.jpg')
def get_dish_name_description(base64_img):
    prompt_template = '''
        You are an advanced food recognition AI that excels in identifying dishes from images and providing concise descriptions. Your expertise lies in accurately naming various cuisines and delivering a brief yet informative overview in just three lines, ensuring precision and clarity in your responses.

        Your task is to analyze the image provided and generate a dish name along with a short description. The output should strictly follow this format: the dish name, followed by the three-line description.
        Here are the details for the task:
            - Note: Ensure that the dish name and decription are on seperate lines.The dish and description should not have any empty line between them.
        Remember to maintain a focus on clarity and brevity in your description while delivering an accurate dish name.
    '''
    prompt = HumanMessage(
        content = [
            {'type':'text','text': prompt_template},
            {'type':'image_url','image_url':f"data:image/jpeg;base64,{base64_img}"}
        ]
    )
    response = model.invoke([prompt])
    response_string = response.dict()
    res = response_string["content"]
    print(res)
    ls_res = res.splitlines()
    print(ls_res)
    i = 0
    while(i<len(ls_res)):
        mycursor.execute(f"INSERT INTO fooditem(dish_name,dish_description) VALUES(%s,%s)",(ls_res[i],ls_res[i+1]))
        db.commit()
        i+=2
def get_prompt_run_model(numberOfPeople, base64_img):
    prompt_template = f'''
    You are an advanced image analysis assistant with expertise in identifying various dishes and their ingredients. Your capabilities allow you to accurately recognize food items and list all associated ingredients in a clear and concise manner.

    Your task is to analyze the input image and provide the name of the dish along with a comprehensive list of all its ingredients.

    Please consider the following details while generating your response:
    - The input image may contain a variety of dishes, from simple to complex.
    - Ensure that every ingridient in your response is seperated by commas and there should be no space after a comma.
    - The output should consist ONLY of the ingredients and their weights, with each ingredient in lowercase letters.
    - Do not include the name of the dish in the list of ingredients.
    - The units used for liquid ngredients should be ml or L.
    - The units used for solid ingredients should be g or kg.
    - The unit used for eggs should be nos.
    - Each ingredient should be followed by its weight in grams, separated by a comma and there should be no space after the comma. If the weight exceeds 1000 grams, use kilograms (kg).
    - However the unit of measurement should be seperate from the numerical weight using commas.
    - The list should be appropriate for serving {numberOfPeople} people.
    - all letters of every ingredient must be in lowercase.
    - there should be no space before the ingredient name starts.
    -do not give the weight in fractions, only decimals.
    '''
    prompt = HumanMessage(
        content = [
            {'type':'text','text': prompt_template},
            {'type':'image_url','image_url':f"data:image/jpeg;base64,{base64_img}"}
        ]
    )
    response = model.invoke([prompt])
    response_string = response.dict()
    res = response_string["content"]
    print(res)
    ls_res = res.split(",")
    print(ls_res)
    i = 0
    while(i<len(ls_res)-1):
        mycursor.execute(f"INSERT INTO ingredients(ingredient,weight,unit) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE ingredient = VALUES(ingredient),weight = weight + VALUES(weight),unit = VALUES(unit);",(ls_res[i],ls_res[i+1],ls_res[i+2]))
        db.commit()
        mycursor.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient = %s",(ls_res[i],))
        res = mycursor.fetchone()
        ing_id = res[0]
        if ing_id:
            mycursor.execute(f"UPDATE my_ingredients SET ingredient_id = %s WHERE my_ingredient = %s AND ingredient_id IS NULL",(ing_id,ls_res[i]))
        db.commit()
        i+=3
def insert_available_item(item,weight,unit):
    mycursor.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient = %s",(item,))
    res = mycursor.fetchone()
    if res:
        ing_id = res[0]
        mycursor.execute(f"INSERT INTO my_ingredients(ingredient_id,my_ingredient,weight,unit) VALUES(%s,%s,%s,%s)",(ing_id,item,weight,unit))
        db.commit()
    else:
        mycursor.execute(f"INSERT INTO my_ingredients(my_ingredient,weight,unit) VALUES(%s,%s,%s)",(item,weight,unit))
        db.commit()
def generate_shopping_list():
    mycursor.execute('''INSERT INTO shoppinglist (ingredient_id, weight, unit)
                        SELECT
                            i.ingredient_id,
                            CASE
                                WHEN mi.weight IS NULL THEN i.weight
                                WHEN mi.unit = i.unit THEN i.weight - mi.weight
                                WHEN i.unit = 'kg' AND mi.unit = 'g' AND (i.weight - (mi.weight / 1000)) > 1  THEN i.weight - (mi.weight / 1000)
                                WHEN i.unit = 'kg' AND mi.unit = 'g' AND (i.weight - (mi.weight / 1000)) < 1  THEN (i.weight - (mi.weight / 1000)) * 1000
                                ELSE i.weight
                            END AS weight,
                            CASE
                                WHEN i.unit = 'kg' AND mi.unit = 'g' AND (i.weight - (mi.weight / 1000)) < 1 THEN 'g'
                                ELSE i.unit
                            END AS unit
                        FROM ingredients i
                        LEFT JOIN my_ingredients mi ON i.ingredient_id = mi.ingredient_id
                        WHERE mi.weight IS NULL
                        OR mi.weight < i.weight
                        OR (mi.weight > i.weight AND i.unit = 'kg' AND mi.unit = 'g')
                        ''')
def update_user_inventory():
    mycursor.execute('''
SET SQL_SAFE_UPDATES = 0;
UPDATE my_ingredients mi
INNER JOIN ingredients i ON mi.ingredient_id = i.ingredient_id
SET
    mi.weight = CASE
        WHEN mi.weight > i.weight AND mi.unit = i.unit THEN mi.weight - i.weight
        WHEN mi.weight <= i.weight AND mi.unit = i.unit THEN 0
        WHEN mi.weight < i.weight AND i.unit = 'g' AND mi.unit = 'kg' AND mi.weight - (i.weight / 1000) > 1  THEN  mi.weight - (i.weight / 1000) 
        WHEN mi.weight < i.weight AND i.unit = 'g' AND mi.unit = 'kg' AND mi.weight - (i.weight / 1000) < 1  THEN  (mi.weight - (i.weight / 1000))*1000 
        WHEN mi.weight > i.weight AND i.unit = 'kg' AND mi.unit = 'g' THEN 0
        ELSE mi.weight
    END,
    mi.unit = CASE
        WHEN i.unit = 'g' AND  mi.unit = 'kg' AND mi.weight - (i.weight / 1000) < 1 THEN 'g'
        WHEN i.unit = 'g' AND mi.unit = 'kg' AND mi.weight - (i.weight / 1000) >= 1 THEN 'kg'
        ELSE mi.unit
    END
WHERE mi.ingredient_id = i.ingredient_id;
SET
    mi.weight = CASE
        WHEN mi.weight > i.weight AND mi.unit = i.unit THEN mi.weight - i.weight
        WHEN mi.weight <= i.weight AND mi.unit = i.unit THEN 0
        WHEN mi.weight < i.weight AND i.unit = 'ml' AND mi.unit = 'l' AND mi.weight - (i.weight / 1000) > 1  THEN  mi.weight - (i.weight / 1000) 
        WHEN mi.weight < i.weight AND i.unit = 'ml' AND mi.unit = 'l' AND mi.weight - (i.weight / 1000) < 1  THEN  (mi.weight - (i.weight / 1000))*1000 
        WHEN mi.weight > i.weight AND i.unit = 'l' AND mi.unit = 'ml' THEN 0
        ELSE mi.weight
    END,
    mi.unit = CASE
        WHEN i.unit = 'ml' AND  mi.unit = 'l' AND mi.weight - (i.weight / 1000) < 1 THEN 'ml'
        WHEN i.unit = 'ml' AND mi.unit = 'l' AND mi.weight - (i.weight / 1000) >= 1 THEN 'l'
        ELSE mi.unit
    END
WHERE mi.ingredient_id = i.ingredient_id;

''')

def sql():
    mycursor.execute(f"INSERT INTO ingredients(ingredient,weight,unit) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE ingredient = VALUES(ingredient),weight = weight + VALUES(weight),unit = VALUES(unit);",("mud",100,"g"))
    db.commit()
    mycursor.execute(f"SELECT ingredient_id FROM ingredients WHERE ingredient = %s",("mud",))
    res = mycursor.fetchone()
    ing_id = res[0]
    print(ing_id)
    if ing_id:
        mycursor.execute(f"UPDATE my_ingredients SET ingredient_id = %s WHERE my_ingredient = %s AND ingredient_id IS NULL",(ing_id,"mud"))
    db.commit()


def main():

    st.title("Welcome to Cookeasy!!")
    st.caption("Your AI guide to an easier cooking and shopping experience")
    base64_img = None
    

    with st.sidebar:

        st.subheader("Enter an image of the dish you want to make") 

        uploaded_file = st.file_uploader("Upload the image (jpg or png)", type=["jpg", "png"])

        if uploaded_file is not None:
        
            base64_img = get_base64(uploaded_file)
            st.success("Image uploaded successfully.")

    if st.button("Get dish name and description"):
        if base64_img is not None:
            get_dish_name_description(base64_img)
        else:
            st.error("Please upload an image before processing.")

    number_of_people = st.number_input("Enter the number of people you want to cook for", min_value=1, step=1, value=1)

    if st.button("Get ingredients for selected number of people"):
        if base64_img is not None:
            get_prompt_run_model(number_of_people, base64_img) 
        else:
            st.error("Please upload an image before processing.")
    
    st.subheader("Insert Available Item")
    item = st.text_input("Ingredient Name")
    weight = st.number_input("Weight (in grams)", min_value=0, step=1)
    unit = st.selectbox("Unit", ["g", "kg", "ml", "L", "nos"])
    
    if st.button("Insert Item"):
        if item and weight > 0:
            insert_available_item(item, weight, unit)
            st.success(f"Item '{item}' with weight {weight} {unit} has been added.")
        else:
            st.error("Please provide a valid ingredient name and weight.")

    if st.button("Generate Shopping List"):
        generate_shopping_list()
        st.success("Shopping list generated successfully!")


    


    #sql()
    #get_prompt_run_model(4)
    #get_dish_name_description()
    #insert_available_item("chicken",200,"g")
    #insert_available_item("fish",50,"g")
    #update_user_inventory()
    #generate_shopping_list()
if __name__ == "__main__":
    main()

