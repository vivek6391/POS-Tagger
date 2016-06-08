import sys
import math

def learnHMM(text, hmmTransitionMap, hmmEmissionMap, countMap, tagList):
    lines = text.split('\n')
    
    
    for line in lines:
        previousWord = 'start'
        if not line:
            continue
        
        listWords = line.split(' ')
        
        for word in listWords:
            tagWords = word.rsplit('/',1)
            
            if tagWords[1] not in tagList:
                tagList.append(tagWords[1])
            
            emissionObj = dict()
            if tagWords[0] in hmmEmissionMap:
                emissionObj = hmmEmissionMap[tagWords[0]]
            
            if tagWords[1] not in emissionObj:
                emissionObj[tagWords[1]] = 0

            emissionObj[tagWords[1]] = emissionObj[tagWords[1]] + 1
            hmmEmissionMap[tagWords[0]] = emissionObj
            
            transitionObj = dict()
            if previousWord in hmmTransitionMap:
                transitionObj = hmmTransitionMap[previousWord]
            
            if tagWords[1] not in transitionObj:
                transitionObj[tagWords[1]] = 0
                
            transitionObj[tagWords[1]] = transitionObj[tagWords[1]] + 1
            hmmTransitionMap[previousWord] = transitionObj
            previousWord = tagWords[1]
            
            if tagWords[1] in countMap:
                countMap[tagWords[1]] = countMap[tagWords[1]] + 1
            else:
                countMap[tagWords[1]] = 1
        
        transitionObj = dict()
        if previousWord in hmmTransitionMap:
            transitionObj = hmmTransitionMap[previousWord]
                
        if 'end' not in transitionObj:
            transitionObj['end'] = 0
        transitionObj['end'] = transitionObj['end'] + 1
        hmmTransitionMap[previousWord] = transitionObj
    
def smoothTransitionProbability(hmmTransitionMap,tagList,countMap):
    for key in hmmTransitionMap:
        transObj = hmmTransitionMap[key]
        totalTrans = 0;
        for tags in transObj:
            totalTrans = totalTrans + transObj[tags]
        if key == 'start':
            totalTrans = totalTrans + len(tagList)
        else:
            totalTrans = totalTrans + (len(tagList) + 1)
        
        for tags in tagList:
            if tags in transObj:
                transObj[tags] = math.log(transObj[tags] + 1) - math.log(totalTrans)
            else:
                transObj[tags] = math.log(1) - math.log(totalTrans)
        
        if key != 'start':
            if 'end' in transObj:
                transObj['end'] = math.log(transObj['end']) - math.log(totalTrans)
            else:
                transObj['end'] = math.log(1) - math.log(totalTrans)
            
def calculateEmissionProbability(hmmEmissionMap,countMap):
    for key in hmmEmissionMap:
        emissionObj = hmmEmissionMap[key]
        for tags in emissionObj:
            emissionObj[tags] = math.log(emissionObj[tags]) - math.log(countMap[tags])
        

def writeProbabilitiesTextFile(hmmTransitionMap,hmmEmissionMap,tagList):
    fileTowrite = open('hmmmodel.txt','w')
    fileTowrite.write('TransitionProbability\n')
    for key in hmmTransitionMap:
        transObj = hmmTransitionMap[key]
        for tag in transObj:
            stringToPrint = key + ' ' + tag + ' ' + str(transObj[tag]) + '\n'
            fileTowrite.write(stringToPrint)
            
    fileTowrite.write('EmissionProbability\n')    
    for key in hmmEmissionMap:
        emmisionObj = hmmEmissionMap[key]
        for tag in emmisionObj:
            stringToPrint = key + ' ' + tag + ' ' + str(emmisionObj[tag]) + '\n'
            fileTowrite.write(stringToPrint)

    fileTowrite.write('TagList\n')    
    for tag in tagList:
        stringToPrint = tag + '\n'
        fileTowrite.write(stringToPrint)

hmmTransitionMap = dict()
hmmEmissionMap = dict()
countMap = dict()
tagList = list()

mainDir = sys.argv[1]
f = open(mainDir)
text =  f.read() 
learnHMM(text,hmmTransitionMap,hmmEmissionMap,countMap,tagList)

smoothTransitionProbability(hmmTransitionMap,tagList,countMap)
calculateEmissionProbability(hmmEmissionMap, countMap)
writeProbabilitiesTextFile(hmmTransitionMap,hmmEmissionMap,tagList)
    
