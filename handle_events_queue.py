import heapq
from block import block
from peer_utils import find_longest_chain
import numpy as np
import uuid

def handle_events_queue(all_event_list, all_peers):

    def handle_generate_transaction_event(all_peers, current_event):
        return
        # Implement handling of transaction event
    def handle_mine_block_event(all_peers, current_event):
        creator_idx = current_event[2] - 1  # Assuming event_data contains the creator's index
        current_time = current_event[0]
        Tb = current_event[3]
        longest_chain = find_longest_chain(all_peers[creator_idx].genesis_block_root)
        prev_block_id = longest_chain[-1].id if longest_chain else None
        block_generation_time = current_time + np.random.exponential(scale=Tb * all_peers[creator_idx].hashing_power)
        new_block = block(str(uuid.uuid4()), prev_block_id, all_peers[creator_idx].id, block_generation_time)

        # Select maximum 999 transactions from the transaction pool and put them into the block
        new_block.fill_block_with_transactions(all_peers[creator_idx])
        # new_block.transactions.extend(transactions_to_add)

        # Add the new block to the blockchain
        if longest_chain:
            longest_chain[-1].children.append(new_block)

        # Propagate the new block event
        heapq.heappush(all_event_list, all_peers[creator_idx].generate_block_propagate_event(new_block, block_generation_time, creator_idx))

    while all_event_list:
        current_event = heapq.heappop(all_event_list)
        # print(current_event)
        event_type = current_event[1]
        print(event_type)

        # Perform operations based on the event type
        if event_type == "generate_transaction_event":
            handle_generate_transaction_event(all_peers, current_event)
        elif event_type == "mine_block_event":
            handle_mine_block_event(all_peers, current_event)
        elif event_type == "block_propogate_event":
            handle_block_propogate_event(all_peers, current_time)
        elif event_type == "transaction_propogate_event":
            handle_transaction_propogate_event(all_peers, current_time)
        # Add more conditions for other event types if needed

    