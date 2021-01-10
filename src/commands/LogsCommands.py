from src.commands import Command, Placeholder, ActivatorType, CommandActivator
from src import tosteamid3, totime, get_logs, get_parsed_log_details, \
                get_closest_demo, PerformanceDisplay
import src.users as LDBU


class LogsStatsCommand(Command):
    activator = CommandActivator(ActivatorType.equals, '!logs')

    async def logic(self, message):
        # checks if author is registerd in the user file
        user = await LDBU.get_player(message.author.id)
        if user:
            # Then grab data of the player
            # Get the newest log of the player+
            demo_link = None
            data = await get_logs(user["steam_id"], 1)
            # Getting data of the log
            if len(data["logs"]) > 0:
                # Grabbing player performance
                logid = data["logs"][0]["id"]
                logiddetails = await get_parsed_log_details(
                    logid,
                    tosteamid3(user["steam_id"])
                )
                performance = PerformanceDisplay(0, logiddetails)

                demo = await get_closest_demo(
                    tosteamid3(user["steam_id"]),
                    data["logs"][0]["date"]
                )
                if demo is not None:
                    demo_link = f"\t\tdemo [<{demo}>]"

                return \
                    f":dart:\t{Placeholder.author_name}'s played the match:\n\t\t   {Placeholder.data('logtitle')}" \
                    f"\t`{Placeholder.data('logtime')}`\n\n" + Placeholder.data('performance') + \
                    f"log [<http://logs.tf/{logid}>]{Placeholder.data('demo_link')}\n\n", \
                    {
                        "demo_link": demo_link,
                        "logtime": totime(data["logs"][0]["date"]),
                        "logtitle": data["logs"][0]["title"],
                        "log_id": logid,
                        "performance": performance
                    }
            else:
                return \
                    ":warning:\tLooks like there a no logs.\n\t\t   Maybe this steamid does not exits, " \
                    "it can be changed by typing `!logs addme <steamid>`", None
        return \
            f":wave: Hey **{Placeholder.author_name}** seems like you are new.\n" \
            "With your Steam information I can offer you details such as your current logs.\n" \
            "You can create teams, fill them with players and get recent matches of the teams.\n" \
            "You can also search for other persons logs and logs.tf profile's.\n\n" \
            "In two steps you can use them:\n" \
            "\t\t\t1. Go to <https://steamid.xyz/> and find your *SteamID64*\n" \
            "\t\t\t2. write `!logs addme ` and then your SteamID64. Example:`!logs addme 76561198041007223`", \
            None


class LogsProfile(Command):
    activator = CommandActivator(ActivatorType.equals, '!logs profile')

    async def logic(self, message):
        # check if user is in userdata
        user = await LDBU.get_player(message.author.id)
        if user:
            # Getting newest 3 logs
            data = await get_logs(user["steam_id"], 3)

            last_3_logs = "\n\n:warning:\tLooks like there a no logs.\n\t\t"\
                "Maybe this steamid does not exits, it can be changed by typing "\
                "`!logs addme <steamid>`"
            # check if this is a real valid user
            if data["results"] != 0:
                # building message
                last_3_logs = "\n\n__Last 3 logs__\n"
                for log in data["logs"]:
                    last_3_logs += f"**{log['title']}**\t`{totime(log['date'])}`\n" \
                        f"<http://logs.tf/{log['id']}>\n\n"

            return \
                f":card_box:\t**{Placeholder.author_name}'s profile**\n\n" \
                f"*logs.tf*\t\t\t\t[<http://logs.tf/profile/{Placeholder.data('steam_id')}>]\n" \
                f"*demos.tf*\t\t   [<http://demos.tf/profiles/{Placeholder.data('steam_id')}>]\n" \
                f"*steam*\t\t\t\t[<http://steamcommunity.com/profiles/{Placeholder.data('steam_id')}>]\n" \
                f"*SteamID64*\t  `{user['steam_id']}`\n" \
                f"{Placeholder.data('last_3_logs')}", \
                {
                    "steam_id": user["steam_id"],
                    "last_3_logs": last_3_logs
                }

        return \
            f"Sorry {Placeholder.author_name} :confused:  "\
            "but i didn't find you in my data."
