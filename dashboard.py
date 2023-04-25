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
    # Check if the selected option is "Club"
    if selected == "Club":

        # Set the page title to club data
        st.title(f"{selected} data")

        # Group the data frame by "Club" and calculate the total for each column
        topClubExpenditure = (df_selection.groupby(by=["Club"]).sum())

        # Calculate money spent per point by dividing expenditure by the points total
        topClubExpenditure['Money Spent Per Point'] = topClubExpenditure['Expenditure'] / \
            topClubExpenditure['Points']

        # Set list of options for the user for the drop down menu
        style_options = ["Balance", "Expenditure", "Income"]

        # Create a two column layout, having the items within the "with" statement on the left side of the layout
        with st.columns(2)[0]:
            # Create a slider widget to ask the user how many clubs should be displayed, default value of ,with a minimum value of 0, maximum 215, incrementing in steps of 1.
            slider_value = st.slider(
                'Select the number of clubs you would like to see displayed:',
                min_value=0, max_value=215, step=1, value=20)
            # Create a drop down menu which asks the user what data they would like to use from the "style_options" list defined above.
            # Default value set to "Balance"
            style_selected = st.selectbox(
                "View Balance, Expenditure or Income: ", options=style_options)

        st.markdown("---")

        # Create a two column layout
        left_column, right_column = st.columns(2)

        # Sort the data frame by the users selection from the drop down, and displays the amount of clubs selected by the slider
        with left_column:
            topClubBalance = topClubExpenditure.sort_values(
                by=[style_selected], ascending=False).head(slider_value)
            # Create a bar chart with the x axis of the clubs, the y axis of the selected drop down style
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

        # Create a heatmap with the league position on the x axis and y axis with selected style
        # Creates a histogram based on the amount of spending per range
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

        # Create a two column layout
        left_column2, right_column2 = st.columns(2)

        with left_column2:
            # Sort data frame by the amount of money spent per point in descending order, with "slider_value" amount of clubs being shown
            topClubBalance = topClubExpenditure.sort_values(
                by=['Money Spent Per Point'], ascending=False).head(slider_value)
            # Create a bar chart with the x axis of the clubs, the y axis of amount of money spent per point
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
            # Create a drop down menu to allow the user to select whether they would like to see Results, Points or Goals, with Results as default option
            results_style_options = ["Results", "Points", "Goals"]
            results_style_selected = st.selectbox(
                "View Results, Points or Goals For", options=results_style_options)

            # Group the data frame by club and calculate total wins, draws, losses, points, expenditure, goals for and against
            clubResultsByYear = (
                df_selection.groupby(['Club'])['Wins', 'Draws',
                                               'Losses', 'Points', 'Expenditure', 'GF', 'GA'].sum().reset_index()
            )

            # Sort the data frame by total points, with slider_value amount of clubs being shown
            clubResultsByYear = clubResultsByYear.sort_values(
                by=['Points'], ascending=False).head(slider_value)

            # If the user selects "Results", create a line graph with club against "wins, draws, losses" with values of total games when the user hovers over a point
            if results_style_selected == "Results":
                figClubResults = px.line(
                    clubResultsByYear, x='Club',
                    y=['Wins', 'Draws', 'Losses'],
                    title="Results by Club",
                    labels={
                        "value": "Games"
                    })
                st.plotly_chart(figClubResults)

            # If the user selects "Goals", create a line graph with club against "GF, GA" with values of total games when the user hovers over a point
            elif results_style_selected == "Goals":
                figClubResults = px.line(
                    clubResultsByYear, x='Club', y=['GF', 'GA'],
                    title="Goals by Club", labels={
                        "value": "Goals"
                    })
                st.plotly_chart(figClubResults)

            # If the user selects "Points", create a line graph with club against "Points"
            else:
                figClubResults = px.line(
                    clubResultsByYear, x='Club', y=results_style_selected,
                    title=f"{results_style_selected} by Club")
                st.plotly_chart(figClubResults)

        st.markdown("---")

        # Create a scatterplot of all expenditure against income, coloured by points, with league symbols
        # Hover data contains club, season and position
        # Create a linear trendline for the overall data set
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

        # Create a two column layout
        left_column3, right_column3 = st.columns(2)

        # Hide the legend for scatterplot
        figClubExpInc.update_traces(showlegend=False)

        # Plot the scatterplot
        with left_column3:
            st.plotly_chart(figClubExpInc)

        # Calculate coefficient between expenditure and income and display.
        # Create an expandable box which displays the definition of the Pearson Coefficient
        with right_column3:
            clubExpIncCoeff = np.corrcoef(
                df_selection['Expenditure'], df_selection['Income'])[0, 1]
            st.subheader("Pearson Coefficient:")
            with st.expander('What is "Pearson Coefficient"?', expanded=False):
                st.markdown(pearsonHelpText)
            st.subheader(clubExpIncCoeff)

        st.markdown("---")

        # Highlight the manipulated data used for majority of graphs on this page
        st.subheader("Data used for this page:")
        topClubExpenditure

        # Create download data frame button as CSV
        topClubExpenditureCsv = topClubExpenditure.to_csv().encode('utf-8')
        st.download_button(
            "Download data as CSV",
            topClubExpenditureCsv,
            "topClubExpenditure.csv",
            "text/csv",
            key='download-csv'
        )

    # LEAGUE DATA DASHBOARD

    # Check if the selected option is "League"
    if selected == "League":
        st.title(f"You have selected {selected}")

        # Group the data frame by League and Season, calculating the total expenditure, income and balance by each league per season
        leagueExpenditureByYear = (
            df_selection.groupby(['League', 'Season'])[
                'Expenditure', 'Income', 'Balance'].sum().reset_index()
        )

        # Create a line graph of the above data frame using plotly_express, with x axis of Season, y axis of expenditure, coloured in regards to league
        figLeagueExpenditureByYear = px.line(
            leagueExpenditureByYear,
            x="Season",
            y="Expenditure",
            color="League",
            orientation="v",
            title="<b>Expenditure by Season</b>",
            template="plotly_white"
        )

        # Create a list of style options, Minimalistic (Tufte-inspired styling) or a standard line graph
        style_options = ["Minimalistic", "Detailed"]
        with st.columns(2)[0]:
            # Create a drop down menu aligned to the left asking the user what type of graph they would like
            style_selected = st.selectbox(
                "Minimalistic or Detailed charts: ", options=style_options)

        # If the user selects detailed and is using system data, create a dashed line at season 11/12 and display graph
        if style_selected == "Detailed":
            if input_type == "Use system data":
                figLeagueExpenditureByYear.add_vline(
                    x="11/12", line_width=3, line_dash="dash", line_color="green")
            st.plotly_chart(figLeagueExpenditureByYear)

        # If the user sticks to a minimalistic graph:
        else:
            # Update the x axis to be invisible and be fixed, showing just where 11/12 is for reference
            figLeagueExpenditureByYear.update_xaxes(
                visible=True, fixedrange=True, tickvals=["11/12"])
            # Update the y axis to be invisible and fixed
            figLeagueExpenditureByYear.update_yaxes(
                visible=False, fixedrange=True)
            # Hide the legend
            figLeagueExpenditureByYear.update_layout(
                showlegend=False,
            )
            # Display modified graph
            st.plotly_chart(figLeagueExpenditureByYear)

        st.markdown("---")

        # Create a scatterplot of all expenditure against income, coloured by league, with league symbols too
        # Hover data contains league and season
        # Create a linear trendline for the overall data set
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

        # Calculate coefficient between expenditure and income and display.
        expIncCoeff = np.corrcoef(
            leagueExpenditureByYear['Expenditure'], leagueExpenditureByYear['Income'])[0, 1]

        left_column, right_column = st.columns(2)

        with left_column:
            # Display scatterplot
            st.plotly_chart(figExpInc)

        with right_column:
            st.subheader("Pearson Coefficient:")
            # Create an expandable box which displays the definition of the Pearson Coefficient
            with st.expander('What is "Pearson Coefficient"?', expanded=False):
                st.markdown(pearsonHelpText)
            # Display the coefficient
            st.subheader(expIncCoeff)

        st.markdown("---")

        # Highlight the manipulated data used for majority of graphs on this page
        st.subheader("Data used for this page:")
        leagueExpenditureByYear

        # Create download data frame button as CSV
        leagueExpenditureByYearCsv = leagueExpenditureByYear.to_csv().encode('utf-8')
        st.download_button(
            "Download data as CSV",
            leagueExpenditureByYearCsv,
            "leagueExpenditureByYear.csv",
            "text/csv",
            key='download-csv'
        )

    # Check if the selected option is "Data"
    if selected == "Data":
        # Create a header
        st.header("Data used for this project:")
        # Provide text from where data was sourced from
        st.markdown(
            "Data sourced from [TransferMarkt](https://www.transfermarkt.co.uk/premier-league/einnahmenausgaben/wettbewerb/GB1)")
        # Display the data frame used for the majority of the project
        df_selection
        # Encode data frame as CSV in utf-8
        dfCsv = df_selection.to_csv().encode('utf-8')
        # Create download data frame button as CSV
        st.download_button(
            "Download data as CSV",
            dfCsv,
            "clubFinanceResults.csv",
            "text/csv",
            key='download-csv'
        )

