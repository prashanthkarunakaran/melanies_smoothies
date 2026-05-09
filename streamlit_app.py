# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Title
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")

st.write(
    """Choose the fruit you want in your custom smoothie"""
)
  

# Input
name_on_order = st.text_input("Name on Smoothie:")

st.write("name on your smoothie will be", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Read table
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col("FRUIT_NAME"))

# Display dataframe
st.dataframe(data=my_dataframe, use_container_width=True)

# Convert dataframe values into Python list
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multiselect
ingredients_list = st.multiselect(
    "Choose upto 5 ingredients",
    fruit_list,
    max_selections=5
)
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
if ingredients_list:

    ingredients_string = ",".join(ingredients_list)

    st.write(ingredients_string)

    my_insert_stmt = f"""
        insert into smoothies.public.orders
        (ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(
            f"Your Smoothie is ordered! {name_on_order}",
            icon="✅"
        )
