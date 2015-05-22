__author__ = 'orceN'

import sys
import ConfigParser
import argparse

parser = ConfigParser.SafeConfigParser()
parser.read('alignmentCalculatorDefinitions.cfg')

argsparser = argparse.ArgumentParser(description='Configurator for alignmentCalculator definitions')
argsparser.add_argument('-g', '--get', nargs=2, action='store', metavar=('definitionGroup', 'definitionName'),
                   help='get the definition for defined definitionGroup and definitionName')
argsparser.add_argument('-s', '--set', nargs=3, action='store', metavar=('definitionGroup', 'definitionName', 'definitionValue'),
                   help='set the definition for defined definitionGroup and definitionName with defined definitionValue')

args = argsparser.parse_args()

if not(args.get is None) and not(args.set is None):
    sys.exit("can't execute get and set command in combination")

elif(args.get is not None):
    definitionGroup, definitionName = args.get
    definitionValue = parser.get(definitionGroup, definitionName)
    sys.exit(definitionValue)

elif(args.set is not None):
    definitionGroup, definitionName, definitionValue = args.set
    parser.set(definitionGroup, definitionName, definitionValue)
    with open('alignmentCalculatorDefinitions.cfg', 'w') as alignmentDef:
        parser.write(alignmentDef)

