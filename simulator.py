import argparse
import random
import csv
import heapq
from peer import peer
from connect_graph import connect_graph
from handle_events_queue import handle_events_queue

def generate_peer_set(total_peers, z0_percent, z1_percent):
    peers_set = [i for i in range(1, total_peers + 1)]
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
    parser.add_argument('--Tx', type=int, default=400, help='Mean Time for Exponential distribution of interarrival transaction times') 
    # mean time for interarrival of blocks (Tb) in seconds
    parser.add_argument('--Tb', type=int, default=600000, help='Mean Time for Exponential distribution of interarrival block times') 
    # observation period / simulator running period
    parser.add_argument('--To', type=int, default=100000000, help='Total observation/simulation period') 
    
    args = parser.parse_args()
    peers_set, z0_peers_set, z1_peers_set = generate_peer_set(args.total_peers, args.z0_percent, args.z1_percent)

    all_peers = [] 

    h = 1/(args.total_peers*(10 - 9*args.z1_percent/100))    # low CPU hashing power
    for peer_id in peers_set:
        is_z0 = not (peer_id in z0_peers_set)  # interpret 0 as slow and 1 as fast
        is_z1 = not (peer_id in z1_peers_set)  # interpret 0 as low and 1 as high
        hashing_power = 10 * h if is_z1 else h
        all_peers.append(peer(peer_id, args.total_peers, is_z0, is_z1, args.initial_balance, hashing_power))

    all_event_list = [] # This is a priority queue which keeps the events sorted based on time

    counter = 0
    for peer_obj in all_peers:
        heapq.heappush(all_event_list, peer_obj.generate_transaction_event(args.total_peers * args.Tx,
                                                                            args.total_peers, args.initial_balance, args.To))
        heapq.heappush(all_event_list, peer_obj.generate_mine_block_event(0))
    
    csv_file_path = "output_events.csv"
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for element in heapq.merge(*all_event_list, key=lambda x: x[1]):
            writer.writerow(element)

    connect_graph(all_peers)
    for peer_obj in all_peers:
        peer_obj.display_properties()
    handle_events_queue(all_event_list, all_peers)

if __name__ == "__main__":
    main()