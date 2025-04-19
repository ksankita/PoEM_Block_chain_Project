# PoEM_Block_chain_Project
 LIGHTWEIGHT MODEL-BASED EVOLUTIONARY CONSENSUS PROTOCOL IN BLOCKCHAIN AS A SERVICE FOR IoT
PoEM Blockchain Simulation using Mininet & Ryu
==============================================

This project demonstrates a lightweight blockchain consensus mechanism, called PoEM (Proof of Evolutionary Model), tailored for IoT and BaaS environments. The simulation runs on a Mininet virtual network, using Ryu SDN Controller to manage topology and traffic.

------------------------------------------------------------
Components
------------------------------------------------------------
- Mininet: Network emulation platform.
- Ryu Controller: OpenFlow-based SDN controller.
- PoEM Nodes: Each host runs a lightweight ML model (Logistic Regression) and participates in consensus.
- UDP Messaging: Used for communication between nodes.

------------------------------------------------------------
Installation Steps
------------------------------------------------------------

1. Install Mininet
------------------
    sudo apt-get update
    sudo apt-get install mininet

2. Set Up Python Environment with Ryu
-------------------------------------
    # Add deadsnakes PPA and install Python 3.9
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt install python3.9 python3.9-distutils virtualenv

    # Create and activate virtual environment
    virtualenv -p `which python3.9` ryu-python3.9-venv
    source ryu-python3.9-venv/bin/activate

    # Install Ryu
    sudo apt-get install python3-ryu

    # Fix eventlet compatibility
    pip uninstall eventlet
    pip install eventlet==0.30.2

    # Verify Ryu installation
    ryu --version
    ryu-manager --version

------------------------------------------------------------
Running the Simulation
------------------------------------------------------------

1. Launch Ryu Controller
------------------------
    ryu-manager --ofp-tcp-listen-port 6633 ryu.app.simple_switch_13

2. Clear Mininet State (Optional)
---------------------------------
    sudo mn -c

3. Start the Mininet Topology and PoEM Nodes
--------------------------------------------
    sudo python3 /home/student/block_chain/poem_topo.py

