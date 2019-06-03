from Storage import UserStats
from RecordKeeperUtils import get_discord_name
from pvp_iv.pvp_iv_util import find_combo, find_top_5, get_csv_header

import discord
import asyncio
import random
import datetime
import math
import time
import sys
import os


def create_elo10(usdb, medal, message):
    """
    Creates the 10 leaderboards for a given medal
    """
    list = usdb.get_elo_leaders(medal + "_elo")
    if len(list) > 0:
        msg = ("ELO Leaderboard for " + medal + "\n" + "```")
        msg += "   |Value      |Name\n"
        msg += "---+-----------+--------------\n"
        cnt = 0
        for el in list[0:10]:
            cnt += 1
            g, v = el
            v = str(round(v, 2))
            while len(v) < 10:
                v += " "
            while len(v) < 10:
                v += " "
            try:
                g = get_discord_name(message, g)
                assert g
            except:
                g = "bidoof"
            g = g.split("#")[0]
            g = g[0:15]
            c = str(cnt)
            while len(c) < 2:
                c += " "
            msg += c + " | " + str(v) + "| " + str(g) + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_leaderboard10(usdb, medal, message):
    """
    Creates the 10 leaderboards for a given medal
    """
    list = usdb.get_leaders(medal)
    if len(list) > 0:
        msg = ("Leaderboard for " + medal + "\n" + "```")
        # build header
        msg += "   |Value      |Name\n"
        msg += "---+-----------+--------------\n"
        cnt = 0
        for el in list[0:10]:
            cnt += 1
            u, d, g, v, n = el
            d = d.split(".")[0]
            d = d.split(" ")[0]
            d = d.split("T")[0]
            while len(d) < 10:
                d += " "
            v = str(v).split(".")[0]
            while len(v) < 10:
                v += " "
            try:
                g = get_discord_name(message, g)
                assert g
            except:
                g = "bidoof"
            g = g.split("#")[0]
            g = g[0:15]
            n = n[0:10]
            c = str(cnt)
            while len(c) < 2:
                c += " "
            msg += c + " | " + str(v) + "| " + str(g) + "\n"
            if n != "":
                msg += "---+-----------+> " + n + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_search_string(usdb, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_trade_board_by_user(str(gamertag))
    if len(list) > 0:
        msg = ""
        array = []
        search = ""
        current = -1
        streak = False
        for el in list:
            u, g, p, num, n = el
            if current + 1 == num:
                current = num
                streak = True
            else:
                if streak:
                    streak = False
                    search += "-" + str(array[len(array) - 1])
                if len(search) == 0:
                    search += str(num)
                else:
                    search += "," + str(num)
                current = num
            array.append(num)
        if streak:
            search += "-" + str(array[len(array) - 1])
        msg += search
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_search_string_table(usdb, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_trade_board_by_user(str(gamertag))
    if len(list) > 0:
        msg = "search string:\n"
        msg += "```"
        array = []
        search = ""
        current = -1
        streak = False
        for el in list:
            u, g, p, num, n = el
            if current + 1 == num:
                current = num
                streak = True
            else:
                if streak:
                    streak = False
                    search += "-" + str(array[len(array) - 1])
                if len(search) == 0:
                    search += str(num)
                else:
                    search += "," + str(num)
                current = num
            array.append(num)
        if streak:
            search += "-" + str(array[len(array) - 1])
        msg += search + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_pokemon_trade_table(usdb, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_trade_board_by_user(str(gamertag))
    if len(list) > 0:
        msg = "```"
        msg += "Pokemon      |#    |Note   \n"
        msg += "-------------+-----+-------------\n"
        for el in list:
            u, g, p, num, n = el
            p = p[0:12]
            while len(p) < 12:
                p += " "
            num = str(num)[0:10]
            while len(num) < 4:
                num += " "
            n = n[0:10]
            if len(n) == 0:
                continue
            while len(n) < 10:
                n += " "
            msg += str(p) + " | " + str(num) + "| " + str(n) + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_per_pokemon_trade_table(usdb, pokemon, message):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_trade_board_by_pokemon(str(pokemon))
    if len(list) > 0:
        msg = "```"
        msg += "Want         |Note   \n"
        msg += "-------------+-------------\n"
        for el in list:
            u, g, p, num, n = el
            n = n[0:10]
            while len(n) < 12:
                n += " "
            try:
                g = get_discord_name(message, g)
                assert g
            except:
                g = "bidoof"
            g = g.split("#")[0][0:12]
            while len(g) < 12:
                g += " "
            msg += str(g) + " | " + str(n) + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_recent_pvp10(usdb, message, medal, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_recent_pvp(medal, str(gamertag))

    if len(list) > 0:
        last_u, d, _, gw, _, _, gl, _, _, t, n = list[0]
        msg = "<@!" + str(gamertag) + "> 's last 10 entries for " + medal + "\n" + "```"
        msg += "Battle Log      \n"
        msg += "----------------------------------\n"
        for el in list[0:10]:
            u, d, _, gw, _, _, gl, _, _, t, n = el
            d = d.split(".")[0]
            d = d.split(" ")[0]
            d = d.split("T")[0]
            while len(d) < 10:
                d += " "
            n = n[0:8]
            while len(n) < 8:
                n += " "
            try:
                gw = get_discord_name(message, gw)
                assert gw
            except:
                gw = "bidoof"
            try:
                gl = get_discord_name(message, gl)
                assert gl
            except:
                gl = "bidoof"
            gw = gw.split("#")[0][0:10]
            gl = gl.split("#")[0][0:10]
            if int(t):
                msg += str(gw) + " tied " + str(gl) + "\n"
            else:
                msg += str(gw) + " beat " + str(gl) + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_recent5(usdb, medal, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_recent(medal, str(gamertag))
    if len(list) > 0:
        u, d, g, v, n = list[0]
        msg = "<@!" + str(gamertag) + ">'s last 5 entries for " + medal + "\n" + "```"
        # build header
        msg += "Date       |Value      |Note \n"
        msg += "-----------+-----------+-----------\n"
        for el in list[0:5]:
            u, d, g, v, n = el
            d = d.split(".")[0]
            d = d.split(" ")[0]
            d = d.split("T")[0]
            while len(d) < 10:
                d += " "
            v = str(v).split(".")[0]
            while len(v) < 10:
                v += " "
            n = n[0:10]
            msg += d + " | " + str(v) + "| " + str(n) + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_stats(usdb, medal, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    if medal in usdb.pvp_leagues:
        day7 = usdb.get_day_wl_avg(medal, str(gamertag), 7)
        day30 = usdb.get_day_wl_avg(medal, str(gamertag), 30)
        day90 = usdb.get_day_wl_avg(medal, str(gamertag), 90)
    else:
        day7 = usdb.get_day_avg(medal, str(gamertag), 7)
        day30 = usdb.get_day_avg(medal, str(gamertag), 30)
        day90 = usdb.get_day_avg(medal, str(gamertag), 90)

    if medal in usdb.pvp_leagues:
        msg = "win rate\n"
    else:
        msg = "averages per day\n"

    msg += "```"
    msg += "Past Week  |Past Month |Past 90 Days\n"
    msg += "-----------+-----------+------------\n"

    day7 = str(round(day7, 2))
    while len(day7) < 10:
        day7 += " "
    day30 = str(round(day30, 2))
    while len(day30) < 10:
        day30 += " "
    day90 = str(round(day90, 2))
    while len(day90) < 10:
        day90 += " "

    msg += str(day7) + " | " + str(day30) + "| " + str(day90) + "\n"
    msg += "```"
    return msg


def create_uuid_table(usdb, medal, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag with uuid
    """
    list = usdb.get_recent(medal, str(gamertag))

    if len(list) > 0:
        u, d, g, v, n = list[0]
        msg = "<@!" + str(gamertag) + ">'s last 5 entries for " + medal + "\n" + "```"
        msg += " uuid                                | value     \n"
        msg += "-------------------------------------+-----------\n"
        for el in list[0:5]:
            u, d, g, v, n = el
            v = str(v).split(".")[0]
            while len(v) < 10:
                v += " "
            n = n[0:10]
            msg += u + " | " + str(v) + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_uuid_table_pvp(usdb, message, medal, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag with uuid
    """
    list = usdb.get_recent(medal, str(gamertag))
    if len(list) > 0:
        u, d, _, gw, _, _, gl, _, _, _, n = list[0]
        msg = "<@!" + str(gamertag) + ">'s last 5 entries for " + medal + "\n" + "```"
        # build header
        msg += " uuid                                | results     \n"
        msg += "-------------------------------------+-----------\n"
        for el in list[0:5]:
            u, d, _, gw, _, _, gl, _, _, _, n = el

            while len(gl) < 10:
                gl += " "
            n = n[0:10]
            try:
                gw = get_discord_name(message, gw)
                assert gw
            except:
                gw = "bidoof"
            try:
                gl = get_discord_name(message, gl)
                assert gl
            except:
                gl = "bidoof"
            gw = gw.split("#")[0][0:10]
            gl = gl.split("#")[0][0:10]
            msg += u + " | w:" + str(gw) + ",l:" + str(gl) + "\n"
        msg += "```"
        return msg
    else:
        return "Bidoof, nothing to see here"


def create_friends_table(usdb, message, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_friends(str(gamertag))
    if len(list) > 0:
        msg = "<@!" + str(gamertag) + ">'s ultra friend list \n```"
        msg += "Status  | Friends\n"
        msg += "--------+--------------------- \n"
        for el in list[0:25]:
            _, g, _, status = el
            try:
                g = get_discord_name(message, g)
                assert g
            except:
                g = "bidoof"
            while len(status) < 7:
                status += " "
            msg += status + " | " + str(g) + "\n"
        msg += "```"
        return msg
    else:
        return "Your ultra friend's list is empty"


def create_ping_table(usdb, message, gamertag):
    """
    Creates a most recent 5 for a medal, gamertag
    """
    list = usdb.get_online_friends(gamertag)
    messages = []
    if len(list) > 0:
        msg = "<@!" + str(gamertag) + "> is looking to battle! \n"

        friends = False
        cnt = 0
        for idx in list:
            if cnt == 20 or len(msg) > 1500:
                messages.append(msg)
                msg = "<@!" + str(gamertag) + "> is looking to battle! \n"
                cnt = 0
            _, g, _, status = idx
            msg += "<@!" + str(g) + "> "
            friends = True
            cnt += 1

        messages.append(msg)

        if not friends:
            return "<@!" + str(gamertag) + "> you have no ultra friends online"
        return messages
    else:
        return "<@!" + str(gamertag) + "> you have no ultra friends online"


def create_rank_header(message):
    if len(message["args"]) == 5:
        folder = message["args"][4]
    elif len(message["args"]) == 2:
        folder = message["args"][1].lower()
    else:
        folder = "wild"
    return str(get_csv_header(message["args"][0], folder)) + " filtered by *" + folder + "* \n"


def create_rank_table(message):
    if len(message["args"]) == 5:
        folder = message["args"][4]
    else:
        folder = "wild"
    result, perfect = find_combo(message["args"][0], message["args"][1], message["args"][2], message["args"][3], folder)
    result = result.replace("\r\n", " ").split(",")
    perfect = perfect.replace("\r\n", " ").split(",")
    print(result)
    print(perfect)

    outstring = "```"
    outstring += "RANK:  " + result[0] + " (" + result[11] + ")\n"
    outstring += "CP:    " + result[5] + "\n"
    outstring += "LVL:   " + result[6] + "  (" + str(round(float(result[6]) - float(perfect[6]), 2)) + ") \n"
    outstring += "ATK:   " + result[7] + " (" + str(round(float(result[7]) - float(perfect[7]), 2)) + ") \n"
    outstring += "DEF:   " + result[8] + " (" + str(round(float(result[8]) - float(perfect[8]), 2)) + ") \n"
    outstring += "HP:    " + result[9] + " (" + str(round(float(result[9]) - float(perfect[9]), 2)) + ")```"

    return outstring


def create_rank_top10_table(message):
    if len(message["args"]) == 5:
        folder = message["args"][4]
    elif len(message["args"]) == 2:
        folder = message["args"][1].lower()
    else:
        folder = "wild"
    msg = "```"
    msg += " |ATK|DEF|HP |CP   |LVL  \n"
    msg += "-+---+---+---+-----+-----\n"
    for line in find_top_5(message["args"][0], folder):
        rank, ATK, DEF, HP, IV_P, CP, LVL, ref_ATK, ref_DEF, ref_HP, SP, P = line.split(",")
        while len(ATK) < 2:
            ATK = " " + ATK
        while len(DEF) < 2:
            DEF = " " + DEF
        while len(HP) < 2:
            HP = " " + HP
        while len(CP) < 4:
            CP += " "
        msg += rank + "|" + str(ATK) + " |" + str(DEF) + " |" + str(HP) + " |" + str(CP) + " |" + str(LVL) + "\n"
    msg += "```"
    return msg
