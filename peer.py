import random
import uuid
import numpy as np
from block import block

class peer:
    def __init__(self, peer_id, total_peers, speed, cpu, initial_balance, hashing_power):
        self.id = peer_id
        self.all_peers_balance = {peer: initial_balance for peer in range(1, total_peers + 1)}
        self.speed = speed  # 0 -> slow, 1 -> fast
        self.cpu = cpu  # 0 -> low, 1 -> high
        self.hashing_power = hashing_power
        self.connected_nodes = []
        self.transaction_pool = []
        self.genesis_block_root = block(str(uuid.uuid4()), None, self.id, 0)

    def display_properties(self):
        print("-----------")
        print("ID:", self.id)
        print("Balance:", self.all_peers_balance[self.id])
        print("Speed:", "fast" if self.speed else "slow")
        print("CPU:", "high" if self.cpu else "low")
        print("Hashing Power:", self.hashing_power)
        print("Connected Nodes:", self.connected_nodes)
        print("-----------")

    def generate_transaction_event(self, Tx, total_peers, initial_balance, To):
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
                transaction_event_list.append(["generate_transaction_event", int(current_time), transaction_id, self.id, recipient_id, coins])
            else:
                break
        return transaction_event_list

    def generate_mine_block_event(self, time):
        current_time = time
        mine_block_event = []
        mine_block_event.append(["mine_block_event", int(current_time), self.id])
        return mine_block_event

    def calculate_latency(self, recipient_id, message_length):
        # returns latency in milliseconds, takes message_length in bits
        link_speed = 100000 if self.speed and recipient_id.speed else 5000
        propagation_delay = random.uniform(10, 500)  # Random value between 10ms and 500ms
        queuing_delay = np.random.exponential(scale=96000000/link_speed)
        latency = propagation_delay + message_length / link_speed + queuing_delay
        return latency

