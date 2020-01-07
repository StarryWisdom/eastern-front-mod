#!/usr/bin/python
import xml.etree.ElementTree
import sys

def warning(msg) :
    global areChecksOK
    areChecksOK = False
    print "warning: " + msg

def error(msg) :
    print "error: " + msg
    sys.exit(1)

def readVesselData(filename) :
    global hullRaces
    root= xml.etree.ElementTree.parse(filename).getroot()
    for tag in root.findall('hullRace') :
        tmp = {
                'name'  : tag.attrib['name'],
                'id'    : tag.attrib['ID'] ,
                'keys'  : tag.attrib['keys'] ,
                'bases' : 0
                }
        id=int(tmp['id'])
        if (len(hullRaces)!=id) :
            error("next element of vessel data hullRace is not the next integer - this may be invalid artemis")
        hullRaces+=[{}]
        hullRaces[id]= tmp
    for tag in root.findall('vessel') :
        if 'base' in tag.attrib['broadType'] :
        #TODO does artemis check for the string "base" or just a substring?
            hullRaces[int(tag.attrib['side'])]['bases']+=1
    for race in hullRaces :
        if 'enemy' in race['keys'] :
            if race['bases'] == 0 :
                if not 'biomech' in race['keys'] :#TODO Errr really - maybe? test
                    warning('There is an enemy race "' + race['name'] +'" which has no bases, this means that the stock siege and deep strike missions will spawn ID 0 ships as a base (and look wrong due to that)')

hullRaces =[]
areChecksOK = True

optNoWarn = False

argn = 1
while (len(sys.argv)>argn) :
    if sys.argv[argn] == "--no-warn" :
        optNoWarn = True
    argn = argn + 1

readVesselData("dat/vesselData.xml")
if not areChecksOK and not optNoWarn:
    sys.exit(1)

#TODO check all files are used
#TODO check ordiance types
#TODO check invalid tags or elements (like torp type, carrier loads)
#TODO check files refered from vesselData are correct
#TODO check the faction name thing that was present in TSN 2.0 or so
#TODO investgate what is required for the vessel data to be vaild (biomechs? friendlies?)
#TODO check about PC ships having ID's that non seqentual
#TODO check carrierload without carrier tag (also investigate what artemis does)
#TODO info for missing nodes?
#TODO nodes co-planar with hulls (wishlist - this would be hard)
#TODO check mission scripting
