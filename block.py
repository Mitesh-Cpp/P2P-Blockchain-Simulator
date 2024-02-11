from peer_utils import find_longest_chain,execute_transactions
import uuid
class block:
    def __init__(self, block_id, prev_block_id, miner_id, creation_time):
        self.id = block_id
        self.prev_block_id = prev_block_id
        self.miner_id = miner_id
        self.creation_time = creation_time
        self.children = []  # List of child blocks
        self.transactions = []  # List to store transactions

    def __lt__(self, other):
        # Define the less-than comparison
        return self.creation_time < other.creation_time
    
    # def __repr__(self):
    #     print("BLOCK ::"+str(self.id))

    # def add_transaction()

    def fill_block_with_transactions(self, miner_peer,all_peers, mining_start_time):
        # Get the transaction IDs in the longest chain
        longest_chain = find_longest_chain(miner_peer.genesis_block)
        # print("Current block: ", self.id, "Prev id: ", self.prev_block_id)
        # print("Longest Chain size: ", len(longest_chain))
        # print("Miner ID", miner_peer.id)
        longest_chain_transaction_ids = []
        for block in longest_chain:
            for txn in block.transactions:
                longest_chain_transaction_ids.append(txn[2])
                
        # print(longest_chain_transaction_ids)
        # print("Txns in longest chain length: ", len(longest_chain_transaction_ids))
        
        # Verify and add transactions to the block
        transactions_to_add = []
        transactions_to_remove = set()
        
        exec_balance = execute_transactions(all_peers,longest_chain)
        
        # Coinbase Transaction
        transactions_to_add.append([mining_start_time, "transaction_propogate_event", str(uuid.uuid4()), "COINBASE", miner_peer.id, 50, miner_peer.id, miner_peer.id])
        exec_balance[miner_peer.id] += 50

        # print("Miner Txn Pool size: ", len(miner_peer.transaction_pool))
        for transaction_id in miner_peer.transaction_pool:
            transaction = miner_peer.transaction_dict[transaction_id]

            sender_id = transaction[3]
            rec_id = transaction[4]
            coins = transaction[5]
            if transaction_id not in longest_chain_transaction_ids:
                if(coins <= exec_balance[sender_id] and transaction[0] <= mining_start_time):
                    transactions_to_add.append(list(transaction))
                    transactions_to_remove.add(transaction_id)
                    exec_balance[sender_id] -= coins
                    exec_balance[rec_id] += coins

            # Check if the block has reached the maximum allowed transactions
            if len(transactions_to_add) == 1000:
                break
        
        # Add transactions to the block
        for transaction in transactions_to_add:
            self.transactions.append(transaction)
            # self.add_transaction(transaction)

        # print("Txns inside block: ", len(self.transactions))
        
        # Remove transactions from the transaction pool
        # miner_peer.transaction_pool[:] = [txn for txn in miner_peer.transaction_pool if txn[2] not in transactions_to_remove]
