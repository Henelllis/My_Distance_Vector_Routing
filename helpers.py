# Project 3 for CS 6250: Computer Networks
#
# Helper functions for the DistanceVector project. Students should not
# modify this file.
#
# Copyright 2015 Sean Donovan

"Helpers for Project 3."
logfile = None
current_logs = None
ROUND_SEP = "-----\n"
ALPHABETIZE = True


def open_log(filename):
    global logfile
    global current_logs

    logfile = open(filename, "w")
    current_logs = dict()


def add_entry(switch, logstring):
    global current_logs

    current_logs[switch] = logstring
    print switch + ":" + logstring


def finish_round():
    global logfile
    global current_logs
    
    indices = current_logs.keys()
    if ALPHABETIZE:
        indices = sorted(indices)
    for index in indices:
        logfile.write(index + ":" + current_logs[index] + "\n")

    logfile.write(ROUND_SEP)
    current_logs = dict()


def finish_log():
    global logfile

    logfile.close()
