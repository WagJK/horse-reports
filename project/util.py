def print_table(table):
    print()
    for row in table: print(row)


def make_list(table):
    result = []
    allrows = table.findAll('tr')
    for row in allrows:
        result.append([])
        allcols = row.findAll('td')
        for col in allcols:
            thestrings = [str(s).strip('\r\n ').replace('\xa0', '') for s in col.findAll(text=True)]
            thetext = ''.join(thestrings)
            result[-1].append(thetext)
    return result
