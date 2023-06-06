def get_compare_players(first_name_1, last_name_1, first_name_2, last_name_2):
    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    import plotly.express as px
    import pandas as pd
    
    # Player 1
    from nba_api.stats.static import players
    players = [player for player in players.find_players_by_full_name(first_name_1 + ' ' + last_name_1)]
    if len(players) == 1: player_1_id, player_1_name = players[0]['id'], players[0]['full_name']
    else: print('None or more than one player(s) found.'); return
    
    # Player 2
    from nba_api.stats.static import players
    players = [player for player in players.find_players_by_full_name(first_name_2 + ' ' + last_name_2)]
    if len(players) == 1: player_2_id, player_2_name = players[0]['id'], players[0]['full_name']
    else: print('None or more than one player(s) found.'); return
    
    # Players stats
    columns = ['PTS', 'REB', 'AST', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'BLK', 'PF', 'TOV', 'STL']

    from nba_api.stats.endpoints import leaguedashplayerstats
    players_stats = leaguedashplayerstats.LeagueDashPlayerStats()
    players_stats = players_stats.get_data_frames()[0][['PLAYER_ID'] + columns]
    
    for column in columns:
            players_stats[column] = MinMaxScaler().fit_transform(np.array(players_stats[column]).reshape(-1, 1)).reshape(-1)
            
    player_1 = players_stats.query(f'PLAYER_ID == {player_1_id}').drop(columns=['PLAYER_ID']).T.reset_index()
    player_1 = player_1.rename(columns={'index': 'param', list(player_1)[1]: 'level'})
    player_1['name'] = player_1_name

    player_2 = players_stats.query(f'PLAYER_ID == {player_2_id}').drop(columns=['PLAYER_ID']).T.reset_index()
    player_2 = player_2.rename(columns={'index': 'param', list(player_2)[1]: 'level'})
    player_2['name'] = player_2_name

    data = pd.concat([player_1, player_2])

    # Plot
    fig = px.line_polar(data, r='level', theta='param', color='name', line_close=True, title=f'{player_1_name} vs. {player_2_name} during this season')
    fig.update_traces(fill='toself', opacity=.6)
    fig.write_image(f'compareplayers_{first_name_1}_{last_name_1}_{first_name_2}_{last_name_2}.png')
