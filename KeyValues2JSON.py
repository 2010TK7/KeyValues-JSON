__author__ = "TK7"
__version__ = "1.3"

def basichardplan(text):
    import re
    text = re.sub("\"\"\"", r'" ""', text)
    text = re.sub("\"\s+\"(\s+)\"", r'" "^\1"', text)
    text = re.sub("(?<=[\"\{\}])\s+(?=[\"\{\}])", "\r\n", text)
    text = re.sub("\"\^(\s+)\"", r'"\1"', text)
    return text

def preplan(text, index=1, hardplan=False):
    import re
    text = re.sub("(?<!\:)//.*", "", text)
    start = text.find('"')
    ender = max(text.rfind('"'), text.rfind('}'))+1
    text = text[start: ender]
    if type(hardplan) == type(lambda:0):
        text = hardplan(text)
    return [re.split("\r\n", text), text][index]

def convert(text, index=0):
    import sys
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
    charmode = False
    checker = False
    for i in range(len(text)):
        if i+index == len(text):
            break
        if not charmode:
            if text[i+index] == '"':
                string = []
                charmode = True
            elif text[i+index] == '{':
                if not checker:
                    print("ERROR: dict for no key.")
                    sys.exit()
                index = _assign(table, key, convert(text, i+index+1))-i
                checker = False
            elif text[i+index] == '}':
                if checker:
                    print("ERROR: last key no value.")
                    sys.exit()
                return [table, i+index]
        else:
            if text[i+index] == '"':
                j = 0
                while(text[i+index-j-1] == '\\'):
                    j += 1
                if j%2:
                    string.append('"')
                else:
                    if not checker:
                        key = ''.join(string)
                        checker = True
                    else:
                        _assign(table, key, ''.join(string))
                        checker = False
                    charmode = False
            else:
                string.append(text[i+index])
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
        json.dump(table, file, ensure_ascii=False)

def undojson(table, filename):
    text = backer(table)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

