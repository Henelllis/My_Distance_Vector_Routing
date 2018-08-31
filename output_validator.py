# Project 3 output validator for OMS6250 (Fall 2015)+
#
# This output validator is designed to check the student's result log files for errors.
# Errors Detected:
# No intermediate steps shown
# Incorrect separator between steps
# Improper node label format
# Improper node link weight format
# Distance vector to self not included in DVT
# 
#
# Copyright 26 August 2015 Michael D. Brown

import sys
import re
from helpers import ROUND_SEP

line_number = 1

def validateStudentOutput(filename):
    # Overall Formatting Checks
    intermediateStepCheck(filename)

    # Line By Line Chekcs
    with open(filename) as f:
        for line in f:
            if line != ROUND_SEP:
                line = line[0:len(line)-1]          
                validateLine(line)
            global line_number
            line_number = line_number + 1
            
            
def intermediateStepCheck(filename):
    totalSteps=0
    with open(filename) as f:
        for line in f:
            if line == ROUND_SEP:
                totalSteps += 1

    if totalSteps < 2:
        print("Invalid Output: Intermediate steps were not present or step separator was not formatted properly in " + filename)

def validateLine(line):
    node = neighbors = ""
    colonIndex = line.find(':')
    
    if colonIndex > 1:
        node = line[0:colonIndex]
        neighbors = line[colonIndex+1:].split(',')
    elif colonIndex == 1:
        node = line[0]
        neighbors = line[2:].split(',')
    else:
        print "Invalid Output[L" + str(line_number) + "]: Node label should be at least 1 character. (" + node + ")"
        return
    
    if not node.isalpha():
        print "Invalid Output[L" + str(line_number) + "]: Node labels should only contain alphabetic characters. (" + node + ")"
    
    validateNeighbors(neighbors, node)

def validateNeighbors(neighbors, node):
    nodeInDVT = False

    for neighbor in neighbors:
        m = re.search("-*\d", neighbor)
        if m:
            weightIndex = m.start()
            label = neighbor[:weightIndex]
            weight = unicode(neighbor[weightIndex:], 'utf-8')
            
            if not label.isalpha():
                print "Invalid Output[L" + str(line_number) + "]: Node labels should only contain alphabetic characters. (" + label + ")"
            if not validWeight(weight):
                print "Invalid Output[L" + str(line_number) + "]: Link weights should only contain numeric characters. (" + weight + ")"
            if label == node:
                nodeInDVT = True
        else:
            print "Invalid Output[L" + str(line_number) + "]: No link weight present for neighbor " + neighbor + " in DVT entry for node " + node

    if not nodeInDVT:
        print "Invalid Output[L" + str(line_number) + "]: Node does not have a link weight for itself."

def validWeight(weightString):
    if weightString[0] == '-':
        return weightString[1:].isnumeric()
    else:
        return weightString.isnumeric()

# Script Start
# Step 1: check for argument 
if len(sys.argv) != 2:
    print "Syntax:"
    print "    python output_validator.py <log_file>"    
    exit()

# Step 2: Run validator
print "Ouput validation initiated on " + sys.argv[1] + ":"
validateStudentOutput(sys.argv[1])
print "Output validation complete."


