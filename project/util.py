

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
            thestrings = [str(s).strip('\r\n ').replace('\xa0', ' ') for s in col.findAll(text=True)]
            thestrings = list(filter(lambda x: x != '', thestrings))
            if not all(list(map(lambda x: x.isdigit(), thestrings))):
                thetext = ''.join(thestrings)
            else:
                if len(thestrings) > 0:
                    thetext = thestrings[0]
                    for s in thestrings[1:]:
                        thetext = thetext + " " + s
                else:
                    thetext = ""
            result[-1].append(thetext)
    return result


def is_even(value):
    return value % 2 == 0


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def str_to_float(value):
    return float(value.replace(',', ''))


def convert_date(s):
    y, m, d = s[:4], s[4:6], s[6:]
    if m[0] == '0': m = m[1:]
    if d[0] == '0': d = d[1:]
    return y, m, d


def write_table(myList, filePath):
    try:
        file = open(filePath, 'w')
        for items in myList:
            for i, item in enumerate(items):
                file.write(str(item))
                if not i == len(items) - 1:
                    file.write("\t")
            file.write("\n")
    except Exception :
        print("write failed，please check the file location and encoding")
    finally:
        file.close();


def write_table_append(myList, filePath):
    try:
        file = open(filePath, 'a')
        for items in myList:
            for i, item in enumerate(items):
                file.write(str(item))
                if not i == len(items) - 1:
                    file.write("\t")
            file.write("\n")
    except Exception :
        print("write failed，please check the file location and encoding")
    finally:
        file.close();
