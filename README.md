# P2P-currency-simulator
CS765: Assignment 2

Requirements:
- Python
- Graphviz
- SimPy

To run the simulation, run the following command:

```python
python3 run_selfish.py --n 25 --z1 0.4 --Ttx 1000000 --I 6000 --time 5000000 --Z 75 --h 0.5 > out.txt
```

The parameters are:
- n: number of peers
- z1: percent of low CPU peers
- Ttx: mean interarrival time of transactions
- I: mean interarrival time of blocks
- time: simulation time
- Z: Zeta
- h: Hashing power

The graph for each peer (block tree) is generated in the folder `plots*`.
