import pandas as pd
import streamlit as st
df = pd.read_csv("http://data.insideairbnb.com/portugal/norte/porto/2021-12-08/visualisations/listings.csv")
df = df[df['neighbourhood_group']=='PORTO']
st.set_page_config(page_title="Analysis of Airbnb listings in Porto", layout = 'wide', initial_sidebar_state = 'auto')

st.title("Analysis of Airbnb listings in Porto")
st.markdown("Welcome to this in-depth introduction to [...].")

col1, col2, col3 = st.columns(3)
col1.metric("Median price", "70 °F", "1.2 °F")
col2.metric("Median size (m2)", "9 mph", "-8%")
col3.metric("Median smth else", "86%", "4%")

st.sidebar.header('Filter listings')
outside = st.sidebar.checkbox('View listings outside of Porto municipality')
values = st.sidebar.slider("Price range", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
left_col, right_col = st.columns(2)


left_col.subheader("The first five records of the Airbnb data we downloaded")
left_col.dataframe(df.head())

right_col.subheader('Where are the most expensive properties located?')
right_col.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
right_col.map(df.query("price>=500")[["latitude", "longitude"]].dropna(how="any"))


left_col.subheader("Average price by neighborhood")
left_col.table(df.groupby("neighbourhood").price.mean().reset_index().round(2).sort_values("price", ascending=False).assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))
#st.markdown("The first five records of the Airbnb data we downloaded.")
#st.dataframe(df.head())
# st.header("Where are the most expensive properties located?")
# st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
# st.map(df.query("price>=500")[["latitude", "longitude"]].dropna(how="any"))
# st.subheader("In a table")
# st.markdown("Following are the top five most expensive properties.")
# st.write(df.query("price>=500").sort_values("price", ascending=False).head())



# st.subheader("Selecting a subset of columns")
# st.write(f"Out of the {df.shape[1]} columns, you might want to view only a subset. Streamlit has a [multiselect](https://streamlit.io/docs/api.html#streamlit.multiselect) widget for this.")
# defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
# cols = st.multiselect("Columns", df.columns.tolist(), default=defaultcols)
# st.dataframe(df[cols].head(10))

# st.header("Average price by room type")
# st.write("You can also display static tables. As opposed to a data frame, with a static table you cannot sorting by clicking a column header.")
# st.table(df.groupby("room_type").price.mean().reset_index()\
#     .round(2).sort_values("price", ascending=False)\
#     .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))

# st.header("Average price by neighborhood type")
# st.write("You can also display static tables. As opposed to a data frame, with a static table you cannot sorting by clicking a column header.")
# st.table(df.groupby("neighbourhood").price.mean().reset_index().round(2).sort_values("price", ascending=False).assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))

# st.header("Which host has the most properties listed?")
# listingcounts = df.host_id.value_counts()
# top_host_1 = df.query('host_id==@listingcounts.index[0]')
# top_host_2 = df.query('host_id==@listingcounts.index[1]')
# st.write(f"""**{top_host_1.iloc[0].host_name}** is at the top with {listingcounts.iloc[0]} property listings.
# **{top_host_2.iloc[1].host_name}** is second with {listingcounts.iloc[1]} listings. Following are randomly chosen
# listings from the two displayed as JSON using [`st.json`](https://streamlit.io/docs/api.html#streamlit.json).""")

# st.json({top_host_1.iloc[0].host_name: top_host_1\
#     [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
#         .sample(2, random_state=4).to_dict(orient="records"),
#         top_host_2.iloc[0].host_name: top_host_2\
#     [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
#         .sample(2, random_state=4).to_dict(orient="records")})

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
