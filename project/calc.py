import util


def wp(wp_no, qty, table_awards, table_main):
    result = -(qty["W"] + qty["P"])

    w_awards = table_awards[1][1]
    p_awards = table_awards[2][1]
    # win
    for i, pair in enumerate(w_awards): 
        if wp_no == int(pair[0]):
            result += util.str_to_float(pair[1]) * qty["W"] / 10
    # position
    for i, pair in enumerate(p_awards): 
        if wp_no == int(pair[0]):
            result += util.str_to_float(pair[1]) * qty["P"] / 10
    return result
    


def big(wp_no, big_no, qty, table_awards, table_main):
    result = -(qty["Q"] + qty["PQ"])
    bet = set([str(wp_no), str(big_no)])

    q_awards = table_awards[3][1]
    pq_awards = table_awards[4][1]
    # queue
    for i, pair in enumerate(q_awards):
        q = set(pair[0].split(','))
        if bet == q:
            result += util.str_to_float(pair[1]) * qty["Q"] / 10
    # position queue
    for i, pair in enumerate(pq_awards):
        pq = set(pair[0].split(','))
        if bet == pq:
            result += util.str_to_float(pair[1]) * qty["PQ"] / 10
    return result