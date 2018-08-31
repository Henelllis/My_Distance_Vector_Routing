# Project 3 for CS 6250: Computer Networks
#
# This defines a Node that can fun the Bellman-Ford algorithm. Students
# should not modify this file, but should instead modify the DistanceVector
# class that inherits from Node.
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Sean Donovan and Jeffrey Randow

class Neighbor(object):

    def __init__(self, neighbor_node, weight):
    # This class is to define a data structure to hold the neighbor name and the
    # weight to each neighbor.   
        self.name = neighbor_node
        self.weight = weight        

class Node(object):

    def __init__(self, name, topolink, outgoing_links, incoming_links):
    # name is the name of the local node
    # links is a list of all neighbor objects. 
    # neighbor_name is a list of the names of the neighbors.
    # topology is a backlink to the Topology class. Used for accessing neighbors
    #   as follows: self.topology.topodict['A']  NOTE: Students should NOT use this functionality!
    # messages is a list of pending messages from neighbors to be processed.
    #   The format of the message is up to you; a tuple will work.
        self.name = name
        self.incoming_links = incoming_links
        self.outgoing_links = outgoing_links
        self.neighbor_names = []
        self.topology = topolink
        self.messages = []
        
        for neighbor in self.incoming_links:
            self.neighbor_names.append(neighbor.name)               

    def get_outgoing_neighbor_weight(self, neighbor_name):
        ''' This function returns the weight for a specific outgoing neighbor name '''
        for neighbor in self.outgoing_links:
            if neighbor_name == neighbor.name:
                return neighbor.weight
        return "Node Not Found"

    def __len__(self):
        ''' Returns the length of the message queue. '''
        return len(self.messages)

    def __str__(self):
        ''' Returns a string representation of the node. '''

        retstr = self.name + " :  outgoing links ( "
        for neighbor in self.outgoing_links:
            retstr = retstr + neighbor.name + neighbor.weight + " "
        
        retstr = retstr + ")  incoming links ( "
        for neighbor in self.incoming_links:
            retstr = retstr + neighbor.name + neighbor.weight + " "        

        return retstr + ")"        

    def __repr__(self):
        return self.__str__()    

    def verify_neighbors(self):
        ''' Verify that all your neighbors exist. '''
        for neighbor in self.outgoing_links:
            if neighbor.name not in self.topology.topodict.keys():           
                raise Exception(self.name + " has outgoing link to neighbor " + neighbor.name + " that does not exist in Topology!")           

    def send_msg(self, msg, dest):
        ''' Performs the send operation, after verifying that the neighbor is
            valid.
        '''
        if dest not in self.neighbor_names:
            raise Exception("Neighbor " + dest + " does not have an incoming link to " + self.name)
        
        self.topology.topodict[dest].queue_msg(msg)
        

    def queue_msg(self, msg):
        ''' Allows neighbors running Bellman-Ford to send you a message, to be
            processed next time through self.process_BF(). '''
        self.messages.append(msg)
