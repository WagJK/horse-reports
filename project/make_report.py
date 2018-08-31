import time
import math
import util
import calc


def make_table(race_no, bet_info, race_info, table_awards, table_main):
    table = []
    table.append([race_info["tag"]]) 
    # 1st win odds, queue odds, 1st hot performance
    table.append([util.str_to_float(table_awards[1][2]), util.str_to_float(table_awards[5][2])])
    # 2nd pos odds, 2nd hot performance
    table.append([util.str_to_float(table_awards[3][2]), ''])
    # 3rd pos odds
    table.append([util.str_to_float(table_awards[4][2])])
    # add hot performance now
    thead = table_main[0]
    for i, row in enumerate(table_main):
        if i == 0: continue
        hot = row[thead.index("熱門")]
        dist = row[thead.index("頭馬距離")]
        if hot == "1st Hot":
            if i == 1:
                table[1].append("H W + {}".format(dist))
            elif i <= 3:
                table[1].append("H Q - {}".format(dist))
            else:
                table[1].append("H {} - {}".format(i, dist))
        elif hot == "2nd Hot":
            if i == 1:
                table[2].append("h W + {}".format(dist))
            elif i <= 3:
                table[2].append("h Q - {}".format(dist))
            else:
                table[2].append("h {} - {}".format(i, dist))
    
    # add bet & win/loss info
    for bet in bet_info["bet"]:
        if bet["id"] == race_no:
            # WP
            wp_name = ""
            for i, row in enumerate(table_main):
                if i == 0: continue
                if util.is_int(row[thead.index("馬號")]) and bet["WP"] == int(row[thead.index("馬號")]):
                    wp_name = row[thead.index("馬名")][:-6]
                    dist = row[thead.index("頭馬距離")]
                    # WP: append info row
                    table.append([
                        "{}号 {}".format(bet["WP"], wp_name), ''
                        "W {} P {}".format(bet_info["qty"]["W"], bet_info["qty"]["P"])
                    ])
                    # WP: append result row
                    if i == 1:
                        table.append(['', '', "W + {}".format(dist)])
                    elif i <= 3:
                        table.append(['', '', "Q - {}".format(dist)])
                    else:
                        table.append(['', '', "{} - {}".format(i, dist)])
                    # WP: append win/loss row
                    table.append(['', '', "${}".format(calc.wp(
                        wp_no = bet["WP"],
                        qty = bet_info["qty"], 
                        table_awards = table_awards, 
                        table_main = table_main
                    ))])
            # Each Big
            for big in bet["Big"]:
                for i, row in enumerate(table_main):
                    if i == 0: continue
                    if util.is_int(row[thead.index("馬號")]) and big == int(row[thead.index("馬號")]):
                        big_name = row[thead.index("馬名")][:-6]
                        dist = row[thead.index("頭馬距離")]
                        # Big: append info row
                        table.append([
                            "{}号 {} + {}号 {}".format(bet["WP"], wp_name, big, big_name), ''
                            "Q {} PQ {}".format(bet_info["qty"]["Q"], bet_info["qty"]["PQ"])
                        ])
                        # Big: append result row
                        if i == 1:
                            table.append(['', '', "{}号 {} W + {}".format(big, big_name, dist)])
                        elif i <= 3:
                            table.append(['', '', "{}号 {} Q - {}".format(big, big_name, dist)])
                        else:
                            table.append(['', '', "{}号 {} {} - {}".format(big, big_name, i, dist)])
                        # Big: append win/loss row
                        table.append(['', '', "${}".format(calc.big(
                            wp_no = bet["WP"],
                            big_no = big,
                            qty = bet_info["qty"], 
                            table_awards = table_awards, 
                            table_main = table_main
                        ))])
    # TODO: output overall win/loss and bet results
    # ....
    return table


def combine_tables(tables):
    full_table = []
    for i, table in enumerate(tables):
        full_table.extend(table)
    return full_table