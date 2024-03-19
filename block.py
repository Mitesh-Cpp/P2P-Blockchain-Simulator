from peer_utils import find_longest_chain,execute_transactions
import uuid
class block:
    def __init__(self, block_id, prev_block_id, miner_id, creation_time):
        self.id = block_id
        self.prev_block_id = prev_block_id
        self.miner_id = miner_id # miner of the block
        self.creation_time = creation_time # block generation time
        self.children = []  # List of child blocks
        self.transactions = []  # List to store transactions

    def __lt__(self, other):
        # Define the less-than comparison
        return self.creation_time < other.creation_time

    def fill_block_with_transactions(self, miner_peer,all_peers, mining_start_time):
        # Get the transaction IDs in the longest chain
        longest_chain = find_longest_chain(miner_peer.genesis_block)
        
        # populate this list with all transactions in the longest chain
        longest_chain_transaction_ids = []
        for block in longest_chain:
            for transaction in block.transactions:
                longest_chain_transaction_ids.append(transaction[2])
                
        # Verify and add transactions to the block
        transactions_to_add = []
        
        # Get the updated balance of the longest chain
        exec_balance = execute_transactions(all_peers,longest_chain)
        
        # Coinbase Transaction
        transactions_to_add.append([mining_start_time, "transaction_propogate_event", str(uuid.uuid4()), "COINBASE", miner_peer.id, 50, miner_peer.id, miner_peer.id])
        exec_balance[miner_peer.id] += 50

        # Iterate through each transaction in the trasaction pool
        for transaction_id in miner_peer.transaction_pool:
            transaction = miner_peer.transaction_dict[transaction_id]
            sender_id = transaction[3]
            rec_id = transaction[4]
            coins = transaction[5]

            # Add transactions to the block which are not in the longest chain
            # and which arrived in the pool before creation of the block
            if transaction_id not in longest_chain_transaction_ids:
                if(coins <= exec_balance[sender_id] and transaction[0] <= mining_start_time):
                    transactions_to_add.append(list(transaction))
                    exec_balance[sender_id] -= coins
                    exec_balance[rec_id] += coins

            # Check if the block has reached the maximum allowed transactions
            if len(transactions_to_add) == 1000:
                break
        
        # Add transactions to the block
        for transaction in transactions_to_add:
            self.transactions.append(transaction)
