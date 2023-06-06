# Data Vizualization Discord Bot with Python

## About The Project

This projects consists in designing a discord bot with Python which answers to specific commands with graphs. The data used is NBA data collected from the **NBA API**.

### What is in the API?
The NBA API can be used to access NBA-related data without credentials. It contains all imaginable NBA data (more than 100 endpoints).

## Getting Started

### Project Files Description

Our project contains five python scripts:

- main.py: it's the main project file which serves as bot controller. Bot commands are defined there.
- compareplayers.py: contains the compare_players function which returns a polar graph comparing two NBA players' skills.
- shootrecap.py: contains the shoot_recap function which returns shot attempts and made shots of a player during a game.
- teamsefficiency.py: contains the teams_efficiency function which returns each team efficiency landscape for the last 15 games.

### Usage

First run the main.py file to get the bot logged in.

#### Compare two players skills
!compare_players [player_1_first_name] [player_1_last_name] [player_2_first_name] [player_2_last_name]

#### Visualize the number of shot attempts and made shot of a player
!shoot_recap [first_name] [last_name] [match_day]

#### Get the teams efficiency landscape
!team_efficiency
