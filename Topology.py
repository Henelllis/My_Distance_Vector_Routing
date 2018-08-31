# Project 3 for CS 6250: Computer Networks
#
# Defines a Topology, which is a collection of Nodes. Students should not
# modify this file.  This is NOT a topology like the ones defined in Mininet projects.
#
# The topology is a weighted directed graph.  This means that each link has a direction from
# a source node to a destination node, and that link has a weight that is permitted to be
# positive, negative, or 0 (weightless).
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Sean Donovan and Jeffrey Randow

from DistanceVector import *
import csv


class Topology(object):

    def __init__(self, conf_file):
        ''' Initializes the topology. Called from outside of DistanceVector.py '''
        self.topodict = {}
        self.nodes = []
        self.topo_from_conf_file(conf_file)
    
    def topo_from_conf_file(self, conf_file):
        ''' This creates all the nodes in the Topology  from the configuration
            file passed into __init__(). Can throw an exception if there is a
            problem with the config file. '''

        input_file = open(conf_file,"rb")
        topology_data = csv.reader(input_file)

        node_list = []
        incoming_links = {}
        outgoing_links = {}        

        for row in topology_data:
            if len(row) == 0:
                ''' Empty row '''
                continue
            if  row[0].startswith('#'):
                ''' This is a comment row.  Ignore '''
                continue                      
            
            node_list.append(row[0])
            outgoing_links[row[0]] = []
            
            if row[0] not in incoming_links.keys():
                incoming_links[row[0]] = []            
            
            column = 1
            while column < len(row):
                outgoing_links[row[0]].append(Neighbor(row[column],row[column+1]))
                
                if row[column] not in incoming_links.keys():
                    incoming_links[row[column]] = []

                incoming_links[row[column]].append(Neighbor(row[0],row[column+1]))

                column += 2                   

        for node in node_list:
            new_node = DistanceVector(node,self,outgoing_links[node], incoming_links[node])
            self.nodes.append(new_node)
            self.topodict[node] = new_node

        self.verify_topo()

    def verify_topo(self):
        ''' Once the topology is imported, we verify the topology to make sure
            it is actually valid. '''
        
        for node in self.nodes:
            try:
                node.verify_neighbors()
            except:
                print "error with neighbors of " + node.name
                raise            

    def run_topo(self):
        ''' This is where most of the action happens. First, we have to "prime 
        the pump" and send to each neighbor that they are connected. 

        Next, in a loop, we go through all of the nodes in the topology running
        their instances of Bellman-Ford, passing and receiving messages, until 
        there are no further messages to service. Each loop, print out the 
        distances after the loop instance. After the full loop, check to see if 
        we're finished (all queues are empty).
        '''
        #Prime the pump
        for node in self.nodes:
            node.send_initial_messages()


        done = False
        while done == False:
            for node in self.nodes:
                node.process_BF()
                node.log_distances()
            

            # Done with a round. Now, we call finish_round() which writes out
            # each entry in log_distances(). By default, this will will print 
            # out alphabetical order, which you can turn off so the logfile 
            # matches what is printed during log_distances().
            finish_round()

            done = True
            for node in self.nodes:
                if len(node) != 0:
                    done = False
                    break
