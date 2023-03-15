import argparse
import simpy
import time
from peer import Peer
from block import Block
from network import Network
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P currency simulator")
    parser.add_argument("--n", type=int, default=10, help="Number of peers")
    parser.add_argument("--z0", type=float, default=0.5, help = "percent of slow peers")
    parser.add_argument("--z1", type=float, default=0.5, help = "percent of low CPU peers")
    parser.add_argument("--Ttx", type=float, default=0.5, help = "mean interarrival time of transactions")
    parser.add_argument("--time", type=float, default=100, help = "simulation time")
    parser.add_argument("--I", type=float, default=0.5, help = "mean interarrival time of blocks")

    args = parser.parse_args()

    env = simpy.Environment()  # simulated in simpy
    genesis = Block(None, 0, set([]), -1) # genesis block

    num_slow = int(args.n*args.z0)
    slow_peers = random.sample(range(args.n+1), num_slow)
    
    num_low = int(args.n*args.z1)
    low_peers = random.sample(range(args.n+1), num_low)

    # Generate the peers
    peers = []
    for i in range(args.n):
        config = {}
        if i in slow_peers:
            config["speed"] = "slow"
        else:
            config["speed"] = "fast"

        if i in low_peers:
            config["cpu"] = "low"
            config["hashing power"] = 1/(10*args.n - 9*num_low) # 1/10 of the hashing power of a high CPU peer
        else:
            config["cpu"] = "high"
            config["hashing power"] = 10/(10*args.n - 9*num_low) # 10 times the hashing power of a low CPU peer

        p = Peer(i, genesis, env, config)
        peers.append(p)
        genesis.balances = {i: 0 for i in range(args.n)}

    # Generate the network
    network = Network(peers, args.I, env)

    for peer in peers:
        peer.use_network(network)
        env.process(peer.generate_transactions(args.Ttx, peers))
        if random.random() < 0.25:
            env.process(peer.create_block())

    env.run(until=args.time)

    # time.sleep(10)
    for peer in peers:
        longest_chain = peer.longest_chain.height
        peer.print_tree(f"plots_{args.n}_{args.z0}_{args.z1}_{args.Ttx}_{args.I}_{args.time}/tree_{peer.id}_{longest_chain}.dot")
        peer.save_tree(f"trees_{args.n}_{args.z0}_{args.z1}_{args.Ttx}_{args.I}_{args.time}/tree_{peer.id}_{longest_chain}.tree")

# python3 run.py --n 50 --z0 0.8 --z1 0.3 --Ttx 1 --I 1 --time 1000