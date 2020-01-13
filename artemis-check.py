#!/usr/bin/python
import xml.etree.ElementTree
import sys
import os

def warning(msg) :
    global areChecksOK
    areChecksOK = False
    print "warning: " + msg

def error(msg) :
    print "error: " + msg
    sys.exit(1)

def is_file_in_stock(filename) :
    files=["dat/TSNMediumCarrier.snt",
    "dat/ximni-battleship.snt",
    "dat/PirateBrigantine.snt",
    "dat/PirateLongbow.snt",
    "dat/artemis-scout.snt",
    "dat/ximni-light-cruiser.snt",
    "dat/ximni-missile.snt",
    "dat/artemis-4.snt",
    "dat/TSNMineLayer.snt",
    "dat/PirateStrongbow.snt",
    "dat/artemis.snt",
    "dat/ximni-carrier.snt",
    "dat/ximni-scout.snt",
    "dat/artemis-3.snt",
    "dat/ximni-dread.snt",
    "dat/TSNSuperDread.snt",
    "dat/artemis-5.snt"]
    for file in files :
        if filename==file :
            return True
    return False

def warn_if_no_file(filename) :
    if not os.path.exists(filename) :
        if not is_file_in_stock(filename) :
            warning("unable to find the file " + filename)

def readVesselData(filename) :
    global hullRaces
    global vessels
    root= xml.etree.ElementTree.parse(filename).getroot()
    for tag in root.findall('hullRace') :
        tmp = {
                'name'  : tag.attrib['name'],
                'id'    : tag.attrib['ID'] ,
                'keys'  : tag.attrib['keys'] ,
                'bases' : 0 #number of bases on this hull race
                }
        id=int(tmp['id'])
        if (len(hullRaces)!=id) :
            error("next element of vessel data hullRace is not the next integer - this may be invalid artemis")
        hullRaces+=[{}]
        hullRaces[id]= tmp
    for tag in root.findall('vessel') :
        tmp = {
                'id'        : tag.attrib['uniqueID'],
                'side'      : tag.attrib['side'],
                'classname' : tag.attrib['classname'],
                'broadType' : tag.attrib['broadType']
                #mesh type, diffuse file, glow file, specular file, scale, push raduis
                }
        internal_data=tag.findall('internal_data')
        if len(internal_data) == 1 :
            snt_node=internal_data[0].attrib['file'];
            tmp['snt_node']=snt_node
            warn_if_no_file(snt_node)
        elif len(internal_data)!=0 :
            warning("multiple internal data for a single vessel - I'm unsure what artemis does in this case")
        vessels += tmp
        if 'base' in tag.attrib['broadType'] :
        #TODO does artemis check for the string "base" or just a substring?
            hullRaces[int(tag.attrib['side'])]['bases']+=1
    for race in hullRaces :
        if 'enemy' in race['keys'] :
            if race['bases'] == 0 :
                if not 'biomech' in race['keys'] :#TODO Errr really - maybe? test
                    warning('There is an enemy race "' + race['name'] +'" which has no bases, this means that the stock siege and deep strike missions will spawn ID 0 ships as a base (and look wrong due to that)')

vessels = []
hullRaces = []
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
#TODO check missing texture files
#TODO check snt file is valid
