import streamlit as st
import pandas as pd
import plotly.express as px

#we'll start by reading in our DataFrame and executing clean-up code from our Jupyter Notebook
df = pd.read_csv("vehicles_us.csv")

#fills missing values and converts column type
df['paint_color'] = df['paint_color'].fillna('unspecified')
df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform('median'))
df['cylinders'] = df['cylinders'].fillna(df.groupby('model')['cylinders'].transform('median'))
df['odometer'] = df['odometer'].fillna(df.groupby(['model_year','model'])['odometer'].transform('median'))
df['is_4wd'] = df['is_4wd'].fillna(0)
df['is_4wd'] = df['is_4wd'].astype(int)


#web app begins
st.header("Analyzing Car \'For Sale\' Ads")

st.write("On this page, we'll be performing Exploratory Data Analysis on a CSV of car advertisement data provided by TripleTen.  After cleaning up our data, we're left with the following DataFrame:")

#displays our cleaned data in the web app 
st.dataframe(df, use_container_width=True)

st.write(
    "We can see that each line in our DataFrame represents an individual car that was advertised for sale.  "  
    "The information includes the price, model and year, condition of the vehicle, some technical specifics and classifications, and the color of the vehicle.  "  
    "We also have information as to when the vehicle was posted for sale and for how long the vehicle was listed before being sold."
    )

#prepare our charts
fig = px.scatter(df, x='odometer', y='price')
fig2 = px.histogram(df, x='price', color='condition')
fig3 = px.bar(df, x='type', color='condition')

#presents each chart as a displayable option to the reader
st.write("Select the charts you would like to view:")
show_scatter = st.checkbox("Mileage to price correlation")
show_hist = st.checkbox("Price of car by vehicle condition")
show_bar = st.checkbox("Condtion of vehicle based on type")

if show_scatter:
    st.plotly_chart(fig, use_container_width=True)

if show_hist:
    st.plotly_chart(fig2, use_container_width=True)

if show_bar:
    st.plotly_chart(fig3, use_container_width=True)