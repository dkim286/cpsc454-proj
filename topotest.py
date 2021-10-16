from mininet.net import Mininet 
from mininet.cli import CLI 
from mininet.topo import Topo 
from mininet.node import RemoteController, OVSSwitch, Host


class TestTopo(Topo):
    def __init__(self):
        Topo.__init__(self) 

        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1') 
        h2 = self.addHost('h2') 
        h3 = self.addHost('h3', ip='10.0.0.100/24')

        self.addLink(h1, s1) 
        self.addLink(h2, s1) 
        self.addLink(h3, s1)

if __name__ == '__main__':
    topo = TestTopo() 
    c0 = RemoteController('c0', ip='127.0.0.1', port=6633) 

    net = Mininet(topo=topo, switch=OVSSwitch, controller=c0, build=True, cleanup=True)

    net.start()

    CLI(net)
    net.stop() 
