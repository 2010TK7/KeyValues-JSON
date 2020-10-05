import json, sys, requests
__author__ = "TK7"
__version__ = "1.0"

def readfile(filename, code="utf-16-le"):
    with open(filename, "r", encoding=code) as f:
        return f.read()

def readurl(url, code="utf-8"):
    r = requests.get(url)
    r.encoding = code
    return r.text

def savefile(text, filename, code="utf-8"):
    with open(filename, "w", encoding=code) as f:
        return f.write(text)

def KeyValues2dict(text, index=0, marker=False):
    table = {}
    charmode = False
    checker = False
    for i in range(len(text)):
        if not charmode:
            if text[i+index] == '"':
                list = []
                charmode = True
            elif text[i+index] == '{':
                if not checker:
                    print("ERROR: no key.")
                    sys.exit()
                table[key], index = KeyValues2dict(text, i+index+1, True)
                checker = False
                index -= i
            elif text[i+index] == '}':
                if checker:
                    print("ERROR: last key no value.")
                    sys.exit()
                if marker:
                    return [table, i+index-1]
                else:
                    return table
        else:
            if text[i+index] == '"':
                if text[i+index-1] == '\\':
                    list.append('"')
                else:
                    if not checker:
                        key = ''.join(list)
                        checker = True
                    else:
                        table[key] = ''.join(list)
                        checker = False
                    charmode = False
            elif text[i+index] == '\n':
                list.extend(['\\','n'])
            else:
                list.append(text[i+index])

def dict2KeyValues(table):
    text = ""
    charmode = False
    checker = False
    for key, value in table.items():
        text = text + '"' + key + '"'
        if type(value) == dict:
            text = text + "\n{\n" + dict2KeyValues(value) + "}\n"
        elif type(value) == str:
            text = text + "\t\"" + value + "\"\n"
        else:
            print("ERROR: value only string and dict allowed.")
            sys.exit()
    return text

def dict2json(table, filename):
    with open(filename, "w", encoding="utf-8") as f:
        return json.dump(table, f, ensure_ascii=False)

def json2dict(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
