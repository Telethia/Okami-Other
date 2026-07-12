#Sort of like a whatever for other non-main files.

import os
import struct

File1 = 0
File1 = input("Drag file here: ")
Path, Ext = os.path.splitext(File1)
Ext = Ext.lower()
MapFile = open("map.tbl", 'r', encoding="UTF-8")
MapBase = []
MapBytes = []
MapChars = []

def Match(Ext):
    match Ext:
        case ".jmp":
            JMP()
        case ".sca":
            SCA()
        case ".tre" | ".tat" | ".tsc":
            TRE()
        case _:
            #invalid extension probably!
            print("This file extension isn't supported!")
            pass

def JMP():
        #you can pry this code from my cold dead hands
    for line in MapFile:
        MapBase.append(line)
        
    for item in MapBase:
        #print(item)
        try:
            item1, item2 = item.split(': ')
            MapBytes.append(item1)
            MapChars.append(item2)
        except ValueError:
            #print("Malformed value at" + item)
            pass
    FileOpen = open(Path + ".JMP", 'rb')
    OutputFile = open(Path + ".txt", 'w', encoding="UTF-8")
    EntryCount = int.from_bytes(FileOpen.read(4), 'little') #Grab how many entries are in this file
    print(EntryCount)
    i = 0
    while i < EntryCount:
        Text = "Entry: " + str(i) + "\n"
        OutputFile.write(Text)
        CoordsX = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        Text = "X = " + str(CoordsX) + "\n"
        OutputFile.write(Text)
        CoordsY = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        Text = "Y = " + str(CoordsY) + "\n"
        OutputFile.write(Text)
        CoordsZ = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        Text = "Z = " + str(CoordsZ) + "\n"
        OutputFile.write(Text)
        AmmyOrient = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        Text = "Ammy's Orientation is " + str(AmmyOrient) + "\n"
        OutputFile.write(Text)
        AreaID = int.from_bytes(FileOpen.read(2), 'little')
        AIDHex = str("0x" + format(AreaID, 'x').zfill(2))
        index = 0
        TrueAreaID = 999999
        for x in MapBytes:
            if x == AIDHex: #If we find it, print it out.
                #print("Index found at " + str(index))
                TrueAreaID = str((MapChars[index].replace('\n',''))) + "\n"
                #OutputFile.write(Text)
                index = 0
                break
            else:
                if index >= len(MapChars) - 1: #Print it MAYBE
                    TrueAreaID = "{" + str(AIDHex) + "}"
                    #print(Text)
                    pass
                else: #Iterate value
                    index+=1
        Text = "Area ID is " + TrueAreaID.replace('\n','') + "\n"
        OutputFile.write(Text)
        RegionID = int.from_bytes(FileOpen.read(1), 'little')
        Text = "Region ID is " + (str(format(RegionID, 'x').zfill(2))) + "\n"
        OutputFile.write(Text)
        #Unk = int.from_bytes(FileOpen.read(1), 'little')
        ThisIndex = int.from_bytes(FileOpen.read(1), 'little')
        Text = "~~~~~~~~~~~~~~~~~~~~\n\n"
        OutputFile.write(Text)
        i += 1

