__author__ = 'orceN'

import sys
import ConfigParser
import argparse

argscount = len(sys.argv)
if(argscount == 0):
    print("can't execute without parameters")
elif(argscount > 0):
    argsparser = argparse.ArgumentParser(description='Configurator for alignmentCalculator definitions')
    argsparser.add_argument('-g', '--get', nargs=3, action='store', metavar=('definitionGroup', 'definitionName'),
                       help='get the definition for defined definitionGroup and definitionName')
    argsparser.add_argument('-s', '--set', nargs=4, action='store', metavar=('definitionGroup', 'definitionName', 'definitionValue'),
                       help='set the definition for defined definitionGroup and definitionName with defined definitionValue')
    try:
        args = argsparser.parse_args()
    except:
        print("can't execute! wrong parameters!")
        sys.exit(1)
    if not(args.get is None) and not(args.set is None):
        print("can't execute get and set command in combination")
        sys.exit(1)
    elif(args.get is not None):
        argscount = len(args.get)
        if(argscount == 3):
            configFile, definitionGroup, definitionName = args.get
            parser = ConfigParser.SafeConfigParser()
            parser.read(configFile)
            definitionValue = parser.get(definitionGroup, definitionName)
            print(definitionValue)
            sys.exit(1)
        elif(argscount != 3):
            print("can't execute get and set command in combination")
            sys.exit(1)
    elif(args.set is not None):
        argscount = len(args.set)
        if(argscount == 4):
            configFile, definitionGroup, definitionName, definitionValue = args.set
            parser = ConfigParser.SafeConfigParser()
            parser.read(configFile)
            parser.set(definitionGroup, definitionName, definitionValue)
            with open(configFile, 'w') as alignmentDef:
                parser.write(alignmentDef)
        elif(argscount != 4):
            print("can't execute get and set command in combination")
            sys.exit(1)