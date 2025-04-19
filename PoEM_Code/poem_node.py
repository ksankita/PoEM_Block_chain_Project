import numpy as np
import random
import socket
import threading
import sys
import json
from sklearn.linear_model import LogisticRegression
from collections import Counter

# ---------------- CONFIG ----------------
PORT_BASE = 9000
NODE_COUNT = 5
ROUNDS = 4
received_votes = []
lock = threading.Lock()
# ----------------------------------------


# --- Simulated PoEM Node Class ---
class PoEMNode:
    def __init__(self, name):
        self.name = name
        self.model = LogisticRegression()
        self.feature_history = []
        self.fitness_history = []
        self.votes_received = 0
        self.init_training()

    def init_training(self):
        for i in range(10):
            X = np.random.rand(10, 3)
            y = np.array([0]*5 + [1]*5)
            np.random.shuffle(y)
            self.model.fit(X, y)

    def collect_features(self):
        return np.array([round(random.uniform(0.3, 1.0), 2) for _ in range(3)])

    def predict_fitness(self, feature_vec, alpha=0.5):
        weight = self.model.coef_[0]
        bias = self.model.intercept_[0]
        z = np.dot(weight, feature_vec) + bias
        sigmoid = 1 / (1 + np.exp(-z))
        eta = self.fitness_history.count(0)
        poem_score = sigmoid - alpha * eta
        return poem_score

    def evolve_model(self):
        if len(set(self.fitness_history)) > 1:
            self.model.fit(np.array(self.feature_history), np.array(self.fitness_history))
        self.feature_history.clear()
        self.fitness_history.clear()


def vote_strategy(scores):
    return max(scores, key=scores.get)


# --- Networking Utils ---
def extract_node_id(name):
    return int(name[1:])


def start_listener(my_name):
    my_port = PORT_BASE + extract_node_id(my_name)

    def listener():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', my_port))
        while True:
            data, _ = s.recvfrom(4096)
            vote = json.loads(data.decode())
            with lock:
                received_votes.append(vote)  # ✅ FIXED

    threading.Thread(target=listener, daemon=True).start()



def send_vote(my_name, vote):
    sender_id = extract_node_id(my_name)
    msg = json.dumps({'voter': my_name, 'vote': vote}).encode()
    for i in range(1, NODE_COUNT + 1):
        ip = f'10.0.0.{i}'
        port = PORT_BASE + i
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, (ip, port))


# --- PoEM Consensus Round (Distributed) ---
def one_round_with_network(nodes,i):
    print(f"\n--- PoEM Consensus Round :{i} Start ---\n")
    all_features = {}

    for name, node in nodes.items():
        all_features[name] = node.collect_features()

    # Step 2: Each node computes and sends vote
    for voter_name, voter_node in nodes.items():
        scores = {n: voter_node.predict_fitness(all_features[n]) for n in nodes}
        voted = vote_strategy(scores)
        print(f"{voter_name} votes for {voted}")
        send_vote(voter_name, voted)

    # Step 3: Wait for all votes to be received
    while True:
        with lock:
            if len(received_votes) >= NODE_COUNT:
                break

    # Step 4: Aggregate votes
    with lock:
        all_votes = [v['vote'] for v in received_votes]
        received_votes.clear()

    vote_counts = Counter(all_votes)
    winner = vote_counts.most_common(1)[0][0]
    print(f"\nWinner of consensus round: {winner}\n")

    # Step 5: Propose block
    print(f"{winner} proposes a block")

    # Step 6: Validate block
    for name in nodes:
        if name != winner:
            print(f"{name} validates block from {winner} – [VALID]")

    # Step 7: Evolve models
    for name, node in nodes.items():
        node.feature_history.append(all_features[name])
        node.fitness_history.append(1 if name == winner else 0)
        node.evolve_model()

    print("\n--- PoEM Consensus Round End ---\n")


# --- Simulation Start ---
def simulate_poem(my_name):
    nodes = {}
    for i in range(NODE_COUNT):
        name = f'h{i+1}'
        nodes[name] = PoEMNode(name)
        nodes[name].init_training()

    start_listener(my_name)

    for i in range(ROUNDS):
        one_round_with_network(nodes,i)


# --- Entry Point ---
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 poem_node.py h1|h2|h3|...")
        sys.exit(1)

    my_node_name = sys.argv[1]

    # Each node starts the simulation and listener
    simulate_poem(my_node_name)

