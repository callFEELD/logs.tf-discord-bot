# This Class containing important functions that will be used in other Classes
# last edit: 20.02.2019 (callFEELD)

# third party imports
from datetime import datetime
from collections import Counter
import logging
import aiohttp

import src.users as LDBU


def tosteamid3(steamID64: str) -> str:
    """
    Converts steam ID 64 into a steam ID 3
    :returns: Steam ID 3
    """
    if len(steamID64) == 17:
        id32 = int(steamID64[3:]) - 61197960265728
        return "[U:1:" + str(id32) + "]"


def totime(timestamp: int) -> str:
    """
    Converts a UNIX timestamp to a human readable time string
    """
    return datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S %z')


async def get_logs(steamid64, limit=1, map_name=None) -> dict:
    """
    Fetches the logs.tf api, to search for the logs of the steamid64
    :returns: JSON details of the log
    """
    if isinstance(steamid64, list):
        steamid64 = ",".join(steamid64)

    url = f"https://logs.tf/api/v1/log?player={steamid64}&limit={limit}"
    if map_name is not None:
        url += f"&map={map_name}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_log_details(logid: int) -> dict:
    url = f"http://logs.tf/api/v1/log/{logid}"
    # going on the Logs.tf APi and search for the logid
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


# Returns a Player Demos.tf search, by inputting steamid64
async def get_demos(steamid64: int) -> dict:
    url = f"https://api.demos.tf/profiles/{steamid64}"
    # going on the Logs.tf API and search for the player with a limit
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_closest_demo(steam_id64: int, logs_unix_timestamp: int) -> str:
    demos = await get_demos(steam_id64)
    diffs = []
    ids = []
    for demo in demos:
        diff = float(demo["time"]) - float(logs_unix_timestamp)
        if 0 < diff <= 60:
            diffs.append(diff)
            ids.append(demo["id"])

    if len(diffs) > 0:
        min_diff = min(diffs)
        index = diffs.index(min_diff)
        return f"https://demos.tf/{ids[index]}"


# Returns String with performance details
def PerformanceDisplay(yourorplayer, data: dict):
    # Only shows performance details if player is in the log
    if data["playerinlog"]:
        # show played classes (sorted after playtime)
        played_classes_msg = ""
        classes_amount = len(list(data["classes"].keys()))
        k = 0
        if classes_amount != 1:
            for played_class in data["classes"].keys():
                k += 1
                if k >= classes_amount:
                    played_classes_msg += str(played_class)
                else:
                    played_classes_msg += f"{played_class}, "
        else:
            played_classes_msg = list(data["classes"].keys())[0]

        returnvar = f"*map*\t\t\t\t{data['map']}\n*class(es)*\t   {played_classes_msg}\n" \
                    f"```kills: {data['kills']},   assists: {data['assists']},   deaths: {data['deaths']}\n\n" \
                    f"k/d: {data['kd']},   ka/d: {data['kapd']}\n\n" \
                    f"dpm: {data['dpm']},   dmg: {data['dmg']}\n\n" \
                    f"heals: {data['heal_perc']}%,   as: {data['as']}```"

        if data["medic"] is not None:
            med = data["medic"]
            returnvar += f"```ubers: {med['ubers']}\tdrops: {med['drops']}\n\n" \
                         f"heals/min: {med['hpm']}\n\n{med['uber_types']}```"
    return returnvar


async def get_parsed_log_details(logid, steamid3):
    data = await get_log_details(logid)

    # when player is in the log output his performance
    if steamid3 in data["players"]:
        # get the classes the player played and sort them after playtime
        classes_data = {}
        played_medic = False
        for class_stat in data["players"][steamid3]["class_stats"]:
            if str(class_stat["type"]).lower() == "medic":
                played_medic = True

            # key -> class name, value -> playtime
            classes_data[class_stat["type"]] = class_stat["total_time"]

        # sort the classes after playtime
        sorted(classes_data.keys())

        medic = None
        # med stats if he is medic
        if played_medic:
            ubers = str(data["players"][steamid3]["ubers"])
            drops = str(data["players"][steamid3]["drops"])
            uber_types = ""
            k = 0
            for _ in data["players"][steamid3]["ubertypes"]:
                uber_types = uber_types + list(data["players"][steamid3]["ubertypes"].keys())[k] + ": " + str(list(data["players"][steamid3]["ubertypes"].values())[k]) + "\t"
                k += 1

            hpm = round(float(data["players"][steamid3]["heal"]) / (float(data["info"]["total_length"])/60), 2)
            medic = {
                "hpm": hpm,
                "ubers": ubers,
                "drops": drops,
                "uber_types": uber_types
            }

        # get heals percentage
        sum_of_heals = 0
        for player in data["players"]:
            # only increase the sum of heals, when the current player is on
            # the same teams as the passed steamid
            if data["players"][player]["team"] == data["players"][steamid3]["team"]:
                sum_of_heals += data["players"][player]["hr"]

        return {
            "kills": data["players"][steamid3]["kills"],
            "deaths": data["players"][steamid3]["deaths"],
            "assists": data["players"][steamid3]["assists"],
            "kd": data["players"][steamid3]["kpd"],
            "kapd": data["players"][steamid3]["kapd"],
            "dpm": data["players"][steamid3]["dapm"],
            "dt": data["players"][steamid3]["dt"],
            "hr": data["players"][steamid3]["hr"],
            "dmg": data["players"][steamid3]["dmg"],
            "as": data["players"][steamid3]["as"],
            "heal_perc": round(
                int(data["players"][steamid3]["hr"]/sum_of_heals) * 100, 2
            ) if sum_of_heals > 0 else 0,
            "classes": classes_data,
            "medic": medic,
            "map": data["info"]["map"],
            "playerinlog": True
        }
    else:
        return {
            "playerinlog": False
        }


# find the newsest team match
async def findMatch(message, team):
    # minplayers: minimal amount of players to be a match
    # numoflogs: amount of logs that should be checked for each player
    # fomrat: either 6 or 9 to represent 6s or HL

    # Steam ID64 and Steam ID3 of the author
    user = await LDBU.get_player(message.author.id)
    steamid3 = tosteamid3(user["steam_id"])

    # Go trough all Players of the Team
    steamids = []
    for player in team["players"]:
        steamids.append(player["steam_id"])

    logs = await get_logs(steamids)

    if len(logs["logs"]) > 0:
        logdetails = await get_parsed_log_details(logs["logs"][0]["id"], steamid3)
        performance = PerformanceDisplay(0, logdetails)

        return f":trophy: match found\n**{logs['logs'][0]['title']}**\n" \
               f"{totime(logs['logs'][0]['date'])}\n\n" \
               f"<http://logs.tf/{logs['logs'][0]['id']}>\n\n{performance}"
