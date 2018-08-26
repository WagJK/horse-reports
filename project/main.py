from data import data_input_results
from data import data_input_racecard

link_results = "http://racing.hkjc.com/racing/Info/Meeting/Results/Chinese/Local"
link_racecard = "http://racing.hkjc.com/racing/Info/Meeting/RaceCard/Chinese/Local"

number_of_races = 11
race_date = "20180715"
race_place = "ST"


def main():
	# data_input_racecard('http://racing.hkjc.com/racing/Info/Meeting/RaceCard/Chinese/Local/20180715/ST/')
	for i in range(1, number_of_races + 1):
		link_i = link_results + "/" + race_date + "/" + race_place + "/"  + str(i)
		print(link_i)
		table_results, table_awards = data_input_results(link_i)


if __name__ == "__main__":
	main()