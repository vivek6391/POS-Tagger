import sys

def performTagging(text,transitionMap,emissionMap,tagList, startProbMap, outputList):
    lines = text.split('\n')
    
    for line in lines:
        listWords = line.split(' ')
        if line:
            viterbiAlgorithm(listWords, tagList, startProbMap, transitionMap, emissionMap, outputList)
    
def viterbiAlgorithm(listWords, tagList, startProbMap, transitionMap, emissionMap,outputList):
    timeFrames = [{}]
    
    if listWords[0] in emissionMap:
        for state,val in emissionMap[listWords[0]].items():
            if state not in timeFrames[0]:
                timeFrames[0][state] = {}
            timeFrames[0][state]['val'] = startProbMap[state] + val
            timeFrames[0][state]['previous'] = 'start'
    else:
        for i in tagList:
            if i not in timeFrames[0]:
                timeFrames[0][i] = {}
            if listWords[0] in emissionMap:
                if i in emissionMap[listWords[0]]:
                    timeFrames[0][i]['val'] = startProbMap[i] + emissionMap[listWords[0]][i]
                    timeFrames[0][i]['previous'] = 'start'
                else:
                    timeFrames[0][i]['val'] = startProbMap[i]
                    timeFrames[0][i]['previous'] = 'start'
            else:
                timeFrames[0][i]['val'] = startProbMap[i]
                timeFrames[0][i]['previous'] = 'start'
                
    
    # Run Viterbi Algorithm for words from 1 to end
    for t in range(1, len(listWords)):
        timeFrames.append({})
        if listWords[t] not in emissionMap:
            for emissionTag in tagList:
                valueProb = float(-sys.maxint)
                prevState = ''
                for previousTag in timeFrames[t-1]:
                    tempVal = float(-sys.maxint)
                    if listWords[t] in emissionMap:
                        if emissionTag in emissionMap[listWords[t]]:
                            tempVal = timeFrames[t - 1][previousTag]['val'] + transitionMap[previousTag][emissionTag] + emissionMap[listWords[t]][emissionTag]
                        else:
                            tempVal = timeFrames[t - 1][previousTag]['val'] + transitionMap[previousTag][emissionTag]
                    else:
                        tempVal = timeFrames[t - 1][previousTag]['val'] + transitionMap[previousTag][emissionTag]
                    if valueProb < tempVal:
                        valueProb = tempVal
                        prevState = previousTag
                if emissionTag not in timeFrames[t]:
                    timeFrames[t][emissionTag] = {}
                timeFrames[t][emissionTag]['val'] = valueProb
                timeFrames[t][emissionTag]['previous'] = prevState
        else:
            for emissionTag in emissionMap[listWords[t]]:
                valueProb = float(-sys.maxint)
                prevState = ''
                for previousTag in timeFrames[t-1]:
                    tempVal = float(-sys.maxint)
                    if listWords[t] in emissionMap:
                        if emissionTag in emissionMap[listWords[t]]:
                            tempVal = timeFrames[t - 1][previousTag]['val'] + transitionMap[previousTag][emissionTag] + emissionMap[listWords[t]][emissionTag]
                        else:
                            tempVal = timeFrames[t - 1][previousTag]['val'] + transitionMap[previousTag][emissionTag]
                    else:
                        tempVal = timeFrames[t - 1][previousTag]['val'] + transitionMap[previousTag][emissionTag]
                    if valueProb < tempVal:
                        valueProb = tempVal
                        prevState = previousTag
                if emissionTag not in timeFrames[t]:
                    timeFrames[t][emissionTag] = {}
                timeFrames[t][emissionTag]['val'] = valueProb
                timeFrames[t][emissionTag]['previous'] = prevState
                

    lastElement = len(timeFrames)-1
    
    prevState = ''
    valueProb = float(-sys.maxint)
    tempVal = float(-sys.maxint)
    for previousTag in timeFrames[lastElement]:
        if 'end' not in transitionMap[previousTag]:
            tempVal = timeFrames[lastElement][previousTag]['val']
        else:
            tempVal = timeFrames[lastElement][previousTag]['val'] + transitionMap[previousTag]['end']
        if valueProb < tempVal:
            valueProb = tempVal
            prevState = previousTag
    
    
    stringToDisplay = listWords[lastElement] + '/' + previousTag
    j = lastElement 
    while j >= 1 : 
        temp = timeFrames[j][previousTag]
        previousTag = temp['previous']
        stringToDisplay = listWords[j-1] + '/' + previousTag + ' ' + stringToDisplay
        j = j - 1
        
    outputList.append(stringToDisplay)
    
def readHMMTextFile(transitionMap, emissionMap, startProbMap, tagList):
    isTransition = False
    isEmission = False
    isTagList = False
    with open('hmmmodel.txt') as fileToRead:
        for line in fileToRead:
            if 'TransitionProbability' in line : 
                isTransition = True
                isEmission = False
                isTagList = False
                continue
            if 'EmissionProbability' in line  : 
                isTransition = False
                isEmission = True
                isTagList = False
                continue
            if 'TagList' in line  : 
                isTransition = False
                isEmission = False
                isTagList = True 
                continue
            if isTransition:
                tList = line.split(' ')
                Obj = dict()
                if 'start' in tList[0]:
                    startProbMap[tList[1]] = float(tList[2])
                else:
                    if tList[0] in transitionMap:
                        Obj = transitionMap[tList[0]]
                    Obj[tList[1]] = float(tList[2])
                    transitionMap[tList[0]] = Obj
            if isEmission:
                tList = line.split(' ')
                Obj = dict()
                if tList[0] in emissionMap:
                    Obj = emissionMap[tList[0]]
                Obj[tList[1]] = float(tList[2])
                emissionMap[tList[0]] = Obj
            if isTagList:
                tagList.append(line.replace('\n',''))  

transitionMap = dict()
emissionMap = dict()
startProbMap = dict()
tagList = list()

readHMMTextFile(transitionMap, emissionMap, startProbMap, tagList)

mainDir = sys.argv[1]
outputList = list()
    

f = open(mainDir)
text =  f.read() 
performTagging(text,transitionMap,emissionMap,tagList, startProbMap,outputList)


fileTowrite = open('hmmoutput.txt','w')
for strToPrint in outputList:
    fileTowrite.write(strToPrint + '\n')    
