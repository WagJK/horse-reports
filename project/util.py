

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
            thetext = ''.join(thestrings)
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


def write_table(myList, filePath):
    try:
        file = open(filePath, 'w')
        for items in myList:
            for i, item in enumerate(items):
                file.write(str(item))
                if i != len(items) - 1:
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
                if i != len(items) - 1:
                    file.write("\t")
            file.write("\n") 
    except Exception :
        print("write failed，please check the file location and encoding")
    finally:
        file.close();