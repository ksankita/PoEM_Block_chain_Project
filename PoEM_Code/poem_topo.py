# from mininet.topo import Topo
# from mininet.net import Mininet
# from mininet.node import Controller
# from mininet.link import TCLink
# from mininet.cli import CLI
# from mininet.log import setLogLevel

# class PoEMTopology(Topo):
#     def build(self, n=5):
#         switch = self.addSwitch('s1')
#         for i in range(n):
#             host = self.addHost(f'h{i+1}', ip=f'10.0.0.{i+1}')
#             self.addLink(host, switch)

# def run():
#     topo = PoEMTopology()
#     net = Mininet(topo=topo, build=False, controller=None, link=TCLink)
#     net.build()
#     net.start()

#     print("Starting PoEM Nodes...")
#     for i, host in enumerate(net.hosts):
#         host.cmd(f'xterm -hold -e "python3 /home/student/block_chain/poem_node.py h{i+1}" &')

#     CLI(net)
#     net.stop()

# if __name__ == '__main__':
#     setLogLevel('info')
#     run()


from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class SingleSwitchTopo(Topo):
    def build(self, n=5):
        switch = self.addSwitch('s1')
        for i in range(n):
            host = self.addHost(f'h{i+1}', ip=f'10.0.0.{i+1}')
            self.addLink(host, switch)

def run():
    topo = SingleSwitchTopo(n=5)
    net = Mininet(topo=topo, controller=RemoteController, build=False, link=TCLink)
    net.addController('c1', controller=RemoteController, ip='127.0.0.1', port=6633)  # Ryu's default port
    net.build()
    net.start()

    print("Starting PoEM Nodes...")
    for i, host in enumerate(net.hosts):
        host.cmd(f'xterm -hold -e "python3 /home/student/block_chain/poem_node.py h{i+1}" &')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()


# ryu-manager --ofp-tcp-listen-port 6633 ryu.app.simple_switch_13
# sudo mn -c
#  sudo apt-get install python3-ryu

# sudo add-apt-repository ppa:deadsnakes/ppa
# sudo add-apt install virtualenv python3.9 python3.9-distutils 
# sudo apt-get install virtualenv python3.9 python3.9-distutils 
# virtualenv -p`which python3.9` ryu-python3.9-venv
# ryu --version
# ryu-manager --version
# pip uninstall eventlet
#  pip install eventlet==0.30.2
# ryu-manager --help
#  ryu --version
# ryu-manager --version
# sudo python3 /home/student/block_chain/poem_topo.py
# ryu-manager --ofp-tcp-listen-port 6633 ryu.app.simple_switch_13
