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
    
# python3 run.py --n 50 --z0 0.8 --z1 0.3 --Ttx 1 --I 1 --time 1000