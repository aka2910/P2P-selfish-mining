class Transaction:
    """
    A transaction is a transfer of coins from one user to another.
    """
    def __init__(self, id, sender, receiver, amount, timestamp) -> None:
        """
        :param id: The id of the transaction
        :param sender: The sender of the transaction (who is paying)
        :param receiver: The receiver of the transaction (who is receiving)
        :param amount: The amount of coins transferred
        :param timestamp: The time of the transaction
        """
        # Assume that sender and receiver are ids
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp

    def __str__(self):
        output = f"{self.id}: {self.sender.id} pays {self.receiver.id} {self.amount} coins"
        return output