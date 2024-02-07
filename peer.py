import random
import uuid
import numpy as np
from block import block

class peer:
    def __init__(self, peer_id, total_peers, speed, cpu, initial_balance, hashing_power, Tb, genesis_block):
        self.id = peer_id
        self.all_peers_balance = {peer: initial_balance for peer in range(0, total_peers)}
        self.speed = speed  # 0 -> slow, 1 -> fast
        self.cpu = cpu  # 0 -> low, 1 -> high
        self.hashing_power = hashing_power
        self.connected_nodes = []
        self.transaction_pool = []
        self.genesis_block = genesis_block
        self.Tb = Tb

    def display_properties(self):
        print("-----------")
        print("ID:", self.id)
        print("Balance:", self.all_peers_balance[self.id])
        print("Speed:", "fast" if self.speed else "slow")
        print("CPU:", "high" if self.cpu else "low")
        print("Hashing Power:", self.hashing_power)
        print("Connected Nodes:", self.connected_nodes)
        print("-----------")

    def generate_block_propagate_event(self, block, block_generation_time, receiver_peer_idx):
        return [int(block_generation_time), "block_propagate_event", block, receiver_peer_idx]
        # print(type(block_propagate_event))
        # return block_propagate_event

    def generate_transaction_event_list(self, Tx, total_peers, initial_balance, To):
        transaction_event_list = []  # [["transaction_event", time, TxnId, IDx, IDy, C], [], [], ...]
        current_time = 0
        while current_time < To:
            transaction_id = str(uuid.uuid4())
            recipient_id = random.randint(1, total_peers) 
            coins = random.randint(1, initial_balance)
            # Generate exponential distribution for interarrival times
            interarrival_time = np.random.exponential(scale=Tx)
            current_time += interarrival_time
            if current_time < To:
                transaction_event_list.append([int(current_time), "generate_transaction_event", transaction_id, self.id, recipient_id, coins])
            else:
                break
        # print(transaction_event_list)
        return transaction_event_list

    def generate_mine_block_event(self, time):
        current_time = time
        mine_block_event = [int(current_time), "mine_block_event", self.id, self.Tb]
        return mine_block_event