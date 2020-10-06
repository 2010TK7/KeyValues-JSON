KVT = {}

KVT.info = {
    author = "TK7",
    version = "1.0",
    contact = {"https://steamcommunity.com/id/2010TK7/"}
}

--[[function KVT.readfile(filename)
    file = io.open(filename, "r")
    text = file:read("*all")
    file:close()
    return text
end]]

--[[function KVT.savefile(text, filename)
    file = io.open(filename, "w")
    file:write(text)
    return file:close()
end]]

function KVT.readurl(url)
    file = io.popen("curl -k " .. url)
    text = file:read("*all")
    file:close()
    return text
end

function KVT.KeyValues2table(text, index)
    index = index or 0
    local dict = {}
    local charmode, checker, key, marker
    for i=1, #text do
        local char = string.sub(text, i+index, i+index)
        if not charmode then
            if char == '"' then
                marker = i+index+1
                charmode = true
            elseif char == '{' then
                if not checker then
                    print("ERROR: no key.")
                    os.exit()
                end
                dict[key], index = KVT.KeyValues2table(text, i+index)
                checker = false
                index = index-i
            elseif char == '}' then
                if checker then
                    print("ERROR: last key no value.")
                    os.exit()
                end
                return dict, i+index
            end
        else
            if char == '"' and string.sub(text, i+index-1, i+index-1) ~= '\\' then
                if not checker then
                    key = string.sub(text, marker, i+index-1)
                    checker = true
                else
                    dict[key] = string.sub(text, marker, i+index-1)
                    checker = false
                end
                charmode = false
            end
        end
    end
    return dict, index
end

--[[function KVT.table2KeyValues(dict)
    local text = ""
    for k, v in pairs(dict) do
        text = text .. '"' .. k .. '"'
        if type(v) == "table" then
            text = text .. "\n{\n" .. KVT.table2KeyValues(v) .. "}\n"
        elseif type(v) == "string" then
            text = text .. "\t\"" .. v .. "\"\n"
        else
            print("ERROR: value only string and dict allowed.")
            os.exit()
        end
    end
    return text
end]]

function KVT.wikifileurl(homepage, filename, File)
    File = File or "File"
    local checker = string.sub(filename, 1, 1)
    local Filename, marker
    if string.find(checker, "%u") then
        Filename = filename
        filename = string.lower(checker) .. string.sub(filename, 2)
    else
        Filename = string.upper(checker) .. string.sub(filename, 2)
    end
    text = KVT.readurl(homepage .. "wiki/" .. File .. ':' .. Filename)
    marker = string.find(text, "fullMedia")
    _, start = string.find(text, "<a href=\"/", marker)
    _, ender = string.find(text, Filename, marker)
    return homepage .. string.sub(text, start+1, ender)
end

function KVT.updatetable(dict)
    for k, v in pairs(dict) do
        KVT.dictable[k] = v
    end
end

KVT.dictable = KVT.dictable or {}

KVT.lang = {
    en = "english",
    cs = "czech",
    da = "danish",
    de = "german",
    es = "spanish",
    fi = "finnish",
    fr = "french",
    hu = "hungarian",
    it = "italian",
    ja = "japanese",
    ko = "korean",
    no = "norwegian",
    nl = "dutch",
    pl = "polish",
    pt = "portuguese",
    ru = "russian",
    sv = "swedish",
    tr = "turkish"
}

function KVT.preset(name, language)
    KVT.lang["pt-br"] = "brazilian"
    KVT.lang["zh-hans"] = "schinese"
    KVT.lang["zh-hant"] = "tchinese"
    homepage = "https://wiki.teamfortress.com/"
    language = string.sub(language, 2) or "en"
    enfilename = name .. KVT.lang.en .. ".txt"
    KVT.updatetable(KVT.KeyValues2table(KVT.readurl(KVT.wikifileurl(homepage, enfilename))).lang.Tokens)
    if language ~= "en" then
        filename = name .. KVT.lang[language] .. ".txt"
        KVT.updatetable(KVT.KeyValues2table(KVT.readurl(KVT.wikifileurl(homepage, filename))).lang.Tokens)
    end
end

function KVT.getvalue(key)
    return KVT.dictable[key]
end

return KVT
