from pox.core import core 
from pox.lib.addresses import IPAddr 
from forwarding.l2_learning import *
import pox.openflow.libopenflow_01 as of 
import pox.lib.packet as PKT 

class TestFW(object):
    def __init__(self, fw_dpid, srv_list): 
        core.openflow.addListeners(self)
        self.fwdpid = fw_dpid
        self.srv_list = srv_list

    def _handle_ConnectionUp(self, event): 
        # handle switch with wanted DPID
        if event.dpid == self.fwdpid: 
            # save the connection obj
            self.connection = event.connection 
            log.debug("firewall %d : %s is now up", event.dpid, dpid_to_str(event.dpid))


            ### INSTALL THE NEW RULES ON THE SWITCH ### 
            rules = set() 
            for web_server in self.srv_list["web"]: 
                # generate TCP rules for talking to webservers from out (pub/priv zone) to inner
                msg = of.ofp_flow_mod(
                        action = of.ofp_action_output(port=2), 
                        match = of.ofp_match(
                                in_port = 1, 
                                dl_type = PKT.ethernet.IP_TYPE, 
                                nw_proto = PKT.ipv4.TCP_PROTOCOL, 
                                nw_dst = IPAddr(web_server), 
                                dp_dst = 80
                            ), 
                        priority = 111
                )
                print("ALLOWING TCP 80 IN FW {} TO {}".format(event.dpid, web_server))
                rules.add(msg) 

                # from inner webservice to outer (public/priv zone) 
                msg = of.ofp_flow_mod(
                        action = of.ofp_action_output(port=1),
                        match = of.ofp_match(
                                in_port = 2,
                                dl_type = PKT.ethernet.IP_TYPE, 
                                nw_proto = PKT.ipv4.TCP_PROTOCOL,
                                nw_src = IPAddr(web_server), 
                                tp_src = 80
                            ), 
                        priority = 111
                )
                print("ALLOWING TCP 80 IN FW {} TO {}".format(event.dpid, web_server))
                rules.add(msg)

            # send out all the collected generated rules to the switch 
            for rule in rules: 
                self.connection.send(rule) 

            # then act as a normal L2 switch 
            LearningSwitch(event.connection, False)




