import os, shutil
import argparse
import simpy
import time
from peer import Peer
from selfish_peer import SelfishPeer
from block import Block
from network import Network
import random
import params

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P2P currency simulator")
    parser.add_argument("--n", type=int, default=10, help="Number of peers")
    parser.add_argument("--z1", type=float, default=0.5, help = "fraction of low CPU peers")
    parser.add_argument("--Ttx", type=float, default=0.5, help = "mean interarrival time of transactions")
    parser.add_argument("--time", type=float, default=100, help = "simulation time")
    parser.add_argument("--I", type=float, default=0.5, help = "mean interarrival time of blocks")
    parser.add_argument("--h", type=float, default=0.5, help = "hashing power of the adversary")
    parser.add_argument("--Z", type=float, default=50, help = "percentage of honest nodes connected to the adversary")

    args = parser.parse_args()

    # Generating only the honest peers here and the adversary will be added later
    n = args.n - 1

    env = simpy.Environment()  # simulated in simpy
    genesis = Block(None, 0, set([]), -1) # genesis block
    
    num_slow = int(n//2)
    slow_peers = random.sample(range(n), num_slow)
    
    num_low = int(n*args.z1)
    low_peers = random.sample(range(n), num_low)

    # Generate the peers
    peers = []
    for i in range(n):
        config = {}
        if i in slow_peers:
            config["speed"] = "slow"
        else:
            config["speed"] = "fast"

        if i in low_peers:
            config["cpu"] = "low"
            config["hashing power"] = 1/(10*n - 9*num_low) # 1/10 of the hashing power of a high CPU peer
        else:
            config["cpu"] = "high"
            config["hashing power"] = 10/(10*n - 9*num_low) # 10 times the hashing power of a low CPU peer

        p = Peer(i, genesis, env, config)
        peers.append(p)
        genesis.balances = {i: 0 for i in range(n)}

    # Generate the adversary
    adv = SelfishPeer(n, genesis, env, {"speed": "fast", "cpu": "high", "hashing power": args.h}, params.selfish)
    genesis.balances[n] = 0

    # Generate the network
    # Assuming that Z is not normalized
    network = Network(peers, adv, args.I, args.Z, env)

    for peer in peers:
        peer.use_network(network)
        env.process(peer.generate_transactions(args.Ttx, peers))
        if random.random() < 0.25:
            env.process(peer.create_block())

    adv.use_network(network)
    env.process(adv.generate_transactions(args.Ttx, peers))
    env.process(adv.create_block())

    env.run(until=args.time)

    with open("MPU.txt", 'w') as f:
        tot_gen = 0
        for p in peers:
            tot_gen += p.num_gen
        
        print("Overall MPU : ", peers[0].longest_chain.height/tot_gen, file=f)

    if(params.selfish):
        if os.path.exists(os.path.dirname(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/")):
            shutil.rmtree(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/")

        if os.path.exists(os.path.dirname(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/")):
            shutil.rmtree(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/")

        # time.sleep(10)
        for peer in peers:
            longest_chain = peer.longest_chain.height
            peer.print_tree(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/tree_{peer.id}_{longest_chain}.dot")
            peer.save_tree(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/tree_{peer.id}_{longest_chain}.tree")
        
        # Printing actions of the adversary
        longest_chain = adv.longest_chain.height
        adv.print_tree(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/tree_{adv.id}_{longest_chain}.dot")
        adv.save_tree(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_selfish/tree_{adv.id}_{longest_chain}.tree")
    elif(params.stubborn):
        if os.path.exists(os.path.dirname(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/")):
            shutil.rmtree(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/")

        if os.path.exists(os.path.dirname(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/")):
            shutil.rmtree(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/")

        # time.sleep(10)
        for peer in peers:
            longest_chain = peer.longest_chain.height
            peer.print_tree(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/tree_{peer.id}_{longest_chain}.dot")
            peer.save_tree(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/tree_{peer.id}_{longest_chain}.tree")
        
        # Printing actions of the adversary
        longest_chain = adv.longest_chain.height
        adv.print_tree(f"plots_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/tree_{adv.id}_{longest_chain}.dot")
        adv.save_tree(f"trees_{args.n}_{args.z1}_{args.Ttx}_{args.I}_{args.time}_{args.h}_{args.Z}_stubborn/tree_{adv.id}_{longest_chain}.tree")

# python3 run.py --n 50 --z1 0.3 --Ttx 1 --I 1 --time 1000