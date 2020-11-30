import hashlib
from uuid import uuid4
import json
import datetime
from flask import Flask, request , jsonify
from urllib.parse import urlparse
import requests


class Certification_managment: 
    
    ### constructor #####
    def __init__(self):

        self.chain=[]
        self.blacklist=set()
        self.node_name=set()
        self.node_address=set()
        self.node_name.add(('Genisis_Block'))
        self.added=None
        certificates=[{ "id":"abc00ad3",
                        "issued to":"Certification_managment",
                        "issued by":"PBFT trust protocol",
                        "remarks":"Welcome to the blockchain",
                        "issued  on":"2020",
                        "valid_through":"Forever"}]

        block=self.create_block(certificates,0,'Genisis_Block')
        ### block is added to personal blockchain, needs confirmation of the network to be confirmed
        
        self.add_block_to_chain(block)
            
    ### bloack creation #####
    def create_block(self,certificates,previous_hash,publisher):
        block={'datetime':datetime.datetime.now(),
                'index':self.length()+1,
                'previous_hash':previous_hash,
                'certificates':certificates,
                'publisher':publisher}

        return block


    ##### adding block to block chain ##########
    def add_block_to_chain(self, block):
        if(block['index']!=len(self.chain)+1):
            return  "Unable to add due to error in length of the block"
        if len(block['certificates'])>1001:
            return  "too many records, status: not added "
        if block['publisher'] not in self.node_name:
            return  "unauthroirised user"
        if block['publisher'] in self.blacklist:
            return  "blacklisted user"

        if self.length()>100:
            if block['datetime']<self.chain[self.length-100]["datetime"]:
                return "block is too old to be added now"
            for i in self.chain[len(self.chain)-100:]:
                if (i[publisher]==block['publisher']):
                    return  "you cant publish soon again, wait "

        if self.length()==0:
            if block['previous_hash']!=0:
                return "Fatal error, provided a wrong hash"
        else:
            if block['previous_hash']!=self.hash(self.get_previous_block()):
                return "Fatal error, provided a wrong hash"

        self.chain.append(block)
        self.added=block
    

        return "successfully added"
                        

    ######  chain ##########                
    def length(self):
        return len(self.chain)

    def get_chain(self):
        return self.chain

    def get_previous_block(self):
        return self.chain[-1]
   
    def get_added(self):
        return self.added


    ######## SHA256 #####
    def hash(self,block):
        h = hashlib.sha256()
        h.update(str(block['datetime']).encode('utf-8')+
                str(block['index']).encode('utf-8')+
                str(block['previous_hash']).encode('utf-8')+
                str(block['certificates'][0]['id']).encode('utf-8')+
                str(block['publisher']).encode('utf-8'))
        return h.hexdigest()

    

    ##########   NODE #######
    
    def get_node_name(self):
        return self.node_name
    
    def get_node_address(self):
        return self.node_address

    
    def add_to_node_name(self,name):
        self.node_name.add(name)

    def add_to_node_address(self,address):
        parsed_url=urlparse(address)
        self.node_address.add(parsed_url.netloc)

    def add_node(self,name,address):
        self.add_to_node_address(address)
        self.add_to_node_name(name)

  ### Blacklist #########
    
    def get_black_list(self):
        return self.blacklist

    def add_to_black_list(self,name):
        self.blacklist.add(name)      


    ###  validating and adding new block that have been created and added by other nodes  ##################
    def update_chain(self):
        for node in self.node_address:

            response=requests.get(f'http://{node}/get_added_block')
            new_block=response.json()['block']
            return self.add_block_to_chain(new_block)
         

    def is_chain_valid(self,chain):
        c_len=1
        for block in chain: 
            if(block['index']!=c_len):
                return False

            if(len(block['certificates'])>1001):
                return False

            if(block['publisher'] not in self.node_name):
                return False
            

            if c_len>100:
                if(block['datetime']<chain[c_len-100]["datetime"]):
                    return False

                for temp_block in chain[c_len-100:]:
                    if(block['publisher']==temp_block['publisher']):
                        return False
                    
            if c_len==1:
                if(block['previous_hash']!=0):
                    return False
            else:
                if(block['previous_hash']!=self.hash(chain[c_len-2])):
                    return False
            c_len=c_len+1
        return True 

    
  

    def replace_chain(self):
        status=False
        for node in self.node_address:

            response=requests.get(f'http://{node}/get_chain')
            chain=response.json()['chain']
            chain_len=response/json()['length']
            if chain_len>self.length():
                if self.is_chain_valid(chain):
                    self.chain=chain
                    self.added=self.chain[-1]
                    status=True

        return status 
            




    

    ####### verify certufication authencity ##############

    def verify(self,block_hash,certificate_id):
        block_index=0
        for i in range(1,self.length()):
            if self.chain[i]['previous_hash']==block_hash:
                block_index=i-1
        if block_index==0:
            return False
        else:
            for i in self.chain[block_index]['certificates']:
                if i['id']==certificate_id:
                    return True
            return False


   





