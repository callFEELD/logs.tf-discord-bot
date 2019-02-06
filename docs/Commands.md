# Commands
These commands are for the current version `1.3 -dev Server Edition`

## Help commands

- `!logs help` shows you all the commands listed below

- `!logs teamhelp` shows you all the team specific commands
 

## Basic commands

- `!logs` shows your last played match with details about your performance

- `!logs profile` shows your logs.tf profile

- `!logs <@name>` shows the last log of the player you looked for

- `!logs <@name> profile` shows the logs.tf profile of the player you looked for


## Basic team commands

- `!logs match <teamname>` shows the latest match (scrim, lobby, official) of a team with details about your performance

- `!logs teams` shows the available teams

- `!logs teams <teamname> players ` shows the players in the team

- `!logs addme <SteamID64>` adds your self to the bot with your steamid


##Team management commands

- `!logs teams create <teamname> <format>` Creates a new team. Format is the type of the team (6 = 6v6, 9 = Highlander, 4 = 4v4 and so on).

- `!logs teams delete <teamname>` Removes a team from the system.

- `!logs teams add <teamname> <@name> <name> <class>` Stores a player with a specific name into a team.

- `!logs teams remove <teamname> <@name>` Removes a player from a team.