def SCA():
    FileOpen = open(Path + ".SCA", 'rb')
    OutputFile = open(Path + ".txt", 'w', encoding="UTF-8")
    FileOpen.seek(6, 1) #Skip the header and first unknown
    ZoneNr = int.from_bytes(FileOpen.read(1), 'little') #Number of zones in file
    FileOpen.seek(9, 1) #Skip even more stuff!
    i = 0
    while i < ZoneNr:
        FileOpen.seek(5, 1)
        #print("We are at " + str("0x" + format(FileOpen.tell(), 'x')) + " at the beginning")
        ZoneShape = int.from_bytes(FileOpen.read(1), 'little')
        if ZoneShape == 1:
            ZoneShapeStr = "Quadrilateral Prism"
        elif ZoneShape == 2:
            ZoneShapeStr = "Cylinder"
        #print(ZoneShape)
        #print(ZoneShapeStr)
        FileOpen.seek(2, 1)
        #print("We are at " + str("0x" + format(FileOpen.tell(), 'x')) + " in the middle")
        CoordY = struct.unpack('<f', FileOpen.read(4))[0] #it took me too long to realise the < is supposed to represent the BYTE ORDER???????
                                                          #WHY???????? GOOD LORD
        Height = struct.unpack('<f', FileOpen.read(4))[0]
        Radius = struct.unpack('<f', FileOpen.read(4))[0]
        p1x = struct.unpack('<f', FileOpen.read(4))[0]
        p1z = struct.unpack('<f', FileOpen.read(4))[0]
        p2x = struct.unpack('<f', FileOpen.read(4))[0]
        p2z = struct.unpack('<f', FileOpen.read(4))[0]
        p3x = struct.unpack('<f', FileOpen.read(4))[0]
        p3z = struct.unpack('<f', FileOpen.read(4))[0]
        p4x = struct.unpack('<f', FileOpen.read(4))[0]
        p4z = struct.unpack('<f', FileOpen.read(4))[0]
        FileOpen.seek(1, 1)
        ZoneTypeRaw = int.from_bytes(FileOpen.read(1), 'little')
        match ZoneTypeRaw:
            case 0:
                ZoneType = "a bit flag"
            case 1:
                ZoneType = "a loading zone"
            case 2:
                ZoneType = "unknown"
            case 3:
                ZoneType = "unknown"
            case 4:
                ZoneType = "an examine spot"
            case 5:
                ZoneType = "something Issun jumps to"
            case 6:
                ZoneType = "something Issun jumps arround Amaterasu for"
            case 7:
                ZoneType = "unknown"
            case 8:
                ZoneType = "unknown"
            case 9:
                ZoneType = "some weird collision"
            case 10:
                ZoneType = "an examine tooltip"
            case _:
                ZoneType = "invalid"
        Text = "Y Coord is " + str(round(CoordY, 2)) + "\n"
        OutputFile.write(Text)
        Text = "Height is " + str(round(Height, 2)) + "\n"
        OutputFile.write(Text)
        if ZoneShape == 1:
            Text = "Point 1 is at " + str(round(p1x, 2)) + ", " + str(round(p1z, 2)) + "\n"
            OutputFile.write(Text)
            Text = "Point 2 is at " + str(round(p2x, 2)) + ", " + str(round(p2z, 2)) + "\n"
            OutputFile.write(Text)
            Text = "Point 3 is at " + str(round(p3x, 2)) + ", " + str(round(p3z, 2)) + "\n"
            OutputFile.write(Text)
            Text = "Point 4 is at " + str(round(p4x, 2)) + ", " + str(round(p4z, 2)) + "\n"
            OutputFile.write(Text)
        elif ZoneShape == 2:
            Text = "Radius is " + str(round(Radius, 2)) + "\n"
            OutputFile.write(Text)
            Text = "Center is at " + str(round(p1x, 2)) + ", " + str(round(p1z, 2)) + "\n"
            OutputFile.write(Text)
        Text = "Zone type is " + str(ZoneType) + "\n"
        OutputFile.write(Text)
        EffIndex = int.from_bytes(FileOpen.read(2), 'little')
        Text = "Effect index is " + str(EffIndex) + "\n"
        OutputFile.write(Text)
        Text = "~~~~~~~~~~~~~~~~~~~~\n\n"
        OutputFile.write(Text)
        i += 1
        FileOpen.seek(100, 1) #lmao

def TRE():
    #this might say TRE but it works for TRE, TAT and TSC
    FileOpen = open(Path + Ext, 'rb')
    OutputFile = open(Path + ".txt", 'w', encoding="UTF-8")
    EntryCount = int.from_bytes(FileOpen.read(4), 'little') #Grab how many entries are in this file
    #print(EntryCount)
    ObjType = ["scr","pl","em","et","hm","an","wp","ef","ut","gt","it","vt","dr","ms","es","us"]
    i = 0
    while i < EntryCount:
        #print(str("0x" + format(FileOpen.tell(), 'x')))
        ObjEntry = int.from_bytes(FileOpen.read(1), 'little')
        ObjEntryHex = format(ObjEntry, 'x').zfill(2)
        ObjTypeRaw = int.from_bytes(FileOpen.read(1), 'little')
        #print(ObjTypeRaw)
        Unk = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        SizeX = int.from_bytes(FileOpen.read(1), 'little', signed=True)
        SizeY = int.from_bytes(FileOpen.read(1), 'little', signed=True)
        SizeZ = int.from_bytes(FileOpen.read(1), 'little', signed=True)
        RotX = int.from_bytes(FileOpen.read(1), 'little', signed=True)
        RotY = int.from_bytes(FileOpen.read(1), 'little', signed=True)
        RotZ = int.from_bytes(FileOpen.read(1), 'little', signed=True)
        CoordsX = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        CoordsY = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        CoordsZ = int.from_bytes(FileOpen.read(2), 'little', signed=True)
        Unk4 = int.from_bytes(FileOpen.read(4), 'little')
        Unk1 = int.from_bytes(FileOpen.read(1), 'little')
        Unk42 = int.from_bytes(FileOpen.read(4), 'little')
        UnkFF = int.from_bytes(FileOpen.read(1), 'little')
        Unk12 = int.from_bytes(FileOpen.read(1), 'little')
        ObjParam = int.from_bytes(FileOpen.read(1), 'little')
        Padding = int.from_bytes(FileOpen.read(4), 'little')
        Text = "Entry: " + str(i) + "\n"
        OutputFile.write(Text)
        Text = "Object is " + ObjType[ObjTypeRaw] + str(ObjEntryHex) + "\n"
        OutputFile.write(Text)
        Text = "Size is " + str(SizeX) + ", " + str(SizeY) + ", " + str(SizeZ) + "\n"
        OutputFile.write(Text)
        Text = "Rotation is " + str(RotX) + ", " + str(RotY) + ", " + str(RotZ) + "\n"
        OutputFile.write(Text)
        Text = "Coords are " + str(CoordsX) + ", " + str(CoordsY) + ", " + str(CoordsZ) + "\n"
        OutputFile.write(Text)
        Text = "~~~~~~~~~~~~~~~~~~~~\n\n"
        OutputFile.write(Text)
        i += 1

Match(Ext)