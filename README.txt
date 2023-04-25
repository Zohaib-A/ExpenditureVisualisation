INSTRUCTIONS TO USE dashboard.py:
Project has been hosted on the web and can be accessed via this link:
https://expenditure-visualisation-zohaib-a.streamlit.app/

The data sources being used in this project can be found via:
https://raw.githubusercontent.com/Zohaib-A/footballData/main/TransferExpenditure.csv
https://raw.githubusercontent.com/Zohaib-A/footballData/main/league.csv

Further testing can be done using these dummy data links:
https://raw.githubusercontent.com/Zohaib-A/footballData/main/archive/TransferExpenditureTest.csv
https://raw.githubusercontent.com/Zohaib-A/footballData/main/archive/leagueTest.csv


FILE STRUCTURE:
The main folder contains dashboard.py, which is the main bulk of the web application.
The "requirements.txt" are all the external modules used and installed.
The "Webscrape.ipynb" contains the code to create CSV files from tables scraped from TransferMarkt.
An example of the tables created can be found in the "resources" folder, being labelled "TransferExpenditure.csv" and "league.csv".

Everything should also be available here: https://github.com/Zohaib-A/ExpenditureVisualisation

INSTRUCTIONS TO LOAD dashboard.py LOCALLY:
1) Install Python from https://www.python.org/downloads/
2) Install pip by using "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py" and then "python get-pip.py" in Terminal
3) Install all necessary modules in Terminal:
pip install numpy
pip install pandas
pip install plotly_express
pip install scipy
pip install streamlit
4) Launch application by using "python -m streamlit run FILE PATH\dashboard.py" in Terminal

INSTRUCTIONS TO LOAD Webscrape.ipynb:
1) Install Python from https://www.python.org/downloads/
2) Install pip by using "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py" and then "python get-pip.py"
3) Install all necessary modules:
pip install beautifulsoup4
pip install pandas
pip install notebook
4) Launch Webscrape.ipynb