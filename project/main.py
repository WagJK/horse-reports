import util
import calc
import race_io
import make_main
import make_jktn
import make_report
import bet_results


link_results = "http://racing.hkjc.com/racing/Info/Meeting/Results/Chinese/Local"
link_racecard = "http://racing.hkjc.com/racing/Info/Meeting/RaceCard/Chinese/Local"
link_raceinfo = "http://racing.hkjc.com/racing/information/Chinese/Reports/RaceReportFull.aspx"


def main():
    print("* get bet info")
    bet_info = race_io.get_betinfo('bet.json')
    race_date, race_place, number_of_races = bet_info['date'], bet_info['place'], bet_info['races']

    print("* get race info from", link_raceinfo)
    # raceinfo currently encounter browser problems.
    # all_race_info = race_io.get_raceinfo(link_results)

    bet_results = []
    for i in range(1, number_of_races + 1):
        link_i_results = link_results + "/" + race_date + "/" + race_place + "/"  + str(i)
        link_i_racecard = link_racecard + "/" + race_date + "/" + race_place + "/"  + str(i)

        print("* get results from", link_i_results)
        race_info, table_results, table_awards = race_io.get_results(link_i_results)
        
        print("* get racecard from", link_i_racecard)
        table_racecard = race_io.get_racecard(link_i_racecard)

        # DEBUG: show input
        print(race_info)
        # util.print_table(table_results)
        # util.print_table(table_awards)
        # util.print_table(table_racecard)
        
        print("* processing main table {}".format(i))
        table_main = make_main.make_table(i, table_results, table_awards, table_racecard, bet_info)
        util.write_list_to_csv(table_main, "table.csv")
        # race_io.write_table_main(table_main)

        print("* processing report {}".format(i))
        table_report = make_report.make_table(i, bet_info, race_info, table_results, table_awards, table_main)

        # DEBUG: show output
        # util.print_table(table_main)
        util.print_table(table_report)
        
    
    # TODO: make reports
    print("* output report")
    # race_io.write_report()

    # TODO: make jockey & trainer filter
    # make_jktn.filter_jockeyntrainer()


if __name__ == "__main__":
    main()