import random
import numpy as np 

# finds longest chain from the genesis block and returns blocks in that path in a list
def find_longest_chain(root):
    def dfs(node, current_path):
        if not node:
            return current_path

        current_path.append(node)

        longest_path = current_path
        for child in node.children:
            child_path = dfs(child, current_path.copy())
            if len(child_path) > len(longest_path):
                longest_path = child_path

        return longest_path

    return dfs(root, [])

def calculate_latency(all_peers, sender_idx, recipient_idx, message_length):
    
    # returns latency in milliseconds, takes message_length in bits
    link_speed = 100000 if all_peers[sender_idx].speed and all_peers[recipient_idx].speed else 5000
    
    # Random value between 10ms and 500ms
    propagation_delay = random.uniform(10, 500)

    # Queuing delay  
    queuing_delay = np.random.exponential(scale=96000/link_speed)

    # Total Latency 
    latency = propagation_delay + message_length / link_speed + queuing_delay
    return int(latency)

def block_present(peer, block_to_check):
    # Verify whether the block is present in the peer's block tree by checking the block id
    block_id_to_check = block_to_check.id
    return find_block_by_id(peer.genesis_block, block_id_to_check) is not None

def find_block_by_id(current_block, block_id):
    # Recursively find the block with the given id in the block tree
    if current_block.id == block_id:
        return current_block

    for child_block in current_block.children:
        found_block = find_block_by_id(child_block, block_id)
        if found_block:
            return found_block

    return None

# Returns the path from genesis block to target block
def traverse(current_peer, target):
    final_path = []
    def dfs(node, current_path):
        if not node:
            return

        current_path.append(node)
        if node.id == target:
            final_path.extend(current_path)
            return

        for child in node.children:
            dfs(child, current_path)
            current_path.pop()

    
    dfs(current_peer.genesis_block, [])
    return final_path

# Execute all transactions in the given path, starting from genesis block
def execute_transactions(all_peers,path):
    initial_balance = [100] * len(all_peers)
    for block in path:
        for txn in block.transactions:
            s_id = txn[3]
            r_id = txn[4]
            Amount = txn[5]

            if s_id != "COINBASE":
                initial_balance[s_id] -= Amount
            initial_balance[r_id] += Amount
    return initial_balance

# Verify all transactions in the block, checking if the sender has enough balance
def verify_all_transactions(all_peers, peer, block_to_verify):
    
    # List down all the ancestors of the current block
    final_path = []
    if block_to_verify.prev_block_id != None:
        final_path = traverse(peer, block_to_verify.prev_block_id)
    
    # Execute all transactions from genesis block till the parent of the current block and return final balance
    updated_balance = execute_transactions(all_peers, final_path)
    
    # Start verifying current block with the updated balances
    for transaction in block_to_verify.transactions:
        sender_id = transaction[3]
        recipient_id = transaction[4]
        amount = transaction[5]

        # Coinbase transaction, only receiver's balances gets updated.
        if sender_id == "COINBASE":
            updated_balance[recipient_id] += amount
        else:    
            # Check if the sender has enough balance for the transaction
            if updated_balance[sender_id] < amount:
                return False # Block rejected.
            
            # Update balances by executing current transaction
            updated_balance[sender_id] -= amount
            updated_balance[recipient_id] += amount
    return True

def add_block_to_tree(peer, new_block):
    # Add the given block to the peer's block tree
    prev_block_id = new_block.prev_block_id

    # Find the parent block with the given prev_block_id
    parent_block = find_block_by_id(peer.genesis_block, prev_block_id)

    if parent_block:
        parent_block.children.append(new_block)