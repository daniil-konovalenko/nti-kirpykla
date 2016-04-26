import os


# file - file descriptor
# count - count of lines will be readed (0 - read all lines)
# schema - parsed shema for reading
# indexCol - indexes or names for column which will be index for dictionary
# otherCols - list of names of columns which will be written
# isList - if true present result as lists (it's faster)
def parsePigArray(file, count=0, schema=list(), indexCol="", otherCols=list(),
                  asLists=False):
    fileName = file.name

    counter = 0
    res = list() if indexCol == "" else dict()
    isEnd = False
    fieldListsArr = list()
    typeList = list()
    isFlat = True
    indexColId = -1
    for fieldId in range(0, 0 if len(schema) == 0 else len(schema['fields'])):
        if len(otherCols) > 0 and (
            str(schema['fields'][int(fieldId)]['name']) != "null") and (
        str(schema['fields'][int(fieldId)]['name'])) not in otherCols:
            continue;
        if indexCol != "" and (str(schema['fields'][int(fieldId)]['name']) == indexCol):
            indexColId = len(fieldListsArr)
        fieldListsArr.append(fieldId)
        if (isFlat):
            if (schema['fields'][int(fieldId)]['type'] == "15"):
                typeList.append(15)
                continue
            if (schema['fields'][int(fieldId)]['type'] == "10"):
                typeList.append(10)
                continue
            isFlat = False

    while ((not isEnd) and ((not count) or counter < count)):
        if (counter % 500000 == 0):
            print("lines parsed " + str(counter))
        paramList = list()
        paramList.append(file.readline())
        if (not paramList[0]):
            fileNameList = fileName.split("-")
            last = fileNameList[len(fileNameList) - 1]
            charNum = len(last)
            last = int(last) + 1
            resString = "0" * (int(charNum) - len(str(last)))
            resString += (str(last))
            fileNameList[len(fileNameList) - 1] = str(resString)
            fileName = '-'.join(fileNameList)
            print("File " + str(fileName) + " was opened")
            if (not os.path.isfile(fileName)):
                break
                isEnd = True
                continue
            else:
                file = open(fileName, 'r')

        if (not paramList[0]):
            continue
        counter += 1

        if len(schema) > 0 and (not isFlat or not asLists):
            if len(otherCols) > 0:
                otherCols.append(indexCol)
            paramList.extend([schema, " ", otherCols, asLists, fieldListsArr])
            parsedLine = saveFields(paramList)
        else:
            parsedLine2 = paramList[0].split("\t")
            parsedLine = list()

            if isFlat and len(typeList) > 0:
                for ind in range(0, len(typeList)):
                    if (parsedLine2[fieldListsArr[ind]] != ""):
                        parsedLine.append(
                            int(parsedLine2[fieldListsArr[ind]]) if typeList[
                                                                        ind] == 15 else
                            parsedLine2[fieldListsArr[ind]])
            else:
                parsedLine = parsedLine2

        if indexCol == "":
            res.append(parsedLine)
        else:
            if len(schema) > 0 and (not isFlat and not asLists):
                key = parsedLine[indexCol]
                if type(parsedLine) == list:
                    parsedLine.remove(parsedLine[int(indexCol)])
                else:
                    parsedLine.pop(indexCol, None)
                    parsedLine = parsedLine.values()
            else:
                key = parsedLine[indexColId]
                parsedLine.remove(parsedLine[int(indexColId)])
            if len(parsedLine) == int(1):
                parsedLine = parsedLine[0]
            res[key] = parsedLine
    print("lines parsed " + str(counter))
    return res


# Detect end of block
def getCloseBrace(paramList):
    if (paramList[1] < 0):
        a = c
        exit()

    openPos = paramList[0][paramList[4]:].find(paramList[2])
    
    closePos = paramList[0][paramList[4]:].find(paramList[3])

    if (int(openPos) < int(closePos) and (int(openPos) >= 0)):
        paramList[4] += openPos + 1
        paramList[1] += 1
        foundedPos = getCloseBrace(paramList)
        return foundedPos + openPos + 1;
    else:
        if closePos < 0:
            a = c
            return -1
        paramList[4] += closePos + 1
        
        paramList[1] -= 1
        if paramList[1] == 0 or paramList[4] >= len(paramList[0]):
            return closePos + 1
        else:
            foundedPos = getCloseBrace(paramList)
            return foundedPos + closePos + 1;
    return 0;


