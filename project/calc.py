import util


def wp(wp_no, qty, table_awards, table_main):
    result, feedback = -(qty["W"] + qty["P"]), 0

    w_awards = table_awards[1][1]
    p_awards = table_awards[2][1]
    w_flag, p_flag = False, False
    # win
    for i, pair in enumerate(w_awards): 
        if wp_no == int(pair[0]):
            w_flag = True
            result += util.str_to_float(pair[1]) * qty["W"] / 10
    # position
    for i, pair in enumerate(p_awards): 
        if wp_no == int(pair[0]):
            p_flag = True
            result += util.str_to_float(pair[1]) * qty["P"] / 10
    if not w_flag and not p_flag:
        feedback += qty["W"] / 10 + qty["P"] / 10
    return result, feedback, int(w_flag), int(p_flag)
    


def big(wp_no, big_no, qty, table_awards, table_main):
    result, feedback = -(qty["Q"] + qty["PQ"]), 0
    bet = set([str(wp_no), str(big_no)])

    q_awards = table_awards[3][1]
    pq_awards = table_awards[4][1]
    q_flag, pq_flag = False, False
    # queue
    for i, pair in enumerate(q_awards):
        q = set(pair[0].split(','))
        if bet == q:
            q_flag = True
            result += util.str_to_float(pair[1]) * qty["Q"] / 10
    # position queue
    for i, pair in enumerate(pq_awards):
        pq = set(pair[0].split(','))
        if bet == pq:
            pq_flag = True
            result += util.str_to_float(pair[1]) * qty["PQ"] / 10
    if not q_flag and not pq_flag:
        feedback += qty["Q"] / 10 + qty["PQ"] / 10
    return result, feedback, int(q_flag), int(pq_flag)