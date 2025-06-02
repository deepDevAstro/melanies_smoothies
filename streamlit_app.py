# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests, pandas

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruit you want in your Custom Smoothies!
  """
)

NAME_ON_ORDER  = st.text_input("Name on Smoothie:")
st.write("The Name on Smoothie is", NAME_ON_ORDER)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True) 
#st.stop()

#Converting snowpark dataframe to pandas datafram so that to use LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 fruits: ",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
      
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + NAME_ON_ORDER + """')"""
    # st.write(my_insert_stmt)
    time_to_order = st.button("Submit Order")
    
    if time_to_order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ NAME_ON_ORDER, icon="✅")




