# P2P-Blockchain-Simulator

## Visualization Results

Visualizations for any **five randomly chosen peers** (with duplicates possible) are stored in the `Blockchain_of_each_peer` folder. Please **clear this folder using `rm ./Blockchain_of_each_peer/*`** before running a new simulation.

## Blockchain Trees

The blockchain trees of **Any five randomly chosen nodes/peers** are stored in the `BFS_of_blockchain` folder. Each tree is represented as a list of its **edges in parent-child format**. Please **clear this folder using `rm ./BFS_of_blockchain/*`** before running a new simulation.

**Note:** Due to time constraints associated with I/O overhead, we limit visualizations to five randomly chosen peers, potentially including duplicates.

## Compiling and Running the Simulation

**Default Command:** `python3 simulator.py`

**Note:** During execution, the simulation will display timestamps of occurring events to gauge progress. It will run until the specified `observation_time` or `simulation_time` is reached for determinism.

## Command-Line Arguments for Customization

To explore different network behaviors, use the following command-line arguments:

* `total_peers`: The total number of peers in the network.
* `Z0_percent`: The percentage of peers with slow processing capabilities.
* `Z1_percent`: The percentage of peers with low CPU capacity.
* `Tb`: The average time between block generation (in milliseconds).
* `Tx`: The average time between transaction generation (in milliseconds).
* `To`: The total observation time or simulation duration (in milliseconds).
* To add: `network_delay`: Currently can be manually changed in the code.

## Example Simulation Commands

1. `python3 simulator.py --total_peers 100 --z0_percent 50 --z1_percent 50 --Tx 5000 --Tb 600000 --To 24000000`
2. `python3 simulator.py --total_peers 100 --z0_percent 50 --z1_percent 50 --Tx 5000 --Tb 25000 --To 1000000`
3. `python3 simulator.py --total_peers 100 --z0_percent 50 --z1_percent 50 --Tx 5000 --Tb 10000 --To 400000`
4. `python3 simulator.py --total_peers 100 --z0_percent 50 --z1_percent 50 --Tx 5000 --Tb 1000 --To 40000`
5. `python3 simulator.py --total_peers 100 --z0_percent 50 --z1_percent 50 --Tx 50 --Tb 200 --To 8000`
