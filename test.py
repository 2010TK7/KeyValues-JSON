#%%
import json, requests
import KeyValues2JSON as KV
from bs4 import BeautifulSoup
#%%
filename = "tf_proto_obj_defs_tchinese.txt"
text = requests.get("https://wiki.teamfortress.com" + BeautifulSoup(requests.get("https://wiki.teamfortress.com/wiki/File:" + filename).content, "html5lib").find(class_="fullMedia").a["href"])
text.encoding = "utf-8"
text = text.text
KV.savejson(text, "tf_proto_obj_defs_tchinese.json")
#%%
filename = "gamemodes.txt"
with open(filename, "r", encoding="utf-8") as file:
    text = file.read()
KV.savejson(text, "gamemodes.json")
#%%
filename = "tf_proto_obj_defs_tchinese.txt"
with open("tf_proto_obj_defs_tchinese.json", "r", encoding="utf-8") as file:
    table = json.load(file)
KV.undojson(table, filename)
#%%
