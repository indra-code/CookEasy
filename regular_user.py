import streamlit as st
from sql_functions import get_base64,get_dish_name_description,get_prompt_run_model,insert_available_item,generate_shopping_list,clear_ingredients,update_user_inventory,get_your_ing,get_shopping_list_ing
from PIL import Image
import pandas as pd
def regular_user():
    home,your_ingredients,cart = st.tabs(["Home","Your Ingredients","Your cart"])
    hide_streamlit_style = """
        <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2rem;}
        </style>

        """
    st.markdown(hide_streamlit_style,unsafe_allow_html=True)
    if 'dish_id' not in st.session_state:
        st.session_state.dish_id = None
    with home:
        #st.write({st.session_state.userid})
        st.title("Welcome to Cookeasy!!")
        st.caption("Your AI guide to an easier cooking and shopping experience")
        base64_img = None
        with st.sidebar:

            st.subheader("Enter an image of the dish you want to make") 

            uploaded_file = st.file_uploader("Upload the image (jpg or png)", type=["jpg", "png"])
            if uploaded_file is not None :
                base64_img = get_base64(uploaded_file)
                image = Image.open(uploaded_file)
                st.image(image,caption="Uploaded image",use_column_width=True)
                st.success("Image uploaded successfully.")
            if st.button('Logout'):
                st.session_state.userid = None
                st.session_state.page = 'login'
                st.rerun()

        if st.button("Get dish name and description"):
            if base64_img is not None:
                dish_desc = get_dish_name_description(base64_img)
                print("Returned items: ",dish_desc)
                st.session_state.dish_id = dish_desc[0][0]
                st.write(f"{dish_desc[0][2]}")
            else:
                st.error("Please upload an image before processing.")

        number_of_people = st.number_input("Enter the number of people you want to cook for", min_value=1, step=1, value=1)

        if st.button("Get ingredients for selected number of people"):
            if base64_img is not None:
                ing = get_prompt_run_model(number_of_people, base64_img)
                df = pd.DataFrame(
                    ing,columns = ["ingredient","weight","unit"]
                )
                st.table(df)
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

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate Shopping List"):
                generate_shopping_list()
                st.success("Shopping list generated successfully!")

            if st.button("Clear list"):
                clear_ingredients()
                st.success("List cleared")

        with col2:
            if st.button("I have cooked the dish"):
                update_user_inventory(st.session_state.dish_id)
                st.success("Great, enjoy your meal!")
    with your_ingredients:
        ing = get_your_ing()
        df = pd.DataFrame(
            ing,columns = ["ingredient","weight","unit"]
        )
        st.table(df)
    with cart:
        ing = get_shopping_list_ing()
        df = pd.DataFrame(
            ing,columns = ["ingredient","weight","unit"]
        )
        st.table(df)
if __name__ == "__main__":
    regular_user()

