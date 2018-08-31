# Project 3 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *
import math

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        #TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data    
        self.vector = {}
        ##print("this is what my number looks like " + str(number))
        self.vector[self.name] = int(0)

    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        vectorMappings = {}
        #msg = msg(vectorMappings)
        ##print("Testing map features of " + str(self.incoming_links[0]))
        for upstreamNeighbor in self.incoming_links:
            #print("THE NODE : " + self.name + " Sending this to this upstream neighbor " + str(upstreamNeighbor.name) + "\n")
            ##print("With a weight of  " + str(upstreamNeighbor.weight) + "\n")
            ##print("This is the associated message " + str(vectorMappings))
            #innermapping = {}
            #innermapping[self.name] = 0 #upstreamNeighbor.weight
            vectorMappings[self.name] = self.vector
            self.send_msg(vectorMappings, upstreamNeighbor.name)

 
    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''
 
        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages
        MappingToSend = {}
        toBeSent = False
        counter = 1
        for msg in self.messages:
            #print("NODE " + self.name  + " > msg : " + str(counter) + ", " + str(msg) )
            counter += 1
            sendMessage = False # I Dont think you need a boolean 
            #print("\t Node " + self.name + " looks like a got a message")
           # #print( "This node sent me this Map, quite interseting!!!!" + str(msg))
            for node_name, vector_mappings in msg.items(): #out mapping
                #print ("\t\tThis is the associated weight wiht outgoing node : " + str(self.get_outgoing_neighbor_weight(node_name)) + " For " + node_name)
                #print("\t\tincoming outer vector name:" + str(node_name) + "\n\t\tvector_mappings" +  str(vector_mappings))
                
                #Check to add Keys of Zero
                for inner_node_name, inner_value in vector_mappings.items(): # inner mapping
                    if(inner_node_name == node_name and  inner_node_name not in self.vector):
                        self.vector[inner_node_name] = self.get_outgoing_neighbor_weight(inner_node_name);
                        #print("ALPHA AREA In side counter " + str(counter -1) + " creating a message to send")                        
                        MappingToSend[self.name] = self.vector
                        toBeSent = True


                #add up all the nodes in the algorithm
                for inner_node_name, inner_value in vector_mappings.items(): # inner mapping
                    if(inner_node_name == node_name and  inner_node_name not in self.vector):
                        self.vector[inner_node_name] = self.get_outgoing_neighbor_weight(inner_node_name);
                        #print(" BETA AREA In side counter " + str(counter - 1) +  " creating a message to send")
    
                        MappingToSend[self.name] = self.vector
                        #messages_to_send.append( )
                        toBeSent = True

                    elif(inner_node_name not in self.vector or (int(self.vector[inner_node_name]) > int(self.vector[node_name]) + int(inner_value) )):
                        
                        if(int(self.vector.get(node_name) is None)):
                            weightFromNode = 0
                        else:
                            weightFromNode = int(self.vector.get(node_name))

                        self.vector[inner_node_name] =  (weightFromNode + int(inner_value))
                        #print("GAMMA AREA In side counter " + str(counter - 1) +  " creating a message to send")
                        MappingToSend[self.name] = self.vector
                        toBeSent = True

                        if(self.vector[inner_node_name] <= -99):
                        #    MappingToSend = None
                            self.vector[inner_node_name] = -99
                            toBeSent = False


        #    pass
        ##print("Processed the node of " + self.name  + " Has a vector map of "  + str(self.vector))
        
        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        if(toBeSent is True):
            #print("SENDING MESSAGE")               
            for upstreamNeighbor in self.incoming_links:
                self.send_msg(MappingToSend, upstreamNeighbor.name)

    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        #prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which #prints the format example text above (hardcoded) is provided.
        formatString = ""

        for node_name in sorted(self.vector):

            formatString +=   node_name  + str(self.vector[node_name]) + ","

        #formatString = formatString[-1]
        add_entry(self.name, formatString[:-1])                           
        #add_entry("A", "A0,B1,C2")        