# Define main initialising function


def main():
    global df, df2, input_type

    # Define templates for transfer and league data to be imported
    transfer_data_template = ["Club", "Season", "Expenditure",
                              "Arrivals", "Income", "Departures", "Balance", "League"]
    transfer_data_template = [word.lower() for word in transfer_data_template]

    league_data_template = ["Position", "Club", "Played", "Wins",
                            "Draws", "Losses", "Goals", "GD", "Points", "Season", "League"]
    league_data_template = [word.lower() for word in league_data_template]

    # Create a radio button allowing user to use their own data or select system data
    input_type = st.radio("Select whether you would like to enter your own data or use system data:", [
        "Use own data", "Use system data"])

    if input_type == "Use own data":
        try:
            # Provide the user with information as to what the format of the data should be
            st.write("For the transfer expenditure data, the required columns are: Club, Season, Expenditure, Arrivals, Income, Departures, Balance, League")
            # Allow the user to input data
            url = st.text_input("Enter transfer expenditure data")
            # Provide the user with information as to what the format of the data should be
            st.write("For the league table data, the required columns are: Position, Club, Played, Wins, Draws, Losses, Goals, GD, Points, Season, League")
            # Allow the user to input data
            url2 = st.text_input("Enter league data")

            # Check if both URLs are provided and then append them to a data frame
            if url and url2:
                df = pd.read_csv(url)
                df2 = pd.read_csv(url2)
                st.write(df.head(), df2.head())
                # Convert column names to lower case
                url_column = [word.lower() for word in list(df.columns)]
                url2_column = [word.lower() for word in list(df2.columns)]
                # Check if the column format is the same as the template for both URLs
                if (url_column == transfer_data_template) & (url2_column == league_data_template):
                    st.title("Data valid")
                    # Merge the data based on club, season or league
                    df = pd.merge(df, df2, on=['Club', 'Season', 'League'])
                    df[['GF', 'GA']] = df['Goals'].str.split(':', expand=True)
                    df[['GF', 'GA']] = df[['GF', 'GA']].astype(int)
                    # Call dataVis to display visualisations
                    dataVis()
                else:
                    st.title("Data invalid")
        except:
            # If URL is invalid, instead of erroring out, the user will be presented with this message
            st.title("URL Invalid")

    # Check if user selects system data
    elif input_type == "Use system data":
        # Define the two data frames, transfer and league datasets
        df = pd.read_csv(
            'https://raw.githubusercontent.com/Zohaib-A/footballData/main/TransferExpenditure.csv')
        df2 = pd.read_csv(
            'https://raw.githubusercontent.com/Zohaib-A/footballData/main/league.csv')

        # Merge the data based on club, season or league
        df = pd.merge(df, df2, on=['Club', 'Season', 'League'])
        df[['GF', 'GA']] = df['Goals'].str.split(':', expand=True)
        df[['GF', 'GA']] = df[['GF', 'GA']].astype(int)
        # Call dataVis to display visualisations
        dataVis()


# Running the main function
if __name__ == "__main__":
    main()

# Hiding streamlit header and footer
hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# References:
# https://youtu.be/hEPoto5xp3k (Coding Is Fun 2022): This source was used to create the navigation pane used to explore the web application
# https://youtu.be/Sb0A9i6d320 (Coding Is Fun 2021): This source was used to provide the skeleton for the web application and assist with learning Streamlit
