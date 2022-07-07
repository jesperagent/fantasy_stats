import pandas as pd
import requests

matches = pd.read_csv('fotmob_matcher_22.csv')
match_id = matches['match_id'].tolist()


def get_match_data(match_id):
    url = 'https://www.fotmob.com/api/matchDetails?matchId=' + str(match)
    r = requests.get(url)
    jsonResponse = r.json()

    if jsonResponse['general']['started'] == True:

        match_round = jsonResponse['general']['matchRound']
        lineups = jsonResponse['content']['lineup']['lineup']

        players_data = pd.DataFrame([],
                                    columns=[
                                        'player_id',
                                        'first_name',
                                        'last_name',
                                        'team_name',
                                        'match_round',
                                        'match_id',
                                        'starts',
                                        'sub_in',
                                        'minutes',
                                        'xGoals',
                                        'xAassists',
                                        'goals',
                                        'assists',
                                        'shots',
                                        'key_passes',
                                        'corners',
                                        'recoveries',
                                        'clearances',
                                        'blocked_shots',
                                        'interceptions']).set_index('player_id')

        for lineup in lineups:
            team_name = lineup['teamName']

            for players in lineup['players']:
                for player in players:
                    players_data = append_player_data_to_dataframe(player, team_name, match_round, players_data)
            for player in lineup['bench']:
                players_data = append_player_data_to_dataframe(player, team_name, match_round, players_data)

        return players_data


def append_player_data_to_dataframe(player, team_name, match_round, df):
    id = player['id']
    first_name = player['name']['firstName']
    last_name = player['name']['lastName']

    try:
        starts = 1 if player['timeSubbedOn'] == None and player['minutesPlayed'] != 0 else 0
    except:
        starts = 0
    try:
        sub_in = 0 if player['timeSubbedOn'] == None else 1
    except:
        sub_in = 0
    try:
        minutes = player['minutesPlayed']
    except:
        minutes = 0
    try:
        xG = float(player['stats'][0]['stats']['Expected goals (xG)'])
    except:
        xG = 0.0
    try:
        xA = float(player['stats'][0]['stats']['Expected assists (xA)'])
    except:
        xA = 0.0
    try:
        goals = player['stats'][0]['stats']['Goals']
    except:
        goals = 0
    try:
        assists = player['stats'][0]['stats']['Assists']
    except:
        assists = 0
    try:
        shots = player['stats'][0]['stats']['Total shots']
    except:
        shots = 0
    try:
        key_passes = player['stats'][0]['stats']['Chances created']
    except:
        key_passes = 0
    try:
        corners = player['stats'][1]['stats']['Corners']
    except:
        corners = 0
    try:
        recoveries = player['stats'][2]['stats']['Recoveries']
    except:
        recoveries = 0
    try:
        clearances = player['stats'][2]['stats']['Clearances']
    except:
        clearances = 0
    try:
        blocked_shots = player['stats'][2]['stats']['Blocks']
    except:
        blocked_shots = 0
    try:
        interceptions = player['stats'][2]['stats']['Interceptions']
    except:
        interceptions = 0

    player_match_data = [[
        id,
        first_name,
        last_name,
        team_name,
        match_round,
        match,
        starts,
        sub_in,
        minutes,
        xG,
        xA,
        goals,
        assists,
        shots,
        key_passes,
        corners,
        recoveries,
        clearances,
        blocked_shots,
        interceptions
    ]]

    return df.append(pd.DataFrame(player_match_data, columns=
    [
        'player_id',
        'first_name',
        'last_name',
        'team_name',
        'match_round',
        'match_id',
        'starts',
        'sub_in',
        'minutes',
        'xGoals',
        'xAssists',
        'goals',
        'assists',
        'shots',
        'key_passes',
        'corners',
        'recoveries',
        'clearances',
        'blocked_shots',
        'interceptions']).set_index('player_id'))

players_data = pd.DataFrame([],
columns= [
    'player_id',
    'first_name',
    'last_name',
    'team_name',
    'match_round',
    'match_id',
    'starts',
    'sub_in',
    'minutes',
    'xGoals',
    'xAssists',
    'goals',
    'assists',
    'shots',
    'key_passes',
    'corners',
    'recoveries',
    'clearances',
    'blocked_shots',
    'interceptions']).set_index('player_id')

for match in match_id:
    match_data = get_match_data(match)
    players_data = players_data.append(match_data, sort=False)

players_data.loc[players_data['match_id'] == 3805038, 'match_round'] = '7'
players_data.loc[players_data['match_id'] == 3805009, 'match_round'] = '8'

players_data[['match_round', 'minutes', 'goals', 'assists',
    'shots', 'key_passes', 'corners', 'recoveries',
    'clearances', 'blocked_shots', 'interceptions']] = players_data[['match_round', 'minutes', 'goals', 'assists',
                                                                     'shots', 'key_passes', 'corners', 'recoveries',
                                                                     'clearances', 'blocked_shots',
                                                                     'interceptions']].astype(int)

players_data['xGI'] = players_data['xGoals'] + players_data['xAssists']
players_data['xGI'] = players_data['xGI'].round(decimals = 2)
players_data['def_act'] = players_data['recoveries'] + players_data['clearances'] + players_data['blocked_shots'] \
                          + players_data['interceptions']
players_data['name'] = players_data["first_name"] + str(' ') + players_data["last_name"]
df = players_data[['name','team_name', 'match_round', 'minutes', 'xGoals', 'xAssists', 'xGI', 'goals',
                   'assists', 'shots', 'key_passes', 'corners', 'def_act', 'recoveries', 'clearances', 'blocked_shots',
                   'interceptions']].reset_index(drop=True)

df = df.sort_values(by=['match_round', 'name'])

df.to_csv('fotmob_players.csv',index=False)