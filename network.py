import random 

class Network:
    """
    Network class that contains that handles the propagtions of transactions and blocks
    """
    def __init__(self, peers, adv, interarrival, adv_conn, env) -> None:
        """
        peers: list of peers in the network
        adversary: the adversary peer
        interarrival: interarrival time of transactions
        env: simpy environment
        """
        self.peers = peers
        self.adv = adv
        self.peer_ids = []
        self.adv_id = adv.id
        self.interarrival = interarrival
        
        # Unnormalized percentage
        self.adv_conn = adv_conn

        for i in range(len(self.peers)):
            self.peer_ids.append(self.peers[i].id)

        self.generate_network()
        self.check_graph()
        self.init_properties()

        self.env = env

    def generate_network(self):
        """
        Generate a random network with 4 neighbors for each peer 
        Fully connected graph
        """
        for peer in self.peers:
            num_neighbors = random.randint(4, 8)
            num_neighbors = min(num_neighbors, len(self.peers))

            temp_list = list(set(self.peers.copy()) - set([peer]))
            neighbors = random.sample(temp_list, num_neighbors)

            for n in neighbors:
                peer.add_neighbor(n)
                n.add_neighbor(peer)

        adv_neighbors = random.sample(range(len(self.peers)), (int) (self.adv_conn*len(self.peers)//100))

        print("Neighbors of adversary:", adv_neighbors)

        for i in adv_neighbors:
            self.peers[i].add_neighbor(self.adv)
            self.adv.add_neighbor(self.peers[i])

    def check_graph(self):
        # check if the graph is connected
        # if not, connect the graph

        # Check this implementation again
        # Adversary behaves just as the last of the peers
        visited = [False for i in range(len(self.peers)+1)]

        def dfs(node):
            visited[node.id] = True
            for n in node.neighbors:
                if not visited[n.id]:
                    dfs(n)
        dfs(self.peers[0])
        connected = True

        for i in range(len(visited)):
            if not visited[i]:
                connected = False

        print("connected: ", connected)

        if not connected:
            # connect the graph
            num_peers = len(self.peers)
            for i in range(num_peers):
                peer = self.peers[i]
                peer.disconnect_peer()

                for j in range(4):
                    peer.add_neighbor(self.peers[(i+j-2)%num_peers])
                    peer.add_neighbor(self.peers[(i+j-1)%num_peers])
                    peer.add_neighbor(self.peers[(i+j+1)%num_peers])
                    peer.add_neighbor(self.peers[(i+j+2)%num_peers])

    def init_properties(self):
        """
        Init the propagation delay, computation delay, and queueing delay for each peer pair
        """
        temp_peers = self.peers + [self.adv]

        self.p = [[0 for i in range(len(temp_peers))] for j in range(len(temp_peers))]
        self.c = [[0 for i in range(len(temp_peers))] for j in range(len(temp_peers))]
        self.d = [[None for i in range(len(temp_peers))] for j in range(len(temp_peers))]

        for i in range(len(temp_peers)):
            for j in range(len(temp_peers)):
                if i == j:
                    self.p[i][j] = 0
                    self.c[i][j] = 0
                    self.d[i][j] = None
                else:
                    # Init the propagation delay
                    val = self.p[j][i]
                    
                    # In ms
                    if val != 0:
                        self.p[i][j] = val
                    else:
                        r = random.randint(10, 500)
                        self.p[i][j] = r

                    # Init the computation delay
                    speed_i = temp_peers[i].speed
                    speed_j = temp_peers[j].speed

                    # In Mbps
                    if speed_i == 'fast' and speed_j == 'fast':
                        self.c[i][j] = 100
                    else:
                        self.c[i][j] = 5

                    # Init the queueing delay
                    # In ms
                    if self.d[j][i] is not None:
                        self.d[i][j] = self.d[j][i]
                    else:
                        self.d[i][j] = random.expovariate

    def send_transaction(self, sender, receiver, transaction):
        """
        Send and recieve a transaction from sender to receiver with latency
        """
        # print("Send transaction from", sender.id, "to", receiver.id)
        # Each transaction is 1KB = 8Kb
        latency = self.p[sender.id][receiver.id] + 8/self.c[sender.id][receiver.id] + self.d[sender.id][receiver.id](self.c[sender.id][receiver.id]/96)
        # print("Latency:", latency)

        yield self.env.timeout(latency)
        yield self.env.process(receiver.receive_transaction(sender, transaction))

    def send_block(self, sender, receiver, block):
        """
        Send and recieve a block from sender to receiver with latency
        """
        latency = self.p[sender.id][receiver.id] + block.size/self.c[sender.id][receiver.id] + self.d[sender.id][receiver.id](self.c[sender.id][receiver.id]/96)
        yield self.env.timeout(latency)
        yield self.env.process(receiver.receive_block(sender,block))
        print("Block received by", receiver.id)