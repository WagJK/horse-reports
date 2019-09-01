import util
import calc
import time
import race_io
import make_main
import make_report
import shutil


link_results = "http://racing.hkjc.com/racing/Info/Meeting/Results/Chinese/Local"
link_racecard = "http://racing.hkjc.com/racing/Info/Meeting/RaceCard/Chinese/Local"
link_raceinfo = "http://racing.hkjc.com/racing/information/Chinese/Reports/RaceReportFull.aspx"


def main():
    print("* get bet info")
    bet_info = race_io.get_betinfo('bet.json')
    race_date, race_place, number_of_races = bet_info['date'], bet_info['place'], bet_info['races']

    print("* get race info from", link_raceinfo)
    # all_race_info = race_io.get_raceinfo(link_results)

    tables_main = []
    tables_report = []
    for i in range(1, number_of_races + 1):
        link_i_results = link_results + "/" + race_date + "/" + race_place + "/"  + str(i)
        link_i_racecard = link_racecard + "/" + race_date + "/" + race_place + "/"  + str(i)

        # input
        print("* get results from", link_i_results)
        race_info, table_results, table_awards = race_io.get_results(link_i_results)

        print("* get racecard from", link_i_racecard)
        table_racecard = race_io.get_racecard(link_i_racecard)

        # DEBUG: show input
        # print(race_info)
        # util.print_table(table_results)
        # util.print_table(table_awards)
        # util.print_table(table_racecard)

        # process
        print("* processing main table {}".format(i))
        table_main = make_main.make_table(
            race_no = i,
            race_info = race_info,
            bet_info = bet_info,
            table_results = table_results,
            table_awards = table_awards,
            table_racecard = table_racecard
        )

        print("* processing report {}".format(i))
        table_report, result_info = make_report.make_table(
            race_no = i,
            race_info = race_info,
            bet_info = bet_info,
            table_awards = table_awards,
            table_main = table_main
        )

        # DEBUG: show processing output
        # util.write_table(table_main, "table_main.csv")
        # util.write_table(table_report, "table_report.csv")
        # util.print_table(table_main)
        # util.print_table(table_report)

        # output tables
        print("* append table to the table list")
        tables_main.append(table_main)
        tables_report.append((table_report, result_info))

    print("* combine all tables")
    combined_main = make_main.combine_tables(tables_main)
    combined_report = make_report.combine_tables(tables_report, bet_info)

    # DEBUG: show combined tables
    # util.write_table(combined_main, "table_main.csv")
    # util.write_table(combined_report, "table_report.csv")

    print("* output main & report")
    y, m, d = util.convert_date(bet_info["date"])
    # backup files
    shutil.copyfile(
        "output/Data Base (2018-2019).csv",
        "backup/Data Base (2018-2019) pre-{}-{}.csv".format(m,d)
    ) # main table
    make_main.output(combined_main, "output/Data Base (2018-2019).csv")
    make_report.output(combined_report, "output/Horse Report {}-{}-{}.csv".format(y, m, d))


if __name__ == "__main__":
    main()
