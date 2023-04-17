import pandas as pd
import plotly_express as px
import streamlit as st

st.set_page_config(page_title="Expenditure Dashboard",
                   page_icon=":soccer:",
                   layout="wide")

df = pd.read_csv('resources/TransferExpenditure.csv')

st.sidebar.header("Please Filter Here:")

club = st.sidebar.multiselect(
    "Select the club:",
    options = df["Club"].unique(),
    default = df["Club"].unique()
)

season = st.sidebar.multiselect(
    "Select the season:",
    options = df["Season"].unique(),
    default = df["Season"].unique()
)

league = st.sidebar.multiselect(
    "Select the league:",
    options = df["League"].unique(),
    default = df["League"].unique()
)

df_selection = df.query(
    "Club == @club & Season == @season & League == @league"
)

st.title(":soccer: Football Expenditure Dashboard")
st.markdown("##")

total_spending = int(df_selection["Expenditure"].sum())
average_profit = round(df_selection["Balance"].mean(), 1)

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Total Expenditure: ")
    st.subheader(f"€{total_spending:,}")

with right_column:
    st.subheader("Average Balance: ")
    st.subheader(f"€{average_profit:,}")

st.markdown("---")

topClubExpenditure = (
    df_selection.groupby(by=["Club"]).sum()
).sort_values(by=['Balance'],ascending=True).head(20)

leagueExpenditureByYear = (
    df.groupby(['League', 'Season'])['Expenditure'].sum().reset_index()
)

figClubExpenditure = px.bar(
    topClubExpenditure,
    x = topClubExpenditure.index,
    y = "Balance",
    color = topClubExpenditure.index,
    orientation = "v",
    title = "<b>Balance by Club</b>",
    template = "plotly_white"
)

figLeagueExpenditureByYear = px.line(
    leagueExpenditureByYear,
    x = "Season",
    y = "Expenditure",
    color = "League",
    orientation = "v",
    title = "<b>Expenditure by Season</b>",
    template = "plotly_white"
)

left_column, right_column = st.columns(2)

with left_column:
    st.plotly_chart(figClubExpenditure)

with right_column:
    figLeagueExpenditureByYear.update_xaxes(visible=False, fixedrange=True)
    figLeagueExpenditureByYear.update_yaxes(visible=False, fixedrange=True)
    figLeagueExpenditureByYear.update_layout(
        showlegend=False,
    )
    st.plotly_chart(figLeagueExpenditureByYear)

st.markdown("---")

st.dataframe(df_selection)
