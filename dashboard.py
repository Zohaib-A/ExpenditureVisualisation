# Import required libraries
import pandas as pd
import plotly_express as px
import streamlit as st
import numpy as np
from scipy.stats import linregress
from streamlit_option_menu import option_menu

# Pandas is used to read data files, put them into a data frame and provide functions for manipulating this data for advanced usage
# plotly_express is used to create visualisations with built in interaction and provide scope for expanding upon those visualisations with customisation
# streamlit is used to create the framework for the web application and allow for hosting this application as well as providing seamless integration with plotly_express
# numpy is used to provide functions for math operations and allow for manipulating values stored in arrays
# The linregress function from scipy.stats is utilised to provide linear regression based on two variables
# The option_menu function from streamlit provides a navigation bar for the code so not everything is stored on a single page, reducing eye clutter

# Set the configuration for the web application
# Set the title, icon to be displayed on the browser tab
# Set the layout of the tab to take advantage of the width of the screen as opposed to being centered
st.set_page_config(page_title="Expenditure Dashboard",
                   page_icon=":soccer:",
                   layout="wide")

# Set the header to "Football Expenditure Dashboard" in Markdown styling
st.title(":soccer: Football Expenditure Dashboard")
# Add a markdown line to separate content
st.markdown("##")

# Define function 'dataVis()' containing all visualisation


def dataVis():

    # Create a sidebar using built-in streamlit function
    st.sidebar.header("Please Filter Here:")

    # Create a widget which filters seasons, the options being unique pieces of data within "Season" columns in the data frame.
    season = st.sidebar.multiselect(
        "Select the season:",
        options=df["Season"].unique(),
        default=df["Season"].unique()
    )

    # Create a widget which filters leagues, the options being unique pieces of data within "League" columns in the data frame.
    league = st.sidebar.multiselect(
        "Select the league:",
        options=df["League"].unique(),
        default=df["League"].unique()
    )

    # Create a widget which filters clubs, the options being unique pieces of data within "Club" columns in the data frame.
    club = st.sidebar.multiselect(
        "Select the club:",
        options=df["Club"].unique(),
        default=df["Club"].unique()
    )

    # Create a data frame which filters based on the widgets defined above, using the selected values of season, league, and club
    df_selection = df.query(
        "Season == @season & League == @league & Club == @club"
    )

    # Create a navigaton bar with a horizontal orientation utilising the 'option_menu' library imported
    # Creates four options, each with icons and having the "General" page as default (index 0)
    selected = option_menu(
        menu_title=None,
        options=["General", "Club", "League", "Data"],
        icons=["house", "club", "football", "graph"],
        default_index=0,
        orientation="horizontal"
    )

    # Add a markdown line to separate content
    st.markdown("---")

    # Creates a variable with the definition for the Pearson Coefficient which allows it to be reused efficiently
    pearsonHelpText = (""" The Pearson Coefficient is a type of **correlation coefficient** that represents the relationship between two variables, measured on the same scale.
            For this example, both income and expenditure are measured in Euros, so the Pearson Coefficient is relevant here.
            The coefficient ranges from -1 to 1, where -1 is a perfectly negative correlation and 1 is a perfectly positive correlation.
            """)

    # GENERAL DATA DASHBOARD (BOTH LEAGUE AND CLUB)

    # Check if user selects General
    if selected == "General":

        # Add a title indicating the option
        st.title(f"You have selected {selected}")

        # Calculate total spending from filtered data frame
        total_spending = int(df_selection["Expenditure"].sum())
        # Calculate average balance (gross profit/loss) from filtered data frame
        average_profit = round(df_selection["Balance"].mean(), 1)

        # Group the dataframe by league and season to get the total expenditure for each season
        totalSpendingSeason = df.groupby(['League', 'Season'])[
            'Expenditure'].sum().reset_index()

        # Create a two column layout
        left_column, right_column = st.columns(2)

        # Display the total expenditure in the left column
        with left_column:
            st.subheader("Total Expenditure: ")
            st.subheader(f"€{total_spending:,}")

        # Display the average balance in the right column
        with right_column:
            st.subheader("Average Balance: ")
            st.subheader(f"€{average_profit:,}")

        st.markdown("---")

        # Create a stacked bar chart, coloured by league, showing total expenditure by season
        figTotalExpenditure = px.bar(
            totalSpendingSeason,
            x="Season",
            y="Expenditure",
            color="League",
            title="<b>Total Expenditure by Season</b>"
        )

        # Add an annotation to the chart, highlighting when financial fair play was introduced, if the user uses System data
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

        # Display the chart figTotalExpenditure
        st.plotly_chart(figTotalExpenditure)

        st.markdown("---")

        # Add a slider to select position values
        pos_value = st.slider(
            'Select the position displayed:',
            min_value=1, max_value=20, step=1, value=1)

        # Group the dataframe by club, season, league, and position to get the total expenditure for each club that finished in the slider position
        df_LeagueWinners = df_selection.groupby(['Club', 'Season', 'League', 'Position'])[
            'Expenditure'].sum().reset_index()
        df_LeagueWinners = df_LeagueWinners[df_LeagueWinners['Position'] == pos_value]

        # Sort dataframe by season in ascending order
        df_LeagueWinners = df_LeagueWinners.sort_values(
            by="Season", ascending=True)

        # Create another two column layout
        left_column2, right_column2 = st.columns(2)

        # Create a bar chart showing the money spent by clubs who finished in the slider position
        figLeagueWinners = px.bar(
            df_LeagueWinners,
            hover_data=['Club'],
            x="Season",
            y="Expenditure",
            color="League",
            title="<b>Money spent by clubs who finished {position}</b>".format(
                position=pos_value)
        )

        # Display bar chart in the left column
        with left_column2:
            st.plotly_chart(figLeagueWinners)

        # Display the manipulated data frame in the right column
        with right_column2:
            df_LeagueWinners

    # CLUB PAGE DASHBOARD

    if selected == "Club":
        st.title(f"{selected} data")

        topClubExpenditure = (df_selection.groupby(by=["Club"]).sum())
        topClubExpenditure['Money Spent Per Point'] = topClubExpenditure['Expenditure'] / \
            topClubExpenditure['Points']

        style_options = ["Balance", "Expenditure", "Income"]

        with st.columns(2)[0]:
            slider_value = st.slider(
                'Select the number of clubs you would like to see displayed:',
                min_value=0, max_value=215, step=1, value=20)
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
            color='Points',
            symbol='League',
            color_continuous_scale=px.colors.sequential.Cividis_r,
            hover_data=['Club', 'Season', 'Position'],
            trendline="ols",
            trendline_scope="overall",
            title="Expenditure against Income")
        left_column3, right_column3 = st.columns(2)

        figClubExpInc.update_traces(showlegend=False)

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
                visible=True, fixedrange=True, tickvals=["11/12"])
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
    transfer_data_template = [word.lower() for word in transfer_data_template]

    league_data_template = ["Position", "Club", "Played", "Wins",
                            "Draws", "Losses", "Goals", "GD", "Points", "Season", "League"]
    league_data_template = [word.lower() for word in league_data_template]

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
                url_column = [word.lower() for word in list(df.columns)]
                url2_column = [word.lower() for word in list(df2.columns)]
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