symbols = (",", "]", "}")


def getEndOfBlock(paramList):
    if paramList[0][0:1] == "\"":
        res = paramList[0][1:len(paramList[0]) - 1]
        return res.find("\"") + int(2);
    if paramList[0][0:1] == "{":
        paramList.extend([int(0), "{", "}", int(0)])
        return getCloseBrace(paramList)
    if paramList[0][0:1] == "[":
        paramList.extend([int(0), "[", "]", int(0)])
        return getCloseBrace(paramList)
    if paramList[0][0:1] == "(":
        paramList.extend([int(0), "(", ")", int(0)])
        return getCloseBrace(paramList)
    minPos = len(paramList[0])
    for symb in symbols:
        pos = paramList[0].find(",")
        if (pos < minPos and pos >= 0):
            minPos = pos

    return minPos


# It's needed on;y for schema parsing(it's fast)
def parseNextElement(line):
    if line[0:1] == "\"":
        res = line[1:len(line)]
        nameField = res[:res.find("\"")];
        return (nameField, len(nameField) + 2)
    if line[0:1] == "{":
        close = getCloseBrace([line, 0, "{", "}", 0])
        return parseFields(line[1:close - 1])
    if line[0:1] == "[":
        close = getCloseBrace([line, 0, "[", "]", 0])
        resLine = line[1:int(close) - 1]
        res = list()
        while (len(resLine) > 4):
            (val, valLen) = parseNextElement(resLine)
            res.append(val)
            resLine = resLine[valLen + 2:]

        return (res, close)

    minPos = len(line)
    for symb in symbols:
        pos = line.find(",")
        if (pos < minPos and pos >= 0):
            minPos = pos

    return (line[0:minPos], minPos)


# It's needed on;y for schema parsing(it's fast)
def parseField(line):
    fieldName = line[1:line.find(":") - 1]
    valLine = line[line.find(":") + 1:]
    fieldValStr = valLine[:getEndOfBlock([valLine])]
    (fieldVal, fieldLen) = parseNextElement(fieldValStr)
    res = (fieldName, fieldVal, len(fieldName) + len(fieldValStr) + 3)
    return res


# It's needed on;y for schema parsing(it's fast)
def parseFields(line):
    resLine = line
    res = dict()
    totalLen = 0
    while (len(resLine) > 4):
        (fieldName, fieldVal, fieldLen) = parseField(resLine)

        res[fieldName] = fieldVal
        resLine = resLine[fieldLen + 1:]
        totalLen += fieldLen + 1
    return (res, totalLen)


# It's needed for data reading. Saving array of values (in '[' brackets)
def saveArray(testLine, schema, otherCols, asLists=False):
    fieldListsArr = list()
    fieldsLen = len(schema['fields'])
    if len(otherCols) > 0:
        if type(otherCols[0]) == int:
            fieldListsArr = otherCols
        else:
            for fieldId in range(0, fieldsLen):
                if (str(schema['fields'][int(fieldId)]['name']) != "null") and (
                str(schema['fields'][int(fieldId)]['name'])) not in otherCols:
                    continue;
                fieldListsArr.append(fieldId)
    res = list()
    testLine = testLine.split(")")
    testLine[0] = "," + testLine[0]
    for elemLine in testLine:
        if elemLine == "":
            continue
        elemLine = elemLine[2:]
        elemLine = saveFields([elemLine, schema, ",", otherCols, asLists, fieldListsArr])
        res.append(elemLine)
    if len(res) == int(1):
        res = res[0]

    return res;


