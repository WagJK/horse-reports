from util import print_table
from util import write_list_to_csv
from input import get_betinfo
from input import get_results
from input import get_racecard
from input import get_raceinfo
from table_main import combine_tables

link_results = "http://racing.hkjc.com/racing/Info/Meeting/Results/Chinese/Local"
link_racecard = "http://racing.hkjc.com/racing/Info/Meeting/RaceCard/Chinese/Local"
link_raceinfo = "http://racing.hkjc.com/racing/information/Chinese/Reports/RaceReportFull.aspx"


def main():
    print("* get bet info")
    bet_info = get_betinfo('bet.json')
    race_date, race_place, number_of_races = bet_info['date'], bet_info['place'], bet_info['races']

    print("* get race info from", link_raceinfo)
    # get_raceinfo(link_raceinfo)

    for i in range(1, number_of_races + 1):
        link_i_results = link_results + "/" + race_date + "/" + race_place + "/"  + str(i)
        link_i_racecard = link_racecard + "/" + race_date + "/" + race_place + "/"  + str(i)

        print("* get results from", link_i_results)
        table_results, table_awards = get_results(link_i_results)
        
        print("* get racecard from", link_i_racecard)
        table_racecard = get_racecard(link_i_racecard)
        
        table_main = combine_tables(i, table_results, table_awards, table_racecard, bet_info)
        write_list_to_csv(table_main, "table.csv")

        # report
        # profit, loss = calc_profit(bef_info, table_awards)



if __name__ == "__main__":
    main()