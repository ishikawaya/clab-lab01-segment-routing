# lab01

## Topology
![Topology Diagram](https://github.com/ishikawaya/clab-lab01-segment-routing/blob/main/images/lab01-topology.png)

## Overview
Deploying SRv6 over an SR-MPLS network.  
The SR-MPLS network is configured with IPv4 single-stack.  
ICMP communication was confirmed between node1 <---> node2.  

## pe1 bgp ipv4 vpn route(node2 loopback)
```
pe1# show bgp ipv4 vpn 200.0.0.0/32 
BGP routing table entry for 65002:20:200.0.0.0/32, version 8
not allocated
Paths: (3 available, best #1)
  Advertised to peers:
  4:4:4::4 5:5:5::5 6:6:6::6
  65002
    0.0.0.0 from 5:5:5::5 (5.5.5.5)
      Origin incomplete, metric 0, valid, external, multipath, best (Older Path)
      Extended Community: RT:65000:20
      Remote label: 16
      Remote SID: 5:5:5::, sid structure=[24 24 16 0 16 48]
      Last update: Sat Dec 13 10:45:39 2025
  65002
    0.0.0.0 from 6:6:6::6 (6.6.6.6)
      Origin incomplete, metric 0, valid, external, multipath
      Extended Community: RT:65000:20
      Remote label: 16
      Remote SID: 6:6:6::, sid structure=[24 24 16 0 16 48]
      Last update: Sat Dec 13 10:45:58 2025
  65002
    0.0.0.0 from 4:4:4::4 (4.4.4.4)
      Origin incomplete, metric 0, localpref 100, valid, internal
      Extended Community: RT:65000:20
      Remote label: 16
      Remote SID: 5:5:5::, sid structure=[24 24 16 0 16 48]
      Last update: Sat Dec 13 10:45:39 2025
pe1#
```

## pe1 ipv4 route (vrf red)
```
pe1# show ip route vrf red
Codes: K - kernel route, C - connected, L - local, S - static,
       R - RIP, O - OSPF, I - IS-IS, B - BGP, E - EIGRP, N - NHRP,
       T - Table, v - VNC, V - VNC-Direct, A - Babel, F - PBR,
       f - OpenFabric, t - Table-Direct,
       > - selected route, * - FIB route, q - queued, r - rejected, b - backup
       t - trapped, o - offload failure

IPv4 unicast VRF red:
C>* 3.0.0.0/31 is directly connected, eth3, weight 1, 00:10:24
L>* 3.0.0.0/32 is directly connected, eth3, weight 1, 00:10:24
B>  3.0.0.2/31 [200/0] via 4:4:4:: (vrf default) (recursive), label 16, seg6 4:4:4:1::, weight 1, 00:05:17
  *                      via fe80::a8c1:abff:fe60:1ceb, eth2 (vrf default), label 16, seg6 4:4:4:1::, weight 1, 00:05:17
B>  4.0.0.0/31 [20/0] via 5:5:5::5 (vrf default) (recursive), label 16, seg6 5:5:5:1::, weight 1, 00:03:20
  *                     via 1000::1, eth1 (vrf default), label 16, seg6 5:5:5:1::, weight 1, 00:03:20
                      via 6:6:6::6 (vrf default) (recursive), label 16, seg6 5:5:5:1::, weight 1, 00:03:20
                        via 1000::1, eth1 (vrf default) (dup), label 16, seg6 5:5:5:1::, weight 1, 00:03:20
B>  4.0.0.2/31 [20/0] via 5:5:5::5 (vrf default) (recursive), label 16, seg6 6:6:6:1::, weight 1, 00:03:20
  *                     via 1000::1, eth1 (vrf default), label 16, seg6 6:6:6:1::, weight 1, 00:03:20
                      via 6:6:6::6 (vrf default) (recursive), label 16, seg6 6:6:6:1::, weight 1, 00:03:20
                        via 1000::1, eth1 (vrf default) (dup), label 16, seg6 6:6:6:1::, weight 1, 00:03:20
S>* 100.0.0.0/32 [1/0] via 3.0.0.1, eth3, weight 1, 00:10:24
B>  200.0.0.0/32 [20/0] via 5:5:5::5 (vrf default) (recursive), label 16, seg6 5:5:5:1::, weight 1, 00:03:21
  *                       via 1000::1, eth1 (vrf default), label 16, seg6 5:5:5:1::, weight 1, 00:03:21
                        via 6:6:6::6 (vrf default) (recursive), label 16, seg6 6:6:6:1::, weight 1, 00:03:21
  *                       via 1000::1, eth1 (vrf default), label 16, seg6 6:6:6:1::, weight 1, 00:03:21
pe1#
```

## node1 to node2 ping result
```sh
$ docker exec -ti clab-lab01-node1 sh -c 'ping 200.0.0.0 -I 100.0.0.0 -c 3'
PING 200.0.0.0 (200.0.0.0) from 100.0.0.0: 56 data bytes
64 bytes from 200.0.0.0: seq=0 ttl=63 time=4.425 ms
64 bytes from 200.0.0.0: seq=1 ttl=63 time=3.127 ms
64 bytes from 200.0.0.0: seq=2 ttl=63 time=2.952 ms

--- 200.0.0.0 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.952/3.501/4.425 ms
```

## ping capture
```sh
$ tshark -r pe1_eth1_20251213_1936.pcap icmp
  --- snip ---
  887 929.736843    100.0.0.0 → 200.0.0.0    ICMP 162 Echo (ping) request  id=0x0090, seq=0/0, ttl=64
  891 930.737419    100.0.0.0 → 200.0.0.0    ICMP 162 Echo (ping) request  id=0x0090, seq=1/256, ttl=64
  892 931.737808    100.0.0.0 → 200.0.0.0    ICMP 162 Echo (ping) request  id=0x0090, seq=2/512, ttl=64

tshark: The file "pe1_eth1_20251213_1936.pcap" appears to have been cut short in the middle of a packet.

$ tshark -r pe2_eth1_20251213_1936.pcap icmp
  --- snip ---
  802 929.740657    200.0.0.0 → 100.0.0.0    ICMP 162 Echo (ping) reply    id=0x0090, seq=0/0, ttl=64
  809 930.739996    200.0.0.0 → 100.0.0.0    ICMP 162 Echo (ping) reply    id=0x0090, seq=1/256, ttl=64
  810 931.740251    200.0.0.0 → 100.0.0.0    ICMP 162 Echo (ping) reply    id=0x0090, seq=2/512, ttl=64

tshark: The file "pe2_eth1_20251213_1936.pcap" appears to have been cut short in the middle of a packet.
```