# It's needed to save different fields according to schema
def saveFields(param_list):
    splitter = param_list[2]
    otherCols = param_list[3]
    asLists = param_list[4]
    fieldListArr = param_list[5]
    res = list() if asLists else dict()
    lineSplitted = param_list[0].split() if (splitter == " ") else param_list[0].split(
        splitter)
    fieldsLen = min(len(param_list[1]['fields']), len(lineSplitted))
    fieldLists = list()
    if (len(fieldListArr) > 0):
        fieldLists = fieldListArr
    else:
        for fieldId in range(0, fieldsLen):
            if (len(otherCols) > 0 and str(
                    param_list[1]['fields'][int(fieldId)]['name']) != "null") and (
            str(param_list[1]['fields'][int(fieldId)]['name'])) not in otherCols:
                continue;
            fieldLists.append(fieldId)
    if (len(otherCols) == 0):
        fieldLists = range(0, fieldsLen)
    fieldsLenActual = len(fieldLists)
    for fieldId in fieldLists:
        if len(otherCols) > 0 and (
            str(param_list[1]['fields'][int(fieldId)]['name']) != "null") and (
        str(param_list[1]['fields'][int(fieldId)]['name'])) not in otherCols:
            continue;

        fieldDesc = param_list[1]['fields'][int(fieldId)]
        if (fieldDesc['type'] == "15" or fieldDesc['type'] == "10"):
            if asLists:
                val = lineSplitted[fieldId] if (fieldDesc['type'] != "15") else int(
                    lineSplitted[fieldId])
                if fieldsLenActual > 1:
                    res.append(val)
                else:
                    res = val
            else:
                res[str(param_list[1]['fields'][int(fieldId)]['name'])] = lineSplitted[
                    fieldId] if (fieldDesc['type'] != "15") else int(
                    lineSplitted[fieldId])
        if (fieldDesc['type'] == "120"):
            close = getEndOfBlock([lineSplitted[fieldId]]) - 1;
            if fieldsLenActual == 1:
                res = saveFields(
                    [lineSplitted[fieldId][1:close], fieldDesc['schema'], " ", otherCols,
                     asLists, list()])
            else:
                if asLists:
                    res.append(saveFields(
                        [lineSplitted[fieldId][1:close], fieldDesc['schema'], " ",
                         otherCols, asLists, list()]))
                else:
                    res[str(param_list[1]['fields'][int(fieldId)]['name'])] = saveFields(
                        [lineSplitted[fieldId][1:close], fieldDesc['schema'], " ",
                         otherCols, asLists, list()])

        if (fieldDesc['type'] == "110"):
            if fieldsLenActual == 1:
                
                res = saveArray(lineSplitted[fieldId], fieldDesc['schema'], otherCols,
                                asLists)

            else:
                if asLists:
                    res.append(
                        saveArray(lineSplitted[fieldId], fieldDesc['schema'], otherCols,
                                  asLists))
                else:
                    res[str(param_list[1]['fields'][int(fieldId)]['name'])] = saveArray(
                        lineSplitted[fieldId], fieldDesc['schema'], otherCols, asLists)

    return res


def parseSchema(line):
    (schema, schemaLen) = parseNextElement(line)
    return schema


def parseFolder(folderName, linesCount=0, fileDesc="", indexCol="", otherCols=list()):
    import fnmatch
    if fileDesc == "":
        for file in os.listdir(folderName):
            if fnmatch.fnmatch(file, 'part-*-00000'):
                fileDesc = open(folderName + "/" + file, 'r')
    return (parsePigArray(fileDesc, linesCount, list(), indexCol, otherCols), fileDesc)


def parseFolderBySchema(folderName, linesCount=0, fileDesc="", indexCol="",
                        otherCols=list(), isLists=False):
    shemaFileName = folderName + "/.pig_schema"

    f = open(shemaFileName, 'r')
    line = f.readline()
    schema = parseSchema(line)
    import fnmatch
    if fileDesc == "":
        for file in os.listdir(folderName):
            if fnmatch.fnmatch(file, 'part-*-00000'):
                fileDesc = open(folderName + "/" + file, 'r')
    f.close()

    return (
    parsePigArray(fileDesc, linesCount, schema, indexCol, otherCols, isLists), fileDesc)
