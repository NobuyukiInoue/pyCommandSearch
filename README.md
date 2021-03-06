# pyCommandSearch

Extracts the execution result of the specified command from the operation log of the NW device.



## Usage

* pyCommandSearch

Extracts the execution result of the specified command from the operation log of the NW device.

```
$ python pyCommandSearch <logfiles target_path> <target_command> <match_flag>
```

* pyCommandSearch_Power_for_Juniper.py

Cut out the execution result of "show chassis power" and write it to an Excel workbook.

```
$ python pyCommandSearch_Power_for_Juniper.py <logfiles path> <target command> <target Excel Workbook> <match_flag>

```

## Execute example

```
PS Z:\pyCommandSearch> python .\pyCommandSearch.py z:\logs\*.log "show ip route"
##----------------------------------------------------------------------##
## z:\logs\router01_10.15.xx.xxxx_yyyyMMdd-hhmmss.log
##----------------------------------------------------------------------##
router01#show ip route
Load for five secs: 14%/2%; one minute: 13%; five minutes: 12%
Time source is NTP, 15:35:11.469 JST Wed Mar 30 2011

Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 16 subnets, 2 masks
C        10.14.15.0/24 is directly connected, Vlan99
L        10.14.15.254/32 is directly connected, Vlan99
C        10.15.0.0/24 is directly connected, Vlan99
L        10.15.0.254/32 is directly connected, Vlan99
C        10.15.10.0/24 is directly connected, Vlan99
L        10.15.10.254/32 is directly connected, Vlan99
...
...
router01#show ip route vrf *
Load for five secs: 14%/2%; one minute: 13%; five minutes: 12%
Time source is NTP, 15:35:11.542 JST Wed Mar 30 2011

Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 16 subnets, 2 masks
C        10.14.15.0/24 is directly connected, Vlan99
L        10.14.15.254/32 is directly connected, Vlan99
C        10.15.0.0/24 is directly connected, Vlan99
L        10.15.0.254/32 is directly connected, Vlan99
C        10.15.10.0/24 is directly connected, Vlan99
L        10.15.10.254/32 is directly connected, Vlan99
...
...
router01#
##----------------------------------------------------------------------##
## z:\logs\router02_xxx.xxx.xxx.xxx_yyyyMMdd-hhmmss.log
##----------------------------------------------------------------------##
router02#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, m - OMP
       n - NAT, Ni - NAT inside, No - NAT outside, Nd - NAT DIA
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       H - NHRP, G - NHRP registered, g - NHRP registration summary
       o - ODR, P - periodic downloaded static route, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 13 subnets, 2 masks
O IA     10.14.15.0/24 [110/11] via 10.135.20.254, 00:16:47, Vlan120
O IA     10.15.0.0/24 [110/11] via 10.135.20.254, 00:16:47, Vlan120
O IA     10.15.10.0/24 [110/11] via 10.135.20.254, 00:16:47, Vlan120
...
...
router02#
##----------------------------------------------------------------------##
PS Z:\pyCommandSearch>
```


## Relation

* command_exec for TeraTerm<br>
https://www.vector.co.jp/soft/winnt/net/se516693.html

* PS_command_diff<br>
https://github.com/NobuyukiInoue/PS_command_diff


## Licence

[MIT](https://github.com/NobuyukiInoue/pyCommandSearch/blob/master/LICENSE)


## Author

[Nobuyuki Inoue](https://github.com/NobuyukiInoue/)
