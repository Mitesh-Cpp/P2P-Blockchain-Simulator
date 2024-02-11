import heapq
from block import block
import peer_utils
import numpy as np
import uuid
from peer_utils import find_longest_chain, block_present, verify_all_transactions, add_block_to_tree, perform_transactions, calculate_latency
# from simulator import args

def handle_events_queue(all_event_list, all_peers, args):

    block_generation_time_tracking = []
    low_cpu_avg_tracking = [0]
    high_cpu_avg_tracking = [0]
    def average_difference(lst):
    # Check if the list has at least two elements
        if len(lst) < 2:
            raise ValueError("List must have at least two elements")

        # Calculate the differences between consecutive elements
        differences = [lst[i+1] - lst[i] for i in range(len(lst)-1)]

        # Calculate the average of the differences
        average_diff = sum(differences) / len(differences)

        return average_diff

    def handle_block_propogate_event(all_peers, current_event):

        sender_idx = current_event[3]
        current_time = current_event[0]
        block_mining_start_time = current_event[5]

        if current_event[2].miner_id == sender_idx:
            if block_mining_start_time < all_peers[sender_idx].latest_mine_block_event_time:
                return
            # longest_chain_last_block_id = find_longest_chain(all_peers[sender_idx].genesis_block)[-1].id
            # if current_event[2].prev_block_id != longest_chain_last_block_id:
            #     return
        # first check if the block is valid. If not, drop it
        # print(current_event[2].id)
        # if not(block_present(all_peers[sender_idx], current_event[2])):
            # print("yoyo")

        if not(block_present(all_peers[sender_idx], current_event[2])) and verify_all_transactions(all_peers, all_peers[sender_idx], current_event[2]):
            # all_peers[sender_idx].all_peers_balance[current_event[2].miner_id] += 50
            add_block_to_tree(all_peers[sender_idx], current_event[2])
            
            new_longest_chain_length = len(find_longest_chain(all_peers[sender_idx].genesis_block))

            if new_longest_chain_length > all_peers[sender_idx].previous_longest_chain_length:
                heapq.heappush(all_event_list, all_peers[sender_idx].generate_mine_block_event(current_event[0]))
                all_peers[sender_idx].latest_mine_block_event_time = current_event[0]
                all_peers[sender_idx].previous_longest_chain_length += 1

            # if last_block_id != last_block_id_after_new_block:
                # all_peers[sender_idx].latest_mine_block_event_time = current_event[0]

            # perform_transactions(all_peers[sender_idx], current_event[2])
            for nbr in all_peers[sender_idx].connected_nodes:
                time = current_event[0] + calculate_latency(all_peers, sender_idx, nbr, (1 + len(current_event[2].transactions))*8*1000)
                # if time <= args.To:
                heapq.heappush(all_event_list, all_peers[nbr].generate_block_propagate_event(current_event[2], time, nbr, block_mining_start_time))
    
    def handle_transaction_propogate_event(all_peers, current_event):
        current_peer = all_peers[current_event[7]]
        current_time = current_event[0]
        txn_id = current_event[2]
        txn_sender_id = current_event[3]
        txn_receiver_id = current_event[4]
        coins = current_event[5]

        if tuple(current_event) in current_peer.transaction_pool:
            # print("Rejected Txn Prop! Already in Txn Pool")
            return
        # for transaction in current_peer.transaction_pool:
        #     transaction_id = transaction[2]
        #     # print("checking Txn: ", transaction_id, flush=True)
        #     if transaction_id == current_event[2]:
        #         # print("Rejected Txn Prop! Already in Txn Pool")
        #         return
        # print("Passed----------------------------------------")
        # current_peer.transaction_pool.append(current_event)
        current_peer.transaction_pool.add(tuple(current_event))
        # print(len(current_peer.transaction_pool))
        # print("NIGGER::",len(current_peer.transaction_pool))
        
        for nbr in current_peer.connected_nodes:
            # print("current Node: ", current_peer.id, "nbr: ", nbr)
            latency = calculate_latency(all_peers, current_peer.id, nbr, 8000)                
            heapq.heappush(all_event_list, [current_time + latency, "transaction_propogate_event", txn_id, txn_sender_id, txn_receiver_id, coins, current_peer.id,  nbr])

    def handle_generate_transaction_event(all_peers, current_event):
        current_time = current_event[0]
        txn_id = current_event[2]
        txn_sender_id = current_event[3]
        txn_receiver_id = current_event[4]
        coins = current_event[5]
        heapq.heappush(all_event_list, [current_time, "transaction_propogate_event", txn_id, txn_sender_id, txn_receiver_id, coins, txn_sender_id, txn_sender_id])
        return
        # Implement handling of transaction event
    def handle_mine_block_event(all_peers, current_event):
        creator_idx = current_event[2]  # Assuming event_data contains the creator's index
        current_time = current_event[0]
        Tb = current_event[3]
        longest_chain = find_longest_chain(all_peers[creator_idx].genesis_block)
        prev_block_id = longest_chain[-1].id if longest_chain else None
        random_time = int(np.random.exponential(scale=(1.0*Tb)/all_peers[creator_idx].hashing_power))
        block_generation_time = current_time + random_time
        # if(all_peers[creator_idx].cpu):
        #     high_cpu_avg_tracking.append(random_time)
        # else:
        #     low_cpu_avg_tracking.append(random_time)
        new_block = block(str(uuid.uuid4()), prev_block_id, all_peers[creator_idx].id, int(block_generation_time))
        
        # print("Nigga generated a block at: ", int(block_generation_time))
        # block_generation_time_tracking.append(int(block_generation_time))
        # Select maximum 999 transactions from the transaction pool and put them into the block
        new_block.fill_block_with_transactions(all_peers[creator_idx],all_peers, current_time)
        # all_peers[creator_idx].latest_mine_block_event_time = block_generation_time

        # new_block.transactions.extend(transactions_to_add)
        # all_peers[creator_idx].balance += 50
        # Add the new block to the blockchain


        # if longest_chain:
        #     longest_chain[-1].children.append(new_block)

        # Propagate the new block event
        # print("here2")
        # print(type(all_peers[creator_idx].generate_block_propagate_event(new_block, block_generation_time, creator_idx)))
        if block_generation_time <= args.To:
            heapq.heappush(all_event_list, all_peers[creator_idx].generate_block_propagate_event(new_block, block_generation_time, creator_idx, current_time))
    # xxx=0
    while all_event_list:
        current_event = heapq.heappop(all_event_list)
        print(current_event)
        event_type = current_event[1]
        # print(xxx)
        # xxx+=1
        # print("len is ",len(all_event_list))
        # Perform operations based on the event type
        if event_type == "generate_transaction_event":
            handle_generate_transaction_event(all_peers, current_event)
        elif event_type == "mine_block_event":
            handle_mine_block_event(all_peers, current_event)
        elif event_type == "block_propagate_event":
            handle_block_propogate_event(all_peers, current_event)
        elif event_type == "transaction_propogate_event":
            handle_transaction_propogate_event(all_peers, current_event)
        # Add more conditions for other event types if needed
    # block_generation_time_tracking = sorted(block_generation_time_tracking)
    # print(average_difference(block_generation_time_tracking))
    # high_cpu_avg_tracking = sorted(high_cpu_avg_tracking)
    # print(int(average_difference(high_cpu_avg_tracking)))
    # print(high_cpu_avg_tracking)
    # low_cpu_avg_tracking = sorted(low_cpu_avg_tracking)
    # print(int(average_difference(low_cpu_avg_tracking)))



    