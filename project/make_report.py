import time
import math
import util


def make_table(race_no, bet_info, race_info, table_results, table_awards, table_main):
	table = []
	table.append([race_info["tag"]]) 
	# 1st win odds, queue odds, 1st hot performance
	table.append([table_awards[1][2], table_awards[5][2]]) 
	# 2nd pos odds, 2nd hot performance
	table.append([table_awards[3][2], ''])
	# 3rd pos odds
	table.append([table_awards[4][2]])
	# add hot performance now
	for i, row in enumerate(table_main):
		if i == 0: continue
		hot = row[table_main[0].index("熱門")]
		dist = row[table_main[0].index("頭馬距離")]
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
	# TODO:add bet & win/loss info
	# ...
	return table

