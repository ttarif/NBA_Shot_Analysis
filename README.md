# NBA Shot Analysis
This code analyzes data related to NBA shots. The data is stored in a SQLite database and is loaded into Pandas dataframes for analysis. Visualizations and a Tableau data extract are created using the Tableau Hyper API.

# Instructions
To run this code, follow these steps:

Ensure that you have the necessary Python libraries installed (sqlite3, pandas, numpy, matplotlib, seaborn, scikit-learn, and tableauhyperapi).

~~~python 
pip install sqlite3 pandas numpy matplotlib scikit-learn seaborn tableauhyperapi
~~~

Download the nba_shots.db SQLite database file and ensure that it is in the same directory as the code file.
Run the code. As configured it will output a scatterplot of LeBron James' shot data and print the row of data corresponding to his best shot profile. It will also create two Tableau extracts (team_data and player_data) in a nba_shots.hyper file.
Note that this code assumes that the SQLite database and Tableau extract files do not yet exist. If you need to modify the queries or schema, you should delete the existing nba_shots.hyper file before running the code.

# Usage
To use this code, download the SQLite database with the NBA shots data from Kaggle or create your own. Modify the code to specify the location of the SQLite database.

Run the code in a Python environment or from the command line:

~~~python
python nba_shots_analysis.py
~~~

The code generates the following outputs:

A Pandas dataframe with team data, including number of shot attempts, number of made shots, number of missed shots, and shooting accuracy.
A Pandas dataframe with player data, including number of shot attempts, number of made shots, number of missed shots, and shooting accuracy.
A Pandas dataframe with shot data, including number of shot attempts, number of made shots, number of missed shots, shooting accuracy, and shot zone.
A visualization of the best shot profile for a given player. The best shot profile is determined by clustering the player's shots based on accuracy and number of attempts, and selecting the cluster with the most shots.
A Tableau data extract with team data and player data.

# Code Description
This code connects to an SQLite database containing NBA shot data and retrieves team, player, and shot data for the 2019 and later seasons. The team_data_query and player_data_query variables contain SQL queries to retrieve team and player data, respectively. The shot_data_query variable contains a query to retrieve shot data, including the number of attempts, made shots, missed shots, and accuracy for each player and shot zone.

The code uses the pandas library to load the SQL query results into dataframes and the matplotlib and seaborn libraries to create visualizations of the shot data. The get_best_shot_profile function takes a player name as input, retrieves the player's shot data from the shot_data dataframe, and uses k-means clustering and principal component analysis (PCA) to identify the player's best shot profile. It then creates a scatterplot of the shot data, colored by cluster, and returns the row of data corresponding to the player's best shot profile.

The code also uses the tableauhyperapi library to create Tableau data extracts. The team_data_schema and player_data_schema variables define the schema for the team_data and player_data extracts, respectively. The code then creates and inserts data into these extracts using the tabapi.Extract and tabapi.Table.insert functions.







