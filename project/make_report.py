import time
import math
import util
import calc


def make_table(race_no, bet_info, race_info, table_awards, table_main):
    # retrieve awards for easy usage
    w_awards = table_awards[1][1]
    p_awards = table_awards[2][1]
    q_awards = table_awards[3][1]
    pq_awards = table_awards[4][1]
    # --------------------------------
    # add general info (first 3 lines)
    # --------------------------------
    table = []
    table.append([race_info["tag"]]) 
    # win odds, queue odds, !1st hot performance
    table.append([util.str_to_float(w_awards[0][1]), util.str_to_float(q_awards[0][1])])
    # pos odds, !2nd hot performance
    for i, pair in enumerate(p_awards):
        if i == 0: continue
        table.append([util.str_to_float(p_awards[i][1])])
    table[2].append("")
    # add hot performance
    H_W, H_Q, H_P, H_L = 0, 0, 0, 0
    h_W, h_Q, h_P, h_L = 0, 0, 0, 0
    L_W, L_Q, L_P, L_L = 0, 0, 0, 0
    thead = table_main[0]
    for i, row in enumerate(table_main):
        if i == 0: continue
        hot = row[thead.index("熱門")]
        dist = row[thead.index("頭馬距離")]
        if hot == "1st Hot":
            if i == 1:
                H_W += 1
                table[1].append("H W + {}".format(dist))
            elif i == 2:
                H_Q += 1
                table[1].append("H Q - {}".format(dist))
            elif i == 3:
                H_P += 1
                table[1].append("H P - {}".format(dist))
            else:
                H_L += 1
                table[1].append("H {} - {}".format(i, dist))
        elif hot == "2nd Hot":
            if i == 1:
                h_W += 1
                table[2].append("h W + {}".format(dist))
            elif i == 2:
                h_Q += 1
                table[2].append("h Q - {}".format(dist))
            elif i == 3:
                h_P += 1
                table[2].append("h P - {}".format(dist))
            else:
                h_L += 1
                table[2].append("h {} - {}".format(i, dist))
    # -----------------------
    # add bet & win/loss info
    # -----------------------
    # init cnt variables
    total_W, total_P, total_Q, total_PQ = 0, 0, 0, 0
    total_result, total_feedback = 0, 0
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
                        "{}号 {}".format(bet["WP"], wp_name), '',
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
                    result, feedback, W, P = calc.wp(
                        wp_no = bet["WP"],
                        qty = bet_info["qty"], 
                        table_awards = table_awards, 
                        table_main = table_main
                    )
                    table.append(['', '', "${}".format(result)])
                    total_W += W
                    total_P += P
                    total_result += result
                    total_feedback += feedback
            
            # Each Big
            for big in bet["Big"]:
                for i, row in enumerate(table_main):
                    if i == 0: continue
                    if util.is_int(row[thead.index("馬號")]) and big == int(row[thead.index("馬號")]):
                        big_name = row[thead.index("馬名")][:-6]
                        dist = row[thead.index("頭馬距離")]
                        # Big: append info row
                        table.append([
                            "{}号 {} + {}号 {}".format(bet["WP"], wp_name, big, big_name), '',
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
                        result, feedback, Q, PQ = calc.big(
                            wp_no = bet["WP"],
                            big_no = big,
                            qty = bet_info["qty"], 
                            table_awards = table_awards, 
                            table_main = table_main
                        )
                        table.append(['', '', "${}".format(result)])
                        total_Q += Q
                        total_PQ += PQ
                        total_result += result
                        total_feedback += feedback
    result_info = {
        'result': total_result, 
        'feedback': total_feedback, 
        'W-P-Q-PQ': [total_W, total_P, total_Q, total_PQ],
        'H': [H_W, H_Q, H_P, H_L],
        'h': [h_W, h_Q, h_P, h_L],
        'L': [L_W, L_Q, L_P, L_L],
    }
    return table, result_info


def combine_tables(tables, bet_info):
    full_table = []
    H_W, H_Q, H_P, H_L = 0, 0, 0, 0
    h_W, h_Q, h_P, h_L = 0, 0, 0, 0
    L_W, L_Q, L_P, L_L = 0, 0, 0, 0
    total_W, total_P, total_Q, total_PQ = 0, 0, 0, 0
    total_result, total_feedback = 0, 0
    # comine table and stats
    for i, pair in enumerate(tables):
        table, result = pair
        full_table.extend(table)
        
        total_W += result['W-P-Q-PQ'][0]
        total_P += result['W-P-Q-PQ'][1]
        total_Q += result['W-P-Q-PQ'][2]
        total_PQ += result['W-P-Q-PQ'][3]

        H_W += result['H'][0]
        H_Q += result['H'][1]
        H_P += result['H'][2]
        H_L += result['H'][3]

        h_W += result['h'][0]
        h_Q += result['h'][1]
        h_P += result['h'][2]
        h_L += result['h'][3]

        L_W += result['L'][0]
        L_Q += result['L'][1]
        L_P += result['L'][2]
        L_L += result['L'][3]

        total_result += result['result']
        total_feedback += result['feedback']
    
    total_L = len(bet_info["bet"]) - total_P

    # ---------------------------------------
    # output overall win/loss and bet results
    # ---------------------------------------
    def format_result_str(W, P, Q, PQ, L):
        str_result = ""
        if W > 0:       str_result += "-{}W".format(W)
        if P - W > 0:   str_result += "-{}P".format(P)
        if Q > 0:       str_result += "-{}Q".format(Q)
        if PQ - Q > 0:  str_result += "-{}PQ".format(PQ)
        if L > 0:       str_result += "-{}L".format(L)
        return str_result[1:]

    def format_hot_str(W, Q, P, L):
        str_hot = ""
        if W > 0: str_hot += "-{}W".format(W)
        if Q > 0: str_hot += "-{}Q".format(Q)
        if P > 0: str_hot += "-{}P".format(P)
        if L > 0: str_hot += "-{}L".format(L)
        return str_hot[1:]

    # format the overall win/loss string
    str_result = format_result_str(total_W, total_P, total_Q, total_PQ, total_L)
    full_table.append(["{} ${} (另有${}回馈)".format(str_result, total_result, total_feedback)])
    full_table.append(["H {}".format(format_hot_str(H_W, H_Q, H_P, H_L))])
    full_table.append(["h {}".format(format_hot_str(h_W, h_Q, h_P, h_L))])
    full_table.append(["L {}".format(format_hot_str(L_W, L_Q, L_P, L_L))])
    return full_table