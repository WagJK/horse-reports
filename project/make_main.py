import time
import math
import util


def make_table(race_no, table_results, table_awards, table_racecard, bet_info):
    table = table_results
    # combine race info
    for i, row in enumerate(table):
        if i == 0:
            table[i].insert(0, "場次")
        else:
            table[i].insert(0, race_no)

    # combine hot info
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

    
    # combine bet info
    have_bet = False
    for i, bet in enumerate(bet_info["bet"]):
        if bet["id"] == race_no:
            have_bet = True
            for j, row in enumerate(table):
                # append bet for this row
                if j == 0:
                    table[j].append("投注")
                elif row[1] == bet["WP"]:
                    table[j].append("W P")
                    # see which WP according to number of Bigs
                    if len(bet["Big"]) > 1:
                        for k in range(len(bet["Big"])):
                            table[j][-1] += " Big{}(PQ)".format(k+1)
                    elif len(bet["Big"]) != 0:
                        table[j][-1] += " Big(PQ)"
                elif row[1] in bet["Big"]:
                    # see which Big it is
                    if len(bet["Big"]) != 1:
                        for k in range(len(bet["Big"])):
                            if bet["Big"][k] == row[1]:
                                table[j].append("Big{}(PQ)".format(k+1))
                    else:
                        table[j].append("Big(PQ)")
                else:
                    table[j].append("")
    if not have_bet:
        for j, row in enumerate(table):
            if j == 0:
                table[j].append("投注")
            else:
                table[j].append("")

    # combine racecard info
    for i, row in enumerate(table):
        if i == 0:
            table[i].append("優先參賽次序")
            table[i].append("配備")
        else:
            if row[1] != '' and util.is_int(row[1]):
                horse_number = int(row[1])
                table[i].append(table_racecard[horse_number][-6]) # 優先參賽次序
                table[i].append(table_racecard[horse_number][-5]) # 配備
            else:
                table[i].append('-')
                table[i].append('-')

    # combine odds
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
            # P1/2/3
            for j in range(2, 5):
                if table_awards[j][1] == table[i][1]:
                    table[i].append(table_awards[j][2])
                else: table[i].append('')
            # Queue & PQ1/2/3
            for j in range(5, 9):
                horse_number = table_awards[j][1].split(',')
                if horse_number[0] == table[i][1] or horse_number[1] == table[i][1]:
                    table[i].append(table_awards[j][2])
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