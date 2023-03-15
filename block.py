class Block:
    """
    A block is a collection of transactions that are validated together.
    """
    def __init__(self, prevblock, timestamp, transactions, userid):
        """
        prevblock: the previous (parent) block in the chain (None if genesis block)
        timestamp: the time the block was created
        transactions: a set of transactions in the block
        userid: the id of the user who mined the block
        balances: a dictionary of the balances of all users in the network
        """
        self.prevblock = prevblock
        self.timestamp = timestamp
        self.transactions = transactions
        self.userid = userid

        trans_string = ""
        for transaction in transactions:
            trans_string += str(transaction) + " "
        
        if prevblock == None:
            self.balances = {}
            self.height = 0
            self.blkid = hash(str(timestamp))
        else:
            self.balances = self.prevblock.balances.copy()
            self.height = self.prevblock.height + 1
            self.blkid = hash(str(prevblock.blkid) + str(timestamp) + str(trans_string) + str(userid))

        # Size in Kb
        self.size = 8*(len(transactions) + 1) # Each transaction is 1 KB = 8 Kb, +1 due to coinbase transaction

    def validate(self):
        """
        Validates the block by checking that the transactions are valid
        """
        balance_copy = self.balances.copy() #balance_copy shows cumulative balance after each transaction
        for t in self.transactions:
            if t.sender == t.receiver:
                return False
            if t.amount <= 0:
                return False
            if balance_copy[t.sender.id] < t.amount: # Check if the sender has enough coins
                return False
            balance_copy[t.sender.id] -= t.amount
            balance_copy[t.receiver.id] += t.amount
        self.balances = balance_copy

        self.balances[self.userid] += 50 # Reward for mining the block
        return True

    def get_all_transactions(self):
        """
        Returns a set of all transactions in the chain up to this block
        """
        if self.prevblock == None:
            return self.transactions
        return self.transactions.union(self.prevblock.get_all_transactions())
    
    def __str__(self):
        """
        Returns a string representation of the block
        """
        return self.blkid