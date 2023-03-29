import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import tableauhyperapi as tabapi

# Connect to SQL database
conn = sqlite3.connect('nba_shots.db')

# Define SQL queries
team_data_query = """
SELECT team_name, COUNT(*) as attempts, 
SUM(CASE WHEN shot_made_flag = 1 THEN 1 ELSE 0 END) as made, 
SUM(CASE WHEN shot_made_flag = 0 THEN 1 ELSE 0 END) as missed, 
ROUND(SUM(CASE WHEN shot_made_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as accuracy
FROM nba_shots
WHERE season >= 2019
GROUP BY team_name
"""

player_data_query = """
SELECT player_name, COUNT(*) as attempts, 
SUM(CASE WHEN shot_made_flag = 1 THEN 1 ELSE 0 END) as made, 
SUM(CASE WHEN shot_made_flag = 0 THEN 1 ELSE 0 END) as missed, 
ROUND(SUM(CASE WHEN shot_made_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as accuracy
FROM nba_shots
WHERE season >= 2019
GROUP BY player_name
"""

shot_data_query = """
SELECT player_name, shot_zone_basic, COUNT(*) as attempts, 
SUM(CASE WHEN shot_made_flag = 1 THEN 1 ELSE 0 END) as made, 
SUM(CASE WHEN shot_made_flag = 0 THEN 1 ELSE 0 END) as missed, 
ROUND(SUM(CASE WHEN shot_made_flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as accuracy
FROM nba_shots
WHERE season >= 2019
GROUP BY player_name, shot_zone_basic
"""

# Load data into Pandas dataframes
team_data = pd.read_sql_query(team_data_query, conn)
player_data = pd.read_sql_query(player_data_query, conn)
shot_data = pd.read_sql_query(shot_data_query, conn)

# Define function to get best shot profile for a player
def get_best_shot_profile(player_name):
    player_shots = shot_data[shot_data['player_name'] == player_name].reset_index(drop=True)
    if len(player_shots) == 0:
        return None
    kmeans = KMeans(n_clusters=5, random_state=0).fit(player_shots[['accuracy', 'attempts']])
    player_shots['cluster'] = kmeans.predict(player_shots[['accuracy', 'attempts']])
    pca = PCA(n_components=2)
    player_shots[['pca1', 'pca2']] = pca.fit_transform(player_shots[['accuracy', 'attempts']])
    sns.scatterplot(data=player_shots, x='pca1', y='pca2', hue='cluster', palette='tab10')
    plt.show()
    return player_shots.loc[player_shots['cluster'] == player_shots['cluster'].value_counts().idxmax()]

# Get best shot profile for LeBron James
lebron_profile = get_best_shot_profile('LeBron James')
print(lebron_profile)

# Define Tableau Hyper API connection and create data extract
with tabapi.Connection("nba_shots.hyper") as connection:
# Define schema for team data
team_data_schema = tabapi.TableDefinition(
    table_name='team_data',
    columns=[
        tabapi.TableDefinition.Column(name='team_name', type=tabapi.SqlType.text()),
        tabapi.TableDefinition.Column(name='attempts', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='made', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='missed', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='accuracy', type=tabapi.SqlType.double())
    ]
)

# Create and insert data into team data extract
with tabapi.Extract('nba_shots.hyper', mode=tabapi.ExtractMode.CREATE) as extract:
    table = extract.add_table('Extract', team_data_schema)
    for index, row in team_data.iterrows():
        table.insert({
            'team_name': row['team_name'],
            'attempts': row['attempts'],
            'made': row['made'],
            'missed': row['missed'],
            'accuracy': row['accuracy']
        })
    extract.close()

# Define schema for player data
player_data_schema = tabapi.TableDefinition(
    table_name='player_data',
    columns=[
        tabapi.TableDefinition.Column(name='player_name', type=tabapi.SqlType.text()),
        tabapi.TableDefinition.Column(name='attempts', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='made', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='missed', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='accuracy', type=tabapi.SqlType.double())
    ]
)

# Create and insert data into player data extract
with tabapi.Extract('nba_shots.hyper', mode=tabapi.ExtractMode.UPDATE) as extract:
    table = extract.open_table('player_data')
    for index, row in player_data.iterrows():
        table.insert({
            'player_name': row['player_name'],
            'attempts': row['attempts'],
            'made': row['made'],
            'missed': row['missed'],
            'accuracy': row['accuracy']
        })
    extract.close()

# Define schema for shot data
shot_data_schema = tabapi.TableDefinition(
    table_name='shot_data',
    columns=[
        tabapi.TableDefinition.Column(name='player_name', type=tabapi.SqlType.text()),
        tabapi.TableDefinition.Column(name='shot_zone_basic', type=tabapi.SqlType.text()),
        tabapi.TableDefinition.Column(name='attempts', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='made', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='missed', type=tabapi.SqlType.big_int()),
        tabapi.TableDefinition.Column(name='accuracy', type=tabapi.SqlType.double())
    ]
)

# Create and insert data into shot data extract
with tabapi.Extract('nba_shots.hyper', mode=tabapi.ExtractMode.UPDATE) as extract:
    table = extract.open_table('shot_data')
    for index, row in shot_data.iterrows():
        table.insert({
            'player_name': row['player_name'],
            'shot_zone_basic': row['shot_zone_basic'],
            'attempts': row['attempts'],
            'made': row['made'],
            'missed': row['missed'],
            'accuracy': row['accuracy']
        })



