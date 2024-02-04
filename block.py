class block:
    def __init__(self, block_id, prev_block_id, miner_id, creation_time):
        self.id = block_id
        self.prev_block_id = prev_block_id
        self.miner_id = miner_id
        self.creation_time = creation_time
        self.children = []  # List of child blocks
        self.transactions = []  # List to store transactions

    def fill_block_with_transactions(self, transaction_pool, genesis_block):
        # Get the transaction IDs in the longest chain
        longest_chain_transaction_ids = find_longest_chain(genesis_block)
        for block in longest_chain:
            longest_chain_transaction_ids.update(transaction[2] for transaction in block.transactions)

        # Verify and add transactions to the block
        transactions_to_add = []
        transactions_to_remove = set()

        for transaction in transaction_pool:
            transaction_id = transaction[2]

            if transaction_id not in longest_chain_transaction_ids:
                transactions_to_add.append(transaction)
                transactions_to_remove.add(transaction_id)

                # Check if the block has reached the maximum allowed transactions
                if len(self.transactions) == 999:
                    break

        # Add transactions to the block
        for transaction in transactions_to_add:
            self.add_transaction(transaction)

        # Remove transactions from the transaction pool
        transaction_pool[:] = [txn for txn in transaction_pool if txn[2] not in transactions_to_remove]
