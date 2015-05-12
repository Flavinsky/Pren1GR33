__author__ = 'orceN'

import sys
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('alignmentCalculatorDefinitions.cfg')

def setDefinition(definitionGroup, definitionName, definitionValue):

    try:
        config.set(definitionGroup, definitionName, definitionValue)
        with open('alignmentCalculatorDefinitions.cfg', 'w') as alignmentDef:
            config.write(alignmentDef)
    except:
         print("write configfile for alignmentCalculator failed")
         return None

def getDefinition(definitionGroup, definitionName):

    try:
        definitionValue = config.get(definitionGroup, definitionName)
        return definitionValue
    except:
        print("read configfile for alignmentCalculator failed")
        return None

if __name__ == '__main__':

    operationType = sys.argv[1]
    definitionGroup = sys.argv[2]
    definitionName = sys.argv[3]
    if(len(sys.argv) == 3):
        definitionValue = sys.argv[4]

    if(operationType == 'get'):
        sys.exit(getDefinition(definitionGroup, definitionName))
    elif (operationType == 'set'):
        sys.exit(setDefinition(definitionGroup, definitionName, definitionValue))
    else:
        print("invalid input")
        sys.exit(None)

