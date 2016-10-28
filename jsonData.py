import json #import stock python methods
import caching #import python files I've made


def jsonData(data=""):
    jsonData = [] #establish jsonData list
    if data == "fpprojb":
        players = caching.cached_get_fpprojb() #call cached_get_fpb to either display cached data or run GQL query
        for p in players:
            playerData = {} #establish reusable playerData dictionary
            playerData["name"] = p.name #add name to dictionary
            playerData["team"] = p.team #add team to dictionary
            playerData["pos"] = p.pos #add pos to dictionary
            playerData["ab"] = p.ab #add ip to dictionary
            playerData["r"] = p.r #add r to dictionary
            playerData["hr"] = p.hr #add hr to dictionary
            playerData["rbi"] = p.rbi #add rbi to dictionary
            playerData["sb"] = p.sb #add sb to dictionary
            playerData["avg"] = p.avg #add avg to dictionary
            playerData["obp"] = p.obp #add obp to dictionary
            playerData["h"] = p.h #add h to dictionary
            playerData["double"] = p.double #add double to dictionary
            playerData["triple"] = p.triple #add triple to dictionary
            playerData["bb"] = p.bb #add bb to dictionary
            playerData["k"] = p.k #add k to dictionary
            playerData["slg"] = p.slg #add slg to dictionary
            playerData["ops"] = p.ops #add ops to dictionary
            playerData["sgp"] = p.sgp #add sgp to dictionary
            playerData["last_modified"] = p.last_modified.strftime('%m.%d.%Y') #add modified date to dictionary and format
            jsonData.append(playerData) #add dictionary to list
    elif data == "fpprojp":
        players = caching.cached_get_fpprojp() #call cached_get_fpb to either display cached data or run GQL query
        for p in players:
            playerData = {} #establish reusable playerData dictionary
            playerData["name"] = p.name #add name to dictionary
            playerData["team"] = p.team #add team to dictionary
            playerData["pos"] = p.pos #add pos to dictionary
            playerData["ip"] = p.ip #add ip to dictionary
            playerData["k"] = p.k #add k to dictionary
            playerData["w"] = p.w #add w to dictionary
            playerData["sv"] = p.sv #add sv to dictionary
            playerData["era"] = p.era #add era to dictionary
            playerData["whip"] = p.whip #add whip to dictionary
            playerData["er"] = p.er #add er to dictionary
            playerData["h"] = p.h #add h to dictionary
            playerData["bb"] = p.bb #add bb to dictionary
            playerData["hr"] = p.hr #add hr to dictionary
            playerData["g"] = p.g #add g to dictionary
            playerData["gs"] = p.gs #add gs to dictionary
            playerData["l"] = p.l #add l to dictionary
            playerData["cg"] = p.cg #add cg to dictionary
            playerData["sgp"] = p.sgp #add sgp to dictionary
            playerData["last_modified"] = p.last_modified.strftime('%m.%d.%Y') #add modified date to dictionary and format
            jsonData.append(playerData) #add dictionary to list

    return json.dumps(jsonData)
