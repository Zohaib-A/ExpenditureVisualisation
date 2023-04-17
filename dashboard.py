import pandas as pd
import plotly_express as px
import streamlit as st
import numpy as np
from scipy.stats import linregress
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Expenditure Dashboard",
                   page_icon=":soccer:",
                   layout="wide")

st.title(":soccer: Football Expenditure Dashboard")
st.markdown("##")

pearsonHelpText = (""" The Pearson Coefficient is a type of **correlation coefficient** that represents the relationship between two variables, measured on the same scale.
            For this example, both income and expenditure are measured in Euros, so the Pearson Coefficient is relevant here.
            The coefficient ranges from -1 to 1, where -1 is a perfectly negative correlation and 1 is a perfectly positive correlation.
            """)

# FILTERS AND NAVIGATION


def dataVis():
    st.sidebar.header("Please Filter Here:")

    season = st.sidebar.multiselect(
        "Select the season:",
        options=df["Season"].unique(),
        default=df["Season"].unique()
    )

    league = st.sidebar.multiselect(
        "Select the league:",
        options=df["League"].unique(),
        default=df["League"].unique()
    )

    club = st.sidebar.multiselect(
        "Select the club:",
        options=df["Club"].unique(),
        default=df["Club"].unique()
    )

    df_selection = df.query(
        "Season == @season & League == @league & Club == @club"
    )

    st.title(":soccer: Football Expenditure Dashboard")
    st.markdown("##")

    selected = option_menu(
        menu_title=None,
        options=["General", "Club", "League", "Data"],
        icons=["house", "club", "football", "graph"],
        default_index=0,
        orientation="horizontal"
    )
    st.markdown("---")

    # GENERAL DATA DASHBOARD (BOTH LEAGUE AND CLUB)

    if selected == "General":
        st.title(f"You have selected {selected}")
        total_spending = int(df_selection["Expenditure"].sum())
        average_profit = round(df_selection["Balance"].mean(), 1)

        totalSpendingSeason = df.groupby(['League', 'Season'])[
            'Expenditure'].sum().reset_index()

        left_column, right_column = st.columns(2)

        with left_column:
            st.subheader("Total Expenditure: ")
            st.subheader(f"€{total_spending:,}")

        with right_column:
            st.subheader("Average Balance: ")
            st.subheader(f"€{average_profit:,}")

        st.markdown("---")

        figTotalExpenditure = px.bar(
            totalSpendingSeason,
            # x = totalSpendingSeason.index,
            x="Season",
            y="Expenditure",
            color="League",
            title="<b>Total Expenditure by Season</b>"
        )

        if input_type == "Use system data":
            figTotalExpenditure.add_annotation(
                x="11/12",
                y=500,
                text="Introduction of financial fair play",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-150
            )

        st.plotly_chart(figTotalExpenditure)

        pos_value = st.slider(
            'Select the position displayed:',
            min_value=1, max_value=20, step=1, value=1)
        df_LeagueWinners = df_selection.groupby(['Club', 'Season', 'League', 'Position'])[
            'Expenditure'].sum().reset_index()
        df_LeagueWinners = df_LeagueWinners[df_LeagueWinners['Position'] == pos_value]
        df_LeagueWinners = df_LeagueWinners.sort_values(
            by="Season", ascending=True)

        left_column2, right_column2 = st.columns(2)
        figLeagueWinners = px.bar(
            df_LeagueWinners,
            hover_data=['Club'],
            x="Season",
            y="Expenditure",
            color="League",
            title="<b>Money spent by clubs who finished {position}</b>".format(
                position=pos_value)
        )

        with left_column2:
            st.plotly_chart(figLeagueWinners)

        with right_column2:
            df_LeagueWinners

    # CLUB PAGE DASHBOARD

    if selected == "Club":
        st.title(f"{selected} data")

        topClubExpenditure = (df_selection.groupby(by=["Club"]).sum())
        topClubExpenditure['Money Spent Per Point'] = topClubExpenditure['Expenditure'] / \
            topClubExpenditure['Points']

        with st.columns(2)[0]:
            slider_value = st.slider(
                'Select the number of clubs you would like to see displayed:',
                min_value=0, max_value=215, step=1, value=20)

        style_options = ["Balance", "Expenditure", "Income"]
        with st.columns(2)[0]:
            style_selected = st.selectbox(
                "View Balance, Expenditure or Income: ", options=style_options)

        st.markdown("---")

        left_column, right_column = st.columns(2)

        with left_column:
            topClubBalance = topClubExpenditure.sort_values(
                by=[style_selected], ascending=False).head(slider_value)
            figClubBalance = px.bar(
                topClubBalance,
                x=topClubBalance.index,
                y=style_selected,
                color=topClubBalance.index,
                orientation="v",
                title=f"<b>{style_selected} by Club</b>",
                template="plotly_white"
            )
            st.plotly_chart(figClubBalance)

        with right_column:
            figHeatmap = px.density_heatmap(
                df_selection, x='Position',
                y=style_selected,
                nbinsx=20,
                nbinsy=20,
                marginal_y='histogram',
                title=f"<b>League position by {style_selected}</b>",
                color_continuous_scale=px.colors.sequential.Inferno)
            st.plotly_chart(figHeatmap)

        st.markdown("---")
        # position_slider = st.slider(
        #     "Select range of league positions", value=[1, 20], max_value=20, min_value=1)

        left_column2, right_column2 = st.columns(2)

        with left_column2:
            topClubBalance = topClubExpenditure.sort_values(
                by=['Money Spent Per Point'], ascending=False).head(slider_value)

            figClubPts = px.bar(
                topClubBalance,
                x=topClubBalance.index,
                y='Money Spent Per Point',
                color=topClubBalance.index,
                orientation="v",
                title=f"<b>{'Money Spent Per Point'} by Club</b>",
                template="plotly_white"
            )
            st.plotly_chart(figClubPts)

        with right_column2:
            results_style_options = ["Results", "Points", "Goals"]
            results_style_selected = st.selectbox(
                "View Results, Points or Goals For", options=results_style_options)

            clubResultsByYear = (
                df_selection.groupby(['Club'])['Wins', 'Draws',
                                               'Losses', 'Points', 'Expenditure', 'GF', 'GA'].sum().reset_index()
            )
            clubResultsByYear = clubResultsByYear.sort_values(
                by=['Points'], ascending=False).head(slider_value)

            if results_style_selected == "Results":
                figClubResults = px.line(
                    clubResultsByYear, x='Club', y=['Wins', 'Draws',
                                                    'Losses'],
                    title="Results by Club", labels={
                        "value": "Games"
                    })
                st.plotly_chart(figClubResults)

            elif results_style_selected == "Goals":
                figClubResults = px.line(
                    clubResultsByYear, x='Club', y=['GF', 'GA'],
                    title="Goals by Club", labels={
                        "value": "Goals"
                    })
                st.plotly_chart(figClubResults)

            else:
                figClubResults = px.line(
                    clubResultsByYear, x='Club', y=results_style_selected,
                    title=f"{results_style_selected} by Club")
                st.plotly_chart(figClubResults)

        st.markdown("---")
        figClubExpInc = px.scatter(
            df_selection,
            x='Expenditure',
            y='Income',
            color='League',
            hover_data=['Club', 'Season'],
            trendline="ols",
            trendline_scope="overall",
            title="Expenditure against Income")
        left_column3, right_column3 = st.columns(2)
        with left_column3:
            st.plotly_chart(figClubExpInc)

        with right_column3:
            clubExpIncCoeff = np.corrcoef(
                df_selection['Expenditure'], df_selection['Income'])[0, 1]
            st.subheader("Pearson Coefficient:")
            with st.expander('What is "Pearson Coefficient"?', expanded=False):
                st.markdown(pearsonHelpText)
            st.subheader(clubExpIncCoeff)

        st.markdown("---")
        st.subheader("Data used for this page:")
        topClubExpenditure

        topClubExpenditureCsv = topClubExpenditure.to_csv().encode('utf-8')
        st.download_button(
            "Download data as CSV",
            topClubExpenditureCsv,
            "topClubExpenditure.csv",
            "text/csv",
            key='download-csv'
        )

    # LEAGUE DATA DASHBOARD

    if selected == "League":
        st.title(f"You have selected {selected}")
        leagueExpenditureByYear = (
            df_selection.groupby(['League', 'Season'])[
                'Expenditure', 'Income', 'Balance'].sum().reset_index()
        )

        figLeagueExpenditureByYear = px.line(
            leagueExpenditureByYear,
            x="Season",
            y="Expenditure",
            color="League",
            orientation="v",
            title="<b>Expenditure by Season</b>",
            template="plotly_white"
        )

        style_options = ["Minimalistic", "Detailed"]
        with st.columns(2)[0]:
            style_selected = st.selectbox(
                "Minimalistic or Detailed charts: ", options=style_options)
        if style_selected == "Detailed":
            if input_type == "Use system data":
                figLeagueExpenditureByYear.add_vline(
                    x="11/12", line_width=3, line_dash="dash", line_color="green")
            st.plotly_chart(figLeagueExpenditureByYear)

        else:
            figLeagueExpenditureByYear.update_xaxes(
                visible=False, fixedrange=True)
            figLeagueExpenditureByYear.update_yaxes(
                visible=False, fixedrange=True)
            figLeagueExpenditureByYear.update_layout(
                showlegend=False,
            )
            st.plotly_chart(figLeagueExpenditureByYear)

        st.markdown("---")

        figExpInc = px.scatter(
            leagueExpenditureByYear,
            x='Expenditure',
            y='Income',
            color='League',
            symbol='League',
            hover_data=['Season'],
            trendline="ols",
            trendline_scope="overall",
            title="Expenditure against Income")

        expIncCoeff = np.corrcoef(
            leagueExpenditureByYear['Expenditure'], leagueExpenditureByYear['Income'])[0, 1]

        left_column, right_column = st.columns(2)

        with left_column:
            st.plotly_chart(figExpInc)

        with right_column:
            st.subheader("Pearson Coefficient:")
            with st.expander('What is "Pearson Coefficient"?', expanded=False):
                st.markdown(pearsonHelpText)
            st.subheader(expIncCoeff)

        st.markdown("---")

        st.subheader("Data used for this page:")
        leagueExpenditureByYear

        leagueExpenditureByYearCsv = leagueExpenditureByYear.to_csv().encode('utf-8')
        st.download_button(
            "Download data as CSV",
            leagueExpenditureByYearCsv,
            "leagueExpenditureByYear.csv",
            "text/csv",
            key='download-csv'
        )

    if selected == "Data":
        st.header("Data used for this project:")
        st.text("Data sourced from TransferMarkt")
        df_selection
        dfCsv = df_selection.to_csv().encode('utf-8')
        st.download_button(
            "Download data as CSV",
            dfCsv,
            "clubFinanceResults.csv",
            "text/csv",
            key='download-csv'
        )


