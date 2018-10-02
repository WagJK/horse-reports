import time
import math
import util


def make_table(race_no, race_info, table_results, table_awards, table_racecard, bet_info):
    table = table_results
    # -----------------
    # combine race info
    # -----------------
    for i, row in enumerate(table):
        if i == 0:
            table[i].insert(0, "賽道")
            table[i].insert(0, "場地")
            table[i].insert(0, "分數範圍")
            table[i].insert(0, "長度")
            table[i].insert(0, "班次")
            table[i].insert(0, "場次")
            table[i].insert(0, "日期")
        else:
            tags = race_info["tag"].split(" - ")
            y, m, d = util.convert_date(bet_info["date"])
            table[i].insert(0, race_info["track"][5:])
            table[i].insert(0, race_info["cond"][7:])
            # 分數範圍 sometimes does not exist 
            if len(tags) > 2:
                table[i].insert(0, tags[2])
            else:
                table[i].insert(0, '')
            table[i].insert(0, tags[1])
            table[i].insert(0, tags[0])
            table[i].insert(0, race_no)
            table[i].insert(0, "{}/{}/{}".format(y, m, d))
    # ----------------
    # combine hot info
    # ----------------
    sort_arr = []
    for row in table:
        if util.is_float(row[-1]):
            sort_arr.append(float(row[-1]))
    list.sort(sort_arr)
    hot_flag = False
    for i, row in enumerate(table):
        if i == 0:
            table[i].append("熱門")
        else:
            if util.is_float(row[-1]):
                if math.isclose(float(row[-1]), sort_arr[0], rel_tol=1e-9) and not hot_flag: # 1st hot
                    table[i].append("1st Hot")
                    hot_flag = True
                elif math.isclose(float(row[-1]), sort_arr[1], rel_tol=1e-9): # 2nd hot
                    table[i].append("2nd Hot")
                else:
                    table[i].append("-")
            else:
                table[i].append("-")
    # ----------------
    # combine bet info
    # ----------------
    have_bet = False
    thead = table[0]
    for i, bet in enumerate(bet_info["bet"]):
        if bet["id"] == race_no:
            have_bet = True
            for j, row in enumerate(table):
                # append bet for this row
                horse_number = row[thead.index("馬號")]
                if j == 0:
                    table[j].append("投注")
                elif not util.is_int(horse_number):
                    table[j].append("-")
                elif int(horse_number) == bet["WP"]:
                    table[j].append("W P")
                    # see which WP according to number of Bigs
                    if len(bet["Big"]) > 1:
                        for k in range(len(bet["Big"])):
                            table[j][-1] += " Big{}(PQ)".format(k+1)
                    elif len(bet["Big"]) != 0:
                        table[j][-1] += " Big(PQ)"
                elif int(horse_number) in bet["Big"]:
                    # see which Big it is
                    if len(bet["Big"]) != 1:
                        for k in range(len(bet["Big"])):
                            if int(horse_number) == bet["Big"][k]:
                                table[j].append("Big{}(PQ)".format(k+1))
                    else:
                        table[j].append("Big(PQ)")
                else:
                    table[j].append("-")
    if not have_bet:
        for j, row in enumerate(table):
            if j == 0:
                table[j].append("投注")
            else:
                table[j].append("-")
    # ---------------------
    # combine racecard info
    # ---------------------
    thead = table[0]
    col_horse_no = thead.index("馬號")
    for i, row in enumerate(table):
        if i == 0:
            table[i].append("皇牌")
            table[i].append("配備")
        else:
            if row[1] != '' and util.is_int(row[col_horse_no]):
                horse_number = int(row[col_horse_no])
                table[i].append(table_racecard[horse_number][-6]) # 優先參賽次序
                table[i].append(table_racecard[horse_number][-5]) # 配備
            else:
                table[i].append('-')
                table[i].append('-')
    # -------------------
    # combine place & ddy
    # -------------------
    for i, row in enumerate(table):
        if i == 0:
            table[i].append("地點")
            table[i].append("度地儀")
        else:
            if bet_info["place"] == "ST":
                table[i].append("沙田")
            else:
                table[i].append("跑馬地")
            table[i].append(bet_info["ddy"])
    # ------------
    # combine odds
    # ------------
    for i, row in enumerate(table):
        if i == 0:
            table[i].append("P賠率")
            table[i].append("P賠率2")
            table[i].append("P賠率3")
            table[i].append("Queue賠率")
            table[i].append("PQ賠率")
            table[i].append("PQ賠率2")
            table[i].append("PQ賠率3")
        else:
            p_awards = table_awards[2][1]
            q_awards = table_awards[3][1]
            pq_awards = table_awards[4][1]
            # P1/2/3
            for j in range(len(p_awards)):
                if p_awards[j][0] == table[i][col_horse_no]:
                    table[i].append(util.str_to_float(p_awards[j][1]))
                else: table[i].append('')
            # Queue
            for j in range(len(q_awards)):
                horse_number = q_awards[j][0].split(',')
                if horse_number[0] == table[i][col_horse_no] or horse_number[1] == table[i][col_horse_no]:
                    table[i].append(util.str_to_float(q_awards[j][1]))
                else: table[i].append('')
            # Pos-Queue
            for j in range(len(pq_awards)):
                horse_number = pq_awards[j][0].split(',')
                if horse_number[0] == table[i][col_horse_no] or horse_number[1] == table[i][col_horse_no]:
                    table[i].append(util.str_to_float(pq_awards[j][1]))
                else: table[i].append('')
    return table


def combine_tables(tables):
    full_table = []
    for i, table in enumerate(tables):
        if i == 0:
            full_table.extend(table)
        else:
            full_table.extend(table[1:])
    return full_table


def output(table, filename):
    util.write_table_append(table[1:], filename)
