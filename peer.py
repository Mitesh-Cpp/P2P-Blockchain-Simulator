import random
import uuid
import numpy as np
from block import block
import copy

class peer:
    def __init__(self, nature, peer_id, speed, hashing_power, Tb, genesis_block):
        self.nature = nature  # 0 -> hones, 1 -> adv1, 2 -> adv2 
        self.id = peer_id
        self.speed = speed  # 0 -> slow, 1 -> fast
        self.hashing_power = hashing_power # hashing power of the peer
        self.connected_nodes = [] # Adjecent peers of the current peer
        self.transaction_pool = set()
        self.transaction_dict = {}
        self.genesis_block = genesis_block
        self.Tb = Tb
        self.latest_mine_block_event_time = 0 # Stores the latest mine block event time
        self.previous_longest_chain_length = 1 
        self.adv_state = 0
        self.private_chain = []
        self.wait_queue_set = set()


    def display_properties(self):
        print("-----------")
        print("Nature: ", end="")
        if self.nature == 0:
            print("honest")
        elif self.nature == 1:
            print("adv_1")
        else:
            print("adv_2")
        print("ID:", self.id)
        print("Speed:", "fast" if self.speed else "slow")
        # print("CPU:", "high" if self.cpu else "low")
        print("Hashing Power:", self.hashing_power)
        print("Connected Nodes:", self.connected_nodes)
        print("Genesis Block Address:", self.genesis_block)
        print("-----------")

    # Block propagate event
    def generate_block_propagate_event(self, block, block_generation_time, receiver_peer_idx, mining_start_time):
        return [int(block_generation_time), "block_propagate_event", copy.deepcopy(block), receiver_peer_idx, block.id, mining_start_time]

    # Generate all the trasactions and push them into heap
    def generate_transaction_event_list(self, Tx, total_peers, To):
        transaction_event_list = []  # [["transaction_event", time, TxnId, IDx, IDy, C], [], [], ...]
        current_time = 0
        while current_time < To / 2:
            transaction_id = str(uuid.uuid4())
            recipient_id = random.randint(0, total_peers-1) 
            coins = random.randint(1, 100)
            
            # Generate exponential distribution for interarrival times
            interarrival_time = np.random.exponential(scale=Tx)
            current_time += interarrival_time
            if current_time < To:
                transaction_event_list.append([int(current_time), "generate_transaction_event", transaction_id, self.id, recipient_id, coins])
            else:
                break
        return transaction_event_list

    # Generate mine block event
    def generate_mine_block_event(self, time):
        current_time = time
        mine_block_event = [int(current_time), "mine_block_event", self.id, self.Tb]
        return mine_block_event

    # Generate release private chain event
    def generate_release_private_chain_event(self, time, num_release_blocks):
        current_time = time
        release_private_chain_event = [int(current_time), "release_private_chain_event", self.id, num_release_blocks]
        return release_private_chain_event

    def generate_mine_on_private_block_event(self, time, block_to_mine_on):
        current_time = time
        mine_on_private_block_event = [int(current_time), "mine_on_private_block_event", self.id, self.Tb, block_to_mine_on]
        return mine_on_private_block_event