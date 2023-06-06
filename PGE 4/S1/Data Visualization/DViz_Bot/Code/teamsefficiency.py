def get_teams_efficiency():
    from nba_api.stats.endpoints import leaguedashteamstats
    from nba_api.stats.static import teams
    import numpy as np
    import plotly.express as px

    leagues_stats_advanced = leaguedashteamstats.LeagueDashTeamStats(last_n_games=15,measure_type_detailed_defense='Advanced').get_data_frames()[0]
    columns=['TEAM_NAME','OFF_RATING','DEF_RATING']
    leagues_stats_advanced[columns]
    leagues_stats_advanced.TEAM_NAME[12]='Los Angeles Clippers'
    abbreviation=[teams.find_teams_by_full_name(team_name)[0]['abbreviation'] for team_name in leagues_stats_advanced.TEAM_NAME]
    df = leagues_stats_advanced   
    def middle(x):
        maxi=int(x.max())
        mini= int(x.min())
        return (maxi+mini)/2

    fig = px.scatter(df, x=df.OFF_RATING, y=df.DEF_RATING, text=abbreviation,title='<b>The Efficiency Landscape</b>')

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout({'plot_bgcolor': 'rgb(231,210,186)',
                       'paper_bgcolor': 'rgb(231,210,186)'
                      },height=800,
                        title_font_family="Arial",
                        title_font_color="#905d5d",
                        title_x=0.5,
                        title_font_size=30
                        )
    fig.update_traces(textposition='middle right',marker=dict(size=9, color='#905d5d',line=dict(width=2,color='#905d5d')))

    fig.add_layout_image(
            dict(
                source="https://upload.wikimedia.org/wikipedia/fr/8/87/NBA_Logo.svg",
                xref="x",
                yref="y",
                x=middle(df.DEF_RATING)-0.5,
                y=middle(df.OFF_RATING)+2.5,
                sizex=7,
                sizey=7,
                opacity=0.2,
                layer="above")
    )
    fig.add_hline(y=middle(df.DEF_RATING))
    fig.add_vline(x=middle(df.OFF_RATING))
    fig.add_annotation(
         y=df.DEF_RATING.max()+2.5
        ,x=middle(df.DEF_RATING)+0.5
        , text='<i>Defensive Efficiency</i>'
        , showarrow=False
        ,textangle=-90
        ,font=dict(size=18, color="grey", family="Times new roman")
        )
    fig.add_annotation(
         x=df.DEF_RATING.max()+5
        ,y=middle(df.DEF_RATING)-0.3
        , text='<i>Offensive Efficiency</i>'
        , showarrow=False
        ,font=dict(size=17, color="grey", family="Times new roman")
        )
    fig.write_image('teamsefficiency.png')
