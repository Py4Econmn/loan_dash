import streamlit as st # pip install streamlit
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
import datetime as dt

st.set_page_config(page_title="Loan analysis!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Loan analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

df = pd.read_csv('../data/sample_loan_2309.csv', encoding = "ISO-8859-1")
df_out = pd.read_csv('../data/outstanding_2308.csv')

df_out = df_out.groupby('month')['amount'].sum().reset_index()


# outstanding loan monthly
fig = px.line(df_out, x="month", y="amount",
                 title="Outstanding amount")
# Customize the plot appearance
fig.update_traces(marker=dict(sizemode='diameter', opacity=0.7), selector=dict(mode='markers+text'))
st.plotly_chart(fig,use_container_width=True)

# st.text('Due Date')
col1, col2 = st.columns((2))
df["DueDate"] = pd.to_datetime(df["DueDate"])

# Getting the min and max date 
startDate = dt.date.today() #pd.to_datetime(df["DueDate"]).min()
endDate = pd.to_datetime(df["DueDate"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Due Date: From", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("To", endDate))

df = df[(df["DueDate"] >= date1) & (df["DueDate"] <= date2)]

st.sidebar.header("Choose your filter: ")
# Create for Type
type = st.sidebar.multiselect("Loan Type", df["Type"].unique())
if not type:
    df2 = df.copy()
else:
    df2 = df[df["Type"].isin(type)]

# # Create for Branch
branch = st.sidebar.multiselect("Branch", df2["Branch"].unique())
if not branch:
    df3 = df2.copy()
else:
    df3 = df2[df2["Branch"].isin(branch)]

# Create for Status
type = st.sidebar.multiselect("Loan Status", df3["Status"].unique())
if not type:
    df4 = df3.copy()
else:
    df4 = df3[df3["Status"].isin(type)]

category_df = df4.groupby(by = ["Type","Status"], as_index = False)["Amount"].sum()

with col1:
    st.subheader("Loan outstanding")
    fig = px.bar(category_df, x = "Type", y = "Amount",color="Status", 
                 template = "seaborn")  #text = ['${:,.2f}'.format(x) for x in category_df["Amount"]],
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Shares of loan outstanding by type")
    fig = px.pie(df4, values = "Amount", names = "Type", hole = 0.5)
    fig.update_traces(text = df4["Type"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)


col1, col2 = st.columns((2))
category_df = df4.groupby(by = ["Branch","Status"], as_index = False)["Amount"].sum()
with col1:
    st.subheader("Loan outstanding")
    fig = px.bar(category_df, x = "Branch", y = "Amount",color="Status", 
                 template = "seaborn")  #text = ['${:,.2f}'.format(x) for x in category_df["Amount"]],
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Shares of loan outstanding by branch")
    fig = px.pie(df4, values = "Amount", names = "Branch", hole = 0.5)
    fig.update_traces(text = df4["Branch"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Type_ViewData"):
        st.write(df) # .style.background_gradient(cmap="Blues")
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Type.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("Branch_ViewData"):
        region = df.groupby(by = "Branch", as_index = False)["Amount"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Branch.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')


# filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
# st.subheader('Time Series Analysis')

# linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
# fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
# st.plotly_chart(fig2,use_container_width=True)

# with st.expander("View Data of TimeSeries:"):
#     st.write(linechart.T.style.background_gradient(cmap="Blues"))
#     csv = linechart.to_csv(index=False).encode("utf-8")
#     st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

# # Create a treem based on Region, category, sub-Category
# st.subheader("Hierarchical view of Sales using TreeMap")
# fig3 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
#                   color = "Sub-Category")
# fig3.update_layout(width = 800, height = 650)
# st.plotly_chart(fig3, use_container_width=True)

# chart1, chart2 = st.columns((2))
# with chart1:
#     st.subheader('Segment wise Sales')
#     fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
#     fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
#     st.plotly_chart(fig,use_container_width=True)

# with chart2:
#     st.subheader('Category wise Sales')
#     fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
#     fig.update_traces(text = filtered_df["Category"], textposition = "inside")
#     st.plotly_chart(fig,use_container_width=True)

# import plotly.figure_factory as ff
# st.subheader(":point_right: Month wise Sub-Category Sales Summary")
# with st.expander("Summary_Table"):
#     df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
#     fig = ff.create_table(df_sample, colorscale = "Cividis")
#     st.plotly_chart(fig, use_container_width=True)

#     st.markdown("Month wise sub-Category Table")
#     filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
#     sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"],columns = "month")
#     st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# # Create a scatter plot
# data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
# data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
#                        titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
#                        yaxis = dict(title = "Profit", titlefont = dict(size=19)))
# st.plotly_chart(data1,use_container_width=True)

# with st.expander("View Data"):
#     st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# # Download orginal DataSet
# csv = df.to_csv(index = False).encode('utf-8')
# st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")
