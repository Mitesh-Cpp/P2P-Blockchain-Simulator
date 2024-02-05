import heapq
from block import block
import peer_utils
import numpy as np
import uuid
from peer_utils import find_longest_chain, block_present, verify_all_transactions, add_block_to_tree, perform_transactions, calculate_latency


def handle_events_queue(all_event_list, all_peers):

    block_generation_time_tracking = []
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
        # print("here")
        sender_idx = current_event[3]
        # first check if the block is valid. If not, drop it
        # print(current_event[2].id)
        # if not(block_present(all_peers[sender_idx], current_event[2])):
            # print("yoyo")
        if not(block_present(all_peers[sender_idx], current_event[2])) and verify_all_transactions(all_peers[sender_idx], current_event[2]):
            all_peers[sender_idx].all_peers_balance[current_event[2].miner_id] += 50
            add_block_to_tree(all_peers[sender_idx], current_event[2])
            perform_transactions(all_peers[sender_idx], current_event[2])
            for nbr in all_peers[sender_idx].connected_nodes:
                # print("here1")
                # print(type(all_peers[nbr-1].generate_block_propagate_event(current_event[2], current_event[0] + calculate_latency(all_peers, sender_idx, nbr-1, (1 + len(current_event[2].transactions))*8*1000), nbr-1)))
                print("Transfer Latency: ", calculate_latency(all_peers, sender_idx, nbr, (1 + len(current_event[2].transactions))*8*1000))
                heapq.heappush(all_event_list, all_peers[nbr].generate_block_propagate_event(current_event[2], current_event[0] + calculate_latency(all_peers, sender_idx, nbr, (1 + len(current_event[2].transactions))*8*1000), nbr))


    def handle_generate_transaction_event(all_peers, current_event):
        return
        # Implement handling of transaction event
    def handle_mine_block_event(all_peers, current_event):
        creator_idx = current_event[2]  # Assuming event_data contains the creator's index
        current_time = current_event[0]
        Tb = current_event[3]
        longest_chain = find_longest_chain(all_peers[creator_idx].genesis_block)
        prev_block_id = longest_chain[-1].id if longest_chain else None
        # print("prev_block_id")
        # print(prev_block_id)
        block_generation_time = current_time + np.random.exponential(scale=Tb/all_peers[creator_idx].hashing_power)
        new_block = block(str(uuid.uuid4()), prev_block_id, all_peers[creator_idx].id, int(block_generation_time))
        # print("Nigga generated a block at: ", int(block_generation_time))
        block_generation_time_tracking.append(int(block_generation_time))
        # Select maximum 999 transactions from the transaction pool and put them into the block
        new_block.fill_block_with_transactions(all_peers[creator_idx])
        # new_block.transactions.extend(transactions_to_add)
        # all_peers[creator_idx].balance += 50
        # Add the new block to the blockchain


        # if longest_chain:
        #     longest_chain[-1].children.append(new_block)

        # Propagate the new block event
        # print("here2")
        # print(type(all_peers[creator_idx].generate_block_propagate_event(new_block, block_generation_time, creator_idx)))
        print()
        heapq.heappush(all_event_list, all_peers[creator_idx].generate_block_propagate_event(new_block, block_generation_time, creator_idx))

    while all_event_list:
        current_event = heapq.heappop(all_event_list)
        print(current_event)
        event_type = current_event[1]
        # print(current_event)

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
    block_generation_time_tracking = sorted(block_generation_time_tracking)
    print(average_difference(block_generation_time_tracking))

    