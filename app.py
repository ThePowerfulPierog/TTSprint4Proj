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
fig2 = px.histogram(df, x='model_year', color='cylinders')
fig3 = px.bar(df, x='condition', color='type')
fig4 = px.histogram(df, x='odometer', color='condition')

#presents each chart as a displayable option to the reader
st.write("Let's take a closer look at our data with some visualizations.  Please select the charts you would like to view:")
show_scatter = st.checkbox("Mileage to price correlation")
show_hist = st.checkbox("Number of Cylinders by Model Year")
show_bar = st.checkbox("Vehicle Condition by Car type")
show_mileage = st.checkbox("Vehicle Condition by Mileage")

if show_scatter:
    st.plotly_chart(fig, use_container_width=True)
    st.write("From our graph, it is clear that there is a negative correlation between mileage (odometer value) and price.  "
             "This makes sense logically, as a car with more miles is typically used more than a car with less miles.")

if show_hist:
    st.plotly_chart(fig2, use_container_width=True)
    st.write("We can see that the bulk of our vehicles are either 4, 6, or 8 cylinder engines, so we'll focus on those here.  "
             "All have a peak count between model year 2011-2013.  "
             "At a glance, there doesn't appear to be any change in number of cylinders over time, as all three of these engines are represented heavily.  "
             "One thing we can see is that 4-cylinder engines have a higher representation as the model year increases towards our peak.  "
             "While 4-cylinder engines represent a smaller proportion of vehicles in the the earlier years of 1997-2008, "
             "the 4-cylinder engine has the highest count for model year 2009, surpassing both 6 and 8 cylinder engines.")
    st.write("Another piece of information we can gather form this histrogram relates to the number of vehicles being sold by model year. "
             "Once again, the peak of the combined histogram is for model years 2011-2013.  "
             "One possible explanation for this has to do with the timeframe from which this data was taken.  "
             "Our model year high is 2019, which indicates this data set is likely from 2019/2020.  "
             "A peak of 6-8 years prior may relate to vehicle owners recently upgrading to a newer model car after paying off a car loan a few years before.  "
             "Newer models may be less represented in for sale advertisments as the vehicles are still on the road with the original purchaser.  "
             "Older models may be seen as unreliable and would more frequently be scrapped (in an accident, old-age, parts failures, etc.) rather than re-sold, "
             "accounting for the lower number of older model year cars in the chart.")

if show_bar:
    st.plotly_chart(fig3, use_container_width=True)
    st.write("From our graph, we can see that `excellent` and `good` make up the majority of our vehicle conditions.  "
             "Both `new` and `salvage` have a low vehicle count. "
             "Examining each vehicle type one-by-one reveals that certain car types have more `good` vehicles than `excellent`.  "
             "These car types include vans, coupes, and busses.  Vans and busses are typically seen as work/utility vehicles that may see more abuse than a daily-driver sedan.  "
             "Similarly, vehicles such as pickups and trucks have a fairly even split between `good` and `excellent`.  "
             "These car types can often be work vehicles, particularly in construction and trades, but many people also have these as daily-drivers.  "
             "Finally, the standard 'family cars' have a higher proportion of `excellent` than `good`.  "
             "These include sedans, SUVs, and mini-vans, and is likely due to these cars being used only to drive to-and-from work or for errands.")

if show_mileage:
    st.plotly_chart(fig4, use_container_width=True)
    st.write("This histrogam is a bit more straightforward than our other visualizations.  "
             "We would expect that the average car's condition would degrade as it is driven more.  "
             "By examining the `like new`, `excellent`, `good`, and `fair` conditions, we can see that the histrograms have a roughly normal shape, with slight right skew, ignoring the values at 0 miles.  "
             "The center point of each independent histrogram increases (moves right on the odometer scale) as the condition degrades from `like new` down to `fair`.  ")    
    
st.header("Conclusions")
st.write("From the visualizations above, we can see a few trends that may be worth a deeper dive.  "
         "First, we see that as mileage increases on a vehicle, the sale price of that vehicle trends downward.  "
         "From our second visualization, it is clear that 4-, 6-, and 8-cylinder engines make up the bulk of vehicles sold.  "
         "Furthermore, the years 2011-2013 had the highest numbers of cars sold in our dataset.  "
         "Our bar graph reveals that most cars are advertised in execellent and then good condition.  "
         "Certain vehicle types, particularly the utility/trade vehicles go against this pattern, being more frequently advertised in good condition.  "
         "From our final visualization, it is clear that vehicle condition trends downward as mileage increases.  "
         "We can see this by examining the peaks of each individual histogram by condtion.  "
         "This supports the correlation between mileage and sale price of the vehicle.  "
         )
