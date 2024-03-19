import argparse
import random
import heapq
from peer import peer
from block import block
import uuid
from connect_graph import connect_graph
from handle_events_queue import handle_events_queue
from peer_utils import traverse
from peer_utils import find_longest_chain, execute_transactions
import copy
from visualize_tree import visualize_tree

# Generates peers
def generate_peer_set(total_peers, z0_percent, z1_percent):
    peers_set = [i for i in range(0, total_peers)]
    z0_peers_set = random.sample(peers_set, int(z0_percent * total_peers / 100))
    z1_peers_set = random.sample(peers_set, int(z1_percent * total_peers / 100))
    return peers_set, z0_peers_set, z1_peers_set

def main():
    parser = argparse.ArgumentParser(description='P2P cryptocurrency network Simulator')
    # Total Peers
    parser.add_argument('--total_peers', type=int, default=100, help='Total number of peers')
    # Percentage of Slow peers
    parser.add_argument('--z0_percent', type=float, default=50.0, help='z0 percent (slow peers percent)')
    # Percentage of low cpu peers
    parser.add_argument('--z1_percent', type=float, default=50.0, help='z1 percent (low cpu peers percent)')
    # mean time for interarrival of transactions (Tx) in milliseconds
    parser.add_argument('--Tx', type=int, default=2000, help='Mean Time for Exponential distribution of interarrival transaction times') 
    # mean time for interarrival of blocks (Tb) in milliseconds
    parser.add_argument('--Tb', type=int, default=6000, help='Mean Time for Exponential distribution of interarrival block times') 
    # observation period / simulator running period in milliseconds
    parser.add_argument('--To', type=int, default=240000, help='Total observation/simulation period')
    # Hashing power of Adversary-1
    parser.add_argument('--hp_adv1', type=float, default=30.0, help='X1 percent (Adversary 1 hashing power percent)') 
    # Hashing power of Adversary-2
    parser.add_argument('--hp_adv2', type=float, default=20.0, help='X2 percent (Adversary 2 hashing power percent)')
    
    args = parser.parse_args()
    peers_set, z0_peers_set, z1_peers_set = generate_peer_set(args.total_peers, args.z0_percent, args.z1_percent)

    all_peers = [] 

    # h = 1/(args.total_peers*(10 - 9*args.z1_percent/100))    # low CPU hashing power
    h = (100-args.hp_adv1-args.hp_adv2)/(args.total_peers*(1000-(9*args.z1_percent)))
    # args.total_peers += 2
    print(h)
    genesis_block_root_id = str(uuid.uuid4()) # block(str(uuid.uuid4()), None, self.id, 0)
    
    curr_total_hash = 0
    # Assign properties to each peer
    for peer_id in peers_set:
        is_z0 = not (peer_id in z0_peers_set)  # interpret 0 as slow and 1 as fast
        is_z1 = not (peer_id in z1_peers_set)  # interpret 0 as low and 1 as high
        hashing_power = 10 * h if is_z1 else h # hashing power
        curr_total_hash += hashing_power
        genesis_block = block(genesis_block_root_id, None, None, 0) # create genesis block
        all_peers.append(peer(0, peer_id, is_z0, hashing_power, args.Tb, copy.deepcopy(genesis_block)))
    
    genesis_block = block(genesis_block_root_id, None, None, 0) # create genesis block
    all_peers.append(peer(1, args.total_peers, True, args.hp_adv1/100, args.Tb, copy.deepcopy(genesis_block)))
    curr_total_hash += args.hp_adv1/100
    genesis_block = block(genesis_block_root_id, None, None, 0) # create genesis block
    all_peers.append(peer(2, args.total_peers+1, True, args.hp_adv2/100, args.Tb, copy.deepcopy(genesis_block)))
    curr_total_hash += args.hp_adv2/100

    print("curr_total_hash: ", curr_total_hash)

    args.total_peers += 2
    
    all_event_list = [] # This is a priority queue which keeps the events sorted based on time

    # Create mine block events for each peer at time 0
    # Generate all the transactions and push them into heap
    for peer_obj in all_peers:
        for event in peer_obj.generate_transaction_event_list(args.total_peers * args.Tx, args.total_peers, args.To):
            heapq.heappush(all_event_list, event)
        heapq.heappush(all_event_list, peer_obj.generate_mine_block_event(0))
    
    # Builds the peer network
    connect_graph(all_peers)
    # connect_node_to_graph(all_peers, args.total_peers)
    # connect_node_to_graph(all_peers, )

    # for peer_obj in all_peers:
    #     peer_obj.display_properties()
    
    # Handles each event in the queue
    handle_events_queue(all_event_list, all_peers, args)

    # Performs the BFS traversal on the tree
    def bfs(start_node, count):
        visited, queue = [], [start_node]
        while queue:
            current_node = queue.pop(0)
            count += 1
            BFS_list.append([current_node.id, [child.id for child in current_node.children]])
            if current_node not in visited:
                visited.append(current_node)
                queue.extend(current_node.children)  # Add unvisited neighbors to the queue
        return count
    
    # For any 5 peers print the information
    for j in range(5):
        
        i = random.randint(0,len(all_peers)-1)
        x = all_peers[i]

        print("Writing in file done for peer: ", i, flush = True)

        BFS_list = []
        count = 0
        y = bfs(x.genesis_block, count)

        # ------------Uncomment below lines to see the information -----------------------
        # print("Peer ", i, ": ", BFS_list, flush = True)
        # print("Total blocks in blockchain: ", y, flush = True)
        # --------------------------------------------------------------------------------------

        # ------------Uncomment below two lines to see the final balance -----------------------
        # final_longest_chain = find_longest_chain(all_peers[i].genesis_block)
        # print("Total blocks in longest chain: ", len(final_longest_chain))
        # print(f"All peer balance at peer {i}: ", execute_transactions(all_peers, final_longest_chain), flush = True)
        # --------------------------------------------------------------------------------------

        root_node = x.genesis_block
        visualize_tree(root_node, i, args.total_peers)

        with open(f'BFS_of_blockchain/peer_{i}.txt', 'w') as file:
            for line in BFS_list:
                file.write(str(line) + '\n')


    #------------Uncomment below lines to see the information written in report--------------------------
            
    # final_longest_chain = find_longest_chain(all_peers[i].genesis_block)
    # print("Longest chain size: ", len(final_longest_chain))

    # slow_fast_lc = [[0,0],[0,0]]
    
    # for blk in final_longest_chain:
    #     if blk.miner_id is not None:
    #         miner = all_peers[blk.miner_id]
    #         slow_fast_lc[miner.speed][miner.cpu] += 1
    
    # slow_fast_total =  [[0,0],[0,0]]
    # branch = []

    # longest_chain_id = [c.id for c in final_longest_chain]
    
    # def dfs(node, count):
    #     if not node:
    #         return

    #     if node.miner_id is not None:
    #         miner = all_peers[node.miner_id]
    #         slow_fast_total[miner.speed][miner.cpu] += 1

    #     if not node.children:
    #         branch.append(count)

    #     for child in node.children:
    #         if child.id in longest_chain_id:
    #             dfs(child, 0)
    #         else:
    #             dfs(child, count + 1)

    # dfs(all_peers[0].genesis_block, 0)

    # dic = {
    #     0: {
    #         0: "Low Speed, Low CPU",
    #         1: "Low Speed, High CPU",
    #     },
    #     1: {
    #         0: "High Speed, Low CPU",
    #         1: "High Speed, High CPU",
    #     },
    # }

    # if slow_fast_total[0][0] != 0:
    #     print(f"{dic[0][0]} - Longest chain: {slow_fast_lc[0][0]}, Total: {slow_fast_total[0][0]}, Ratio: {round(float(slow_fast_lc[0][0]) / slow_fast_total[0][0],2)}")
    # else:
    #     print(f"{dic[0][0]} - Longest chain: {slow_fast_lc[0][0]}, Total: {slow_fast_total[0][0]}, Ratio: No Blocks")
    # if slow_fast_total[0][1] != 0:  
    #     print(f"{dic[0][1]} - Longest chain: {slow_fast_lc[0][1]}, Total: {slow_fast_total[0][1]}, Ratio: {round(float(slow_fast_lc[0][1]) / slow_fast_total[0][1],2)}")
    # else:
    #     print(f"{dic[0][1]} - Longest chain: {slow_fast_lc[0][1]}, Total: {slow_fast_total[0][1]}, Ratio: No Block")
    # if slow_fast_total[1][0] != 0:  
    #     print(f"{dic[1][0]} - Longest chain: {slow_fast_lc[1][0]}, Total: {slow_fast_total[1][0]}, Ratio: {round(float(slow_fast_lc[1][0]) / slow_fast_total[1][0],2)}")
    # else:
    #     print(f"{dic[1][0]} - Longest chain: {slow_fast_lc[1][0]}, Total: {slow_fast_total[1][0]}, Ratio: No Block")
    
    # if slow_fast_total[1][1] != 0:  
    #     print(f"{dic[1][1]} - Longest chain: {slow_fast_lc[1][1]}, Total: {slow_fast_total[1][1]}, Ratio: {round(float(slow_fast_lc[1][1]) / slow_fast_total[1][1],2)}")
    # else:
    #     print(f"{dic[1][1]} - Longest chain: {slow_fast_lc[1][1]}, Total: {slow_fast_total[1][1]}, Ratio: No Block")
    # branch.remove(0)

    # if len(branch) == 0:
    #     print(f"Branch: Total branches: 0, Max Branch length: 0, Min Branch length: 0, Average branch length: 0")
    # else:
    #     print(f"Branch: Total branches: {len(branch)}, Max Branch length: {max(branch)}, Min Branch length: {min(branch)}, Average branch length: {round(sum(branch)/len(branch),2)}")
    
    #-------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()