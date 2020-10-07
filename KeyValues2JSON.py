import re, sys
__author__ = "TK7"
__version__ = "1.1"

def preplan(text, index=0, hardplan=False):
    text = re.sub("//.*", "", text)
    start = text.find('"')
    ender = max(text.rfind('"'), text.rfind('}'))+1
    text = text[start: ender]
    if type(hardplan) == type(lambda:0):
        text = hardplan(text)
    return [re.split("(?<=[\"\{\}])\s+(?=[\"\{\}])", text), text][index]

def convert(array, index=0):
    def _assign(table, key, value):
        checker = False
        if type(value) == list:
            value, index = value
            checker = True
        try:
            if type(table[key]) != list:
                table[key] = [table[key], value]
            else:
                table[key].append(value)
        except:
            table[key] = value
        if checker:
            return index
    table = {}
    checker = False
    for i in range(len(array)):
        if i+index >= len(array):
            break
        if array[i+index] == '{':
            if not checker:
                print("ERROR: dict for no key.")
                sys.exit()
            index = _assign(table, key, convert(array, i+index+1))-i
            checker = False
        elif array[i+index] == '}':
            if checker:
                print("ERROR: last key no value.")
                sys.exit()
            return [table, i+index]
        elif array[i+index] == '"' and array[i+index+1] == '"':
            if checker:
                _assign(table, key, "")
                checker = False
            else:
                key = ""
                checker = True
            index += 1
        else:
            if checker:
                _assign(table, key, array[i+index][1: -1])
                checker = False
            else:
                key = array[i+index][1: -1]
                checker = True
    if checker:
        print("ERROR: last key no value.")
        sys.exit()
    return table

def backer(table, index=0):
    def _addtab(index):
        text = ""
        for i in range(index):
            text += '\t'
        return text
    text = ""
    for key, value in table.items():
        if type(value) == dict:
            text = text + _addtab(index) + '"' + key + "\"\n"
            text = text + _addtab(index) + "{\n"
            text = text + backer(value, index+1)
            text = text + _addtab(index) + "}\n"
        elif type(value) == list:
            for v in value:
                text = text + _addtab(index) + '"' + key + "\"\t\"" + v + "\"\n"
        else:
            text = text + _addtab(index) + '"' + key + "\"\t\"" + value + "\"\n"
    return text

def savejson(text, filename):
    import json
    table = convert(preplan(text))
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(table, file)

def undojson(table, filename):
    text = backer(table)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