def main():
    global df, df2, input_type
    transfer_data_template = ["Club", "Season", "Expenditure",
                              "Arrivals", "Income", "Departures", "Balance", "League"]

    league_data_template = ["Position", "Club", "Played", "Wins",
                            "Draws", "Losses", "Goals", "GD", "Points", "Season", "League"]

    input_type = st.radio("Select whether you would like to enter your own data or use system data:", [
        "Use own data", "Use system data"])

    if input_type == "Use own data":
        try:
            st.write("For the transfer expenditure data, the required columns are: Club, Season, Expenditure, Arrivals, Income, Departures, Balance, League")
            url = st.text_input("Enter transfer expenditure data")
            st.write("For the league table data, the required columns are: Position, Club, Played, Wins, Draws, Losses, Goals, GD, Points, Season, League")
            url2 = st.text_input("Enter league data")
            if url and url2:
                df = pd.read_csv(url)
                df2 = pd.read_csv(url2)
                st.write(df.head(), df2.head())
                url_column = list(df.columns)
                url2_column = list(df2.columns)
                if (url_column == transfer_data_template) & (url2_column == league_data_template):
                    st.title("Data valid")
                    df = pd.merge(df, df2, on=['Club', 'Season', 'League'])
                    df[['GF', 'GA']] = df['Goals'].str.split(':', expand=True)
                    df[['GF', 'GA']] = df[['GF', 'GA']].astype(int)
                    dataVis()
                else:
                    st.title("Data invalid")
        except:
            st.title("URL Invalid")

    elif input_type == "Use system data":
        df = pd.read_csv(
            'https://raw.githubusercontent.com/Zohaib-A/footballData/main/TransferExpenditure.csv')
        df2 = pd.read_csv(
            'https://raw.githubusercontent.com/Zohaib-A/footballData/main/league.csv')

        df = pd.merge(df, df2, on=['Club', 'Season', 'League'])
        df[['GF', 'GA']] = df['Goals'].str.split(':', expand=True)
        df[['GF', 'GA']] = df[['GF', 'GA']].astype(int)
        dataVis()


if __name__ == "__main__":
    main()

hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
