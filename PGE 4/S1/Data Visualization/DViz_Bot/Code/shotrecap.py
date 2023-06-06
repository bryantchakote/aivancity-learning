def get_shot_recap(first_name, last_name, match_day):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime
    import requests

    # Player
    from nba_api.stats.static import players
    players = [player for player in players.find_players_by_full_name(first_name + ' ' + last_name)]
    
    if len(players) == 1:
        player_id = players[0]['id']
    else:
        print('None or more than one player(s) found.')
        return
    
    # Game
    ## match_day to datetime
    try:
        match_day = datetime.strptime(match_day, '%d-%m-%Y')
    except ValueError:
        print('Invalid date format.')
        return
    
    from nba_api.stats.endpoints import leaguegamefinder
    games = leaguegamefinder.LeagueGameFinder(player_id_nullable=player_id)
    game = games.get_data_frames()[0].query(f'GAME_DATE == "{match_day.year}-{match_day.month}-{str(match_day.day).zfill(2)}"')

    if len(game) == 0:
        print('No match found at that date')
        return
    
    # Game actions
    url = f'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{game.GAME_ID.item()}.json'
    game_actions = requests.get(url).json()['game']['actions']

    clock = [0]
    points = [0]
    made_clock = [0]
    made_points = [0]
    
    for game_action in game_actions:
        if ((game_action['personId'] == player_id) &
        (game_action['actionType'] in ['2pt', '3pt', 'freethrow'])):
            clock.append(12 * (game_action['period'] - 1) + 12 - (int(game_action['clock'][2:4]) + int(game_action['clock'][5:7]) / 60.))

            if game_action['actionType'] == 'freethrow': points.append(points[-1] + 1)
            if game_action['actionType'] == '2pt': points.append(points[-1] + 2)
            if game_action['actionType'] == '3pt': points.append(points[-1] + 3)
                
            if game_action['shotResult'] == 'Made':
                made_clock.append(12 * (game_action['period'] - 1) + 12 - (int(game_action['clock'][2:4]) + int(game_action['clock'][5:7]) / 60.))

                if game_action['actionType'] == 'freethrow': made_points.append(made_points[-1] + 1)
                if game_action['actionType'] == '2pt': made_points.append(made_points[-1] + 2)
                if game_action['actionType'] == '3pt': made_points.append(made_points[-1] + 3)

    clock.append(48)
    points.append(points[-1])
    made_clock.append(48)
    made_points.append(made_points[-1])
    
    attempted = pd.DataFrame({'clock': clock, 'points': points})
    made = pd.DataFrame({'clock': made_clock, 'points': made_points})
    
    # Plot
    fig, ax = plt.subplots()
    colors = sns.color_palette('deep', n_colors=5)
    
    ## The steps
    ax.plot(attempted.clock, attempted.points, drawstyle='steps', color=colors[4])
    ax.plot(made.clock, made.points, drawstyle='steps', color=colors[0])
    
    ## The area under curve
    ax.fill_between(attempted.clock, attempted.points, step='pre', label='Attempted', alpha=.4, color=colors[4])
    ax.fill_between(made.clock, made.points, step='pre', label='Made', alpha=.4, color=colors[0])

    ## Axes, ticks, legend and title
    ax.set(xlim=(0, 48), ylim=(0, None))
    plt.xticks(ticks=[0, 12, 24, 36, 48], labels=['Start', '1st q.', '2nd q.', '3rd q.', 'End'])
    ax.tick_params(grid_linewidth=.2)
    plt.grid()
    plt.legend(loc='best')
    
    # Opponent team
    from nba_api.stats.static import teams
    opponent = teams.find_team_by_abbreviation(game.MATCHUP.str[-3:].item())['nickname']
    
    match_day = f'{str(match_day.day).zfill(2)}-{match_day.month}-{match_day.year}'
    plt.title(f'{first_name.title()} {last_name.title()}\'s shoots against {opponent} ({match_day})')
    plt.tight_layout()
    plt.savefig(f'shotrecap_{first_name}_{last_name}_{match_day}.png')
