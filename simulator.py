import argparse
import random
import csv
import heapq
from peer import peer
from block import block
import uuid
from connect_graph import connect_graph
from handle_events_queue import handle_events_queue
from peer_utils import traverse

def generate_peer_set(total_peers, z0_percent, z1_percent):
    peers_set = [i for i in range(0, total_peers)]
    z0_peers_set = random.sample(peers_set, int(z0_percent * total_peers / 100))
    z1_peers_set = random.sample(peers_set, int(z1_percent * total_peers / 100))
    return peers_set, z0_peers_set, z1_peers_set

def main():
    parser = argparse.ArgumentParser(description='P2P cryptocurrency network Simulator')
    parser.add_argument('--total_peers', type=int, default=100, help='Total number of peers')
    parser.add_argument('--initial_balance', type=int, default=100, help='Initial balance for peers')
    parser.add_argument('--z0_percent', type=float, default=50.0, help='z0 percent (slow peers percent)')
    parser.add_argument('--z1_percent', type=float, default=50.0, help='z1 percent (low cpu peers percent)')
    # mean time for interarrival of transactions (Tx) in seconds
    parser.add_argument('--Tx', type=int, default=1000, help='Mean Time for Exponential distribution of interarrival transaction times') 
    # mean time for interarrival of blocks (Tb) in seconds
    parser.add_argument('--Tb', type=int, default=600000, help='Mean Time for Exponential distribution of interarrival block times') 
    # observation period / simulator running period
    parser.add_argument('--To', type=int, default=100000000, help='Total observation/simulation period') 
    
    args = parser.parse_args()
    peers_set, z0_peers_set, z1_peers_set = generate_peer_set(args.total_peers, args.z0_percent, args.z1_percent)

    all_peers = [] 

    h = 1/(args.total_peers*(10 - 9*args.z1_percent/100))    # low CPU hashing power
    print("Nigga2", h)
    genesis_block_root_id = str(uuid.uuid4()) # block(str(uuid.uuid4()), None, self.id, 0)
    for peer_id in peers_set:
        is_z0 = not (peer_id in z0_peers_set)  # interpret 0 as slow and 1 as fast
        is_z1 = not (peer_id in z1_peers_set)  # interpret 0 as low and 1 as high
        hashing_power = 10 * h if is_z1 else h
        print("Nigro ",hashing_power)
        genesis_block = block(genesis_block_root_id, None, None, 0)
        all_peers.append(peer(peer_id, args.total_peers, is_z0, is_z1, args.initial_balance, hashing_power, args.Tb, genesis_block))

    all_event_list = [] # This is a priority queue which keeps the events sorted based on time

    counter = 0
    for peer_obj in all_peers:
        for event in peer_obj.generate_transaction_event_list(args.total_peers * args.Tx,
                                                                            args.total_peers, args.initial_balance, args.To):
            heapq.heappush(all_event_list, event)
        heapq.heappush(all_event_list, peer_obj.generate_mine_block_event(0))
    
    connect_graph(all_peers)

    for peer_obj in all_peers:
        peer_obj.display_properties()
    
    handle_events_queue(all_event_list, all_peers)


    # all_peers[0].genesis_block.children = []
    # id1 = str(uuid.uuid4())
    # all_peers[0].genesis_block.children.append(block(id1, genesis_block_root_id, 0, 5224))
    # id_to_search = str(uuid.uuid4())
    # id2 = str(uuid.uuid4())
    # all_peers[0].genesis_block.children[0].children.append(block(id2, genesis_block_root_id, 0, 5254234))
    # all_peers[0].genesis_block.children[0].children.append(block(id_to_search, genesis_block_root_id, 0, 5254234))

    # traverse(all_peers[0], id_to_search)

    # print(genesis_block_root_id, id1, id_to_search, id2)

if __name__ == "__main__":
    main()