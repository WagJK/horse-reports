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

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def write_list_to_csv(myList, filePath):
    try:
        file=open(filePath,'w')
        for items in myList:
            for item in items:
                file.write(item)
                file.write(",")
            file.write("\n") 
    except Exception :
        print("数据写入失败，请检查文件路径及文件编码是否正确")
    finally:
        file.close();