from data import data_input_results
from data import data_input_racecard
from data import combine_tables
from util import *

link_results = "http://racing.hkjc.com/racing/Info/Meeting/Results/Chinese/Local"
link_racecard = "http://racing.hkjc.com/racing/Info/Meeting/RaceCard/Chinese/Local"

number_of_races = 11
race_date = "20180715"
race_place = "ST"


def main():
	
	for i in range(1, number_of_races + 1):
		link_i_results = link_results + "/" + race_date + "/" + race_place + "/"  + str(i)
		link_i_racecard = link_racecard + "/" + race_date + "/" + race_place + "/"  + str(i)

		print(link_i_results)
		table_results, table_awards = data_input_results(link_i_results)
		
		print(link_i_racecard)
		table_racecard = data_input_racecard(link_i_racecard)
		
		table_main = combine_tables(table_results, table_awards, table_racecard)
		write_list_to_csv(table_main, "table.csv")

if __name__ == "__main__":
	main()