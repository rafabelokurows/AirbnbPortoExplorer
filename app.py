import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
st.set_option('deprecation.showPyplotGlobalUse', False)
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import folium

df = pd.read_csv("http://data.insideairbnb.com/portugal/norte/porto/2021-12-08/visualisations/listings.csv")
df = df[df['neighbourhood_group']=='PORTO']
st.set_page_config(page_title="Analysis of Airbnb listings in Porto", layout = 'wide', initial_sidebar_state = 'auto')

st.title("Analysis of Airbnb listings in Porto")
st.markdown("Welcome to this in-depth introduction to [...].")

col1, col2, col3 = st.columns(3)
col1.metric("Median price", "{:10.3f}".format(df.price.mean()))
col2.metric("Median size (m2)", df.size.mean())
col3.metric("Median smth else", "86%", "4%")

st.sidebar.markdown("**Author**: Rafael Belokurows")
st.sidebar.markdown("**Mail**: rafabelokurows@gmail.com")
st.sidebar.markdown("- [Linkedin](https://www.linkedin.com/in/toniesteves/)")
st.sidebar.markdown("- [Twitter](https://twitter.com/)")
st.sidebar.markdown("- [Medium](https://medium.com/@toni_esteves)")


st.sidebar.markdown("**Version:** 1.0.0")
st.sidebar.header('Filter listings')
outside = st.sidebar.checkbox('View listings outside of Porto municipality')
values = st.sidebar.slider("Price range ($)", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
min_nights_values = st.sidebar.slider('Minimum Nights', 0, 30, (1))
left_col, right_col = st.columns(2)

left_col.subheader("Average price by neighborhood")
left_col.table(df.groupby("neighbourhood").price.mean().reset_index().round(2).sort_values("price", ascending=False).assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))


right_col.subheader('Where are the most expensive properties located?')
right_col.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
right_col.map(df.query("price>=500")[["latitude", "longitude"]].dropna(how="any"))

left_col.subheader("Words that appear the most on property names")
text = ' '.join(str(n).lower() for n in df.name)

wordcloud = WordCloud(max_words=200, background_color = 'white').generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
left_col.pyplot()

map_folium = folium.Map([4.15,8.6],zoom_start=11.4)
HeatMap(df[['latitude','longitude']].dropna(),radius=8,gradient={0.2:'blue',0.4:'purple',0.6:'orange',1.0:'red'}).add_to(map_folium)
right_col.subheader("Another map")
#right_col.display(map_folium)

with right_col:
    folium_static(map_folium)

fig = px.histogram(df.price, x="price", nbins=25, title="Price distribution")
fig.update_xaxes(title="Price")
fig.update_yaxes(title="No. of listings")
# Plot!
left_col.plotly_chart(fig, use_container_width=True)

#st.markdown("The first five records of the Airbnb data we downloaded.")
#st.dataframe(df.head())
# st.header("Where are the most expensive properties located?")
# st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
# st.map(df.query("price>=500")[["latitude", "longitude"]].dropna(how="any"))
# st.subheader("In a table")
# st.markdown("Following are the top five most expensive properties.")
# st.write(df.query("price>=500").sort_values("price", ascending=False).head())

# st.header("Which host has the most properties listed?")
# listingcounts = df.host_id.value_counts()
# top_host_1 = df.query('host_id==@listingcounts.index[0]')
# top_host_2 = df.query('host_id==@listingcounts.index[1]')
# st.write(f"""**{top_host_1.iloc[0].host_name}** is at the top with {listingcounts.iloc[0]} property listings.
# **{top_host_2.iloc[1].host_name}** is second with {listingcounts.iloc[1]} listings. Following are randomly chosen

# st.header("What is the distribution of property price?")
# st.write("""Select a custom price range from the side bar to update the histogram below displayed as a Plotly chart using
# [`st.plotly_chart`](https://streamlit.io/docs/api.html#streamlit.plotly_chart).""")
# #f = px.histogram(df.query(f"price.between{values}"), x="price", nbins=15, title="Price distribution")
# #f.update_xaxes(title="Price")
# #f.update_yaxes(title="No. of listings")
# #st.plotly_chart(f)

# st.header("What is the distribution of availability in various neighborhoods?")
# st.write("Using a radio button restricts selection to only one option at a time.")
# st.write("💡 Notice how we use a static table below instead of a data frame. \
# Unlike a data frame, if content overflows out of the section margin, \
# a static table does not automatically hide it inside a scrollable area. \
# Instead, the overflowing content remains visible.")
# neighborhood = st.radio("Neighborhood", df.neighbourhood_group.unique())
# show_exp = st.checkbox("Include expensive listings")
# show_exp = " and price<200" if not show_exp else ""
st.markdown('-----------------------------------------------------')
st.text('Developed by Rafael Belokurows - 2022')
st.text('Mail: rafabelokurows@gmail.com')
