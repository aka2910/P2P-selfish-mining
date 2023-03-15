# P2P-currency-simulator

Requirements:
- Python
- Graphviz
- SimPy

To run the simulation, run the following command:

```python
python3 run.py --n 10 --z0 0.9 --z1 0.1 --Ttx 1000000 --I 6000 --time 2880000
```

The parameters are:
- n: number of peers
- z0: percent of slow peers
- z1: percent of low CPU peers
- Ttx: mean interarrival time of transactions
- I: mean interarrival time of blocks
- time: simulation time

The graph for each peer (block tree) is generated in the folder `plots*`.
