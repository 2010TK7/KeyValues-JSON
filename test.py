#%%
import KeyValues2JSON as KV
import requests
from bs4 import BeautifulSoup
filename = "tf_proto_obj_defs_tchinese"
#%%
text = KV.readurl("https://wiki.teamfortress.com" + BeautifulSoup(requests.get("https://wiki.teamfortress.com/wiki/File:" + filename + ".txt").content, "html5lib").find(class_="fullMedia").a["href"])
table = KV.KeyValues2dict(text)
KV.dict2json(table, filename + ".json")
#%%
table = KV.json2dict(filename + ".json")
text = KV.dict2KeyValues(table)
KV.savefile(text, filename + ".txt")
#%%
table = KV.KeyValues2dict(KV.readfile(filename + ".txt", "utf-8"))
table = KV.KeyValues2dict(text)
KV.dict2json(table, filename + "2.json")
