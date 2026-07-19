# FRRouting (frr) release notes — GitHub Releases (verbatim tag + body)

## frr-10.7.0

We are pleased to announce FRR release **10.7.0**.

FRR 10.7.0 comes with 1433 commits from 105 developers. 

Debian and RPM release packages are available at:
 
Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:65e5967b922572c0565d968388fb06af69d7e9b3b3eea40ad7e3810687667f68)

Thank you to all contributors!

## Release Overview

### New Features Highlight

- **BFD authentication with keychain support**

  - BFD sessions can now use the FRR keychain framework for authentication.
  - Supported algorithms include cleartext, SHA-1, and the meticulous variant required by operators running strict authentication policies.
  - Keychains integrate with BFD profiles and northbound configuration for single-hop, multi-hop, and SBFD sessions.

- **BGP-LS SRv6 extensions**

  - BGP Link-State now advertises and processes SRv6 topology information, including:
    - SRv6 Capabilities TLV
    - SRv6 Locator TLV
    - SRv6 SID NLRI (including End, End.X, and LAN End.X forms)
    - SRv6 Endpoint Behavior TLV
    - SRv6 SID Structure TLV
  - Static SRv6 SIDs configured in zebra can be exported into BGP-LS, enabling SRv6-aware TE controllers to consume locator and SID information from FRR.

- **BGP route-map based allowas-in**

  - `allowas-in` can be applied selectively through route-maps instead of only as a blanket peer or address-family knob.
  - This allows finer control over which received routes may contain the local AS in the AS_PATH, improving policy flexibility in complex multihomed and hub-and-spoke designs.

- **OSPFv2 RFC 4222 control-plane DSCP marking**

  - OSPFv2 can classify control packets into high- and low-priority queues per RFC 4222 recommendation 1.
  - Recommendation 2 extends the neighbor inactivity timer behavior for low-priority control traffic.
  - Operators can mark OSPF control traffic with DSCP values to protect routing protocol stability under congestion.

- **OSPF BFD quick neighbor**

  - When BFD is enabled on OSPF interfaces, a quick-neighbor mode reduces the time needed to bring up OSPF adjacencies over BFD-monitored links.
  - This is useful on fabrics where fast reconvergence after link-up is required.

- **PIM IGMP proxy route-map filtering**

  - IGMP proxy joins and prunes can be filtered with `ip igmp proxy route-map`.
  - A new route-map match condition, `match multicast-source-interface`, allows policy based on the interface where a join was learned.
  - This helps deployments that proxy IGMP between access and core segments while restricting which groups or sources are forwarded.

- **PIM dense-mode Assert on multi-access LAN**

  - Dense-mode wrong-interface traffic on shared LANs now runs the RFC 3973 Assert procedure instead of immediately pruning all neighbors.
  - On point-to-point links the previous immediate-prune behavior is preserved.
  - This elects a single forwarder on multi-access segments and avoids pruning active branches when duplicate (S,G) packets arrive on a non-RPF interface.

- **PIM Auto-RP allow-rp support**

  - A new `allow-rp` configuration accepts Auto-RP groups even when the embedded RP address does not match the local RP configuration.
  - IPv4 and IPv6 Auto-RP are supported through northbound/YANG modeling.
  - This helps mixed-vendor or transitional Auto-RP deployments where strict RP identity checking would otherwise drop valid control traffic.

- **Static route per-route metric and nexthop ECMP weight**

  - Static routes now support a per-route metric as a non-key attribute, independent of the existing administrative-distance key.
  - Static ECMP nexthops can carry weights for unequal-cost multi-path forwarding.
  - Together these align static routing policy more closely with zebra’s nexthop-group handling used by other protocols.

## What's Changed
* EVPN RMAC management fixes and test coverage by @soumyar-roy in https://github.com/FRRouting/frr/pull/20588
* ospfd: Display message when clearing interface without OSPF by @soumyar-roy in https://github.com/FRRouting/frr/pull/20267
* zebra: FRR restart leads to zebra mlag core by @soumyar-roy in https://github.com/FRRouting/frr/pull/20225
* zebra: limit RTADV socket rcvbuf to 20MB by @hengwu0 in https://github.com/FRRouting/frr/pull/20654
* Evpn test abstraction by @donaldsharp in https://github.com/FRRouting/frr/pull/20637
* pimd,pim6d: fix last-member-query-count and add robustness value by @rzalamena in https://github.com/FRRouting/frr/pull/20613
* bgpd: Changes to include new fields in "show bgp router" command by @soumyar-roy in https://github.com/FRRouting/frr/pull/20631
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… by @routingrocks in https://github.com/FRRouting/frr/pull/20661
* staticd: Fix SRv6 SID use-after-free on locator deletion by @cscarpitta in https://github.com/FRRouting/frr/pull/20660
* yang: Correct pyang errors in frr-nexthop.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20694
* bgpd: Replace 3 with BGP_ALLOWAS_IN_DEFAULT constant by @ton31337 in https://github.com/FRRouting/frr/pull/20698
* Fixes for op-state change notifications being sent to backend clients (daemons) by @choppsv1 in https://github.com/FRRouting/frr/pull/20647
* bgpd: Missing large community value in commAttriSentToNbr JSON by @soumyar-roy in https://github.com/FRRouting/frr/pull/20608
* lib,bgpd: Adding JSON str for time in dd:hh:mm:ss format by @soumyar-roy in https://github.com/FRRouting/frr/pull/20632
* bgpd: use BGP_PATH_INFO_NUM_LABELS macro in bgp_evpn_path_info_get_l3vni by @nick-bouliane in https://github.com/FRRouting/frr/pull/20679
* Add new show command to display only failed routes by @deepak-singhal0408 in https://github.com/FRRouting/frr/pull/20343
* bfdd: early return on socket allocation failure by @ethanmilon-6wind in https://github.com/FRRouting/frr/pull/20700
* zebra: add state column to 'show evpn es' command output by @shashanka-ks in https://github.com/FRRouting/frr/pull/20711
* zebra: add 'no encapsulation' command under segment-routing/srv6 by @hedrok in https://github.com/FRRouting/frr/pull/20716
* tests: Check PIM Register/-Stop handling in pim_igmp_vrf topotest by @gromit1811 in https://github.com/FRRouting/frr/pull/18329
* ospf6d: Fix stack buffer overflow in link LSA by @rminnikanti in https://github.com/FRRouting/frr/pull/20695
* bgpd: fix md5 password unset on dynamic nbr by @chiragshah6 in https://github.com/FRRouting/frr/pull/20740
* bgpd,zebra: EVPNv6 addressing coverity warnings by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/20680
* bgpd: Fix suppress-fib-pending config race condition on startup by @krishna-samy in https://github.com/FRRouting/frr/pull/20622
* bgpd: fix batch clearing resume to use correct lookup APIs by @miteshkanjariya in https://github.com/FRRouting/frr/pull/20738
* bgpd: add a counter for received duplicate updates by @enkechen-panw in https://github.com/FRRouting/frr/pull/20553
* bgpd: Fix AS path exclude not working during VRF route re-import by @soumyar-roy in https://github.com/FRRouting/frr/pull/20556
* Nexthop weight support for static routes (ECMP/UCMP) by @iurmanj6WIND in https://github.com/FRRouting/frr/pull/20559
* Add memberCount into peer-grp json AND GR fields in fields in show bgp vrfs json by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20578
* zebra: uninstall remote neigh even when ifp is down  by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20587
* vtysh: Add JSON output support for `show memory` by @ton31337 in https://github.com/FRRouting/frr/pull/20605
* bgpd: Ignore transitiveness flag when checking type for link bandwidth by @ton31337 in https://github.com/FRRouting/frr/pull/20607
* bgpd: Show all advertised paths including non-best paths only if addpath is enabled by @ton31337 in https://github.com/FRRouting/frr/pull/20618
* bgpd: implement new redistribute json command by @soumyar-roy in https://github.com/FRRouting/frr/pull/20630
* ospf6d: Fix FULL adjacency persisting despite MTU mismatch by @rminnikanti in https://github.com/FRRouting/frr/pull/20681
* doc: Fix VRF-related and PIM docs by @gromit1811 in https://github.com/FRRouting/frr/pull/20717
* zebra: rename BondState to State in 'show evpn es' output by @shashanka-ks in https://github.com/FRRouting/frr/pull/20721
* lib: use MTYPEs for northbound in several places by @mjstapp in https://github.com/FRRouting/frr/pull/20733
* Non route replace semantics by @donaldsharp in https://github.com/FRRouting/frr/pull/20725
* yang: Fix pyang errors in frr-bgp-filter.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20746
* zebra: shorten label for RNH mem type by @mjstapp in https://github.com/FRRouting/frr/pull/20749
* *: Fixed coverity warnings in multiple areas by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/20610
* bgpd: EVPN MH fix unimport ES route on vtep change by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/20730
* Zebra fixup nhg handling from kernel by @donaldsharp in https://github.com/FRRouting/frr/pull/20732
* zebra: Updation of ifp->flags by @hnattamaisub in https://github.com/FRRouting/frr/pull/20769
* fix spell checks round 4 by @chiragshah6 in https://github.com/FRRouting/frr/pull/20771
* tests: Deleted duplicate imported modules by @y-bharath14 in https://github.com/FRRouting/frr/pull/20779
* Sharp send tableid for route by @donaldsharp in https://github.com/FRRouting/frr/pull/20634
* bgpd: unref routes when yielding during clearing iteration by @mjstapp in https://github.com/FRRouting/frr/pull/20789
* bgpd: fix premature deletion of already-stale routes during GR clearing by @miteshkanjariya in https://github.com/FRRouting/frr/pull/20768
* bgpd: validate incoming NOTIFICATION messages by @mjstapp in https://github.com/FRRouting/frr/pull/20796
* tests: Add a default route test to rip by @donaldsharp in https://github.com/FRRouting/frr/pull/20799
* yang: Fix pyang errors in frr-bgp-types.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20797
* Multiple local fix by @donaldsharp in https://github.com/FRRouting/frr/pull/20798
* bgpd: improve flowspec NLRI validation by @mjstapp in https://github.com/FRRouting/frr/pull/20814
* bgpd: Reorder some struct attr members by @ton31337 in https://github.com/FRRouting/frr/pull/20822
* tests: Add additional wait tim to test_bgp_gr_functionality_topo2-3.py by @donaldsharp in https://github.com/FRRouting/frr/pull/20788
* Separate sg rpt sg ifchannels and add ability to set a override-interval and a test. by @donaldsharp in https://github.com/FRRouting/frr/pull/20552
* zebra: EVPN fix access BD deref of mbr intf by @chiragshah6 in https://github.com/FRRouting/frr/pull/20791
* tests: EVPN add dynamic nbr with ext router by @chiragshah6 in https://github.com/FRRouting/frr/pull/20737
* zebra: Allow redistribution events to pass reserved ranges by @donaldsharp in https://github.com/FRRouting/frr/pull/20599
* Fix ospf checksum #20706 by @Ko496-glitch in https://github.com/FRRouting/frr/pull/20729
* Kernel skip some route updates by @donaldsharp in https://github.com/FRRouting/frr/pull/20666
* bgpd: Force sending conditional updates by ignoring MRAI timer by @ton31337 in https://github.com/FRRouting/frr/pull/20668
* tests: Don't try to use identical rmacs in rare situation by @donaldsharp in https://github.com/FRRouting/frr/pull/20844
* tests: Fix rip_default_route_handling to be more consistent by @donaldsharp in https://github.com/FRRouting/frr/pull/20838
* pimd,ospfd: Passing local source address as part of BFD session creation by @usrivastava-nvidia in https://github.com/FRRouting/frr/pull/20739
* tests: Remove SRv6 SID check duplication by @cscarpitta in https://github.com/FRRouting/frr/pull/20843
* babeld: fix NULL pointer dereference in babel_clean_routing_process by @LyZephyr in https://github.com/FRRouting/frr/pull/20727
* vtysh: add additional options to `ping` command by @kaffarell in https://github.com/FRRouting/frr/pull/20283
* ospfd: prefer existing default route over generating by @rzalamena in https://github.com/FRRouting/frr/pull/20699
* tests: Do not fail zebra_nhg_check if skipped is not 0 on initial by @donaldsharp in https://github.com/FRRouting/frr/pull/20855
* Bgp peer sendq timing by @donaldsharp in https://github.com/FRRouting/frr/pull/20839
* tests: Unnecessary pass statement in test_bgp_lu.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/20860
* Add info_count to route_table for accurate RIB entry reporting by @mike-dubrovsky in https://github.com/FRRouting/frr/pull/20206
* * various spell check round 5 by @chiragshah6 in https://github.com/FRRouting/frr/pull/20866
* staticd: in route config, reject keywords as ifname by @mjstapp in https://github.com/FRRouting/frr/pull/20311
* debian: prefer libyang3 over libyang2 when building deb packages by @Jafaral in https://github.com/FRRouting/frr/pull/20871
* yang: Revision statements are not given in reverse chronological order by @y-bharath14 in https://github.com/FRRouting/frr/pull/20870
* tools: Add ldp commands to support bundle generation by @donaldsharp in https://github.com/FRRouting/frr/pull/20863
* lib: minor RCU/atomics improvements by @eqvinox in https://github.com/FRRouting/frr/pull/20864
* ldpd: Reuse port for ldpd sockets that set local ports by @donaldsharp in https://github.com/FRRouting/frr/pull/20858
* tests: Fix grpc-query.py to find micronet by @donaldsharp in https://github.com/FRRouting/frr/pull/20880
* pimd: When address change ensure DR changes too. by @donaldsharp in https://github.com/FRRouting/frr/pull/20881
* A few small Coverity fixes by @mbaldessari in https://github.com/FRRouting/frr/pull/20888
* lib/typesafe: guard skiplist level generation against ctz(0) UB by @florath in https://github.com/FRRouting/frr/pull/20899
* ospf6d: recalculate AS-external routes on non-external RIB updates by @donaldsharp in https://github.com/FRRouting/frr/pull/20882
* tests: fix some python and test syntax by @mjstapp in https://github.com/FRRouting/frr/pull/20905
* Always compare med fix by @donaldsharp in https://github.com/FRRouting/frr/pull/20909
* bgpd: fix memory leak in cluster_intern() by @enkechen-panw in https://github.com/FRRouting/frr/pull/20913
* bgpd: clear several parameters in subgroup_announce_check() by @enkechen-panw in https://github.com/FRRouting/frr/pull/20884
* isisd: fix memory-related issues and RFC-violations by @SpadeMomo in https://github.com/FRRouting/frr/pull/20333
* lib, bgpd: add "unique mode" for route tables, supporting direct lookup only by @mjstapp in https://github.com/FRRouting/frr/pull/20589
* bfdd:  BFD Admin-Down State Management Improvements by @sougatahitcs in https://github.com/FRRouting/frr/pull/20151
* zebra: add 'show evpn es-peer' command for EVPN-MH peer VTEP list by @shashanka-ks in https://github.com/FRRouting/frr/pull/20868
* tests: Allow for different bestpaths to be generated. by @donaldsharp in https://github.com/FRRouting/frr/pull/20889
* yang: Revision statements are not given in reverse chronological order at frr-staticd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20921
* bgpd: fix the local-preference setting for EBGP-OAD by @enkechen-panw in https://github.com/FRRouting/frr/pull/20898
* zebra: Modify rib_process_dplane_results to limmit work done by @donaldsharp in https://github.com/FRRouting/frr/pull/20902
* doc: add some text regarding libyang versions by @choppsv1 in https://github.com/FRRouting/frr/pull/20862
* bgpd: correct the display header by @anlancs in https://github.com/FRRouting/frr/pull/20927
* bgpd: commits for the listening port by @anlancs in https://github.com/FRRouting/frr/pull/20929
* bgpd: Support for new "show bgp <vrf> bestpath [json]" show command by @soumyar-roy in https://github.com/FRRouting/frr/pull/20616
* Zebra neighbor changes by @donaldsharp in https://github.com/FRRouting/frr/pull/20912
* Add support for libyang5 by @choppsv1 in https://github.com/FRRouting/frr/pull/20895
* eigrpd: handle the gr neighbor list safely in update_receive by @mjstapp in https://github.com/FRRouting/frr/pull/20933
* nhrpd: fix packet and buffer handling errors by @mjstapp in https://github.com/FRRouting/frr/pull/20932
* tests: fix a regex in all_protos topotest by @mjstapp in https://github.com/FRRouting/frr/pull/20911
* lib, tests: add a srcdest get_next api by @mjstapp in https://github.com/FRRouting/frr/pull/20906
* zebra: bump dplane minor version for 10.7 by @mjstapp in https://github.com/FRRouting/frr/pull/20943
* doc: add multicast testing guide for topotests by @Jafaral in https://github.com/FRRouting/frr/pull/20945
* lib: display End.DX2 route with appropriate oif attribute by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20954
* bgpd: Fix test for OPEN message with remote-as auto by @ton31337 in https://github.com/FRRouting/frr/pull/20963
* bgpd: Add missing PEER_FLAG_SEND_NHC_ATTRIBUTE for update group flags by @ton31337 in https://github.com/FRRouting/frr/pull/20956
* bgpd: Reuse prep_for_rmap_apply() before route_map_apply() by @ton31337 in https://github.com/FRRouting/frr/pull/20957
* pimd: fix msdp mesh group SA crash by @lpchambers in https://github.com/FRRouting/frr/pull/20900
* isisd: Fix remaining buffer size calculation in lsp_bits2string by @rbgarga in https://github.com/FRRouting/frr/pull/20984
* vrrpd: Notification from zebra is not sent to vrrp by @hnattamaisub in https://github.com/FRRouting/frr/pull/20270
* bgpd: make code more robust in bgp_advertise_attr_unintern() by @enkechen-panw in https://github.com/FRRouting/frr/pull/20989
* babeld: fix RFC violations in babel message parser by @SpadeMomo in https://github.com/FRRouting/frr/pull/20339
* pathd: add 'no traffic-eng' command, add test, don't output 'segment-routing/traffic-eng' in configuration always by @hedrok in https://github.com/FRRouting/frr/pull/20638
* bgpd: Fix condition when evaluating paths by @ton31337 in https://github.com/FRRouting/frr/pull/20975
* bgpd: Fix routes to be removed from rib when suppress fib pending is configed by @nishant111 in https://github.com/FRRouting/frr/pull/20917
* bgpd, isisd, ospfd: coverity fixes by @ashred-lnx in https://github.com/FRRouting/frr/pull/20948
* bgpd: Fix nht to properly notice a change by @donaldsharp in https://github.com/FRRouting/frr/pull/20986
* Zebra MetaQ and dplane provider fixes by @donaldsharp in https://github.com/FRRouting/frr/pull/20944
* bgpd: Fix EVPN-MH route cleanup race condition during interfaces flap by @krishna-samy in https://github.com/FRRouting/frr/pull/20710
* pcep: fix heap buffer overflow by @iurmanj6WIND in https://github.com/FRRouting/frr/pull/20994
* tests: bgp_nhc add test to expose NHC update race on peer changes by @donaldsharp in https://github.com/FRRouting/frr/pull/20949
* bgpd: update on l2attr ecommunity by @lsang6WIND in https://github.com/FRRouting/frr/pull/20980
* ospfd: harden TE/SR TLV iteration against malformed lengths by @Jafaral in https://github.com/FRRouting/frr/pull/21002
* GitHub ci improvements by @Jafaral in https://github.com/FRRouting/frr/pull/21003
* bfdd: Fix wrong memory free when using ttable code by @donaldsharp in https://github.com/FRRouting/frr/pull/21020
* More Neighbor Fixes by @donaldsharp in https://github.com/FRRouting/frr/pull/20934
* yang: Correct pyang errors in frr-pim-candidate.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/21030
* zebra: fix stale remote vtep entries by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/20977
* Bfd QoL improvements by @donaldsharp in https://github.com/FRRouting/frr/pull/21004
* ospf6d: clear local ifp per ECMP path rebuild by @florath in https://github.com/FRRouting/frr/pull/21037
* lib: add rbtree pop_final api by @mjstapp in https://github.com/FRRouting/frr/pull/21034
* doc: bgp: add entry for `neighbor PEER soft-reconfiguration inbound` by @kaffarell in https://github.com/FRRouting/frr/pull/21009
* Fix docker (Alpine) compilation by @ton31337 in https://github.com/FRRouting/frr/pull/21042
* tests: Fix wrong filename and description in test_srv6_locator.py by @cscarpitta in https://github.com/FRRouting/frr/pull/21044
* bgpd: Fix SRv6 SID/locator memory leak in SID notify handler by @cscarpitta in https://github.com/FRRouting/frr/pull/21049
* zebra: Add `no prefix` command for SRv6 locators by @cscarpitta in https://github.com/FRRouting/frr/pull/21048
* Some Yang work by @donaldsharp in https://github.com/FRRouting/frr/pull/21027
* bgpd: fix off-by-one error in FlowSpec operator array bounds check by @Jafaral in https://github.com/FRRouting/frr/pull/21054
* bgpd: Support brief option for show bgp neighbors command by @hnattamaisub in https://github.com/FRRouting/frr/pull/20914
* Docs: Document `import vrf route-map NAME`, several EVPN improvements by @robinchrist in https://github.com/FRRouting/frr/pull/20714
* bgpd: avoid premature memory allocation in subgroup_announce_check() by @enkechen-panw in https://github.com/FRRouting/frr/pull/21005
* bgpd: Add support for BGP-LS (RFC 9552) by @cscarpitta in https://github.com/FRRouting/frr/pull/20470
* bgpd: Fix BGP best path reasoning when using ECMPs with router-id by @ton31337 in https://github.com/FRRouting/frr/pull/21052
* tests: Convert lots of places to use run_and_expect by @donaldsharp in https://github.com/FRRouting/frr/pull/20893
* *: fix spell checks round 6 by @chiragshah6 in https://github.com/FRRouting/frr/pull/21057
* yang: Fix pyang errors in frr-ospf6-route-map.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20991
* lib: fix zclient crash when many peers reconnect after FRR restart by @nick-bouliane in https://github.com/FRRouting/frr/pull/21056
* zebra: Remove neighbor table read on rule addition by @donaldsharp in https://github.com/FRRouting/frr/pull/21053
* bgpd: Fix integer truncation of SRLG count when parsing SRLG TLV by @cscarpitta in https://github.com/FRRouting/frr/pull/21077
* bgpd: Check if the NHC length is enough to fill TLV value + TLV header by @ton31337 in https://github.com/FRRouting/frr/pull/21074
* lib: fix vty_is_closed() falsely reporting VTY_SHELL as closed by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/21082
* lib: use const in vty-is-shell apis by @mjstapp in https://github.com/FRRouting/frr/pull/21094
* bgpd: Fix integer truncation of count when parsing Route Tag TLV by @cscarpitta in https://github.com/FRRouting/frr/pull/21078
* ospfd: fix sequence number check, avoid truncation ambiguity by @Jafaral in https://github.com/FRRouting/frr/pull/21096
* bgpd: Fix late reverse-edge destination linkage in BGP-LS code by @cscarpitta in https://github.com/FRRouting/frr/pull/21109
* nhrpd: Correct addrlen check in os_recvmsg() by @csiltala in https://github.com/FRRouting/frr/pull/21100
* ldpd: improve tlv validation in several places by @mjstapp in https://github.com/FRRouting/frr/pull/21118
* PIM message-handling code fixes by @donaldsharp in https://github.com/FRRouting/frr/pull/21093
* bgpd: Fix issues in BGP-LS node/link/prefix origination by @cscarpitta in https://github.com/FRRouting/frr/pull/21108
* bgpd: fix errors in several paths by @mjstapp in https://github.com/FRRouting/frr/pull/21101
* bgpd: fix I/O thread spinning when peer input queue is full by @kzhang-amzn in https://github.com/FRRouting/frr/pull/21028
* tests: Ensure upstream IIF is in correct state after interface events by @donaldsharp in https://github.com/FRRouting/frr/pull/21114
* lib: fix crash in thread_process_io_inner_loop on stale epoll event by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/21124
* tests: Slow down test_config.py to allow for processing time to happen by @donaldsharp in https://github.com/FRRouting/frr/pull/21127
* isisd: fix edge condition in max_lsp_count computation by @mjstapp in https://github.com/FRRouting/frr/pull/21159
* bgpd: Return 0 if AS4 capability is malformed by @ton31337 in https://github.com/FRRouting/frr/pull/21112
* bgpd: Prevent heap use-after-free for tunnel encapsulation attribute by @ton31337 in https://github.com/FRRouting/frr/pull/21176
* CI:  fix node js deprecation warning, limit mergify backports github ci runs by @Jafaral in https://github.com/FRRouting/frr/pull/21175
* tests: fix grpc_basic xdist collection mismatch by @Jafaral in https://github.com/FRRouting/frr/pull/21158
* bfdd: harden packet validation and reflector handling by @Jafaral in https://github.com/FRRouting/frr/pull/21105
* isisd: fix memory leak in remove_excess_adjs() by @quentinbaradat in https://github.com/FRRouting/frr/pull/21183
* bgpd: include length in cluster_hash_cmp() by @enkechen-panw in https://github.com/FRRouting/frr/pull/20988
* bgpd: add config "nexthop prefer-global" for ipv6 address family by @enkechen-panw in https://github.com/FRRouting/frr/pull/21099
* isisd: Fix missing neighbor address Sub-TLVs after link-params change by @cscarpitta in https://github.com/FRRouting/frr/pull/21204
* bgpd: Free hostname for FQDN capability if the parsing goes wrong by @ton31337 in https://github.com/FRRouting/frr/pull/21043
* bgpd: Do not process route-refresh for AFI/SAFI if it's not negotiated by @ton31337 in https://github.com/FRRouting/frr/pull/21210
* bgpd: fix NHT for explicit link-local BGP peers by @soumyar-roy in https://github.com/FRRouting/frr/pull/21188
* zebra: fix missing vlan change by @anlancs in https://github.com/FRRouting/frr/pull/20350
* bgpd: Validate MP_REACH_NLRI attribute against incorrect next-hop by @ton31337 in https://github.com/FRRouting/frr/pull/21075
* bgpd: harden attribute parsing and packet handling in a few places by @ton31337 in https://github.com/FRRouting/frr/pull/21095
* nhrpd:  harden against malformed packets by @Jafaral in https://github.com/FRRouting/frr/pull/21097
* bgpd: Return original as-path when reconciling AS versus AS4 by @ton31337 in https://github.com/FRRouting/frr/pull/21113
* tests: add EVPN VTEP cleanup and recovery test on uplink flap by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/21126
* bgpd: improve packet parsing for EVPN and ENCAP/VNC by @mjstapp in https://github.com/FRRouting/frr/pull/21098
* bgpd: fix BGP_ATTR_NEXT_HOP flag handling in  bgp_attr_default_set() by @enkechen-panw in https://github.com/FRRouting/frr/pull/21166
* [WIP] nhrpd: guard AFI/table lookups in route resolution by @Jafaral in https://github.com/FRRouting/frr/pull/21187
* bgpd: Fix route-map cleanup ordering in SRv6 unicast SID export by @cscarpitta in https://github.com/FRRouting/frr/pull/21191
* tests: bgp_suppress_duplicates: simplify and split into four tests by @enkechen-panw in https://github.com/FRRouting/frr/pull/21203
* ripd: fix data-handling in several places by @mjstapp in https://github.com/FRRouting/frr/pull/21215
* ripd: fix ip rip send/receive version command by @Shbinging in https://github.com/FRRouting/frr/pull/18217
* bgpd: Fix coverity defects in BGP-LS code by @cscarpitta in https://github.com/FRRouting/frr/pull/21102
* ripngd: fix data handling in several places by @mjstapp in https://github.com/FRRouting/frr/pull/21217
* bfdd: moving bfd socket allocation from static to dynamic by @sougatahitcs in https://github.com/FRRouting/frr/pull/20854
* bgpd: Check if we are not overusing error_data buffer when unknown cap received by @ton31337 in https://github.com/FRRouting/frr/pull/21211
* bgpd: backpressure generic framework by @chiragshah6 in https://github.com/FRRouting/frr/pull/21192
* vrrrpd: improve error handling in several paths by @mjstapp in https://github.com/FRRouting/frr/pull/21251
* bgpd: fix BNC cleanup for explicit link-local peers by @soumyar-roy in https://github.com/FRRouting/frr/pull/21264
* zebra: add debug in route install around nhg not ready by @chiragshah6 in https://github.com/FRRouting/frr/pull/21265
* zebra: Move `allow-external-route-update` to mgmt frontend side by @donaldsharp in https://github.com/FRRouting/frr/pull/21276
* Enable RFC8342 YANG NMDA functionality and add router-id oper-state that uses it. by @choppsv1 in https://github.com/FRRouting/frr/pull/21065
* zebra: lib: use old compatible value for lyd_new_term by @choppsv1 in https://github.com/FRRouting/frr/pull/21281
* bgpd: BGP-LS: add Prefix SID (TLV 1158) by @hedrok in https://github.com/FRRouting/frr/pull/21076
* tests: Fix wrong expectations in `bgp_srv6_unicast` topotest by @cscarpitta in https://github.com/FRRouting/frr/pull/21284
* bgpd: Fix SRv6 SID export route-map update not taking effect by @cscarpitta in https://github.com/FRRouting/frr/pull/21283
* bgpd: Fix incorrect comparisons in BGP-LS *_cmp() functions by @cscarpitta in https://github.com/FRRouting/frr/pull/21285
* pimd: In sparse-dense mode, treat a group as sparse if an RP is configured by @Jafaral in https://github.com/FRRouting/frr/pull/21216
* tests: Give more time for interface information to show up by @donaldsharp in https://github.com/FRRouting/frr/pull/21278
* bgpd: call init, term, copy LS attr admin_group by @mjstapp in https://github.com/FRRouting/frr/pull/21289
* zebra: fix spurious tag mismatch in rib_route_match_ctx() by @enkechen-panw in https://github.com/FRRouting/frr/pull/21293
* bgpd: add brief JSON for ipv4/ipv6 unicast loc-rib by @hnattamaisub in https://github.com/FRRouting/frr/pull/21050
* bgpd: brief JSON for L2VPN EVPN loc-rib by @hnattamaisub in https://github.com/FRRouting/frr/pull/21019
* ospfd, ospf6d: do not install routes for directly attached networks by @rzalamena in https://github.com/FRRouting/frr/pull/20720
* bgpd: Add SRv6 uDT46 SID support for GRT by @cscarpitta in https://github.com/FRRouting/frr/pull/21041
* Move import table around by @donaldsharp in https://github.com/FRRouting/frr/pull/21068
* bgpd: Fix a couple of issues in BGP-LS NLRI encoding/decoding by @cscarpitta in https://github.com/FRRouting/frr/pull/21092
* pceplib, pathd: improve pcep parsing and error-handling by @mjstapp in https://github.com/FRRouting/frr/pull/21208
* lib: fix swapped values, bad setsockopt, and intermittent test failure by @choppsv1 in https://github.com/FRRouting/frr/pull/21214
* bgpd: fix suppress-fib-pending blocking EVPN GR by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/21231
* lib: also compare rmap source address when comparing nexthop source a… by @ak503 in https://github.com/FRRouting/frr/pull/21233
* bgpd: Fix BGP-LS initial TED sync and cleanup on peer deactivation by @cscarpitta in https://github.com/FRRouting/frr/pull/21286
* doc: Update json handling specification in workflow.rst by @donaldsharp in https://github.com/FRRouting/frr/pull/21244
* bgpd: flowspec foobar hardening by @ton31337 in https://github.com/FRRouting/frr/pull/21308
* Soumya/pim allowrp by @soumyar-roy in https://github.com/FRRouting/frr/pull/20326
* pceplib: validate during of_list TLV decoding by @mjstapp in https://github.com/FRRouting/frr/pull/21310
* bgpd: Revalidate locally originated routes against RPKI changes by @ton31337 in https://github.com/FRRouting/frr/pull/21302
* ospf6d: improve/harden packet processing by @mjstapp in https://github.com/FRRouting/frr/pull/21277
* Rpki fix and test improvements by @donaldsharp in https://github.com/FRRouting/frr/pull/21315
* pimd: fix crash due to double free by @Jafaral in https://github.com/FRRouting/frr/pull/21354
* eigrpd: improve validation and error-handling in tlv parsing by @mjstapp in https://github.com/FRRouting/frr/pull/21316
* bgpd: Verify if we correctly parsed BGP-LS attribute by @ton31337 in https://github.com/FRRouting/frr/pull/21344
* bgpd: More validations for labeled unicast and ENCAP attribute by @ton31337 in https://github.com/FRRouting/frr/pull/21343
* bgpd: Reset the stream to attr_start + attribute_len when WITHDRAWN by @ton31337 in https://github.com/FRRouting/frr/pull/21351
* ci: Adjust github workflows (actions) by @ton31337 in https://github.com/FRRouting/frr/pull/21353
* doc: document common daemon options and link -w references by @kaffarell in https://github.com/FRRouting/frr/pull/21342
* bgpd: A couple fixes for NLRI label parsing and flowspec decoding overflow by @ton31337 in https://github.com/FRRouting/frr/pull/21340
* doc: fix indentation error in pim doc by @mjstapp in https://github.com/FRRouting/frr/pull/21373
* bgpd: fix "use-after-free" for updgrp by @anlancs in https://github.com/FRRouting/frr/pull/21081
* bgpd: remove dest list from batch-clearing code by @mjstapp in https://github.com/FRRouting/frr/pull/21382
* bgpd: EVPN json brief optimization by @hnattamaisub in https://github.com/FRRouting/frr/pull/21352
* bgpd: Fix srv6 type parsing and EVPN type-5 NLRI prefix lengh parsing for IPv4 by @ton31337 in https://github.com/FRRouting/frr/pull/21345
* bgpd: Check if Local-Node and Remote-Node TLVs length is within boundaries by @ton31337 in https://github.com/FRRouting/frr/pull/21349
* bgpd: add additional attributes for evpn detail/ipv4/ipv6 detail json by @hnattamaisub in https://github.com/FRRouting/frr/pull/21035
* bgpd: display aggregate->count in show bgp detail for aggregate route by @enkechen-panw in https://github.com/FRRouting/frr/pull/21309
* isisd: improve validation of flex-algo decoder by @mjstapp in https://github.com/FRRouting/frr/pull/21314
* bgpd: Return an error for unknown flowspec component type by @ton31337 in https://github.com/FRRouting/frr/pull/21350
* bgpd: Modify early route processing to include send to zebra by @donaldsharp in https://github.com/FRRouting/frr/pull/21357
* pceplib: add validation to PCEP PST TLV decode by @mjstapp in https://github.com/FRRouting/frr/pull/21372
* bgpd: Fix memory leak for nhc attribute if ipv6 is link-local address by @ton31337 in https://github.com/FRRouting/frr/pull/21377
* tests: Fix time re in all_protocol_startup/test_all_protocol_startup  by @hedrok in https://github.com/FRRouting/frr/pull/21378
* doc: fix BGP interface neighbor IPv4, IPv6, and v6only documentation by @nick-bouliane in https://github.com/FRRouting/frr/pull/21383
* zebra: EVPN prevent stale mbr_zifs entries from early return by @chiragshah6 in https://github.com/FRRouting/frr/pull/21391
* staticd: fix static_disable_vrf() to always send a route DELETE by @enkechen-panw in https://github.com/FRRouting/frr/pull/21392
* bgpd: Do not allocate stream if route-refresh capability is not received by @ton31337 in https://github.com/FRRouting/frr/pull/21394
* bgpd: Check dynamic capability action before validating ENHE capability by @ton31337 in https://github.com/FRRouting/frr/pull/21395
* bgpd: fix wrong overwritten for evpn by @anlancs in https://github.com/FRRouting/frr/pull/21398
* bgpd: Do not allow triggering route-refresh path with a malformed ORF length by @ton31337 in https://github.com/FRRouting/frr/pull/21399
* tools: Upgrade configuration to current format for Mergify by @ton31337 in https://github.com/FRRouting/frr/pull/21409
* topotests: split bgp_evpn_mh_v4_v6_num v4/v6 layout by @ashred-lnx in https://github.com/FRRouting/frr/pull/21389
* doc: fix SRv6 route commands by @iurmanj6WIND in https://github.com/FRRouting/frr/pull/21416
* pimd: guard channel OIL detach against stale pointers by @Jafaral in https://github.com/FRRouting/frr/pull/21431
* yang: Correct pyang errors in frr-pim-route-map.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/21433
* doc: fix SRv6 route commands (bis) by @iurmanj6WIND in https://github.com/FRRouting/frr/pull/21432
* bgpd: Fix copy-paste error in SRv6 DT46 SID duplicate install check (CID 1670455) by @cscarpitta in https://github.com/FRRouting/frr/pull/21443
* bgpd,lib,zebra: use explicit casts in tracepoint definitions by @mjstapp in https://github.com/FRRouting/frr/pull/21438
* bgpd: Skip oversized BGP-LS Node and Link Name TLVs by @cscarpitta in https://github.com/FRRouting/frr/pull/21455
* pimd: `pim_inet4_dump` -> `%pI4s` by @eqvinox in https://github.com/FRRouting/frr/pull/21458
* bgpd: Use `%pI4/%pI6` formatters in BGP-LS NLRI display by @cscarpitta in https://github.com/FRRouting/frr/pull/21456
* bgpd: Fix wrong union member access in `bgp_ls_nlri_display()` by @cscarpitta in https://github.com/FRRouting/frr/pull/21453
* bgpd: Allow overriding "remote-as" per-neighbor by @ton31337 in https://github.com/FRRouting/frr/pull/21450
* zebra: remove kernel route on last address deletion by @hedrok in https://github.com/FRRouting/frr/pull/19564
* bfdd: avoid prefix-list memory allocation in bfd to solve oom issue by @sougatahitcs in https://github.com/FRRouting/frr/pull/21073
* watchfrr,tools: add --collect-core to core dump unresponsive daemon by @nishant111 in https://github.com/FRRouting/frr/pull/21051
* bgpd: remove unreachable json_paths free in evpn_show_all_routes() by @Jafaral in https://github.com/FRRouting/frr/pull/21461
* bfdd: bfd tx timeout topotest cleanup by @sougatahitcs in https://github.com/FRRouting/frr/pull/21026
* ripd,yang: log neighbor events by @rzalamena in https://github.com/FRRouting/frr/pull/21442
* ci: gate github-ci  Build/Test jobs on non-doc paths; add HTML doc job by @Jafaral in https://github.com/FRRouting/frr/pull/21475
* Mgmt frontend problems in zebra by @donaldsharp in https://github.com/FRRouting/frr/pull/21252
* ospf6d: Remove ospf6 route when connected wins by @donaldsharp in https://github.com/FRRouting/frr/pull/21476
* pceplib: obj is already de-refed, no need to check for NULL by @donaldsharp in https://github.com/FRRouting/frr/pull/21462
* zebra: support brief json for show ip route command by @hnattamaisub in https://github.com/FRRouting/frr/pull/20950
* mgmtd: align commit config request argument order by @Babaijan in https://github.com/FRRouting/frr/pull/21483
* pceplib: ignore NULL obj in free_obj api by @mjstapp in https://github.com/FRRouting/frr/pull/21487
* staticd: fix static_cleanup_vrf() nexthop-VRF removal  ordering by @enkechen-panw in https://github.com/FRRouting/frr/pull/21413
* bgpd: fix last Reset timer losing day part after 24 hours by @soumyar-roy in https://github.com/FRRouting/frr/pull/21489
* ospfd: add validation in several places before accessing message bodies by @mjstapp in https://github.com/FRRouting/frr/pull/21303
* pimd: fix NOCACHE MFC resync detection log, add vrf name too by @Jafaral in https://github.com/FRRouting/frr/pull/21481
* doc: refresh README with project links, badges, and contributor notes by @Jafaral in https://github.com/FRRouting/frr/pull/21499
* bgpd: Avoid unnecessary code path for brief command flow by @hnattamaisub in https://github.com/FRRouting/frr/pull/21412
* fix unnecessary BGP peer re-establishment in confederation by @wangdan1323 in https://github.com/FRRouting/frr/pull/21439
* Watchfrr phased restart by @donaldsharp in https://github.com/FRRouting/frr/pull/21460
* lib: mgmt: expose short-circuit bool as `is_mgmtd` by @choppsv1 in https://github.com/FRRouting/frr/pull/21508
* bgpd: Support established and failed options for show bgp neighbor co… by @hnattamaisub in https://github.com/FRRouting/frr/pull/21066
* zebra: add numMacs and numArpNd to L3 VNI detail output by @sougatahitcs in https://github.com/FRRouting/frr/pull/21263
* pimd: improve logging in a few places by @Jafaral in https://github.com/FRRouting/frr/pull/21356
* tests: clean up a build warning in a unit-test by @mjstapp in https://github.com/FRRouting/frr/pull/21509
* zebra: convert EVPN neigh hashes to `typesafe` (+`.h` cleanups) by @eqvinox in https://github.com/FRRouting/frr/pull/21388
* tests: Use abs_srcdir for tests. by @jkroonza in https://github.com/FRRouting/frr/pull/21390
* bgpd: add configurable advertisement delay for suppress-fib-pending by @deepak-singhal0408 in https://github.com/FRRouting/frr/pull/21384
* zebra: fix wrong hash count function call by @rzalamena in https://github.com/FRRouting/frr/pull/21512
* bgpd: Fix mixed remote-as for peer-groups when using auto by @ton31337 in https://github.com/FRRouting/frr/pull/21406
* bgpd: Don't mark nexthop as changed if a set next-hop unchanged is applied by @ton31337 in https://github.com/FRRouting/frr/pull/21445
* tests: update .gitignore for isis test by @mjstapp in https://github.com/FRRouting/frr/pull/21530
* tests: Check if IPv6 MTU change is triggering BGP updates correctly by @ton31337 in https://github.com/FRRouting/frr/pull/21500
* bgpd: PMSI tunnel attribute compatibility by @mjstapp in https://github.com/FRRouting/frr/pull/21507
* ospfd: add LSA validation in the apiserver path by @mjstapp in https://github.com/FRRouting/frr/pull/21536
* eigrpd: reject invalid prefix mask len by @mjstapp in https://github.com/FRRouting/frr/pull/21539
* eigrpd: enforce minimum TLV length in Hello handler by @TristanInSec in https://github.com/FRRouting/frr/pull/21543
* isisd: use correct min size values for srv6 subtlvs by @mjstapp in https://github.com/FRRouting/frr/pull/21540
* bgp_evpn: fix memleak when configuring rd by @lsang6WIND in https://github.com/FRRouting/frr/pull/21566
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values by @hnattamaisub in https://github.com/FRRouting/frr/pull/21559
* bgpd: Replace the actual local-as when using replace-as with the confederation by @ton31337 in https://github.com/FRRouting/frr/pull/21551
* lib: northbound: distinguish unknown schema node from key mismatch by @reinaldosaraiva in https://github.com/FRRouting/frr/pull/21534
* bfdd: Move bfdproflist declaration to header by @pguibert6WIND in https://github.com/FRRouting/frr/pull/21518
* ospfd,tests: fix OSPF connected overlapping prefix bug by @rzalamena in https://github.com/FRRouting/frr/pull/21510
* bgpd: Print neighbor link type correctly according to local-as by @ton31337 in https://github.com/FRRouting/frr/pull/21486
* ospf6d: update auth sequence number after validating digest by @mjstapp in https://github.com/FRRouting/frr/pull/21588
* isisd: Preserve flags when copying SRv6 End SID sub-TLV by @cscarpitta in https://github.com/FRRouting/frr/pull/21584
* eigrpd: fix byte order in Hello authentication decode by @TristanInSec in https://github.com/FRRouting/frr/pull/21545
* lib: Report IPv6 MTU and not IPv4 for if_update_state_mtu6 by @ton31337 in https://github.com/FRRouting/frr/pull/21501
* bgpd: Prevent out-of-bound reading handling soft version dynamic capability by @ton31337 in https://github.com/FRRouting/frr/pull/21602
* bgpd: fix valgrind memory leaks on daemon shutdown by @soumyar-roy in https://github.com/FRRouting/frr/pull/21511
* isisd: continue hardening SRV6 tlv parsing by @mjstapp in https://github.com/FRRouting/frr/pull/21585
* Add new BGP SRv6L3VPN sid configuration test / Add associate test by @pguibert6WIND in https://github.com/FRRouting/frr/pull/21386
* bgpd: Dynamic capability parsing fixes by @ton31337 in https://github.com/FRRouting/frr/pull/21603
* nhrpd: stop debugging auth credentials by @mjstapp in https://github.com/FRRouting/frr/pull/21615
* bgpd: Consolidate redundant stream bounds checks in `bgp_ls_decode_nlri` by @cscarpitta in https://github.com/FRRouting/frr/pull/21607
* bgpd: Harden SRv6 Service Data parser for SID Structure length by @cscarpitta in https://github.com/FRRouting/frr/pull/21612
* bgpd: Clearly check for AS4 against 0 value by @ton31337 in https://github.com/FRRouting/frr/pull/21610
* isisd: consume leftover bytes after FAD sub-sub-TLV loop by @TristanInSec in https://github.com/FRRouting/frr/pull/21544
* bgpd: Prevent zero-length BGP-LS MT-ID TLV by @cscarpitta in https://github.com/FRRouting/frr/pull/21600
* bgpd: Reject BGP-LS Link NLRIs without Link Descriptor by @cscarpitta in https://github.com/FRRouting/frr/pull/21609
* tests: Remove `show running bgpd` from the topotests by @donaldsharp in https://github.com/FRRouting/frr/pull/21629
* Coverity cleanup some more items found by @donaldsharp in https://github.com/FRRouting/frr/pull/21627
* isisd: correct SRv6 End.X SID minimum size constants by @TristanInSec in https://github.com/FRRouting/frr/pull/21541
* bgpd: honor 'no activate' for dynamic neighbors in peer-group by @enissim in https://github.com/FRRouting/frr/pull/21658
* lib: mgmt: use SOMAXCONN for mgmtd socket listen backlog by @reinaldosaraiva in https://github.com/FRRouting/frr/pull/21514
* bgpd: Simplify BGP-LS NLRI TLV encoding by inlining helper functions by @cscarpitta in https://github.com/FRRouting/frr/pull/21657
* bgpd: migrate timers during peer_xfer_conn to fix stale route cleanup by @shashanka-ks in https://github.com/FRRouting/frr/pull/21558
* bgpd: Validate if NHC BGPID TLV value is non-zero by @ton31337 in https://github.com/FRRouting/frr/pull/21611
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero by @cscarpitta in https://github.com/FRRouting/frr/pull/21641
* tests: bgp_suppress_fib was not stable before testing by @donaldsharp in https://github.com/FRRouting/frr/pull/21649
* bgpd: Do not allocate NHC TLV with an extra trailer by @ton31337 in https://github.com/FRRouting/frr/pull/21606
* bgpd: Avoid having a dangling pointer after we free NHC attribute by @ton31337 in https://github.com/FRRouting/frr/pull/21605
* bgpd: v4/v6 neigh advertised & received routes brief json by @hnattamaisub in https://github.com/FRRouting/frr/pull/21411
* tests: Update pytestmark value in scripts by @donaldsharp in https://github.com/FRRouting/frr/pull/21684
* static route bfd admin down state handling improvements by @sougatahitcs in https://github.com/FRRouting/frr/pull/21400
* bgpd: add advertisement-delay to hold route advertisements after startup by @karthikeyav in https://github.com/FRRouting/frr/pull/21430
* bgpd: Add support for BGP-LS for BGP fabric by @cscarpitta in https://github.com/FRRouting/frr/pull/20726
* tests: fix uptime check in test_bgp_default_originate_2links.py by @enkechen-panw in https://github.com/FRRouting/frr/pull/21480
* bgpd: Do not reject the route if confederation AS matches peer AS by @ton31337 in https://github.com/FRRouting/frr/pull/21532
* isisd: Use LAN End.X context for SRv6 sub-sub-TLV parsing by @cscarpitta in https://github.com/FRRouting/frr/pull/21589
* bgpd: Add BGP_AIGP_TLV_MIN_LEN constant to easily read what it is by @ton31337 in https://github.com/FRRouting/frr/pull/21608
* isisd: validate ASLA sub-sub-TLV length before consuming bytes by @TristanInSec in https://github.com/FRRouting/frr/pull/21542
* pimd: reject truncated IP datagrams before IGMP/mtrace handling by @Jafaral in https://github.com/FRRouting/frr/pull/21705
* lib: fix mgmt_msg recv to deal with mis-alignment by @choppsv1 in https://github.com/FRRouting/frr/pull/21651
* isisd: Reject duplicate SRv6 SID Structure Sub-Sub-TLV by @cscarpitta in https://github.com/FRRouting/frr/pull/21656
* Pim fixes in test by @donaldsharp in https://github.com/FRRouting/frr/pull/21691
* ospfd: Fix setting of type by @donaldsharp in https://github.com/FRRouting/frr/pull/21712
* pimd: cap PIM Hello secondary address list parsing by @Jafaral in https://github.com/FRRouting/frr/pull/21707
* tests: Ensure test_bgp_vpnv4_per_nexthop_label.py actually has a chance by @donaldsharp in https://github.com/FRRouting/frr/pull/21699
* zebra: fix EVPN MACIP DEL flag mixup in neighbor delete path by @nick-bouliane in https://github.com/FRRouting/frr/pull/21733
* bgpd: move auto config flag from bgp to srv6 unicast policy by @lsang6WIND in https://github.com/FRRouting/frr/pull/21735
* bgpd: Fixed crash in bgp received-routes detail json and code cleanup by @sougatahitcs in https://github.com/FRRouting/frr/pull/20930
* bgpd: Use `BGP_LS_TLV_SET` macro to set `present_tlvs` bits by @cscarpitta in https://github.com/FRRouting/frr/pull/21604
* BFD miscellaneous fixes by @pguibert6WIND in https://github.com/FRRouting/frr/pull/21613
* bgpd: Replace `BGP_LS_TLV_*` macros with standard FRR `FLAG` macros by @cscarpitta in https://github.com/FRRouting/frr/pull/21755
* nhrpd: improve validation in packet parsing by @mjstapp in https://github.com/FRRouting/frr/pull/21686
* pimd: harden BSM group/RP parsing paths by @Jafaral in https://github.com/FRRouting/frr/pull/21734
* pimd: fix crash in JP agg list due to stale upstream entry by @soumyar-roy in https://github.com/FRRouting/frr/pull/21704
* pimd: Provide better ordering for calling pim_upstream_use_rpt by @donaldsharp in https://github.com/FRRouting/frr/pull/21764
* bgpd: fix NHT for link-local nexthops from global-address peers by @soumyar-roy in https://github.com/FRRouting/frr/pull/21687
* bgpd: dynamic neighbors not up with md5 in non default vrf by @hnattamaisub in https://github.com/FRRouting/frr/pull/21467
* zebra: Fix incorrect update of 'nhe_received' in route_entry_update_nhe() by @GaladrielZhao in https://github.com/FRRouting/frr/pull/21104
* ospf6d: reinstall routes after zebra reconnect by @florath in https://github.com/FRRouting/frr/pull/21011
* Gre fixes by @pguibert6WIND in https://github.com/FRRouting/frr/pull/21300
* bgpd: Add json support for show bgp vrfs cmd by @sougatahitcs in https://github.com/FRRouting/frr/pull/21485
* bgpd: Add some defences for AS4/ENCAP handling by @ton31337 in https://github.com/FRRouting/frr/pull/21777
* add successful commit info msg by @choppsv1 in https://github.com/FRRouting/frr/pull/21711
* bgpd: fix aggregate->count undercount when dampening is cleared by @enkechen-panw in https://github.com/FRRouting/frr/pull/21786
* Bgp crashes by @donaldsharp in https://github.com/FRRouting/frr/pull/21778
* lib, isisd, bgpd: BGP-LS add several tlvs by @hedrok in https://github.com/FRRouting/frr/pull/21376
* tests: Remove invalid link-params command from BGP-LS topotest configs by @cscarpitta in https://github.com/FRRouting/frr/pull/21793
* *: consolidate sockopt_ apis in sockopt.c module by @mjstapp in https://github.com/FRRouting/frr/pull/21746
* tests: Add `evpn` pytestmark to tests that are missing by @donaldsharp in https://github.com/FRRouting/frr/pull/21782
* bgpd: fix shutdown crash by restricting evpn cleanup to owner instance by @soumyar-roy in https://github.com/FRRouting/frr/pull/21698
* ospf6d: packet- and auth-handling improvements by @mjstapp in https://github.com/FRRouting/frr/pull/21783
* pathd: add optional params to `no` cmd versions for frr-reload by @hedrok in https://github.com/FRRouting/frr/pull/21710
* tests: Fix zebra_vrf_netns topotest by @donaldsharp in https://github.com/FRRouting/frr/pull/21741
* *: Support gcc 15 by @mjstapp in https://github.com/FRRouting/frr/pull/21812
* zebra: fix memleak in ip import-table rmap by @chiragshah6 in https://github.com/FRRouting/frr/pull/21811
* Some more bgp connection rework by @donaldsharp in https://github.com/FRRouting/frr/pull/21810
* tests: Catch core dumps *after* teardown has completed by @donaldsharp in https://github.com/FRRouting/frr/pull/21697
* bgpd: fix aggregate->count not decremented when route is dampened by @enkechen-panw in https://github.com/FRRouting/frr/pull/21787
* zebra: Allow quick flaps of interfaces to be handled properly in next… by @donaldsharp in https://github.com/FRRouting/frr/pull/21769
* mgmtd: add periodic notify mode with mode/mode_data and FE test support by @ashred-lnx in https://github.com/FRRouting/frr/pull/21253
* bgpd: Treat malformed BGP-LS TLV as NLRI discard per RFC 9552 by @cscarpitta in https://github.com/FRRouting/frr/pull/21827
* tests: Fix invalid escape warning in BGP-LS test by @cscarpitta in https://github.com/FRRouting/frr/pull/21829
* tests: Fix invalid ISIS max-lsp-lifetime in BGP-LS configs by @cscarpitta in https://github.com/FRRouting/frr/pull/21828
* bgpd: Reject BGP-LS node/link names containing non-printable characters by @cscarpitta in https://github.com/FRRouting/frr/pull/21825
* tests: bgp_community_change_update: use receivedPrefixDup counter by @enkechen-panw in https://github.com/FRRouting/frr/pull/21816
* bgpd: fix aggregate->count errors in ZAPI route notifications by @enkechen-panw in https://github.com/FRRouting/frr/pull/21789
* bgpd: fix EVPN VRF auto RT deletion collision by @kaffarell in https://github.com/FRRouting/frr/pull/21808
* bgpd: set mp_nexthop_len consistently in  subgroup_default_originate() by @enkechen-panw in https://github.com/FRRouting/frr/pull/21840
* staticd: nexthop identity as path-list key, and per-route metric by @enkechen-panw in https://github.com/FRRouting/frr/pull/21296
* bgpd: EVPN rd all or specific rd options based route table  by @chiragshah6 in https://github.com/FRRouting/frr/pull/21843
* Startup after crash issues by @donaldsharp in https://github.com/FRRouting/frr/pull/21550
* bfdd: avoid close(-1) in bfd_dplane_finish_late by @sougatahitcs in https://github.com/FRRouting/frr/pull/21841
* Sockunion cmp wrong by @donaldsharp in https://github.com/FRRouting/frr/pull/21833
* bgpd: fix F-bit incorrectly set after port flap   by @shashanka-ks in https://github.com/FRRouting/frr/pull/21839
* bgpd: enforce guards consistently at aggregate count entry points by @enkechen-panw in https://github.com/FRRouting/frr/pull/21837
* bgpd: send dynamic ENHE capability to peer-group members by @hnattamaisub in https://github.com/FRRouting/frr/pull/21817
* zebra: add json support for svd vxlan type by @sougatahitcs in https://github.com/FRRouting/frr/pull/20886
* bgpd: add detail json fields for v4/v6 neigh adver & recev routes by @sougatahitcs in https://github.com/FRRouting/frr/pull/20951
* docs: evpn: Add new Linux VXLAN Dataplane section by @robinchrist in https://github.com/FRRouting/frr/pull/21664
* zebra: align ctx nh cursor with RIB when skipping DUPLICATE nexthops by @hnattamaisub in https://github.com/FRRouting/frr/pull/21709
* pimd: validate PIM LAN sources and cap neighbors by @Jafaral in https://github.com/FRRouting/frr/pull/21747
* zebra: tear down old L3VNI before adding new one on VNI value change by @enissim in https://github.com/FRRouting/frr/pull/21757
* lib: bound masklen values, don't assert by @mjstapp in https://github.com/FRRouting/frr/pull/21628
* ospfd: add instance shutdown command by @rzalamena in https://github.com/FRRouting/frr/pull/21759
* bgpd: use bgp_node_match() instead of bgp_node_get() in aggregate count by @enkechen-panw in https://github.com/FRRouting/frr/pull/21862
* bgpd: Add BGP-LS Extensions for SRv6 (RFC 9514) by @cscarpitta in https://github.com/FRRouting/frr/pull/21830
* bgpd: warmboot failure when wfi enabled by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/21818
* bgpd: Allow `no network ....` form for safi = EVPN or MPLS_VPN by @donaldsharp in https://github.com/FRRouting/frr/pull/21860
* bgpd: Skip route clearing for peers that were never established by @krishna-samy in https://github.com/FRRouting/frr/pull/21867
* bgpd: A couple link-state nits by @ton31337 in https://github.com/FRRouting/frr/pull/21842
* zebra: route EVPN FDB/neighbor reads through dplane by @rjarry in https://github.com/FRRouting/frr/pull/21206
* bgpd: add EVPN local RT-2 MAC+IP leaking to unicast by @louis-6wind in https://github.com/FRRouting/frr/pull/20005
* yang: allow match-metric value of zero by @mjstapp in https://github.com/FRRouting/frr/pull/21888
* *: don't use static char buffer in srv6 zapi code by @mjstapp in https://github.com/FRRouting/frr/pull/21884
* ospf6d: Fix command output for default route by @hedrok in https://github.com/FRRouting/frr/pull/21886
* bgpd: Remove redundant BGP-LS NLRI forward declarations by @cscarpitta in https://github.com/FRRouting/frr/pull/21895
* Memory leak problems. by @donaldsharp in https://github.com/FRRouting/frr/pull/21844
* debian: add pkg.frr.tcmalloc build profile for tcmalloc support by @rminnikanti in https://github.com/FRRouting/frr/pull/21866
* doc: fix spell check in developer and user rst guide by @chiragshah6 in https://github.com/FRRouting/frr/pull/21901
* bgpd: Reject malformed SRv6 End.X sub-TLV payloads with leftover bytes by @cscarpitta in https://github.com/FRRouting/frr/pull/21904
* zebra: Fix docstr mismatches in show ip route by @mhrn83 in https://github.com/FRRouting/frr/pull/21865
* Log file cleanup by @donaldsharp in https://github.com/FRRouting/frr/pull/21907
* bgpd: only use srv6_l3service attr if it's present by @mjstapp in https://github.com/FRRouting/frr/pull/21916
* bgpd: fix aggregate route not removed on de-configuration by @enkechen-panw in https://github.com/FRRouting/frr/pull/21025
* bgpd: Use ST token for BGP-LS STATIC protocol in NLRI output by @cscarpitta in https://github.com/FRRouting/frr/pull/21909
* bgpd: Fix incorrect BGP_PATH_MULTIPATH flag when route becomes invalid by @yuxuehong in https://github.com/FRRouting/frr/pull/21106
* tools: Add bfd commands to support bundle generation by @donaldsharp in https://github.com/FRRouting/frr/pull/21914
* pimd: Auto-RP hardening for discovery and announcements by @Jafaral in https://github.com/FRRouting/frr/pull/21745
* bgpd: Fix missing Multi-Topology ID in BGP-LS NLRIs by @cscarpitta in https://github.com/FRRouting/frr/pull/21910
* ospfd: Implement rfc4222 Recommendation 1 and 2 by @dfedyk in https://github.com/FRRouting/frr/pull/20936
* pimd: MLAG: skip pim_register_join on non-DR by @hnattamaisub in https://github.com/FRRouting/frr/pull/21920
* bgpd: validate SRV6 service sid transposition values by @mjstapp in https://github.com/FRRouting/frr/pull/21903
* bgpd: delete GR stale routes when nexthop becomes unreachable by @karthikeyav in https://github.com/FRRouting/frr/pull/21742
* bgpd: Initialize BGP-LS Node MSD only after parsing it by @cscarpitta in https://github.com/FRRouting/frr/pull/21929
* bgpd: Harden BGP-LS Node NLRI descriptor length validation by @cscarpitta in https://github.com/FRRouting/frr/pull/21938
* lib: add missing hook_unregister_arg in mgmt_be_client_destroy by @routingrocks in https://github.com/FRRouting/frr/pull/21940
* zebra: show nexthop-group rib brief json by @hnattamaisub in https://github.com/FRRouting/frr/pull/20953
* bgpd: support brief json for bgp v4 and v6 neighbors route by @hnattamaisub in https://github.com/FRRouting/frr/pull/21414
* lib,pceplib: fix DNS resolver and PCEP memory leaks by @jaredmauch in https://github.com/FRRouting/frr/pull/20034
* Tc dplane conversion by @donaldsharp in https://github.com/FRRouting/frr/pull/21883
* Fix event bugs in ldpd/lib and fix bgp_bmp misshandling of memory that leads to a crash by @donaldsharp in https://github.com/FRRouting/frr/pull/21952
* bgpd: Add route-map based allowas-in for flexible route filtering by @karthikeyav in https://github.com/FRRouting/frr/pull/20659
* pimd: Fix crash when up->channel_oil is NULL by @usrivastava-nvidia in https://github.com/FRRouting/frr/pull/21961
* zebra: Get link from the correct netns for vxlan by @leonshaw in https://github.com/FRRouting/frr/pull/8895
* ospfd: eliminate direct origination of Type-5 LSAs on NSSA routers by @rzalamena in https://github.com/FRRouting/frr/pull/20894
* zebra: fix EVPN zero-RMAC in some situations by @chdxD1 in https://github.com/FRRouting/frr/pull/21448
* bgpd: Move some optional feature-specific attributes from struct attr to struct attr_extra by @ton31337 in https://github.com/FRRouting/frr/pull/21859
* ospf6d: fix missing updating the global table by @anlancs in https://github.com/FRRouting/frr/pull/21960
* bgpd: cancel LLGR stale timer on peer AF delete by @Z-Yivon in https://github.com/FRRouting/frr/pull/21947
* topotests: Add a topotest for the no bgp client-to-client reflection command by @PierreNeltner6WIND in https://github.com/FRRouting/frr/pull/21754
* bgpd: limit GR-stale NHT-unreach delete to GR helper context by @karthikeyav in https://github.com/FRRouting/frr/pull/21942
* bgpd: cancel BFD strict hold timer on peer delete by @Z-Yivon in https://github.com/FRRouting/frr/pull/21926
* bgpd: skip stalepath-timer clear for LLGR-negotiated AFI/SAFIs by @hnattamaisub in https://github.com/FRRouting/frr/pull/21932
* *: small fixes roll-up pile by @eqvinox in https://github.com/FRRouting/frr/pull/21957
* lib: remove netns_other.c (unused) by @eqvinox in https://github.com/FRRouting/frr/pull/21973
* tests: Add VRF support for check_ping command by @ton31337 in https://github.com/FRRouting/frr/pull/21753
* bgpd: Fix missing SRv6 advertisement with `distribute bgp-fabric-link-state` by @cscarpitta in https://github.com/FRRouting/frr/pull/21912
* bgpd: Format IGP Router-ID in BGP-LS NLRI based on protocol by @cscarpitta in https://github.com/FRRouting/frr/pull/21908
* bgpd: Fix BGP-LS Attribute Node Name TLV by @cscarpitta in https://github.com/FRRouting/frr/pull/21951
* *: GCC 16 warnings by @eqvinox in https://github.com/FRRouting/frr/pull/21985
* bgpd: BGPd crash due to multiple bnc entry linked to same peer. by @usrivastava-nvidia in https://github.com/FRRouting/frr/pull/21962
* bgpd: preserve IPv6 nexthops when importing EVPN IPv4 routes by @kaffarell in https://github.com/FRRouting/frr/pull/21958
* ospfd: remove unnecessary space by @anlancs in https://github.com/FRRouting/frr/pull/21979
* bgpd: initialise nh_flag attribute by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/21498
* bgpd: Check boundaries when parsing NHC and Prefix SID attributes by @ton31337 in https://github.com/FRRouting/frr/pull/21981
* bgpd: Fix GR helper retaining stale routes after Hard Reset by @selva-nexthop in https://github.com/FRRouting/frr/pull/21823
* tools: Revert 'no interface' when no configuration for interface left by @hedrok in https://github.com/FRRouting/frr/pull/20378
* ospfd: quick neighbor feature with BFD by @nabahr in https://github.com/FRRouting/frr/pull/21784
* ospf6d: only allow positive time strings by @jeremie6wind in https://github.com/FRRouting/frr/pull/21928
* bgpd: validate rfapi subtlv before accessing data octets by @mjstapp in https://github.com/FRRouting/frr/pull/21974
* zebra: clean up VRF handling by using dataplane provided vrf_id by @maxime-leroy in https://github.com/FRRouting/frr/pull/20318
* lib, zebra: bound SRv6 locator name length in ZAPI by @jamestiotio in https://github.com/FRRouting/frr/pull/21868
* bgpd: random format string fixes by @eqvinox in https://github.com/FRRouting/frr/pull/21999
* bgpd: fix AS-path routemap corruption and stale multipath on bestpath, fix tests by @donaldsharp in https://github.com/FRRouting/frr/pull/21982
* bgpd: Fix missing SRv6 unicast SID cleanup on locator delete by @cscarpitta in https://github.com/FRRouting/frr/pull/21948
* BFD authentication support by @pguibert6WIND in https://github.com/FRRouting/frr/pull/21678
* topotests: fix parallel run hangs (mutini teardown, ExaBGP FIFO, Docker hosts) by @Jafaral in https://github.com/FRRouting/frr/pull/22007
* ci: fail topotest step when parallel run lacks JUnit failures by @Jafaral in https://github.com/FRRouting/frr/pull/22011
* tests: Use `show module` to get bgp's pid by @donaldsharp in https://github.com/FRRouting/frr/pull/22023
* lib: warn once when process fd limit is very large by @Jafaral in https://github.com/FRRouting/frr/pull/22031
* pimd: fix shared-LAN (S,G) MFC loop and expand ssm topotest by @Jafaral in https://github.com/FRRouting/frr/pull/21998
* ospfd: prevent stale LSA from corrupting local OSPF DB after reboot by @Jafaral in https://github.com/FRRouting/frr/pull/20601
* pimd: add IGMP/MLD proxy route-map filtering by @Jafaral in https://github.com/FRRouting/frr/pull/21906
* Fix keychain acceptance in BFD authentication by @donaldsharp in https://github.com/FRRouting/frr/pull/22028
* bgpd: fix attr comparison when using attr_intern_reuse cache by @mjstapp in https://github.com/FRRouting/frr/pull/22008
* bgpd: Fix stack overflow when debug printing label information & BMP code by @ton31337 in https://github.com/FRRouting/frr/pull/22056
* bgpd: Move OTC and IPv6 extended community attributes to attr_extra by @ton31337 in https://github.com/FRRouting/frr/pull/22021
* staticd: add 'show static routes' command by @kaffarell in https://github.com/FRRouting/frr/pull/21232
* ripd: add full RTE bounds check to response/request processing loops by @DeadPackets in https://github.com/FRRouting/frr/pull/21889
* pceplib: Validate lengths during object decoding by @mjstapp in https://github.com/FRRouting/frr/pull/22032
* tests: fix flaky IGMP source baseline in pim_boundary_acl by @Jafaral in https://github.com/FRRouting/frr/pull/22055
* pimd: move dense (S,G) to sparse mode when an RP is added by @Jafaral in https://github.com/FRRouting/frr/pull/20003
* tests: harden bgp_conditional_advertisement_track_peer convergence waits by @Jafaral in https://github.com/FRRouting/frr/pull/22057
* pimd: fix AutoRP stale RPs and selective multicast joins, add missing docs by @Jafaral in https://github.com/FRRouting/frr/pull/22039
* bgpd: bmp: don't prepend local-AS to AS_PATH in BMP updates by @kalash-nexthop in https://github.com/FRRouting/frr/pull/21815
* pimd,tests: refactor PIM join prune packet generation by @rzalamena in https://github.com/FRRouting/frr/pull/21795
* zebra: fix neighbor entries ns_id by @louis-6wind in https://github.com/FRRouting/frr/pull/22034
* Cleanup of memory allocation and usage of events by @donaldsharp in https://github.com/FRRouting/frr/pull/21943
* zebra: fix DVNI route encap type for IPv6 VTEPs by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/21911
* No kernel nhg original by @donaldsharp in https://github.com/FRRouting/frr/pull/21893
* bgpd: Fix use-after-free for ORF case by @ton31337 in https://github.com/FRRouting/frr/pull/22080
* zebra: Track netlink carrier changes value by @donaldsharp in https://github.com/FRRouting/frr/pull/22084
* In a removal operation do not allow a creation of the route_node in bgp by @donaldsharp in https://github.com/FRRouting/frr/pull/21878
* bgpd: Move srte_color from attr struct to bgp_path_info_extra by @ton31337 in https://github.com/FRRouting/frr/pull/22059
* Revert "bgpd: do not flag old best as multipath when it is also the n… by @donaldsharp in https://github.com/FRRouting/frr/pull/22095
* bgpd: Move link_bw from attr_extra to bgp_path_info_extra by @ton31337 in https://github.com/FRRouting/frr/pull/22093
* bgpd: Skip route-map LPM optimisation for AF_FLOWSPEC by @ton31337 in https://github.com/FRRouting/frr/pull/22083
* bgpd: Fix infinite loop in MRT route dump for oversized paths by @ton31337 in https://github.com/FRRouting/frr/pull/22082
* tests: reap mutini zombies and skip post-teardown support bundles by @Jafaral in https://github.com/FRRouting/frr/pull/22096
* build, lib, zebra: OpenBSD fixes by @eqvinox in https://github.com/FRRouting/frr/pull/22009
* tests: add multi-edit test with commit for mgmtd by @choppsv1 in https://github.com/FRRouting/frr/pull/22010
* zebra: fix missing cleaning vni entry by @anlancs in https://github.com/FRRouting/frr/pull/22079
* tests: fix grpc topotest xdist collection mismatch in CI  by @Jafaral in https://github.com/FRRouting/frr/pull/22048
* tests: harden topotest gcov coverage setup and reporting by @Jafaral in https://github.com/FRRouting/frr/pull/22104
* Fix some topotest skipping problems by @donaldsharp in https://github.com/FRRouting/frr/pull/22113
* pimd: fix AutoRP holdtime parsing and minor cleanup by @Jafaral in https://github.com/FRRouting/frr/pull/22120
* docker: Add snmptrapd to list of thingies to install by @donaldsharp in https://github.com/FRRouting/frr/pull/22125
* bgpd: Cleanup debug memory on shutdown by @donaldsharp in https://github.com/FRRouting/frr/pull/22123
* tests: Remove unknown `pytest.mark.tools` by @donaldsharp in https://github.com/FRRouting/frr/pull/22114
* bgpd: Add vrf name to more bestpath debugs by @donaldsharp in https://github.com/FRRouting/frr/pull/22124
* tests: fix bgp_soo topotest by separating IPv4/IPv6 address families by @enkechen-panw in https://github.com/FRRouting/frr/pull/22128
* yang: use relative path for remaining route-map when clauses by @enkechen-panw in https://github.com/FRRouting/frr/pull/22127
* bgpd: refactor bgp_aggregate_{increment,decrement} by @enkechen-panw in https://github.com/FRRouting/frr/pull/22126
* pimd: guard NULL RP lookups in BSM and RP deletion paths by @Jafaral in https://github.com/FRRouting/frr/pull/22131
* pimd: fix mapping agent AutoRP discovery packet size by @Jafaral in https://github.com/FRRouting/frr/pull/22121
* mgmtd: fix link order for libmgmt_be_nb by @enkechen-panw in https://github.com/FRRouting/frr/pull/22119
* ospf6d: bypass MinLSArrival for self-originated MaxAge LSAs by @hnattamaisub in https://github.com/FRRouting/frr/pull/22103
* lib: test the right bytes in flowspec prefixes by @mjstapp in https://github.com/FRRouting/frr/pull/22138
* bgpd: remove unneeded sort of communities in rmap delete by @mjstapp in https://github.com/FRRouting/frr/pull/22151
* pimd: fix BSR failover RP not setting i_am_rp locally by @Jafaral in https://github.com/FRRouting/frr/pull/22157
* bgpd: reorder parameters in bgp_remove_route_from_aggregate() by @enkechen-panw in https://github.com/FRRouting/frr/pull/22136
* zebra: fix wrong comparision for nexthop by @anlancs in https://github.com/FRRouting/frr/pull/21503
* bgpd: Set extended flag for NHC attribute when re-encoding by @ton31337 in https://github.com/FRRouting/frr/pull/22159
* pimd: dense mode fixes and topotest coverage by @Jafaral in https://github.com/FRRouting/frr/pull/22115
* pimd: BSR/C-RP fixes with expanded topotest coverage by @Jafaral in https://github.com/FRRouting/frr/pull/22117
* bgpd: Avoid cluster list attribute truncation by @ton31337 in https://github.com/FRRouting/frr/pull/22081
* pimd: fix multicast boundary list lifetime and ACL evaluation by @Jafaral in https://github.com/FRRouting/frr/pull/22122
* bgpd: Fixes in comm/lcomm/ecomm str functions by @mjstapp in https://github.com/FRRouting/frr/pull/22176
* bgpd: comment style modifications for verify source test by @PierreNeltner6WIND in https://github.com/FRRouting/frr/pull/22112
* yang: Prefix mismatch in frr-zebra.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/22189
* bgpd: Fix stale EVPN type-5 route for suppressed prefix during L3VNI bounce by @raja-rajasekar in https://github.com/FRRouting/frr/pull/21992
* pimd: defer static mroute install until interfaces are ready by @Jafaral in https://github.com/FRRouting/frr/pull/22156
* pimd: fix dense mode State Refresh relay forwarding by @Jafaral in https://github.com/FRRouting/frr/pull/22177
* ospf: fix the return value for the invalid VRF name by @SindhuParvathi-Gopi in https://github.com/FRRouting/frr/pull/22161
* bgpd: free srv6_l3service object in failed parse path by @mjstapp in https://github.com/FRRouting/frr/pull/22198
* zebra: EVPN clean up stale L2 NH/NHG from kernel at startup by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/22002
* ospfd: validate extended prefix TLV before accessing prefix SID by @mjstapp in https://github.com/FRRouting/frr/pull/22215
* bgpd: Limit as-path segments up to 255 by @ton31337 in https://github.com/FRRouting/frr/pull/22212
* bgpd: Clearly put 4-bytes when encoding SAFI_FLOWSPEC MP_REACH msg by @ton31337 in https://github.com/FRRouting/frr/pull/22213
* pimd: fix heap OOB write in BSM fragmenter by @Jafaral in https://github.com/FRRouting/frr/pull/22222
* lib: use XSTRDUP/XFREE for yang_data value field by @enkechen-panw in https://github.com/FRRouting/frr/pull/22196
* staticd: avoid XPath set_sort in ecmp_path_list_validate by @enkechen-panw in https://github.com/FRRouting/frr/pull/22118
* zebra: Allow rnh evaluation for a queued and !installed rn by @donaldsharp in https://github.com/FRRouting/frr/pull/22221
* ospfd: Validate PREFIX_SID subtlv len before accessing by @mjstapp in https://github.com/FRRouting/frr/pull/22218
* bfdd: fix show bfd peers brief json output identical to show bfd peers by @JackeySparrow in https://github.com/FRRouting/frr/pull/22064
* bgpd: Fix community string truncation for big community sets by @ton31337 in https://github.com/FRRouting/frr/pull/22160
* zebra: remove unused struct buf_req by @iurmanj6WIND in https://github.com/FRRouting/frr/pull/22242
* pimd: fix wrong endian convertion by @anlancs in https://github.com/FRRouting/frr/pull/22244
* yang: inet type mismatch in frr-bfdd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/22241
* lib: Some smaller code fixes for typesafe hash _member function by @robinchrist in https://github.com/FRRouting/frr/pull/22233
* bgpd: fix local rt2 mac+ip leak race conditions by @louis-6wind in https://github.com/FRRouting/frr/pull/21967
* zebra: add dplane helpers to provide interface speed by @maxime-leroy in https://github.com/FRRouting/frr/pull/19412
* bgpd: add LLGR to capability length validation switch by @guoguojia2021 in https://github.com/FRRouting/frr/pull/22249
* bgpd: fixes for NH and aggregator attribute parsing by @mjstapp in https://github.com/FRRouting/frr/pull/22200
* bgpd: remove duplicate snprintf in FlowSpec redirect VRF display by @guoguojia2021 in https://github.com/FRRouting/frr/pull/22272
* bgpd: fix return NULL in bool function ecommunity_node_target_match by @guoguojia2021 in https://github.com/FRRouting/frr/pull/22273
* eigrpd: fix out-of-bounds reads in SHA256 digest computation by @arshsmith in https://github.com/FRRouting/frr/pull/22271
* bgpd: fix holdtime_ptr unsafe pointer aliasing in OPEN receive path by @guoguojia2021 in https://github.com/FRRouting/frr/pull/22270
* Network Byte Order Fixes for Little Endian Machines by @donaldsharp in https://github.com/FRRouting/frr/pull/22251
* bgpd: skip peers not activated for AFI/SAFI in bgp_gr_check_all_eors() (backport #22295) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22302
* bgpd: Fix extended optional parameters handling in OPEN message (backport #22308) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22321
* pceplib: slightly relax a pcep object validation (backport #22298) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22309
* tools: Use the topotest log directory instead of /tmp (backport #22315) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22326
* pceplib: add length validation for pcep obj decoders (backport #22318) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22335
* zebra: bump dplane major version for 10.7 by @mjstapp in https://github.com/FRRouting/frr/pull/22337
* Also build for linux/riscv64 on release (backport #22256) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22341
* tools: Normalize aggregate-address command when doing frr-reload (backport #22284) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22344
* bgpd,tests: improve validation of incoming oid arrays (backport #22116) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22379
* tests, tools: Shutdown daemons in tests same order in systemd (backport #22314) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22382
* tools: Fix frr-reload.py crashes with UnboundLocalError (backport #22378) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22386
* pimd: use RFC 3973 dm graft retry period for retransmission (backport #22376) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22389
* tests: Fix bgp conditional advertisement test to ensure route is received (backport #22327) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22384
* bgpd: don't advertise LLGR stale routes to non-LLGR peers (backport #22297) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22400
* tests: load frr.conf by default (backport #22398) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22415
* bgpd: reduce ibuf_scratch size to match ibuf_work (backport #22347) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22393
* pimd: run Assert for dense mode wrong-interface handling (backport #22377) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22424
* pimd: compensate for missing WRVIFWHOLE upcall on old kernels (backport #22240) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22395
* bgpd: fix strlcat/strlcpy size parameter in NOTIFICATION send path (backport #22279) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22431
* Add restart_frr, document topotest router and daemon restart helpers (backport #22399) by @Jafaral in https://github.com/FRRouting/frr/pull/22435
* yang: Swapped RPF lookup mode descriptions (backport #22375) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22437
* doc, tests: require frr.conf and load_frr_config() in new topotests (backport #22420) by @Jafaral in https://github.com/FRRouting/frr/pull/22436
* debian, redhat: 10.7.0  release preparation by @Jafaral in https://github.com/FRRouting/frr/pull/22438
* bgpd: Ignore parsing ORF route-refresh messages (backport #22429) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22455
* ospf6d: log KillNbr adjacency changes on interface down (backport #22459) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22462
* pimd: fix BSR_PENDING timer being overwritten by BS liveness timer (backport #22460) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22463
* Revert #20005 for stable/10.7 only by @ton31337 in https://github.com/FRRouting/frr/pull/22471
* pimd: fix NOCACHE forwarding for non-connected sources and static mroute upcalls (backport #22466) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22487
* pimd: fix elected BSR not updating when priority changes (backport #22465) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22477
* bgpd: fix bmp connect deletion with source-interface (backport #22469) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22508
* bgpd: Do not accept AIGP for OAD peers if not enabled (backport #22519) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22525
* Merge pull request #22423 from rdemsystems/fix/bgp-extended-message-r… by @rdemsystems in https://github.com/FRRouting/frr/pull/22545
* ospf6d: check length before accessing grace LSA TLVs (backport #22539) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22556
* ldpd: check fec elem length before accessing (backport #22537) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22559
* pimd: fix C-RP processing crash during BSR_PENDING state (backport #22467) by @Jafaral in https://github.com/FRRouting/frr/pull/22566
* pimd: MLAG: gate FHR flag on DR check in wrvifwhole/wholepkt upcalls (backport #22529) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22572
* *: fix overflow in comparator functions used by sorted containers (backport #22498) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22574
* pimd: fix stack overflow and IGMPv3 fragmentation in group_retransmit_sources (backport #21047) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22604
* pimd: clean stale upstream NHT tracking on RP delete (backport #22505) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22605
* pimd: prefer kernel ingress on WRONGVIF when MFC iif is stale (backport #22607) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22624
* lib: Print multicast-source-interface rmap match (backport #22612) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22618
* pimd: allow WRONGVIF prefer-ingress with (*,G)-only ifchannel (backport #22626) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22641
* bgpd: anchor parsed attr in bgp_nlri_parse_vpn to preserve srv6_l3service (backport #22492) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22620
* Missing show run output (backport #22619) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22644
* bgpd: fix const-qualifier build error with strrchr (backport #22642) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22647
* pimd: do not proxy IGMP leave while other downstream receivers remain (backport #22622) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22658
* pimd: defer join-group socket joins until the interface exists (backport #22634) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22668
* bgpd: Validate NEXT_HOP attribute if we have NLRIs and MP_REACH_ATTR (backport #22637) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22660
* pimd: avoid stale RPF ifp during vrf/interface events (backport #22650) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22669
* bgpd: don't emit "no neighbor X capability link-local" for unnumbered… (backport #22540) by @mergify[bot] in https://github.com/FRRouting/frr/pull/22664

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.7.0-dev...frr-10.7.0

## frr-10.6.1

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:813497af103e972600f6161012b3bf2a2a1c5ea10d09cd1eacd74f1dc510a57b)

## What's Changed
* doc: fix indentation error in pim doc (backport #21373)
* Fix/bgp hardening backports 10.6
* isisd: improve validation of flex-algo decoder (backport #21314)
* bgpd: Do not allocate stream if route-refresh capability is not received (backport #21394)
* bgpd: Check dynamic capability action before validating ENHE capability (backport #21395)
* bgpd: Do not allow triggering route-refresh path with a malformed ORF length (backport #21399)
* pimd: guard channel OIL detach against stale pointers (backport #21431)
* ospfd: add validation in several places before accessing message bodies (backport #21303)
* pimd: fix NOCACHE MFC resync detection log, add vrf name too (backport #21481)
* bgpd: Fix mixed remote-as for peer-groups when using auto (backport #21406)
* bgpd: Don't mark nexthop as changed if a set next-hop unchanged is applied (backport #21445)
* ospfd: add LSA validation in the apiserver path (backport #21536)
* eigrpd: reject invalid prefix mask len (backport #21539)
* eigrpd: enforce minimum TLV length in Hello handler (backport #21543)
* isisd: use correct min size values for srv6 subtlvs (backport #21540)
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values (backport #21559)
* bgp_evpn: fix memleak when configuring rd (backport #21566)
* eigrpd: fix byte order in Hello authentication decode (backport #21545)
* lib: Report IPv6 MTU and not IPv4 for if_update_state_mtu6 (backport #21501)
* bgpd: Prevent out-of-bound reading handling soft version dynamic capability (backport #21602)
* isisd: continue hardening SRV6 tlv parsing (backport #21585)
* bgpd: Dynamic capability parsing fixes (backport #21603)
* isisd: consume leftover bytes after FAD sub-sub-TLV loop (backport #21544)
* bgpd: Harden SRv6 Service Data parser for SID Structure length (backport #21612)
* nhrpd: stop debugging auth credentials (backport #21615)
* bgpd: honor 'no activate' for dynamic neighbors in peer-group (backport #21658)
* bgpd: migrate timers during peer_xfer_conn to fix stale route cleanup (backport #21558)
* isisd: correct SRv6 End.X SID minimum size constants (backport #21541)
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero (backport #21641)
* bgpd: Validate if NHC BGPID TLV value is non-zero (backport #21611)
* bgpd: Check if BGPID NHC TLV exists when IPv6 next-hop is link-local (backport #21377, #21605, #21611)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.6.0...frr-10.6.1

## frr-10.5.4

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:17a66aa754b4f60d58fae6cf3c357b62cfb574beb2a4cacd26d50e3df8440b78)

## What's Changed

* pimd: When address change ensure DR changes too. (backport #20881)
* lib/typesafe: guard skiplist level generation against ctz(0) UB (backport #20899)
* bgpd: fix memory leak in cluster_intern() (backport #20913)
* doc: add some text regarding libyang versions (backport #20862)
* eigrpd: handle the gr neighbor list safely in update_receive (backport #20933)
* nhrpd: fix packet and buffer handling errors (backport #20932)
* bgpd: Fix test for OPEN message with remote-as auto (backport #20963)
* bgpd: Add missing PEER_FLAG_SEND_NHC_ATTRIBUTE for update group flags (backport)
* bgpd: check more during flowspec nlri parsing (backport #19909)
* bgpd: Fix condition when evaluating paths (backport #20975)
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002)
* bfdd: Fix wrong memory free when using ttable code (backport #21020)
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054)
* lib: fix zclient crash when many peers reconnect after FRR restart (backport #21056)
* lib: fix vty_is_closed() falsely reporting VTY_SHELL as closed (backport #21082)
* bgpd: Check if the NHC length is enough to fill TLV value + TLV header (backport #21074)
* ospfd: fix sequence number check, avoid truncation ambiguity (backport #21096)
* nhrpd: Correct addrlen check in os_recvmsg() (backport #21100)
* ldpd: improve tlv validation in several places (backport #21118)
* PIM message-handling code fixes (backport #21093)
* lib: disable warning in zlog.c to match master
* bgpd: fix some packet-parsing issues (10.5 version)
* bgpd: Return 0 if AS4 capability is malformed (backport #21112)
* isisd: fix edge condition in max_lsp_count computation (backport #21159)
* bgpd: Prevent heap use-after-free for tunnel encapsulation attribute (backport #21176)
* isisd: fix memory leak in remove_excess_adjs() (backport #21183)
* isisd: Fix missing neighbor address Sub-TLVs after link-params change (backport #21204)
* bgpd: improve packet parsing for EVPN and ENCAP/VNC (backport #21098)
* nhrpd:  harden against malformed packets (backport #21097)
* ripngd: fix data handling in several places (10.5 backport)
* bgpd: Recent bugs for 10.5
* vrrrpd: improve error handling in several paths (backport #21251)
* bgpd: fix NHT for explicit link-local BGP peers (backport)
* bgpd: flowspec foobar hardening (backport #21308)
* bgpd: fix import vrf on non existing vrf (backport)
* ospf6d: improve/harden packet processing (backport #21277)
* bfdd: harden packet validation and reflector handling (backport #21105) (backport #21255)
* pceplib: validate during of_list TLV decoding (backport #21310)
* pimd: fix crash due to double free (backport #21354)
* eigrpd: improve validation and error-handling in tlv parsing (backport #21316 to 10.5)
* bgpd: Revalidate locally originated routes against RPKI changes (backport #21302)
* bgpd: hardening backports 10.5
* bgpd: Move rpki strict check to bgp_accept() (backport #21328)
* bgpd: Do not allocate stream if route-refresh capability is not received (backport #21394)
* bgpd: Check dynamic capability action before validating ENHE capability (backport #21395)
* pimd: guard channel OIL detach against stale pointers (backport #21431)
* isisd: improve validation of flex-algo decoder (backport)
* ospfd: add validation in several places before accessing message bodies (backport #21303)
* pimd: fix NOCACHE MFC resync detection log, add vrf name too (backport #21481)
* bgpd: Fix mixed remote-as for peer-groups when using auto (backport #21406)
* bgpd: Don't mark nexthop as changed if a set next-hop unchanged is applied (backport #21445)
* ospfd: add LSA validation in the apiserver path (backport #21536)
* eigrpd: enforce minimum TLV length in Hello handler (backport #21543)
* eigrpd: reject invalid prefix mask len (backport #21539)
* isisd: use correct min size values for srv6 subtlvs (backport #21540)
* eigrpd: Handling for malformed update packets (10.5 version)
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values (backport #21559)
* eigrpd: fix byte order in Hello authentication decode (backport #21545)
* bgp_evpn: fix memleak when configuring rd (backport #21566)
* lib: Report IPv6 MTU and not IPv4 for if_update_state_mtu6 (backport #21501)
* bgpd: Dynamic capability parsing fixes (backport #21603)
* isisd: consume leftover bytes after FAD sub-sub-TLV loop (backport #21544)
* nhrpd: stop debugging auth credentials (backport #21615)
* bgpd: honor 'no activate' for dynamic neighbors in peer-group (backport #21658)
* bgpd: migrate timers during peer_xfer_conn to fix stale route cleanup (backport #21558)
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero (backport #21641)
* bgpd: Validate if NHC BGPID TLV value is non-zero (backport #21611)
* bgpd: Check if BGPID NHC TLV exists when IPv6 next-hop is link-local (backport #21377, #21605, #21611)
* bgpd: Do not allocate NHC TLV with an extra trailer (backport #21606)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.5.2...frr-10.5.4

## frr-10.4.4

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:a066f5b1489c198b599dd10613f463ecb4f7c6b93098b765a6bdb0ab0b4be983)

## What's Changed
* pimd: When address change ensure DR changes too. (backport #20881)
* bgpd: fix memory leak in cluster_intern() (backport #20913)
* doc: add some text regarding libyang versions (backport #20862)
* eigrpd: handle the gr neighbor list safely in update_receive (backport #20933)
* nhrpd: fix packet and buffer handling errors (backport #20932)
* bgpd: Add missing PEER_FLAG_SEND_NHC_ATTRIBUTE for update group flags (backport)
* bgpd: check more during flowspec nlri parsing (backport #19909)
* bgpd: Fix test for OPEN message with remote-as auto (backport #20963)
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002)
* bfdd: Fix wrong memory free when using ttable code (backport #21020)
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054)
* bgpd: Check if the NHC length is enough to fill TLV value + TLV header (backport #21074)
* ospfd: fix sequence number check, avoid truncation ambiguity (backport #21096)
* nhrpd: Correct addrlen check in os_recvmsg() (backport #21100)
* ldpd: improve tlv validation in several places (backport #21118)
* PIM message-handling code fixes (backport #21093)
* lib: disable warning in zlog.c to match master
* bgpd: fix some packet-parsing issues (10.4 version)
* isisd: fix edge condition in max_lsp_count computation (backport #21159)
* bgpd: Return 0 if AS4 capability is malformed (backport #21112)
* bgpd: Prevent heap use-after-free for tunnel encapsulation attribute (backport #21176)
* isisd: fix memory leak in remove_excess_adjs() (backport #21183)
* bgpd: improve packet parsing for EVPN and ENCAP/VNC (backport #21098)
* nhrpd:  harden against malformed packets (backport #21097)
* bgpd: fix NHT for explicit link-local BGP peers (backport)
* ripngd: fix data handling in several places (10.4 version)
* bgpd: Recent bugs for 10.4
* vrrrpd: improve error handling in several paths (backport #21251)
* lib: fix zclient crash when many peers reconnect after FRR restart (backport #21056)
* bgpd: flowspec foobar hardening (backport #21308)
* bgpd: fix import vrf on non existing vrf (backport)
* ospf6d: improve/harden packet processing (backport #21277)
* pceplib: validate during of_list TLV decoding (backport #21310)
* bgpd: Revalidate locally originated routes against RPKI changes (backport)
* bfdd: harden packet validation and reflector handling (backport #21105)
* pimd: fix crash due to double free (backport #21354)
* eigrpd: improve validation and error-handling in tlv parsing (backport #21316)
* bgpd: hardening backports 10.4
* bgpd: Do not allocate stream if route-refresh capability is not received (backport #21394)
* bgpd: Check dynamic capability action before validating ENHE capability (backport #21395)
* pimd: guard channel OIL detach against stale pointers (backport #21431)
* isisd: improve validation of flex-algo decoder (backport) (backport #21463)
* ospfd: add validation in several places before accessing message bodies (backport #21303)
* bgpd: Fix mixed remote-as for peer-groups when using auto (backport #21406)
* ospfd: add LSA validation in the apiserver path (backport #21536)
* bgpd: Don't mark nexthop as changed if a set next-hop unchanged is applied (backport #21445)
* eigrpd: enforce minimum TLV length in Hello handler (backport #21543)
* isisd: use correct min size values for srv6 subtlvs (backport #21540)
* eigrpd: reject invalid prefix mask len (backport #21539)
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values (backport #21559)
* eigrpd: Handling for malformed update packets (10.4 version)
* eigrpd: fix byte order in Hello authentication decode (backport #21545)
* lib: Report IPv6 MTU and not IPv4 for if_update_state_mtu6 (backport #21501)
* bgp_evpn: fix memleak when configuring rd (backport #21566)
* isisd: consume leftover bytes after FAD sub-sub-TLV loop (backport #21544)
* nhrpd: stop debugging auth credentials (backport #21615)
* bgpd: honor 'no activate' for dynamic neighbors in peer-group (backport #21658)
* bgpd: Dynamic capability parsing fixes (backport #21603)
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero (backport #21641)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.4.3...frr-10.4.4

## frr-10.3.4

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:c8790a83db3cb105c0823f76afe55de5c9f77d968fb1ebd28174a8ddd49b989c)

## What's Changed
* Alpine Docker fix ups for 3.22 (backport #20004)
* bgpd: update source address for bgp neighbor (backport #20330)
* docker: Add missing `pytest` package for Alpine as dependency (backport #20369)
* bgpd: Use the default local-preference value and not 0 when adjusting (backport #20400)
* eigrpd: Prevent crash in packet handling (backport #20410)
* zebra: Fix memory leak when SRv6 explicit SID allocation fails (backport #20429)
* isisd: fix crash when changing isis type (backport #20171)
* zebra: Fix memory leak when SRv6 dynamic SID allocation fails (backport #20445)
* ospfd: fixed ospf nssa flush issue (backport #20428)
* zebra: EVPN check l3vni vxlan intf exist in rmac install (backport #20494)
* bgpd: Fix multipath decision when multipath is 1 (backport #20493)
* bgpd: reduce ibuf_work ring buffer size (backport #20554)
* zebra: fix crash on inactive VRF and import table (backport #20525)
* zebra: FRR restart leads to zebra mlag core (backport #20225)
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… (backport #20661)
* staticd: Fix SRv6 SID use-after-free on locator deletion (backport #20660 for 10.3)
* bgpd: fix md5 password unset on dynamic nbr (backport #20740)
* bgpd: Ignore transitiveness flag when checking type for link bandwidth (backport #20607)
* bgpd: EVPN MH fix unimport ES route on vtep change (backport #20730)
* Zebra fixup nhg handling from kernel (backport #20732)
* bgpd: validate incoming NOTIFICATION messages (backport #20796)
* Multiple local fix (backport #20798)
* bgpd: improve flowspec NLRI validation (backport #20814)
* zebra: EVPN fix access BD deref of mbr intf (backport #20791)
* doc: add some text regarding libyang versions (backport #20862)
* bgpd: Fix test for OPEN message with remote-as auto (backport #20963)
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002)
* bfdd: Fix wrong memory free when using ttable code (backport #21020)
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054)
* ospfd: fix sequence number check, avoid truncation ambiguity (backport #21096)
* ldpd: improve tlv validation in several places (backport #21118)
* isisd: fix edge condition in max_lsp_count computation (backport #21159)
* bgpd: Return 0 if AS4 capability is malformed (backport #21112)
* bgpd: Prevent heap use-after-free for tunnel encapsulation attribute (backport #21176)
* bgpd: improve packet parsing for EVPN and ENCAP/VNC (backport #21098)
* nhrpd:  harden against malformed packets (backport #21097)
* vrrrpd: improve error handling in several paths (backport #21251)
* ripngd: fix data handling in several places (backport #21257)
* ospf6d: improve/harden packet processing (backport #21277)
* bgpd: Revalidate locally originated routes against RPKI changes (backport)
* lib: fix zclient crash when many peers reconnect after FRR restart (backport #21056)
* pceplib: validate during of_list TLV decoding (backport #21310)
* bgpd: Do not allocate stream if route-refresh capability is not received (backport #21394)
* bgpd: Check dynamic capability action before validating ENHE capability (backport #21395)
* bgpd: Don't mark nexthop as changed if a set next-hop unchanged is applied (backport #21445)
* ospfd: add LSA validation in the apiserver path (backport #21536)
* eigrpd: enforce minimum TLV length in Hello handler (backport #21543)
* lib: ignore gcc warning in 10.3 zlog lttng code
* eigrpd: reject invalid prefix mask len (10.3 backport)
* isisd: use correct min size values for srv6 subtlvs (backport #21540)
* ospfd: add validation in several places before accessing message bodies (backport #21303)
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values (backport #21559)
* eigrpd: fix byte order in Hello authentication decode (backport #21545)
* bgpd: Dynamic capability parsing fixes (backport #21603)
* isisd: consume leftover bytes after FAD sub-sub-TLV loop (backport #21544)
* nhrpd: stop debugging auth credentials (backport #21615)
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero (backport #21641)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.3.3...frr-10.3.4

## frr-10.2.6

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:f8592b2b3e629e0a31ffa48a8b5c8e026db48a72c52437a40f85e5aec0b90031)

## What's Changed
* Alpine Docker fix ups for 3.22 (backport #20004)
* docker: Add missing `pytest` package for Alpine as dependency (backport #20369)
* isisd: fix crash when changing isis type (backport #20171)
* zebra: Fix memory leak when SRv6 dynamic SID allocation fails (backport #20445)
* ospfd: fixed ospf nssa flush issue (backport #20428)
* zebra: EVPN check l3vni vxlan intf exist in rmac install (backport #20494)
* bgpd: Fix multipath decision when multipath is 1 (backport #20493)
* bgpd: reduce ibuf_work ring buffer size (backport #20554)
* zebra: fix crash on inactive VRF and import table (backport #20525)
* zebra: FRR restart leads to zebra mlag core (backport #20225)
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… (backport #20661)
* bgpd: fix md5 password unset on dynamic nbr (backport #20740)
* bgpd: validate incoming NOTIFICATION messages (backport #20796)
* bgpd: improve flowspec NLRI validation (backport #20814)
* zebra: EVPN fix access BD deref of mbr intf (backport #20791)
* bgpd: Fix test for OPEN message with remote-as auto (backport #20963)
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002)
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054)
* ospfd: fix sequence number check, avoid truncation ambiguity (backport #21096)
* ldpd: improve tlv validation in several places (backport #21118)
* isisd: fix edge condition in max_lsp_count computation (backport #21159)
* bgpd: Return 0 if AS4 capability is malformed (backport #21112)
* bgpd: Prevent heap use-after-free for tunnel encapsulation attribute (backport #21176)
* bgpd: improve packet parsing for EVPN and ENCAP/VNC (backport #21098)
* bgpd: fix NHT for explicit link-local BGP peers (backport #21188)
* nhrpd:  harden against malformed packets (backport #21097)
* vrrrpd: improve error handling in several paths (backport #21251)
* ripngd: fix data handling in several places (backport #21257)
* ospf6d: improve/harden packet processing (backport #21277)
* bgpd: Do not allocate stream if route-refresh capability is not received (backport #21394)
* bgpd: Don't mark nexthop as changed if a set next-hop unchanged is applied (backport #21445)
* ospfd: add validation in several places before accessing message bodies (backport #21303)
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values (backport #21559)
* eigrpd: fix byte order in Hello authentication decode (backport #21545)
* isisd: consume leftover bytes after FAD sub-sub-TLV loop (backport #21544)
* nhrpd: stop debugging auth credentials (backport #21615)
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero (backport #21641)
* bgpd: Revalidate locally originated routes against RPKI changes (backport)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.2.5...frr-10.2.6

## frr-10.1.5

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/

## What's Changed
* bgpd: fix DEREF_OF_NULL.EX.COND in community_list_dup_check (backport #19325)
* bgpd: fix overflow when decoding zapi nexthop for srv6 max segments (backport #19324)
* bgpd: fix memory leak in evpn mh  (backport #19334)
* bgpd: Fix default vrf check while configuring md5 password for prefix on the bgp listen socket (backport #19317)
* zebra: Explicitly print "exit" at the end of srv6 encap node config (backport #19409)
* bgpd: Fix crash due to dangling pointer in bnc nht_info (backport #19362)
* pim6d: don't SEGV on repeated MLD records (backport #19732)
* lib: mgmt_msg: fix bug with disconnect and event scheduling (backport #19994)
* isisd: fix crash when changing isis type (backport #20171)
* bgpd: reduce ibuf_work ring buffer size (backport #20554)
* zebra: FRR restart leads to zebra mlag core (backport #20225)
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… (backport #20661)
* bgpd: validate incoming NOTIFICATION messages (backport #20796)
* bgpd: improve flowspec NLRI validation (backport #20814)
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002)
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054)
* ldpd: improve tlv validation in several places (backport #21118)
* bgpd: Return 0 if AS4 capability is malformed (backport #21112)
* bgpd: improve packet parsing for EVPN and ENCAP/VNC (backport #21098)
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values (backport #21559)
* eigrpd: fix byte order in Hello authentication decode (backport #21545)
* bgpd: Dynamic capability parsing fixes (backport #21603)
* isisd: consume leftover bytes after FAD sub-sub-TLV loop (backport #21544)
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero (backport #21641)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.1.4...frr-10.1.5

## frr-10.0.5

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/

## What's Changed
* bgpd: fix DEREF_OF_NULL.EX.COND in community_list_dup_check (backport #19325)
* bgpd: fix overflow when decoding zapi nexthop for srv6 max segments (backport #19324)
* bgpd: fix memory leak in evpn mh  (backport #19334)
* bgpd: Fix default vrf check while configuring md5 password for prefix on the bgp listen socket (backport #19317)
* zebra: Explicitly print "exit" at the end of srv6 encap node config (backport #19409)
* bgpd: Fix crash due to dangling pointer in bnc nht_info (backport #19362)
* lib: mgmt_msg: fix bug with disconnect and event scheduling (backport #19994)
* isisd: fix crash when changing isis type (backport #20171)
* bgpd: reduce ibuf_work ring buffer size (backport #20554)
* zebra: FRR restart leads to zebra mlag core (backport #20225)
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… (backport #20661)
* bgpd: validate incoming NOTIFICATION messages (backport #20796)
* bgpd: improve flowspec NLRI validation (backport #20814)
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002)
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054)
* ldpd: improve tlv validation in several places (backport #21118)
* bgpd: Return 0 if AS4 capability is malformed (backport #21112)
* bgpd: improve packet parsing for EVPN and ENCAP/VNC (backport #21098)
* bgpd: fix neighbor IP comparison for IPv6 memcmp return values (backport #21559)
* eigrpd: fix byte order in Hello authentication decode (backport #21545)
* isisd: consume leftover bytes after FAD sub-sub-TLV loop (backport #21544)
* isisd: Reject SRv6 Locator TLV with Loc-Size of zero (backport #21641)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.0.4...frr-10.0.5

## frr-10.6.0

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:eae3340ca578bb588d92ab3d1e77deb806f80d1da2bc0053cb1dfcfef2aa236f)

## Release Overview

### New Features Highlight

- **LTTng traces for BFD**
  - Added support for LTTng tracing in BFD, enabling improved observability and debugging capabilities for BFD sessions.
- **Extended weights for the next-hop**
  - Support for 16-bit next-hop weights has been added, aligning with capabilities introduced in Linux kernel v6.12.
FRRouting now supports extended weight values for improved ECMP distribution accuracy.
- **BGP ECMP by using Underlay Weights**
  - BGP now provides a configuration option to use underlay-computed weights for ECMP path selection.
Traditionally, BGP derives ECMP weights from extended community attributes. With this enhancement, operators may configure BGP to instead use underlay weights when calculating traffic distribution.
- **BGP ECMP by using Next-next nodes (Next-hop dependent characteristic) count**
  - An additional ECMP weighting mode has been introduced based on next-hop dependent characteristics (e.g., next-next-hop node count).
  - When `bgp bestpath bandwidth ignore` is enabled and next-hop characteristics are present, BGP uses the number of underlying next-next-hop paths to derive ECMP weights.
- **BGP software version capability encoding changes**
  - Encoding has been updated to align with version 15 of draft-abraitis-bgp-version-capability. Starting with this revision:
The TLV length field is no longer explicitly encoded. The capability length field alone determines the encoding size.
  - A new command has been introduced `bgp default software-version-capability latest-encoding`. This enables use of the updated encoding format.
- **BGP SRv6 unicast at the global (default) VRF**
  - Support has been added for global (default VRF) unicast routing over an SRv6 core:
    * Global IPv4 over SRv6 Core (RFC 9252)
    * Global IPv6 over SRv6 Core (RFC 9252)
  - This enables SRv6-based transport for IPv4 and IPv6 services in the default routing table.
- **BGP IPv6 VTEP support**
  - Comprehensive IPv6 VTEP support has been added throughout the EVPN codebase. This enables EVPN deployments using IPv6 tunnel endpoints while maintaining full backward compatibility with IPv4 VTEPs.
- **BGP multiple labels support for labeled unicast**
  - FRRouting now supports multiple MPLS labels in BGP Labeled Unicast. 
    * Previously: If multiple labels were received, only the bottom label was used. 
    * Now: Up to 10 labels are supported per prefix.
  - This aligns with the maximum label stack depth defined in RFC 3017 and RFC 8277.
- **BGP graceful restart for EVPN**
  - Graceful Restart capability has been extended to EVPN address families. This aligns EVPN behavior with existing graceful restart support for IPv4 and IPv6 unicast.
- **Implement forwarding-address-self command for OSPFv2**
  - A new forwarding-address-self command has been implemented for OSPFv2. By default, when redistributing routes into OSPF, the forwarding address field is set based on the original next-hop. When forwarding-address-self is configured, the router sets the forwarding address field to its own address.
  - This is particularly useful in multi-homed (ECMP) ASBR deployments where traffic must be directed explicitly to the redistributing router.
- **PIM/PIMv6 filter support for IGMP/MLD joins**
  - Added support for filtering IGMP (IPv4) and MLD (IPv6) joins in PIM and PIMv6.
- **libyang3 changes**
  - Binary packages are now built against libyang3 by default. Users requiring libyang2 may still recompile FRRouting with libyang2 support.

## What's Changed
* ospfd: On cleanup, actually free vertexes by @donaldsharp in https://github.com/FRRouting/frr/pull/19686
* tools: add nhrp support bundle by @Jafaral in https://github.com/FRRouting/frr/pull/19674
* bgpd: Transfer through the return code by @donaldsharp in https://github.com/FRRouting/frr/pull/19653
* bgpd, lib, pbrd: Use hash_lookup where appropriate by @donaldsharp in https://github.com/FRRouting/frr/pull/19652
* eigrpd, ospfd, pimd: Fix usage of packed member unaligned by @donaldsharp in https://github.com/FRRouting/frr/pull/19663
* Improve handling of vrf backend type by @donaldsharp in https://github.com/FRRouting/frr/pull/19651
* Revert "ospfd: On cleanup, actually free vertexes" by @donaldsharp in https://github.com/FRRouting/frr/pull/19691
* build: add warning for extra format args by @mjstapp in https://github.com/FRRouting/frr/pull/19645
* tests: Corrected unidiomatic-typecheck by @ramapalleti in https://github.com/FRRouting/frr/pull/19676
* lib, zebra: Add fib installed NH count in json show cmd by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19656
* bgpd: improve/clarify bgp static tables by @mjstapp in https://github.com/FRRouting/frr/pull/19640
* tests: Ensure key exists for bgp_evpn_mh by @donaldsharp in https://github.com/FRRouting/frr/pull/19697
* build: Add warning for address of packed member by @donaldsharp in https://github.com/FRRouting/frr/pull/19690
* tests: fix memory leaks in `make check` for ASAN run by @eqvinox in https://github.com/FRRouting/frr/pull/19701
* ospfd: plug leaks in TI-LFA code by @eqvinox in https://github.com/FRRouting/frr/pull/19700
* bgpd: display reset cause consistently in bgp_show_failed_summary() by @enkechen-panw in https://github.com/FRRouting/frr/pull/19711
* Coverity low medium by @donaldsharp in https://github.com/FRRouting/frr/pull/19627
* bgpd: ensure batch clearing flags are clear by @mjstapp in https://github.com/FRRouting/frr/pull/19696
* Bgp evpn pass originator by @donaldsharp in https://github.com/FRRouting/frr/pull/19492
* doc: Fix a bunch of the duplicate commands during build by @donaldsharp in https://github.com/FRRouting/frr/pull/19703
* *: don't access invalid zapi route msg nexthops by @mjstapp in https://github.com/FRRouting/frr/pull/19714
* eigrpd: Handling for malformed update packets by @ritika0313 in https://github.com/FRRouting/frr/pull/19699
* zebra: Cleanup early route Q when removing routes. by @donaldsharp in https://github.com/FRRouting/frr/pull/19338
* doc: Fix documentation regarding capability link-local by @ton31337 in https://github.com/FRRouting/frr/pull/19713
* pim6d: don't SEGV on repeated MLD records by @eqvinox in https://github.com/FRRouting/frr/pull/19732
* zebra: fix neighbor table name length by @kunkku in https://github.com/FRRouting/frr/pull/18872
* bgpd: type-5 routes were sometimes being injected when they should not by @donaldsharp in https://github.com/FRRouting/frr/pull/19731
* Allow Route Resolution via same prefix Cross VRF by @donaldsharp in https://github.com/FRRouting/frr/pull/19718
* *: Support IPv6 VTEP for EVPN single-homing by @mjstapp in https://github.com/FRRouting/frr/pull/19498
* zebra: Free early route objects after we done only by @ton31337 in https://github.com/FRRouting/frr/pull/19746
* tests: Stop double run of a large number of commands by @donaldsharp in https://github.com/FRRouting/frr/pull/19755
* Bgp curr to connection by @donaldsharp in https://github.com/FRRouting/frr/pull/19753
* Weighted ECMP by using Next-Next Hop Nodes characteristic by @ton31337 in https://github.com/FRRouting/frr/pull/19633
* gdb: Add a walk_bgp_table macro by @donaldsharp in https://github.com/FRRouting/frr/pull/19728
* tests: correct one assert for ldp test by @anlancs in https://github.com/FRRouting/frr/pull/19572
* ospf6d: Fix summary deletion dropping redistributed routes by @donaldsharp in https://github.com/FRRouting/frr/pull/19733
* bgp_bmp: fix pullwr bump call by @lsang6WIND in https://github.com/FRRouting/frr/pull/19744
* Items found via valgrind running and gcoverage by @donaldsharp in https://github.com/FRRouting/frr/pull/19719
* lib,zebra: make nhg nexthop show output consistent by @mjstapp in https://github.com/FRRouting/frr/pull/19762
* Coverity fix: unchecked return value by @aprathik04 in https://github.com/FRRouting/frr/pull/19702
* pimd/pim6d: fix router-alert crash by @anlancs in https://github.com/FRRouting/frr/pull/19757
* zebra: Initialize vtep_ip before passing to dplane_local_mac_add/del by @ton31337 in https://github.com/FRRouting/frr/pull/19763
* zebra: include EVPN encap info with recursive nexthops by @mjstapp in https://github.com/FRRouting/frr/pull/19720
* tests: Allow --with-timestamp-precision=X to actually work w/ make check by @donaldsharp in https://github.com/FRRouting/frr/pull/19772
* lib: fix SA warnings re. typesafe _add return val by @eqvinox in https://github.com/FRRouting/frr/pull/19771
* bgpd: Fix resource leak coverity by @aprathik04 in https://github.com/FRRouting/frr/pull/19775
* lib: Remove unnecessary #includes by @jkoshy in https://github.com/FRRouting/frr/pull/19777
* bgpd: EVPN fix auto derive rd when user cfg removed by @chiragshah6 in https://github.com/FRRouting/frr/pull/19779
* Test speedups of long running tests by @donaldsharp in https://github.com/FRRouting/frr/pull/19770
* bgpd: check the peer state when recording the down cause by @enkechen-panw in https://github.com/FRRouting/frr/pull/19667
* bgpd: ensure evpn prefix locals are inited by @mjstapp in https://github.com/FRRouting/frr/pull/19790
* zebra: EVPN fix alignment of access-vlan cli output by @chiragshah6 in https://github.com/FRRouting/frr/pull/19795
* pim6d: drop mismatch report packets by @anlancs in https://github.com/FRRouting/frr/pull/19198
* Cleanup `show debugging` and isisd, fabricd, bgpd and ospfd debug commands by @kaffarell in https://github.com/FRRouting/frr/pull/19544
* isis: fix advertise-passive-only routes install by @hedrok in https://github.com/FRRouting/frr/pull/19593
* zebra: Show prefix on failed lookup by @donaldsharp in https://github.com/FRRouting/frr/pull/19789
* bgpd: Prevent unnecessary re-install of routes by @donaldsharp in https://github.com/FRRouting/frr/pull/19788
* lib, build: support gperftools tcmalloc, release free memory to host OS by @mjstapp in https://github.com/FRRouting/frr/pull/19377
* lib: Add json support for 'show version' command by @donaldsharp in https://github.com/FRRouting/frr/pull/19803
* zebra: Fix SRv6 explicit SID allocation to use the provided locator by @cscarpitta in https://github.com/FRRouting/frr/pull/19806
* pimd : Added support for multi-oif static mroute by @e-wing in https://github.com/FRRouting/frr/pull/19765
* bgpd: EVPN-MH fix ES-EVI memleak during shutdown by @chiragshah6 in https://github.com/FRRouting/frr/pull/19814
* Bgpd coverity medium issues by @hnattamaisub in https://github.com/FRRouting/frr/pull/19774
* zebra: workaround for a race condition caused by if_zebra_speed_update timer by @markx-arista in https://github.com/FRRouting/frr/pull/19794
* bgpd: Do not complain in the logs if we intentionally withdraw specific attrs by @ton31337 in https://github.com/FRRouting/frr/pull/19821
* bfdd: Turn zlog_fatal into zlog_err by @donaldsharp in https://github.com/FRRouting/frr/pull/19822
* bgpd: Put local BGP ID when sending NNHN TLV for NH characteristic by @ton31337 in https://github.com/FRRouting/frr/pull/19808
* doc: Update bgp's treat-as-withdraw command doc by @donaldsharp in https://github.com/FRRouting/frr/pull/19823
* doc: Update kernel route redistribution doc by @donaldsharp in https://github.com/FRRouting/frr/pull/19813
* Route-map command to filter out VPN paths based on their origin (MPLS /SRv6 / VXLAN) by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19717
* bgpd: add SRv6 unicast at default VRF by @lsang6WIND in https://github.com/FRRouting/frr/pull/19496
* zebra/bgpd: Coverity issues by @hnattamaisub in https://github.com/FRRouting/frr/pull/19820
* Sphinx issues by @donaldsharp in https://github.com/FRRouting/frr/pull/19841
* *: modify RANGE vty token to use int64_t type by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19474
* yang: fix wrong comment to match-condition entry by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19847
* zebra: fix yang data for mcast-group by @idryzhov in https://github.com/FRRouting/frr/pull/19845
* bgpd: fix attr intern overhead by @krishna-samy in https://github.com/FRRouting/frr/pull/19547
* bgpd: changes for code maintainability by @sri-mohan1 in https://github.com/FRRouting/frr/pull/19857
* Add debug bgp neighbor-events detail command by @Pdoijode in https://github.com/FRRouting/frr/pull/19843
* zebra: EVPN fix show interface vxlan json by @chiragshah6 in https://github.com/FRRouting/frr/pull/19846
* bgpd: EVPN fix memleak in adv type5 cli cmd by @chiragshah6 in https://github.com/FRRouting/frr/pull/19858
* lib : Set the correct timeout attribute in ppoll by @nishant111 in https://github.com/FRRouting/frr/pull/19715
* ospfd: fix the inconsistency between lsdb and route table by @anlancs in https://github.com/FRRouting/frr/pull/19745
* Frr headers by @maxime-leroy in https://github.com/FRRouting/frr/pull/19351
* bgpd: Double check all connection events are stopped on peer shutdown. by @donaldsharp in https://github.com/FRRouting/frr/pull/19871
* tests: Add a cluster-length test by @donaldsharp in https://github.com/FRRouting/frr/pull/19870
* bgpd: High coverity changes - Uninitialzed scalar variable by @hnattamaisub in https://github.com/FRRouting/frr/pull/19869
* pbrd: fix memleak during pbr map deletion by @aprathik04 in https://github.com/FRRouting/frr/pull/19863
* zebra: Null pointer dereferences (medium) by @hnattamaisub in https://github.com/FRRouting/frr/pull/19851
* test: bgp_extcomm_list_delete add regex case by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/19848
* bgpd: BGP_CONFIG_VRF_TO_VRF_IMPORT flag not set correctly by @vijayalaxmi-basavaraj in https://github.com/FRRouting/frr/pull/19710
* ospfd: Drop support for SSL1 and update to SSL3 by @donaldsharp in https://github.com/FRRouting/frr/pull/19842
* bgpd: Track route-map references for srv6 when rmap is used by @ton31337 in https://github.com/FRRouting/frr/pull/19868
* zebra: update dataplane api version for 10.5 release by @mjstapp in https://github.com/FRRouting/frr/pull/19856
* Interface speed handling improvements by @donaldsharp in https://github.com/FRRouting/frr/pull/19811
* vrrpd: IPv6 VRRP macvlan doesn't have IPv6 link-local address by @hnattamaisub in https://github.com/FRRouting/frr/pull/19861
* bgpd: Crash due to usage of freed up evpn_overlay attr by @soumyar-roy in https://github.com/FRRouting/frr/pull/19879
* bfdd: Return an error before using negative fd for setsockopt() by @ton31337 in https://github.com/FRRouting/frr/pull/19886
* zebra: fix missing fpm messages by @anlancs in https://github.com/FRRouting/frr/pull/19807
* zebra: fix for unchecked return value coverity issues by @aprathik04 in https://github.com/FRRouting/frr/pull/19695
* zebra: Add `show zebra client json` command by @donaldsharp in https://github.com/FRRouting/frr/pull/19840
* bgpd: Notify all incoming/outgoing on peer group notify unconfig by @donaldsharp in https://github.com/FRRouting/frr/pull/19891
* Convert a couple of bfd tests to use frr.conf unified config by @donaldsharp in https://github.com/FRRouting/frr/pull/19597
* pimd: demote a warning to a debug to avoid spamming the logs by @Jafaral in https://github.com/FRRouting/frr/pull/19902
* zebra: Coverity issue (Null pointer dereference) by @hnattamaisub in https://github.com/FRRouting/frr/pull/19911
* bgpd: When creating a peer_connection pass in the sockunion for it by @donaldsharp in https://github.com/FRRouting/frr/pull/19901
* bgpd: check more during flowspec nlri parsing by @mjstapp in https://github.com/FRRouting/frr/pull/19909
* bgpd: fix routemap evpn type-5 default route check by @chiragshah6 in https://github.com/FRRouting/frr/pull/19895
* bgpd: Check L3VNI status before adv evpn vrf routes by @chiragshah6 in https://github.com/FRRouting/frr/pull/19896
* bgpd: fix BGP_ATTR_ORIGINATOR_ID flag in outbound attribute cache by @enkechen-panw in https://github.com/FRRouting/frr/pull/19918
* bgpd: fix BGP_ATTR_LOCAL_PREF being set appropriately by @donaldsharp in https://github.com/FRRouting/frr/pull/19927
* bgpd: fix expanded extcomm list delete  by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/19903
* ldpd: fix missing the pw message by @anlancs in https://github.com/FRRouting/frr/pull/19912
* bgpd: Check MED flag correctly in encap_attr_export() by @ton31337 in https://github.com/FRRouting/frr/pull/19940
* zebra: Return checks are missing in some spots by @donaldsharp in https://github.com/FRRouting/frr/pull/19951
* bgpd: Use bgp_attr_[exists/set/unset] helpers when doing attr stuff by @ton31337 in https://github.com/FRRouting/frr/pull/19953
* doc: add note to the dev guide regrading backports by @Jafaral in https://github.com/FRRouting/frr/pull/19950
* zebra: Refactor SRv6 netlink code to remove duplication by @cscarpitta in https://github.com/FRRouting/frr/pull/19955
* bgpd: Do not cast to a larger size than an argument for encode_rd_type() by @ton31337 in https://github.com/FRRouting/frr/pull/19952
* doc, docker: fix Ubuntu 24.04 snmp issues and enable 24.04 github CI by @Jafaral in https://github.com/FRRouting/frr/pull/19483
* bgpd: EVPN init local variable by @chiragshah6 in https://github.com/FRRouting/frr/pull/19960
* lib: fix memleak in nexthop label copy by @chiragshah6 in https://github.com/FRRouting/frr/pull/19959
* zebra: Check return code to make coverity happy by @donaldsharp in https://github.com/FRRouting/frr/pull/19965
* Thread event cleanup by @donaldsharp in https://github.com/FRRouting/frr/pull/19957
* debian, redhat: release updates housekeeping  by @Jafaral in https://github.com/FRRouting/frr/pull/19971
* ospfd: reorder ospf apiserv opaque unregistration by @mjstapp in https://github.com/FRRouting/frr/pull/19970
* docs: bgp: fix sid-export command formatting by @kaffarell in https://github.com/FRRouting/frr/pull/19974
* ospfd: Fix crash when entering `ospf authentication key XX` by @donaldsharp in https://github.com/FRRouting/frr/pull/19975
* zebra: move netlink parsing to a separate shared-lib by @mjstapp in https://github.com/FRRouting/frr/pull/19197
* zebra: increment dplane version number by @mjstapp in https://github.com/FRRouting/frr/pull/19976
* *: Fix SRv6 uA SID programming with IPv6 link-local addresses by @cscarpitta in https://github.com/FRRouting/frr/pull/19844
* *: Add commit to .git-blame-ignore-revs by @donaldsharp in https://github.com/FRRouting/frr/pull/19984
* Big header cleanup by @donaldsharp in https://github.com/FRRouting/frr/pull/19956
* bgpd: fix show running-config encapsulation-[mpls/srv6] by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19989
* lib: mgmt_msg: fix bug with disconnect and event scheduling by @choppsv1 in https://github.com/FRRouting/frr/pull/19994
* bgpd: Convince coverity that dest is still valid by @donaldsharp in https://github.com/FRRouting/frr/pull/19992
* lib: Properly set event_execute type by @donaldsharp in https://github.com/FRRouting/frr/pull/19990
* Bgp keepalives data race by @donaldsharp in https://github.com/FRRouting/frr/pull/20001
* 32bit problems by @donaldsharp in https://github.com/FRRouting/frr/pull/19991
* lib: hold event loop mutex during show commands by @mjstapp in https://github.com/FRRouting/frr/pull/19985
* zebra: Coverity issue (Null pointer dereference -med severity) by @hnattamaisub in https://github.com/FRRouting/frr/pull/19907
* Alpine Docker fix ups for 3.22 by @ton31337 in https://github.com/FRRouting/frr/pull/20004
* Coverity uninitialized by @donaldsharp in https://github.com/FRRouting/frr/pull/20006
* bgpd: Activate listening socket for a default VRF when created by @ton31337 in https://github.com/FRRouting/frr/pull/20012
* lib: Change sizeof(..) to actual byte sizes for addresses by @donaldsharp in https://github.com/FRRouting/frr/pull/20013
* *:EVPN over IPv6 underlay fabric - single homed  by @chiragshah6 in https://github.com/FRRouting/frr/pull/19721
* zebra: fix import of non zebra extern_learn neighbors by @louis-6wind in https://github.com/FRRouting/frr/pull/19122
* bgpd: add evpn prefix in json output by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20024
* lib: ospf_snmp.c is compiling with warnings by @donaldsharp in https://github.com/FRRouting/frr/pull/20020
* bgpd: fix memory leak in BGP NHC TLV processing by @jaredmauch in https://github.com/FRRouting/frr/pull/20032
* bgpd: fix uninitialized variable in bgp_need_listening by @jaredmauch in https://github.com/FRRouting/frr/pull/20035
* bgpd: fix srv6-only command defaulted when 'no segment-routing ipv6' by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20040
* lib: Support epoll APIs in thread management lib by @mjstapp in https://github.com/FRRouting/frr/pull/19917
* Some initializations by @ton31337 in https://github.com/FRRouting/frr/pull/20049
* Coexistence withdraw event by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20038
* bgpd: Link L2VNI to L3VNI only when it really exists by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20050
* bgpd: print rd in evpn route output by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20044
* tests: topotest for EVPNv6 L3 functionality -- single homed by @chiragshah6 in https://github.com/FRRouting/frr/pull/19915
* bgpd: trigger inbound policy re-evaluation on AS-path list changes by @ashred-lnx in https://github.com/FRRouting/frr/pull/19832
* Extend show ip route nexthop-group commands (Summary view and ECMP filtering) by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19833
* vrrpd: [Mem leak] Vrrp interface delete fails to free connected route by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20058
* bgpd: Fix maximum-prefix session recovery for peers and peer-groups by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20068
* bgpd: Do not put confederation ASNs into AS-SET, leave them as alone by @ton31337 in https://github.com/FRRouting/frr/pull/20073
* debian, redhat: update changelog with 10.5.0 release by @Jafaral in https://github.com/FRRouting/frr/pull/20057
* evpn vxlan fixes batch1 by @soumyar-roy in https://github.com/FRRouting/frr/pull/20046
* zebra: Check if the netlink socket is _active_ before doing batch ops by @ton31337 in https://github.com/FRRouting/frr/pull/20059
* zebra: ensure zif mac_list exists before unlinking mac by @soumyar-roy in https://github.com/FRRouting/frr/pull/20095
* pimd: Prevent crash on interface removal by @soumyar-roy in https://github.com/FRRouting/frr/pull/20097
* bgpd: bounds-check when parsing incoming label in nlri by @mjstapp in https://github.com/FRRouting/frr/pull/20062
* lib: Coverity fixes by @krishna-samy in https://github.com/FRRouting/frr/pull/20082
* ospfd: Fix sign comparison warnings in SNMP code by @jaredmauch in https://github.com/FRRouting/frr/pull/20029
* lib: NULL-check idalloc pools by @soumyar-roy in https://github.com/FRRouting/frr/pull/20094
* isisd: use IPv6 MTID for SRv6 locator TLVs when IPv6 MT is enabled by @k-akashi in https://github.com/FRRouting/frr/pull/20053
* tools: fix checkpatch.pl for 'FOO < BAR && ...' by @hedrok in https://github.com/FRRouting/frr/pull/20111
* doc:fix isis narrow metric, the correct range should be 0-63 by @Shbinging in https://github.com/FRRouting/frr/pull/20119
* ospfd/isisd: fix sr local block request bug, bitmap should be uint64_t by @Shbinging in https://github.com/FRRouting/frr/pull/20118
* ospfd: Implement forwarding-address-self command by @ton31337 in https://github.com/FRRouting/frr/pull/20077
* ospfd: Fix DO_NOT_AGE flag handling by @arikauppi in https://github.com/FRRouting/frr/pull/20112
* zebra: fix crash due to lack of control of received number of srv6 SID from netlink by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/20093
* tools: increase the number of FD in frr.service by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20115
* bgpd: Allow proper shutdown of bgp dynamic peers in rare case by @donaldsharp in https://github.com/FRRouting/frr/pull/20120
* bgp: Support multiple labels in BGP-LU by @hedrok in https://github.com/FRRouting/frr/pull/19961
* bgpd: fix labeled-unicast output by @lsang6WIND in https://github.com/FRRouting/frr/pull/20018
* bfdd, ripd, ripngd: implement yang:date-and-time by @idryzhov in https://github.com/FRRouting/frr/pull/20144
* bgpd: Implement "sh bgp l2vpn evpn rt X" by @diego-lopez8 in https://github.com/FRRouting/frr/pull/20150
* zebra: EVPN L3VNI display vlan and bridge info by @chiragshah6 in https://github.com/FRRouting/frr/pull/20141
* zebra: avoid using freed vtep pointer in debug log by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20135
* Some coverity warnings fixes by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20134
* increasing vtysh cli length constraint by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20110
* bgpd: Fix Coverity issues after 19506 by @hedrok in https://github.com/FRRouting/frr/pull/20153
* lib: revert fix nexthop node entry from nhg_list by @aprathik04 in https://github.com/FRRouting/frr/pull/19862
* docs: bgp: fix typos by @kaffarell in https://github.com/FRRouting/frr/pull/20173
* bgpd: add remoteTransposedSid value in json output of vpn paths by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20126
* Revert "bgpd: add remoteTransposedSid value in json output of vpn paths" by @donaldsharp in https://github.com/FRRouting/frr/pull/20174
* bgpd: add prefix info to bgp update debug by @soumyar-roy in https://github.com/FRRouting/frr/pull/20175
* ospf6d: Fix LSA scope check in flooding for unknown LSAs by @jaredmauch in https://github.com/FRRouting/frr/pull/20081
* isisd: update snp end after pdu validate by @mgsmith1000 in https://github.com/FRRouting/frr/pull/20079
* pimd related fixes by @soumyar-roy in https://github.com/FRRouting/frr/pull/20109
* Dplane mutex cleanup by @donaldsharp in https://github.com/FRRouting/frr/pull/20015
* Apply GSHUT to originated routes when neighbor GSHUT configured by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20179
* doc: correct bfd detect-multiplier behavior by @diego-lopez8 in https://github.com/FRRouting/frr/pull/20191
* zebra: Crash within bgp_evpn_vxlan_svd_topo1 test by @hnattamaisub in https://github.com/FRRouting/frr/pull/20192
* bgpd: [TP] Add BGP FSM and session tracing with conditional fsm_event by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20193
* Simplify and cleanup mgmtd by @choppsv1 in https://github.com/FRRouting/frr/pull/20088
* bgpd: Fix Coverity issue after 19506 by @hedrok in https://github.com/FRRouting/frr/pull/20195
* ospfd: Fix ospf mtu-ignore json show command by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20113
* bgpd: fix peer type for route-map during VRF route leaking by @soumyar-roy in https://github.com/FRRouting/frr/pull/20197
* lib,bgpd,zebra: add a more efficient hash cleanup api by @mjstapp in https://github.com/FRRouting/frr/pull/20189
* lib: print ipv4 mapped ipv6 address in mixed notation by @soumyar-roy in https://github.com/FRRouting/frr/pull/20176
* docker: build/install latest libyang3 in ubuntu test container by @choppsv1 in https://github.com/FRRouting/frr/pull/20207
* Address some new coverity issues by @choppsv1 in https://github.com/FRRouting/frr/pull/20209
* bgpd: Fix link-local NH assignment on GUA deletion by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20180
* Handle RESTCONF RPC/Action input format by @choppsv1 in https://github.com/FRRouting/frr/pull/20208
* bgpd: Software version old/new encoding by @ton31337 in https://github.com/FRRouting/frr/pull/20183
* lib: event scheduling lib changes by @mjstapp in https://github.com/FRRouting/frr/pull/20216
* lib, bgpd: Move BGP-specific funcs out of lib and refactor by @hedrok in https://github.com/FRRouting/frr/pull/20139
* zebra: Drop deprecated netns command by @ton31337 in https://github.com/FRRouting/frr/pull/20227
* bgpd: Start BFD hold timer ONLY if hold-time is configured (not zero) by @ton31337 in https://github.com/FRRouting/frr/pull/20223
* lib: fix some issue with lttng tracing by @mjstapp in https://github.com/FRRouting/frr/pull/20230
* lib: Print identity for log facility by @ton31337 in https://github.com/FRRouting/frr/pull/20229
* bgpd: make route redistribution deterministic by @enkechen-panw in https://github.com/FRRouting/frr/pull/20187
* lib: northbound: fix coverity #1667734 by @choppsv1 in https://github.com/FRRouting/frr/pull/20231
* lib: fix nb_cli_apply_changes_mgmt() return code by @ak503 in https://github.com/FRRouting/frr/pull/20226
* build: minor fixes (inet_ntop, no_sanitize, C++ strlcpy) by @eqvinox in https://github.com/FRRouting/frr/pull/20234
* tests: don't access event struct in grpc unit test by @mjstapp in https://github.com/FRRouting/frr/pull/20235
* A few small improvements to topotests by @choppsv1 in https://github.com/FRRouting/frr/pull/20217
* tests: Fix pim_dense by @donaldsharp in https://github.com/FRRouting/frr/pull/20247
* bgpd: Add more connection direction debugging by @donaldsharp in https://github.com/FRRouting/frr/pull/20250
* bgpd: Support sending multiple labels in BGP-LU + topotest by @hedrok in https://github.com/FRRouting/frr/pull/20218
* ripd: Do not send updates on disabled networks by @ton31337 in https://github.com/FRRouting/frr/pull/20253
* A few small  fixes (mgmtd/northbound) from a separate project. by @choppsv1 in https://github.com/FRRouting/frr/pull/20251
* vtysh: implement clear command by @kaffarell in https://github.com/FRRouting/frr/pull/20242
* Spelling errors have krept in by @donaldsharp in https://github.com/FRRouting/frr/pull/20254
* *: only include frr json.h where needed by @mjstapp in https://github.com/FRRouting/frr/pull/20244
* zebra: fix dvni nexthop install for IPv6 routes with ipv4 VTEP by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/20228
* tests: A bunch of tests have had debug statements creep in by @donaldsharp in https://github.com/FRRouting/frr/pull/20258
* bgpd: add remoteTransposedSid value in json output of vpn paths by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20255
* Some test fixes by @donaldsharp in https://github.com/FRRouting/frr/pull/20261
* Use underlay weights by @donaldsharp in https://github.com/FRRouting/frr/pull/20257
* bgpd: correction in json output structure for no data case by @Pdoijode in https://github.com/FRRouting/frr/pull/20268
* ospfd: fix bug allowing vlink creation on non-ABRs by @diego-lopez8 in https://github.com/FRRouting/frr/pull/20213
* tests: add topotest for deleting rip instance by @drosarius in https://github.com/FRRouting/frr/pull/20236
* bgpd: Additional commits for graceful restart by @Pdoijode in https://github.com/FRRouting/frr/pull/20239
* lib: Fix snprintf buffer overflow in PTM CSV encoding by @soumyar-roy in https://github.com/FRRouting/frr/pull/20237
* bgpd: Fix route node lock leak in NHT resolved prefix marking by @mike-dubrovsky in https://github.com/FRRouting/frr/pull/20211
* zebra: ra lifetime and interval check by @soumyar-roy in https://github.com/FRRouting/frr/pull/20096
* doc: Expand some of the acronyms in EVPN page by @remram44 in https://github.com/FRRouting/frr/pull/20051
* bgpd: Fix Coverity analysis by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20293
* tests: add topotest for setting RIP default-metric by @drosarius in https://github.com/FRRouting/frr/pull/20269
* Bgp peer connection changes by @donaldsharp in https://github.com/FRRouting/frr/pull/20263
* route-map encapsulation gretap by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19786
* zebra: notify nht client about protocol type change by @enkechen-panw in https://github.com/FRRouting/frr/pull/17117
* staticd: Fix SRv6 uA SID installation by @cscarpitta in https://github.com/FRRouting/frr/pull/19981
* tests: remove incorrect test code by @choppsv1 in https://github.com/FRRouting/frr/pull/20312
* zebra: add CLI 'no' versions for max-bw and others by @hedrok in https://github.com/FRRouting/frr/pull/20313
* bgpd: fix coverity "Dereferencing null pointer" by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20309
* ripd: Speed up convergence of rip_default_metric by @donaldsharp in https://github.com/FRRouting/frr/pull/20307
* staticd: Prevent deleting a static route if blackhole type is not the same by @ton31337 in https://github.com/FRRouting/frr/pull/20298
* ospf6d: Fix handling of default-routes by @Max-Mustermann33 in https://github.com/FRRouting/frr/pull/20296
* zebra: don't access ifp from dplane pthread by @mjstapp in https://github.com/FRRouting/frr/pull/20289
* bgpd: flood of trace commits by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20196
* zebra: make nd ra prefix cmd idompotent by @soumyar-roy in https://github.com/FRRouting/frr/pull/20320
* bgpd: Allow LL peering to update v6 GUA by @donaldsharp in https://github.com/FRRouting/frr/pull/20315
* ospf6d: Route-Map parameter forwarding-address functionality not work… by @soumyar-roy in https://github.com/FRRouting/frr/pull/20306
* tests: Add a `show ip rip` to test_rip_del_instance by @donaldsharp in https://github.com/FRRouting/frr/pull/20275
* zebra: flood of trace commits by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20232
* bgpd: Treat as withdraw iBGP session when total attr length is path attributes by @ton31337 in https://github.com/FRRouting/frr/pull/20322
* Move client-specific data out of mgmtd source. by @choppsv1 in https://github.com/FRRouting/frr/pull/20323
* ospfd:add vrf option to clear process and neighbor by @soumyar-roy in https://github.com/FRRouting/frr/pull/20178
* bfd: store actual timeout information in bfd by @sougatahitcs in https://github.com/FRRouting/frr/pull/20210
* Peer connection on startup by @donaldsharp in https://github.com/FRRouting/frr/pull/20265
* bgpd: add 'match as-path-count' command to restrict AS path count by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/20282
* bgpd: Do not send software-version capability if it's disabled explictly by @ton31337 in https://github.com/FRRouting/frr/pull/20281
* zebra: Add counter for ND router solicitations received by @soumyar-roy in https://github.com/FRRouting/frr/pull/20319
* bgpd: Send route-refresh and/or trigger soft reconfig on enforce-first-as by @ton31337 in https://github.com/FRRouting/frr/pull/20341
* Fix unnecessary mgmtd, daemon connection reset on config validation failure by @choppsv1 in https://github.com/FRRouting/frr/pull/20332
* various srv6 fixes by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20256
* Fix mgmtd abort (core) during exit with in-progress config change by @choppsv1 in https://github.com/FRRouting/frr/pull/20356
* docker: modify libyang version in Dockerfile for centos-8 by @yushoyamaguchi in https://github.com/FRRouting/frr/pull/20342
* Add error codes and improve operator messaging by @Pdoijode in https://github.com/FRRouting/frr/pull/20302
* ospfd: fix delete sr-local-label bug by @Shbinging in https://github.com/FRRouting/frr/pull/20363
* tests: Unreachable code at bgp.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/20362
* bgpd: Move mpath pointer from bgp_path_info to bgp_dest by @GaladrielZhao in https://github.com/FRRouting/frr/pull/19880
* bgpd: Do not crash if we receive a next-hop length not as expected for NHC by @ton31337 in https://github.com/FRRouting/frr/pull/20367
* bgpd: fix import vrf command by @louis-6wind in https://github.com/FRRouting/frr/pull/20288
* Bgp explicit connection direction by @donaldsharp in https://github.com/FRRouting/frr/pull/20328
* bgpd: output 'graceful-restart' value for peer group in 'write' command by @hedrok in https://github.com/FRRouting/frr/pull/20338
* bgpd: update source address for bgp neighbor by @anlancs in https://github.com/FRRouting/frr/pull/20330
* pimd: Remove weird Hidden message in help string by @donaldsharp in https://github.com/FRRouting/frr/pull/20368
* lib: adapt to libyang4 NBC API changes by @choppsv1 in https://github.com/FRRouting/frr/pull/20259
* Graceful restart for EVPN  by @Pdoijode in https://github.com/FRRouting/frr/pull/19778
* docker: Add missing `pytest` package for Alpine as dependency by @ton31337 in https://github.com/FRRouting/frr/pull/20369
* zebra: Transform FreeBSD to use the dplane for route changes. by @donaldsharp in https://github.com/FRRouting/frr/pull/20300
* mgmtd fix init config retry by @choppsv1 in https://github.com/FRRouting/frr/pull/20387
* zebra: Update promiscuity flag silently without route resets by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20181
* zebra: Fix coverity reported issue - 1668074 by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20399
* ci: add retry logic for apt and curl to handle transient failures - default 3 times by @vjardin in https://github.com/FRRouting/frr/pull/20403
* bgpd: Use the default local-preference value and not 0 when adjusting by @ton31337 in https://github.com/FRRouting/frr/pull/20400
* yang: Reorderd must constraints in frr-eigrpd module by @y-bharath14 in https://github.com/FRRouting/frr/pull/20384
* isisd clean up: migrate lists to typesafe DLIST and fix minor memory leaks by @vjardin in https://github.com/FRRouting/frr/pull/20351
* staticd: Fix CID 1668073 (NULL pointer dereference in SRv6 code) by @cscarpitta in https://github.com/FRRouting/frr/pull/20405
* eigrpd: Prevent crash in packet handling by @donaldsharp in https://github.com/FRRouting/frr/pull/20410
* zebra: Remove zrouter.zav.asic_notification_nexthop_control by @donaldsharp in https://github.com/FRRouting/frr/pull/20377
* tests: add topotest for disabling rip neighbor by @drosarius in https://github.com/FRRouting/frr/pull/20411
* fix show `frr-vrf:lib/vrf/state` query by @choppsv1 in https://github.com/FRRouting/frr/pull/20421
* bgpd: Optimize BGP path lookup using typesafe hash for efficient lookup by @krishna-samy in https://github.com/FRRouting/frr/pull/20331
* doc: fix bgp unnumbered neighbor interface command syntax by @kaffarell in https://github.com/FRRouting/frr/pull/20422
* tests: show some broken pim behavior by @donaldsharp in https://github.com/FRRouting/frr/pull/20406
* doc: Exclude 240.0.0.0/4 from allow-reserved-ranges by @ton31337 in https://github.com/FRRouting/frr/pull/20424
* Gdb macros cleanup and add by @donaldsharp in https://github.com/FRRouting/frr/pull/20423
* Some test fixes 2 by @donaldsharp in https://github.com/FRRouting/frr/pull/20264
* Rnh per client by @donaldsharp in https://github.com/FRRouting/frr/pull/20308
* SID extension to 32bits by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19223
* ripngd: Fix CLI description default values for a default flush interval by @ton31337 in https://github.com/FRRouting/frr/pull/20426
* zebra: Modify the function to obtain GR client by @Pdoijode in https://github.com/FRRouting/frr/pull/20419
* bgpd: don't set ATTR_ES_IS_LOCAL for ESI in bypass by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20417
* zebra: Fix memory leak when SRv6 explicit SID allocation fails by @cscarpitta in https://github.com/FRRouting/frr/pull/20429
* tests: rip_topo1: use vtysh_cmd() instead of bare vtysh commands by @vjardin in https://github.com/FRRouting/frr/pull/20433
* zebra: EVPN fix L3VNI to L2VNI transition by @chiragshah6 in https://github.com/FRRouting/frr/pull/20334
* bfdd: Lttng traces for bfdd module by @hnattamaisub in https://github.com/FRRouting/frr/pull/20365
* ripngd: drop listnode, migrate to typesafe container API by @vjardin in https://github.com/FRRouting/frr/pull/20432
* bgpd: Drop unused BGP_NOTIFY_UPDATE_UNREACH_NEXT_HOP notify subcode by @ton31337 in https://github.com/FRRouting/frr/pull/20425
* tests: Catching too general exception Exception by @y-bharath14 in https://github.com/FRRouting/frr/pull/20427
* ripd: drop listnode, migrate to typesafe container API by @vjardin in https://github.com/FRRouting/frr/pull/20431
* tests: add topotest for rip split-horizon by @drosarius in https://github.com/FRRouting/frr/pull/20436
* tests: ripng_topo1: use vtysh_cmd() instead of bare vtysh commands by @vjardin in https://github.com/FRRouting/frr/pull/20434
* zebra: Fix memory leak when SRv6 dynamic SID allocation fails by @cscarpitta in https://github.com/FRRouting/frr/pull/20445
* bgpd: clear write fifo when disabling io writes by @mjstapp in https://github.com/FRRouting/frr/pull/20248
* ospfd: Fix NULL Pointer Deference when dumping opaque lsa by @louis-6wind in https://github.com/FRRouting/frr/pull/19983
* isisd: fix crash when changing isis type by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20171
* tests: add topotest for rip distance command by @drosarius in https://github.com/FRRouting/frr/pull/20276
* pimd: capture pim_msg_send_frame return by @soumyar-roy in https://github.com/FRRouting/frr/pull/20304
* tools: Speed up nested peer-group remote-as search in frr-reload.py by @mwinter-osr in https://github.com/FRRouting/frr/pull/20390
* ripd: Fix default-route accept and announce by @mwinter-osr in https://github.com/FRRouting/frr/pull/20416
* ci: add LTTng tracepoint compilation check by @vjardin in https://github.com/FRRouting/frr/pull/20467
* *:EVPN IPv6 VTEP support  - Multihomed  by @chiragshah6 in https://github.com/FRRouting/frr/pull/20116
* zebra: resolve compilation warnings by @mjstapp in https://github.com/FRRouting/frr/pull/20475
* bgpd: fix compilation with lttng trace by @maxime-leroy in https://github.com/FRRouting/frr/pull/20474
* Revert RIP/RIPng default flush timer change by @ton31337 in https://github.com/FRRouting/frr/pull/20456
* cl frr to upstream frr bfd commits by @sougatahitcs in https://github.com/FRRouting/frr/pull/20327
* tests: add a retry timeout to verify_admin_distance by @mjstapp in https://github.com/FRRouting/frr/pull/20478
* Fix Batch Clearing to not skip path_info's by @donaldsharp in https://github.com/FRRouting/frr/pull/20482
* zebra: EVPN spell check mac n mh files by @chiragshah6 in https://github.com/FRRouting/frr/pull/20465
* zebra: Expand the EVPN help string in `debug zebra evpn..` by @donaldsharp in https://github.com/FRRouting/frr/pull/20483
* tests: comment out debugs in bgp_batch_clearing topotest by @mjstapp in https://github.com/FRRouting/frr/pull/20485
* zebra: EVPN check l3vni vxlan intf exist in rmac install by @chiragshah6 in https://github.com/FRRouting/frr/pull/20494
* bgpd: EVPN MH spell check for evpn_mh files by @chiragshah6 in https://github.com/FRRouting/frr/pull/20480
* ospfd: fixed ospf nssa flush issue by @drosarius in https://github.com/FRRouting/frr/pull/20428
* ripngd: remove dead assignment in ripng_ecmp_delete - Coverity by @vjardin in https://github.com/FRRouting/frr/pull/20492
* bgpd: Improve warning message when the neighbor is not active for AFI/SAFI by @ton31337 in https://github.com/FRRouting/frr/pull/20481
* bgpd: Fix multipath decision when multipath is 1 by @donaldsharp in https://github.com/FRRouting/frr/pull/20493
* pimd,pim6d: PIM interface timer knobs by @rzalamena in https://github.com/FRRouting/frr/pull/18278
* zebra: fix spell check in various files by @chiragshah6 in https://github.com/FRRouting/frr/pull/20513
* lib, vtysh: Fix `log timestamp precision` to actually be carried through by @donaldsharp in https://github.com/FRRouting/frr/pull/20510
* zebra: fix the access-vlan vni refcount on bridge flap by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20512
* lib,pimd,pim6d,yang: IPv6 extended access list by @rzalamena in https://github.com/FRRouting/frr/pull/19581
* pimd, pim6d: display iface ssm mode by @ak503 in https://github.com/FRRouting/frr/pull/20466
* bgpd: fix bugs with suppress-duplicates by @enkechen-panw in https://github.com/FRRouting/frr/pull/20325
* zebra: Cleanup the mac & neigh entry on vni transition(l2->l3) by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20464
* zebra: Allow tentative IPv6 addresses on DOWN interfaces by @routingrocks in https://github.com/FRRouting/frr/pull/20526
* bgpd: fix MRAI in route withdraw by @enkechen-panw in https://github.com/FRRouting/frr/pull/20533
* zebra: Fix tentative address handling to respect dplane data model by @routingrocks in https://github.com/FRRouting/frr/pull/20532
* bgp: ipv4 session comes up before ipv6 address is configured on link (BGP configured to AF6 && AF4) by @enissim in https://github.com/FRRouting/frr/pull/20360
* Add IPv6 support for ip import-table by @marek22k in https://github.com/FRRouting/frr/pull/20142
* bgpd: Reevaluate ead-evi routes for all VNI on disable-ead-evi-tx knob flap by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20479
* bgpd: remove assert in batch-clearing by @mjstapp in https://github.com/FRRouting/frr/pull/20546
* pimd: compute inherited_olist before checking for (S,G,rpt) prune dec… by @hnattamaisub in https://github.com/FRRouting/frr/pull/20521
* github: Rename PR template by @ton31337 in https://github.com/FRRouting/frr/pull/20547
* bgpd: reduce ibuf_work ring buffer size by @ashred-lnx in https://github.com/FRRouting/frr/pull/20554
* bgpd: remove unused argument in bgp_adj_out_unset_subgroup() by @enkechen-panw in https://github.com/FRRouting/frr/pull/20555
* zebra: fix crash on inactive VRF and import table by @hedrok in https://github.com/FRRouting/frr/pull/20525
* yang: Fix pyang errors in frr-filter.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20558
* Send register in fhr lhr case by @donaldsharp in https://github.com/FRRouting/frr/pull/20575
* pimd: Keep track of how long the S,G rpt Prune has been around by @donaldsharp in https://github.com/FRRouting/frr/pull/20576
* pimd: Immediately remove the join/prune from the nbr on ifp change, gdb macros update by @donaldsharp in https://github.com/FRRouting/frr/pull/20586
* tests: Allow connected routes to come up in zebra_rnh_testing by @donaldsharp in https://github.com/FRRouting/frr/pull/20568
* bgpd: fix spell check in various files by @chiragshah6 in https://github.com/FRRouting/frr/pull/20590
* pimd, tests: Add pim test showing that registers work with no path -> rp by @donaldsharp in https://github.com/FRRouting/frr/pull/20577
* bgpd: fix update-group issues with sender-aspath-loop-detection by @enkechen-panw in https://github.com/FRRouting/frr/pull/20593
* update munet to latest version 0.17.2 by @choppsv1 in https://github.com/FRRouting/frr/pull/20597
* mgmtd: fix xpath prefix matching, and a NULL ptr deref by @choppsv1 in https://github.com/FRRouting/frr/pull/20596
* pimd,pim6d: implement PIM join filtering by @rzalamena in https://github.com/FRRouting/frr/pull/19299
* bgpd: Use src path attr under a knob, for bestpath calculation by @soumyar-roy in https://github.com/FRRouting/frr/pull/20056
* lib, zebra: support incremental json output [Draft] by @mjstapp in https://github.com/FRRouting/frr/pull/20166
* zebra: remove unnecessary arg to rib_addnode/rib_link by @DrunkSkipper in https://github.com/FRRouting/frr/pull/20598
* github: Delete merged branches by @ton31337 in https://github.com/FRRouting/frr/pull/20603
* bgpd: Do not clear writes on keeper when transferring connection by @donaldsharp in https://github.com/FRRouting/frr/pull/20602
* zebra: simplify else clause by @DrunkSkipper in https://github.com/FRRouting/frr/pull/20604
* yang: Imported module ietf-yang-types not used at frr-isisd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20473
* tests: Removed duplicate imported modules by @y-bharath14 in https://github.com/FRRouting/frr/pull/20620
* isisd: fix method to access parent structure by @pguibert6WIND in https://github.com/FRRouting/frr/pull/20612
* zebra: skip kernel provider work when skip_kernel is set by @maxime-leroy in https://github.com/FRRouting/frr/pull/20621
* lib: fix array-index logic in json lib module by @mjstapp in https://github.com/FRRouting/frr/pull/20625
* yang: Correct pyang errors in frr-route-map.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20609
* tests: Fix weighted_ecmp, `show nexthop-group rib json` output has ch… by @donaldsharp in https://github.com/FRRouting/frr/pull/20606
* tests: There is no pytest.mark.zebra by @donaldsharp in https://github.com/FRRouting/frr/pull/20626
* fix vrf active value in YANG oper-state by @choppsv1 in https://github.com/FRRouting/frr/pull/20633
* tests: Fix convergence issue in evpn_pim_1 by @donaldsharp in https://github.com/FRRouting/frr/pull/20635
* zebra: Fix early route processing cleanup when kernel routes are clea… by @donaldsharp in https://github.com/FRRouting/frr/pull/20641
* Fix for zebra crash and ASAN on es config, bond unlinked to bridge by @raja-rajasekar in https://github.com/FRRouting/frr/pull/20600
* tests: Add a longer delay for checking vrf state for test_ds_notify.py by @donaldsharp in https://github.com/FRRouting/frr/pull/20642
* ospfd: fix NULL new_table dereference in get_nexthop_by_addr by @LyZephyr in https://github.com/FRRouting/frr/pull/20656
* yang: Fix pyang errors in frr-ospf-route-map.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20655
* tests: Fix test_ds_notify.py to wait for mgmtd to fully have requests by @donaldsharp in https://github.com/FRRouting/frr/pull/20658
* *: various spell fixes round 3 by @chiragshah6 in https://github.com/FRRouting/frr/pull/20662
* pimd: fix the condition under which we print 'no rp' debug msg by @Jafaral in https://github.com/FRRouting/frr/pull/20652
* yang: Correct pyang errors in frr-pim.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/20664
* pimd: regiface added to ssm group mroute by @soumyar-roy in https://github.com/FRRouting/frr/pull/20303
* pimd: fix nexthop update issue during link up/down events by @hnattamaisub in https://github.com/FRRouting/frr/pull/20614
* doc: fix nhrp config typo by @mjstapp in https://github.com/FRRouting/frr/pull/20667
* tests: log test start, end and result to all log files by @choppsv1 in https://github.com/FRRouting/frr/pull/20651
* zebra: FRR restart leads to zebra mlag core (backport #20225) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20677
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… (backport #20661) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20688
* staticd: Fix SRv6 SID use-after-free on locator deletion (backport #20660) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20689
* bgpd: use BGP_PATH_INFO_NUM_LABELS macro in bgp_evpn_path_info_get_l3vni (backport #20679) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20707
* bgpd: fix md5 password unset on dynamic nbr (backport #20740) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20741
* bgpd: Show all advertised paths including non-best paths only if addpath is enabled (backport #20618) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20757
* bgpd: fix batch clearing resume to use correct lookup APIs (backport #20738) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20748
* ospf6d: Fix FULL adjacency persisting despite MTU mismatch (backport #20681) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20758
* Non route replace semantics (backport #20725) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20759
* yang: Fix pyang errors in frr-bgp-filter.yang (backport #20746) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20766
* bgpd: Ignore transitiveness flag when checking type for link bandwidth (backport #20607) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20753
* bgpd: EVPN MH fix unimport ES route on vtep change (backport #20730) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20772
* Zebra fixup nhg handling from kernel (backport #20732) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20780
* zebra: Updation of ifp->flags (backport #20769) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20787
* bgpd: unref routes when yielding during clearing iteration (backport #20789) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20795
* bgpd: validate incoming NOTIFICATION messages (backport #20796) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20806
* bgpd: fix premature deletion of already-stale routes during GR clearing (backport #20768) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20801
* Multiple local fix (backport #20798) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20815
* bgpd: improve flowspec NLRI validation (backport #20814) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20825
* zebra: EVPN fix access BD deref of mbr intf (backport #20791) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20833
* Fix ospf checksum #20706 (backport #20729) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20840
* pimd,ospfd: Passing local source address as part of BFD session creation (backport #20739) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20848
* babeld: fix NULL pointer dereference in babel_clean_routing_process (backport #20727) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20849
* debian: prefer libyang3 over libyang2 when building deb packages (backport #20871) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20873
* tools: Add ldp commands to support bundle generation (backport #20863) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20876
* ldpd: Reuse port for ldpd sockets that set local ports (backport #20858) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20878
* tests: Fix grpc-query.py to find micronet (backport #20880) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20885
* pimd: When address change ensure DR changes too. (backport #20881) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20890
* lib/typesafe: guard skiplist level generation against ctz(0) UB (backport #20899) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20903
* tests: fix some python and test syntax (backport #20905) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20915
* Always compare med fix (backport #20909) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20916
* ospf6d: recalculate AS-external routes on non-external RIB updates (backport #20882) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20907
* bgpd: fix memory leak in cluster_intern() (backport #20913) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20918
* tests: Allow for different bestpaths to be generated. (backport #20889) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20922
* doc: add some text regarding libyang versions (backport #20862) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20923
* nhrpd: fix packet and buffer handling errors (backport #20932) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20940
* eigrpd: handle the gr neighbor list safely in update_receive (backport #20933) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20937
* lib: display End.DX2 route with appropriate oif attribute (backport #20954) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20958
* bgpd: Add missing PEER_FLAG_SEND_NHC_ATTRIBUTE for update group flags (backport #20956) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20969
* bgpd: Fix test for OPEN message with remote-as auto (backport #20963) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20964
* isisd: Fix remaining buffer size calculation in lsp_bits2string (backport #20984) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20987
* bgpd: Fix condition when evaluating paths (backport #20975) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20996
* bgpd: Fix nht to properly notice a change (backport #20986) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20998
* Add support for libyang5 (backport #20895) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20999
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21012
* GitHub ci improvements (backport #21003) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21021
* ospf6d: clear local ifp per ECMP path rebuild (backport #21037) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21039
* Fix docker (Alpine) compilation (backport #21042) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21046
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21058
* lib: fix zclient crash when many peers reconnect after FRR restart (backport #21056) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21069
* lib: fix vty_is_closed() falsely reporting VTY_SHELL as closed (backport #21082) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21090
* bgpd: Check if the NHC length is enough to fill TLV value + TLV header (backport #21074) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21083
* ospfd: fix sequence number check, avoid truncation ambiguity (backport #21096) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21110
* nhrpd: Correct addrlen check in os_recvmsg() (backport #21100) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21119
* ldpd: improve tlv validation in several places (backport #21118) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21129
* bgpd: fix errors in several paths (backport #21101) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21144
* PIM message-handling code fixes (backport #21093) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21136
* tests: Slow down test_config.py to allow for processing time to happen (backport #21127) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21157
* isisd: fix edge condition in max_lsp_count computation (backport #21159) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21160
* lib: fix crash in thread_process_io_inner_loop on stale epoll event (backport #21124) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21156
* bgpd: Return 0 if AS4 capability is malformed (backport #21112) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21168
* tests: Ensure upstream IIF is in correct state after interface events (backport #21114) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21155
* bgpd: Prevent heap use-after-free for tunnel encapsulation attribute (backport #21176) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21177
* CI:  fix node js deprecation warning, limit mergify backports github ci runs (backport #21175) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21184
* isisd: fix memory leak in remove_excess_adjs() (backport #21183) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21200
* isisd: Fix missing neighbor address Sub-TLVs after link-params change (backport #21204) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21212
* bgpd: improve packet parsing for EVPN and ENCAP/VNC (backport #21098) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21234
* nhrpd:  harden against malformed packets (backport #21097) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21226
* bgpd: harden attribute parsing and packet handling in a few places (backport #21095) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21223
* bgpd: fix NHT for explicit link-local BGP peers (backport #21188) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21218
* ripngd: fix data handling in several places (backport #21217) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21246
* bgpd: Recent bugs for 10.6 by @ton31337 in https://github.com/FRRouting/frr/pull/21256
* vrrrpd: improve error handling in several paths (backport #21251) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21267
* bfdd: harden packet validation and reflector handling (backport #21105) by @Jafaral in https://github.com/FRRouting/frr/pull/21255
* pimd: In sparse-dense mode, treat a group as sparse if an RP is configured (backport #21216) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21291
* tests: Give more time for interface information to show up (backport #21278) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21292
* bgpd: flowspec foobar hardening (backport #21308) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21311
* ospf6d: improve/harden packet processing (backport #21277) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21322
* bgpd: Revalidate locally originated routes against RPKI changes (backport #21302) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21332
* Rpki fix and test improvements (backport #21315) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21327
* pceplib: validate during of_list TLV decoding (backport #21310) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21317
* eigrpd: improve validation and error-handling in tlv parsing (backport #21316) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21362
* pimd: fix crash due to double free (backport #21354) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21358

## New Contributors
* @ritika0313 made their first contribution in https://github.com/FRRouting/frr/pull/19699
* @jkoshy made their first contribution in https://github.com/FRRouting/frr/pull/19777
* @e-wing made their first contribution in https://github.com/FRRouting/frr/pull/19765
* @markx-arista made their first contribution in https://github.com/FRRouting/frr/pull/19794
* @jaredmauch made their first contribution in https://github.com/FRRouting/frr/pull/20032
* @k-akashi made their first contribution in https://github.com/FRRouting/frr/pull/20053
* @arikauppi made their first contribution in https://github.com/FRRouting/frr/pull/20112
* @diego-lopez8 made their first contribution in https://github.com/FRRouting/frr/pull/20150
* @drosarius made their first contribution in https://github.com/FRRouting/frr/pull/20236
* @remram44 made their first contribution in https://github.com/FRRouting/frr/pull/20051
* @yushoyamaguchi made their first contribution in https://github.com/FRRouting/frr/pull/20342
* @enissim made their first contribution in https://github.com/FRRouting/frr/pull/20360
* @marek22k made their first contribution in https://github.com/FRRouting/frr/pull/20142
* @DrunkSkipper made their first contribution in https://github.com/FRRouting/frr/pull/20598

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.6.0-dev...frr-10.6.0

## frr-10.5.3

Debian Packages - https://deb.frrouting.org/

RPM Packages - https://rpm.frrouting.org/

Snaps - https://snapcraft.io/frr

Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:37b42d2b340c322edc5f20dc4598373adb6e813e95cc9d4a18f64f9a37c98a4c)

## What's Changed
* pimd: When address change ensure DR changes too. (backport #20881) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20891
* lib/typesafe: guard skiplist level generation against ctz(0) UB (backport #20899) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20904
* bgpd: fix memory leak in cluster_intern() (backport #20913) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20919
* doc: add some text regarding libyang versions (backport #20862) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20924
* eigrpd: handle the gr neighbor list safely in update_receive (backport #20933) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20938
* nhrpd: fix packet and buffer handling errors (backport #20932) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20941
* bgpd: Fix test for OPEN message with remote-as auto (backport #20963) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20965
* bgpd: Add missing PEER_FLAG_SEND_NHC_ATTRIBUTE for update group flags (backport) by @ton31337 in https://github.com/FRRouting/frr/pull/20972
* bgpd: check more during flowspec nlri parsing (backport #19909) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20982
* bgpd: Fix condition when evaluating paths (backport #20975) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20997
* ospfd: harden TE/SR TLV iteration against malformed lengths (backport #21002) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21013
* bfdd: Fix wrong memory free when using ttable code (backport #21020) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21022
* bgpd: fix off-by-one error in FlowSpec operator array bounds check (backport #21054) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21059
* lib: fix zclient crash when many peers reconnect after FRR restart (backport #21056) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21070
* lib: fix vty_is_closed() falsely reporting VTY_SHELL as closed (backport #21082) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21091
* bgpd: Check if the NHC length is enough to fill TLV value + TLV header (backport #21074) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21084
* ospfd: fix sequence number check, avoid truncation ambiguity (backport #21096) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21111
* nhrpd: Correct addrlen check in os_recvmsg() (backport #21100) by @mergify[bot] in https://github.com/FRRouting/frr/pull/21120

## frr-10.5.2

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:94e78424a15839e0953623e2515c3e54f308644946395bc341b25e43f5c2d323)

## What's Changed
* bgpd: Do not crash if we receive a next-hop length not as expected for NHC (backport #20367) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20370
* bgpd: update source address for bgp neighbor (backport #20330) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20372
* Alpine Docker fix ups for 3.22 (backport #20004) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20379
* docker: Add missing `pytest` package for Alpine as dependency (backport #20369) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20391
* bgpd: Use the default local-preference value and not 0 when adjusting (backport #20400) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20407
* eigrpd: Prevent crash in packet handling (backport #20410) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20414
* zebra: Fix memory leak when SRv6 explicit SID allocation fails (backport #20429) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20438
* zebra: Fix memory leak when SRv6 dynamic SID allocation fails (backport #20445) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20448
* isisd: fix crash when changing isis type (backport #20171) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20458
* ripd: Fix default-route accept and announce (backport #20416) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20471
* Revert RIP/RIPng default flush timer change (backport #20456) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20476
* Fix Batch Clearing to not skip path_info's (backport #20482) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20487
* ospfd: fixed ospf nssa flush issue (backport #20428) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20499
* zebra: EVPN check l3vni vxlan intf exist in rmac install (backport #20494) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20495
* tests: comment out debugs in bgp_batch_clearing topotest (backport #20485) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20511
* bgpd: Fix multipath decision when multipath is 1 (backport #20493) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20504
* pimd, pim6d: display iface ssm mode (backport #20466) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20524
* lib, vtysh: Fix `log timestamp precision` to actually be carried through (backport #20510) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20515
* bgpd: Prevent unnecessary re-install of routes (backport #19788) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20537
* bgpd: remove assert in batch-clearing (backport #20546) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20548
* pimd: compute inherited_olist before checking for (S,G,rpt) prune dec… (backport #20521) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20550
* bgpd: reduce ibuf_work ring buffer size (backport #20554) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20569
* zebra: fix crash on inactive VRF and import table (backport #20525) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20560
* bgpd: output 'graceful-restart' value for peer group in 'write' command (backport #20338) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20564
* pimd: Keep track of how long the S,G rpt Prune has been around (backport #20576) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20583
* Send register in fhr lhr case (backport #20575) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20581
* pimd, tests: Add pim test showing that registers work with no path -> rp (backport #20577) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20594
* fix vrf active value in YANG oper-state (backport #20633) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20640
* zebra: FRR restart leads to zebra mlag core (backport #20225) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20671
* pimd: regiface added to ssm group mroute (backport #20303) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20669
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… (backport #20661) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20682
* staticd: Fix SRv6 SID use-after-free on locator deletion (backport #20660 for 10.5) by @cscarpitta in https://github.com/FRRouting/frr/pull/20701
* bgpd: use BGP_PATH_INFO_NUM_LABELS macro in bgp_evpn_path_info_get_l3vni (backport #20679) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20708
* bgpd: fix md5 password unset on dynamic nbr (backport #20740) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20742
* bgpd: Ignore transitiveness flag when checking type for link bandwidth (backport #20607) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20750
* bgpd: EVPN MH fix unimport ES route on vtep change (backport #20730) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20773
* Zebra fixup nhg handling from kernel (backport #20732) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20781
* bgpd: validate incoming NOTIFICATION messages (backport #20796) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20807
* bgpd: fix premature deletion of already-stale routes during GR clearing (backport) by @ton31337 in https://github.com/FRRouting/frr/pull/20804
* Multiple local fix (backport #20798) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20816
* tests: Stop several tests from running on old branch by @donaldsharp in https://github.com/FRRouting/frr/pull/20823
* bgpd: improve flowspec NLRI validation (backport #20814) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20826
* zebra: EVPN fix access BD deref of mbr intf (backport #20791) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20834
* Fix ospf checksum #20706 (backport #20729) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20841
* babeld: fix NULL pointer dereference in babel_clean_routing_process (backport #20727) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20850


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.5.1...frr-10.5.2

## frr-10.4.3

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:8745af1f9bbbc26ab11d99ccdf35e07aa3427a199749bef0cd6bb5132bb130df)

## What's Changed
* bgpd: Do not crash if we receive a next-hop length not as expected for NHC (backport #20367) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20371
* bgpd: update source address for bgp neighbor (backport #20330) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20373
* Alpine Docker fix ups for 3.22 (backport #20004) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20380
* docker: Add missing `pytest` package for Alpine as dependency (backport #20369) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20392
* bgpd: Use the default local-preference value and not 0 when adjusting (backport #20400) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20408
* eigrpd: Prevent crash in packet handling (backport #20410) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20412
* zebra: Fix memory leak when SRv6 explicit SID allocation fails (backport #20429) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20439
* zebra: Fix memory leak when SRv6 dynamic SID allocation fails (backport #20445) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20449
* isisd: fix crash when changing isis type (backport #20171) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20459
* ripd: Fix default-route accept and announce (backport #20416) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20472
* Revert RIP/RIPng default flush timer change (backport #20456) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20477
* ospfd: fixed ospf nssa flush issue (backport #20428) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20500
* zebra: EVPN check l3vni vxlan intf exist in rmac install (backport #20494) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20496
* bgpd: Fix multipath decision when multipath is 1 (backport #20493) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20505
* pimd, pim6d: display iface ssm mode (backport #20466) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20523
* bgpd: Prevent unnecessary re-install of routes (backport #19788) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20536
* bgpd: remove assert in batch-clearing (backport #20546) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20549
* pimd: compute inherited_olist before checking for (S,G,rpt) prune dec… (backport #20521) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20551
* bgpd: reduce ibuf_work ring buffer size (backport #20554) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20570
* zebra: fix crash on inactive VRF and import table (backport #20525) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20561
* pimd: Keep track of how long the S,G rpt Prune has been around (backport #20576) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20584
* Send register in fhr lhr case (backport #20575) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20582
* pimd, tests: Add pim test showing that registers work with no path -> rp (backport #20577) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20595
* zebra: FRR restart leads to zebra mlag core (backport #20225) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20672
* pimd: regiface added to ssm group mroute (backport #20303) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20670
* bgpd: Fix double-free crash in peer_delete() during doppelganger peer… (backport #20661) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20683
* staticd: Fix SRv6 SID use-after-free on locator deletion (backport #20660 for 10.4) by @cscarpitta in https://github.com/FRRouting/frr/pull/20702
* bgpd:send EOR during GR only when fib install comeplete for suppress … by @vijayalaxmi-basavaraj in https://github.com/FRRouting/frr/pull/20396
* bgpd: fix md5 password unset on dynamic nbr (backport #20740) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20743
* bgpd: Ignore transitiveness flag when checking type for link bandwidth (backport #20607) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20751
* bgpd: EVPN MH fix unimport ES route on vtep change (backport #20730) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20774
* Zebra fixup nhg handling from kernel (backport #20732) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20782
* bgpd: validate incoming NOTIFICATION messages (backport #20796) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20808
* bgpd: fix premature deletion of already-stale routes during GR clearing (backport) by @ton31337 in https://github.com/FRRouting/frr/pull/20805
* Multiple local fix (backport #20798) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20817
* bgpd: improve flowspec NLRI validation (backport #20814) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20827
* tests: Stop several tests from running on old branch (backport #20823) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20832
* zebra: EVPN fix access BD deref of mbr intf (backport #20791) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20835
* Fix ospf checksum #20706 (backport #20729) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20842


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.4.2...frr-10.4.3

## frr-10.5.1

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:848482643a8d6f56452b659ea68f6138472bb57414a4f295a7c4107a0416269c)

## Release Overview

bgpd
* Allow proper shutdown of bgp dynamic peers in rare case
* Check length for dynamic capability (software version new encoding)
* Correction in json output structure for no data case
* Fix labeled unicast inbound policy lookup
* Fix labeled-unicast output
* Fix maximum-prefix session recovery for peers and peer-groups
* Fix memory leak in bgp nhc tlv processing
* Fix route node lock leak in nht resolved prefix marking
* Fix srv6-only command defaulted when 'no segment-routing ipv6'
* Send route-refresh and/or trigger soft reconfig on enforce-first-as
* Try to handle software version capability with the new encoding format

isisd
* Use ipv6 mtid for srv6 locator tlvs when ipv6 mt is enabled

pimd
* Add pim_debug_pim_reg protection for pim register stop debug message
* Crash while trying mroute_read when fd=-1
* Df election on zebra peer down synced to the mlag peer
* Fix for mc frame loss in a sequential traffic test
* Fix pim mlag update peer zebra status upon local mlag connection restoration
* Fix warnings for pimd
* Crash when pimreg interface not present
* Crashed because of indexing invalid index in an array
* Prevent crash on interface removal

vrrpd
* vrrp interface delete fails to free connected route

zebrad
* Fix crash due to lack of control of received number of srv6 sid from netlink

## frr-10.4.2

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:9135f79a5577a5becb44d108af8c7500820fb601e776333aa61b022704a5fe95)

## Release Overview

bgpd
*  Add null-check in evpn-mh code
*  Allow proper shutdown of bgp dynamic peers in rare case
*  Check l3vni status before adv evpn vrf routes
*  Check length for dynamic capability (software version new encoding)
*  Check med flag correctly in encap_attr_export()
*  Clean up coverity warnings in bgp_routemap.c
*  Correction in json output structure for no data case
*  Crash due to usage of freed up evpn_overlay attr
*  Disable link-local capability by default
*  Do not complain in the logs if we intentionally withdraw specific attrs
*  Do not override a specified rd
*  Don't use stale 'evpn' pointer in bgp_update()
*  Evpn fix auto derive rd when user cfg removed
*  Evpn-mh fix es-evi memleak during shutdown
*  Fix bgp_attr_local_pref being set appropriately
*  Fix bgp_attr_originator_id flag in outbound attribute cache
*  Fix crash due to dangling pointer in bnc nht_info
*  Fix default vrf check while configuring md5 password
*  Fix deref_of_null.ex.cond in community_list_dup_check
*  Fix expanded extcomm list delete
*  Fix json wrapper brace consistency in neighbor commands
*  Fix labeled unicast inbound policy lookup
*  Fix labeled-unicast output
*  Fix maximum-prefix session recovery for peers and peer-groups
*  Fix memory leak in evpn mh es-evi del
*  Fix memory leak in evpn mh esi del
*  Fix overflow when decoding zapi nexthop for srv6 max segments
*  Fix refcounts at termination
*  Fix routemap evpn type-5 default route check
*  Fix weird formatting in a function
*  Notify all incoming/outgoing on peer group notify unconfig
*  Put local bgp id when sending nnhn tlv for nh characteristic
*  Try to handle software version capability with the new encoding format

isisd
*  Reorder some free() bits, pass `make check`
*  Use ipv6 mtid for srv6 locator tlvs when ipv6 mt is enabled

ospf6d
*  Fix summary deletion dropping redistributed routes
*  Protect lsa in vertex

ospfd
*  Fix crash when entering `ospf authentication key xx`
*  Ti-lfa: actually delete vertexes on list
*  Ti-lfa: free copied vertex parent
*  Ti-lfa: free tables after use

pbrd
*  Cosmetic change for one name
*  Dscp-only pbr rules not installing due to incorrect family field
*  Fix crash for inconsistent status
*  Fix memleak during pbr map deletion

pim6d
*  Don't segv on repeated mld records

pimd, pim6d
*  Changes to pimreg register socket initialization

pimd
*  Add pim_debug_pim_reg protection for pim register stop debug message
*  Allow freebsd pimd to have permission to do pim
*  Consolidate setting hold time
*  Crash while trying mroute_read when fd=-1
*  Df election on zebra peer down synced to the mlag peer
*  Fix autorp del error logging
*  Fix for mc frame loss in a sequential traffic test
*  Fix pim mlag update peer zebra status upon local mlag connection restoration
*  Fix warnings for pimd
*  Fix wrong bsm case with vrf
*  Pimd crash when pimreg interface not present
*  Pimd crashed because of indexing invalid index in an array
*  Prevent crash on interface removal
*  Properly use ip_recvif on freebsd

staticd
*  Ensure sids are allocated before installation on interface up
*  Ensure sids are uninstalled before sending them to zebra
*  Extend sid dependency check for udt4/udt46 default vrf case
*  Fix typo in srv6 sids debug logs for interface up/down events
*  Handle `udt*` sids for default vrf on sr0 intf state changes
*  Move sid interface dependency check to separate function
*  Refactor and add comments to sid interface dependency logic

vrrpd
*  Ipv6 vrrp macvlan doesn't have ipv6 link-local address
*  [mem leak] vrrp interface delete fails to free connected route

zebrad
*  Add missing debug guard in if netlink code
*  Add missing debug guard in rt netlink code
*  Check if the netlink socket is _active_ before doing batch ops
*  Cleanup early route q when removing routes.
*  Coverity issue (null pointer derefence(cid 109575))
*  Coverity issue (null pointer derefence(cid 18943))
*  Coverity issue (null pointer derefence(cid 71721))
*  Coverity issue (null pointer derefence(cid 72714))
*  Coverity issue (null pointer dereference(cid 72706))
*  Coverity issue (null pointer dereference(cid 90819))
*  Evpn fix alignment of access-vlan cli output
*  Explicitly print "exit" at the end of srv6 encap node config
*  Fix crash due to lack of control of received number of srv6 sid from netlink
*  Fix memory leak dplane providers queued contex
*  Fix memory leak dplane pthread mutex destroy
*  Fix memory leak in dplane zns info entries
*  Fix memory leak in netlink link chg err case
*  Fix missing fpm messages
*  Fix neighbor table name length
*  Fix yang data for mcast-group
*  Metric 0 is valid, don't drop to 1 on bsd
*  Reset encapsulation source address when 'no srv6' is executed
*  Workaround for a race condition caused by if_zebra_speed_update timer

## frr-10.3.3

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:e4dbf63a9b1c0f9c2a94a40feef68efbd282ba142744a5d599ecb72129be36c2)

## Release Overview

bgpd
*  Check l3vni status before adv evpn vrf routes
*  Check length for dynamic capability (software version new encoding)
*  Check med flag correctly in encap_attr_export()
*  Clean up coverity warnings in bgp_routemap.c
*  Correction in json output structure for no data case
*  Crash due to usage of freed up evpn_overlay attr
*  Do not complain in the logs if we intentionally withdraw specific attrs
*  Do not override a specified rd
*  Don't use stale 'evpn' pointer in bgp_update()
*  Evpn fix auto derive rd when user cfg removed
*  Evpn-mh fix es-evi memleak during shutdown
*  Fix bgp_attr_local_pref being set appropriately
*  Fix bgp_attr_originator_id flag in outbound attribute cache
*  Fix crash due to dangling pointer in bnc nht_info
*  Fix default vrf check while configuring md5 password
*  Fix deref_of_null.ex.cond in community_list_dup_check
*  Fix expanded extcomm list delete
*  Fix labeled unicast inbound policy lookup
*  Fix labeled-unicast output
*  Fix maximum-prefix session recovery for peers and peer-groups
*  Fix memory leak in evpn mh es-evi del
*  Fix memory leak in evpn mh esi del
*  Fix overflow when decoding zapi nexthop for srv6 max segments
*  Fix routemap evpn type-5 default route check
*  Notify all incoming/outgoing on peer group notify unconfig
*  Try to handle software version capability with the new encoding format

isisd
*  Reorder some free() bits, pass `make check`
*  Use ipv6 mtid for srv6 locator tlvs when ipv6 mt is enabled

ospf6d
*  Fix summary deletion dropping redistributed routes
*  Protect lsa in vertex

ospfd
*  Fix crash when entering `ospf authentication key xx`
*  Ti-lfa: actually delete vertexes on list
*  Ti-lfa: free copied vertex parent
*  Ti-lfa: free tables after use

pbrd
*  Cosmetic change for one name
*  Dscp-only pbr rules not installing due to incorrect family field
*  Fix crash for inconsistent status
*  Fix memleak during pbr map deletion

pim6d
*  Don't segv on repeated mld records

pimd
*  Allow freebsd pimd to have permission to do pim
*  Consolidate setting hold time
*  Fix wrong bsm case with vrf
*  Prevent crash on interface removal
*  Properly use ip_recvif on freebsd

staticd
*  Ensure sids are allocated before installation on interface up
*  Ensure sids are uninstalled before sending them to zebra
*  Extend sid dependency check for udt4/udt46 default vrf case
*  Fix typo in srv6 sids debug logs for interface up/down events
*  Handle `udt*` sids for default vrf on sr0 intf state changes
*  Move sid interface dependency check to separate function
*  Refactor and add comments to sid interface dependency logic

vrrpd
*  Ipv6 vrrp macvlan doesn't have ipv6 link-local address
*  [mem leak] vrrp interface delete fails to free connected route

zebrad
*  Add missing debug guard in if netlink code
*  Add missing debug guard in rt netlink code
*  Check if the netlink socket is _active_ before doing batch ops
*  Coverity issue (null pointer derefence(cid 109575))
*  Coverity issue (null pointer derefence(cid 18943))
*  Coverity issue (null pointer derefence(cid 71721))
*  Coverity issue (null pointer derefence(cid 72714))
*  Coverity issue (null pointer dereference(cid 72706))
*  Coverity issue (null pointer dereference(cid 90819))
*  Evpn fix alignment of access-vlan cli output
*  Explicitly print "exit" at the end of srv6 encap node config
*  Fix crash due to lack of control of received number of srv6 sid from netlink
*  Fix memory leak dplane providers queued contex
*  Fix memory leak dplane pthread mutex destroy
*  Fix memory leak in dplane zns info entries
*  Fix memory leak in netlink link chg err case
*  Fix missing fpm messages
*  Fix neighbor table name length
*  Fix yang data for mcast-group
*  Metric 0 is valid, don't drop to 1 on bsd

## frr-10.2.5

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:e60e420fdbb4eb54a793057bc5d37c0f3a115149a246b17cbde89ba77b8eec97)

## Release Overview

bgpd
* Check l3vni status before adv evpn vrf routes
* Clean up coverity warnings in bgp_routemap.c
* Crash due to usage of freed up evpn_overlay attr
* Do not override a specified rd
* Evpn fix auto derive rd when user cfg removed
* Evpn-mh fix es-evi memleak during shutdown
* Fix bgp_attr_originator_id flag in outbound attribute cache
* Fix crash due to dangling pointer in bnc nht_info
* Fix default vrf check while configuring md5 password
* Fix deref_of_null.ex.cond in community_list_dup_check
* Fix expanded extcomm list delete
* Fix labeled-unicast output
* Fix maximum-prefix session recovery for peers and peer-groups
* Fix memory leak in evpn mh es-evi del
* Fix memory leak in evpn mh esi del
* Fix overflow when decoding zapi nexthop for srv6 max segments
* Fix routemap evpn type-5 default route check

isisd
* Use ipv6 mtid for srv6 locator tlvs when ipv6 mt is enabled

ospf6d
* Protect lsa in vertex

ospfd
* Fix crash when entering `ospf authentication key xx`

pbrd
* Cosmetic change for one name
* Dscp-only pbr rules not installing due to incorrect family field
* Fix crash for inconsistent status
* Fix memleak during pbr map deletion

pim6d
* Don't segv on repeated mld records

pimd
* Allow freebsd pimd to have permission to do pim
* Fix wrong bsm case with vrf
* Prevent crash on interface removal
* Properly use ip_recvif on freebsd

vrrpd
* Ipv6 vrrp macvlan doesn't have ipv6 link-local address
* [mem leak] vrrp interface delete fails to free connected route

zebrad
* Add missing debug guard in if netlink code
* Add missing debug guard in rt netlink code
* Evpn fix alignment of access-vlan cli output
* Explicitly print "exit" at the end of srv6 encap node config
* Fix crash due to lack of control of received number of srv6 sid from netlink
* Fix neighbor table name length
* Fix yang data for mcast-group
* Metric 0 is valid, don't drop to 1 on bsd

## frr-10.5.0

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:fc7f887ab4d8da06f481a4f8d59afded88b3c5823f03610a7e808f7eba45eeea)

## Release Overview

### New Features Highlight

- **BFD the ability to listen for specific VRFs only**
  - Configure which VRFs the BFD daemon will listen to. By default, BFD listens to all VRFs present in the system, including the default VRF. Default VRF must be specified as `default`.
- **BGP SRv6/MPLS coexistence**
  - Allow MPLS and SRv6 to coexist on the same L3VRF, even for a given prefix. This feature is important in brown fields where some operators want to migrate from MPLS to SRv6 backbone.
- **BGP SRv6 locator per VRF support**
  - Ability to choose SRv6 locator per VRF.
- **BGP Error handling (RFC 7606) for iBGP peers**
  - Before 10.5.0, once we received a malformed packet between iBGP peers, we always reset the session, and with this release, we handle malformed packets the same way as for eBGP (by withdrawing or discarding the malformed packets).
- **BGP IPv6 Link-Local Capability is disabled by default**
  - In 10.4.0, this capability was enabled by default for a “datacenter” profile, but it’s disabled for 10.5.0 and will be backported to 10.4.2 as well. The problem arises when the receiver has configured a route-map with `set ipv6 next-hop prefer-global` and we send only an IPv6 Link-Local address; therefore, it was decided to revert it to be disabled by default.
- **BGP BGPID Next-Hop Characteristic**
  - In some cases, the BGP speaker sending a route might encode only a link-local address and no global address. To provide uniqueness in this case, it is sufficient to associate the BGP Identifier and AS Number of the route's sender. The BGP Identifier Characteristic (BGPID) provides a way to convey this information if required.
- **BGP EVPN flooding per VNI support**
  - Add an ability to adjust BUM flooding per VNI, instead of just globally. E.g., disable flooding only for an arbitrary VNI.
- **BGP RPKI strict mode**
  - RPKI strict mode prevents BGP from establishing a session if no RPKI cache server
    is connected.
- **BGP rejects AS_SET by default**
  - Until 10.5.0, it was disabled by default, and since RFC 9774 was published, we switched this on by default (to reject).
- **BGP has lots of improvements for Graceful-Restart**
- **PIM/PIMv6 route-map support to allow users to filter IGMP/MLD joins using source/group/ interface combinations**
- **Support for multiple SRv6 locators**
  - This extends the SRv6 SID Manager to add support for multiple locators.
- **Zebra 16-bit next hop weights support**
  - The weights used in ECMP’s consistent hashing have been widened from 8 bits to 16 bits since the 6.12 Linux kernel.


## What's Changed
* lib: Fix impossible situation with first variable by @donaldsharp in https://github.com/FRRouting/frr/pull/18995
* bgpd: Clean up evpn mac hash on shutdown. by @donaldsharp in https://github.com/FRRouting/frr/pull/18996
* bgpd: Do not reuse the same adj->adv when flushing fifo (attributes too long) by @ton31337 in https://github.com/FRRouting/frr/pull/18993
* bgpd: Fix crash when fetching statistics for bgp instance by @ton31337 in https://github.com/FRRouting/frr/pull/19003
* pimd: add boundary checks when parsing join/graft source lists (coverity) by @Jafaral in https://github.com/FRRouting/frr/pull/18989
* tests: add new /run/netns tmpfs to each topotest router namespace by @choppsv1 in https://github.com/FRRouting/frr/pull/19007
* tests: Use more complicated topology to show how NHC works by @ton31337 in https://github.com/FRRouting/frr/pull/19009
* babeld: Convert all code to use our code formatting rules by @donaldsharp in https://github.com/FRRouting/frr/pull/18630
* Fix some coverity issues by @donaldsharp in https://github.com/FRRouting/frr/pull/18897
* ospfd: adjust one display command by @anlancs in https://github.com/FRRouting/frr/pull/19022
* Add frr-host yang module - fix bug with reserved IP range config by @choppsv1 in https://github.com/FRRouting/frr/pull/19019
* mgmtd: remove unfinished and unneeded yang-validate code by @choppsv1 in https://github.com/FRRouting/frr/pull/19029
* static: [SRv6] Fixing uninstall and reinstall uA Sids upon Intf flaps by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19027
* lib: add "send log" command to log a message by @choppsv1 in https://github.com/FRRouting/frr/pull/19030
* Update to munet release 0.15.5 by @choppsv1 in https://github.com/FRRouting/frr/pull/19025
* bgpd: Allow BGP NHT resolved nodes to go early by @donaldsharp in https://github.com/FRRouting/frr/pull/19008
* bgpd:fix as-path replace issue with bgp as-path access-list by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/19017
* nhrpd: fix crash when accessing invalid memory zone by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18994
* ospf6d: Fix summary LSA removal by @gromit1811 in https://github.com/FRRouting/frr/pull/18345
* bgpd: Reject AS_SET by default by @ton31337 in https://github.com/FRRouting/frr/pull/19024
* bgpd: [TOPOTEST] stabilize bgp_peergroup_gshut test case by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/18991
* zebra: fix nexthop rib out for duplicate nhg by @chiragshah6 in https://github.com/FRRouting/frr/pull/19015
* topotests: test bfd when bgp is passive by @crosser in https://github.com/FRRouting/frr/pull/18954
* zebra: Start EVPN neighbor hold timer only when interface is operative by @routingrocks in https://github.com/FRRouting/frr/pull/18905
* tests: Notice that the support_bundle is not properly setup by @donaldsharp in https://github.com/FRRouting/frr/pull/19045
* Nhrp redundancy ping by @donaldsharp in https://github.com/FRRouting/frr/pull/19048
* pathd: fix compare function overflow by @guoguojia2021 in https://github.com/FRRouting/frr/pull/19050
* pimd: Fix Register-Stop state machine logic to align with RFC7761 by @hhubb22 in https://github.com/FRRouting/frr/pull/19023
* zebra: Initialize RB tree for router tables by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19049
* tests: Fix `bgp_srv6_sid_explicit` test failures  by @cscarpitta in https://github.com/FRRouting/frr/pull/19068
* bgpd: Soft-reconfig should not completely stall bestpath processing by @donaldsharp in https://github.com/FRRouting/frr/pull/19067
* pimd: eBGP integration for SA loop detection by @rzalamena in https://github.com/FRRouting/frr/pull/17699
* zebra: fix null pointer dereference in zebra_evpn_sync_neigh_del by @routingrocks in https://github.com/FRRouting/frr/pull/19054
* tests: munet release 0.15.6 by @choppsv1 in https://github.com/FRRouting/frr/pull/19079
* Doc and test update by @choppsv1 in https://github.com/FRRouting/frr/pull/19070
* zebra: fix stale NHG in kernel by @krishna-samy in https://github.com/FRRouting/frr/pull/18899
* bgp_bmp: fix missing loc-rib stats reports by @lsang6WIND in https://github.com/FRRouting/frr/pull/19073
* bgpd: Fix incorrect stripping of transitive extended communities due … by @nick-bouliane in https://github.com/FRRouting/frr/pull/19065
* staticd: Remove unnecessary function parameters by @zice312963205 in https://github.com/FRRouting/frr/pull/19090
* Convert logging config to YANG/mgmtd, and add missing mgmtd functionality by @choppsv1 in https://github.com/FRRouting/frr/pull/19060
* doc: remove dead link to quagga website by @mjstapp in https://github.com/FRRouting/frr/pull/19098
* debian, redhat: add missing info to changelog by @Jafaral in https://github.com/FRRouting/frr/pull/19074
* SRv6: Add support for multiple SRv6 locators by @cscarpitta in https://github.com/FRRouting/frr/pull/18806
* tests: exabgp drops `-v` flag in 4.2.25, use `--version`` by @choppsv1 in https://github.com/FRRouting/frr/pull/19111
* Bmp locrib bgp open message by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19063
* bgp_bmp: do not send end of rib by default by @lsang6WIND in https://github.com/FRRouting/frr/pull/19071
* bgpd: Implement RPKI strict mode by @ton31337 in https://github.com/FRRouting/frr/pull/19103
* lib: Fix `no on-match goto NUM` command by @ton31337 in https://github.com/FRRouting/frr/pull/19108
* bgpd: avoid BGP port opening for VRF instances by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/18962
* bgpd: Fix 'no' form for 'neighbor X ip-transparent' command by @ton31337 in https://github.com/FRRouting/frr/pull/19118
* explicit  SRv6 address configurable per address family  by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19088
* zebra: Fix coverity issues by @cscarpitta in https://github.com/FRRouting/frr/pull/19120
* bgpd: fix missing BGP_ROUTE_AGGREGATE for announcing to zebra by @enkechen-panw in https://github.com/FRRouting/frr/pull/19105
* bgpd: Fix extended community check for IP non-transitive type by @ton31337 in https://github.com/FRRouting/frr/pull/19097
* pimd, pim6d: route-map filtering for source/group by @rzalamena in https://github.com/FRRouting/frr/pull/18955
* bgpd: add output support for srv6 l3vpn attribute option by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19117
* ospfd: fix missing debug running configuration by @anlancs in https://github.com/FRRouting/frr/pull/19140
* lib: cleanup one duplicated code by @anlancs in https://github.com/FRRouting/frr/pull/19123
* tests: Allow time for change of state to propagate by @donaldsharp in https://github.com/FRRouting/frr/pull/19138
* bgpd: Fix DEREF_OF_NULL.EX.COND in bgp_updgrp_packet by @petrvaganoff in https://github.com/FRRouting/frr/pull/19126
* bgpd: adjust display format by @anlancs in https://github.com/FRRouting/frr/pull/19141
* ospf6d: Fix OSPFv3 SNMP interface state mapping by @miteshkanjariya in https://github.com/FRRouting/frr/pull/18697
* zebra: zebra core with v6 RA by @soumyar-roy in https://github.com/FRRouting/frr/pull/19000
* bfdd: add option to restrict listening VRFs by @Sashhkaa in https://github.com/FRRouting/frr/pull/19136
* bgpd: Print the warning that `bgp reject-as-sets` is enabled by @ton31337 in https://github.com/FRRouting/frr/pull/19147
* bgpd: Allow setting extcommunity link bandwidth value to zero by @ton31337 in https://github.com/FRRouting/frr/pull/19149
* lib: revert addition of vtysh_flush() call in vty_out() by @eqvinox in https://github.com/FRRouting/frr/pull/19109
* L3VNI should not be attached to Mac only type-2 routes by @miteshkanjariya in https://github.com/FRRouting/frr/pull/19089
* tests: Fix bgp_bmp tests by @donaldsharp in https://github.com/FRRouting/frr/pull/19155
* tools: add KeepEmptyLinesAtEOF to clang-format by @mjstapp in https://github.com/FRRouting/frr/pull/19157
* tests: Increase timeout for any test that uses the @retry mechanism by @donaldsharp in https://github.com/FRRouting/frr/pull/19159
* BGP SRv6 locator per vrf by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19100
* bgpd: free json objects in error paths by @mjstapp in https://github.com/FRRouting/frr/pull/19158
* bgpd: remove duplicated gr timer value by @mjstapp in https://github.com/FRRouting/frr/pull/19160
* tools: revert "tools: add KeepEmptyLinesAtEOF to clang-format" by @mjstapp in https://github.com/FRRouting/frr/pull/19167
* bgpd: Extract link bandwidth value from extcommunity before using for WCMP by @ton31337 in https://github.com/FRRouting/frr/pull/19165
* bgpd: fix "neighbor <n> local-as (null)" in running-config by @aprathik04 in https://github.com/FRRouting/frr/pull/19148
* zebra: Ensure on exit that log buffers are flushed by @donaldsharp in https://github.com/FRRouting/frr/pull/19139
* Ospf6 json output fix by @donaldsharp in https://github.com/FRRouting/frr/pull/19168
* lib,bgpd,ospf6d,zebra: Free json objects in error paths by @mjstapp in https://github.com/FRRouting/frr/pull/19182
* Add ability to see locks in mgmt’s data store, ensure in topotests that daemons are connected to mgmtd by @donaldsharp in https://github.com/FRRouting/frr/pull/19183
* zebra: clean up a json object leak by @mjstapp in https://github.com/FRRouting/frr/pull/19192
* bgpd: Do not try to reuse freed route-maps by @ton31337 in https://github.com/FRRouting/frr/pull/19191
* bgpd: update-delay timer with default-originate by @ton31337 in https://github.com/FRRouting/frr/pull/19186
* zebra: remove IRDP code by @mjstapp in https://github.com/FRRouting/frr/pull/19194
* pim6d: fix wrong residual entry by @anlancs in https://github.com/FRRouting/frr/pull/19166
* tests: Modify isis_srv6_topo1 to allow some ping failures by @donaldsharp in https://github.com/FRRouting/frr/pull/19206
* tools: Allow support bundles to generate output from ip commands by @donaldsharp in https://github.com/FRRouting/frr/pull/19205
* bgpd: fix filtered_routes_count by @mjstapp in https://github.com/FRRouting/frr/pull/19207
* tests: ldp hello generation is not exact under load by @donaldsharp in https://github.com/FRRouting/frr/pull/19208
* lib: incremental vty output, restored by @mjstapp in https://github.com/FRRouting/frr/pull/19181
* bgpd: Ensure addpath does not withdraw selected route in some situations by @donaldsharp in https://github.com/FRRouting/frr/pull/19210
* lib: fix routemap crash by @anlancs in https://github.com/FRRouting/frr/pull/19127
* pimd: drop mismatch report packets by @anlancs in https://github.com/FRRouting/frr/pull/19199
* zebra: Make coverity happy with prefix_sg declaration by @donaldsharp in https://github.com/FRRouting/frr/pull/19221
* bgpd: fix DEREF_AFTER_FREE in bgp_route by @petrvaganoff in https://github.com/FRRouting/frr/pull/19212
* tools: fix daemon starting order for debian packages by @cocomundo in https://github.com/FRRouting/frr/pull/19209
* doc: A bit of release related work by @ton31337 in https://github.com/FRRouting/frr/pull/19222
* zebra: fix typo in ip "forwarding" cli by @mjstapp in https://github.com/FRRouting/frr/pull/19225
* Gr test fixup by @donaldsharp in https://github.com/FRRouting/frr/pull/19219
* doc: Define release tags strictly to be X.Y.Z by @ton31337 in https://github.com/FRRouting/frr/pull/19227
* bgpd: initialize local variable by @mjstapp in https://github.com/FRRouting/frr/pull/19233
* ospfd: Use after free cleanup of lsa by @donaldsharp in https://github.com/FRRouting/frr/pull/19224
* topotests: improve embedded RP test reliability by @rzalamena in https://github.com/FRRouting/frr/pull/19240
* Revert PR #18358: BGP evpn testing and bug fixes related to non default EVPN backbone  by @ton31337 in https://github.com/FRRouting/frr/pull/19241
* vtysh: copy config from file should actually apply by @mjstapp in https://github.com/FRRouting/frr/pull/19242
* lib, zebra: mark singleton nexthops inactive/active on link state changes for wecmp by @karthikeyav in https://github.com/FRRouting/frr/pull/18947
* bgpd: LL next-hop capabilty fixes by @ton31337 in https://github.com/FRRouting/frr/pull/19261
* Doc some missing commands by @donaldsharp in https://github.com/FRRouting/frr/pull/19269
* Support bundle more commands by @donaldsharp in https://github.com/FRRouting/frr/pull/19268
* Test improvements by @donaldsharp in https://github.com/FRRouting/frr/pull/19270
* tests: Fix static routing test by @donaldsharp in https://github.com/FRRouting/frr/pull/19272
* tests: Modify ospf_topo1 to use run and expect for kernel routes by @donaldsharp in https://github.com/FRRouting/frr/pull/19273
* eigrp: validate hello packets and tlvs better by @mjstapp in https://github.com/FRRouting/frr/pull/19251
* bgpd: Reduce EVPN VNI processing delay from 20ms to 10ms by @routingrocks in https://github.com/FRRouting/frr/pull/19265
* bgpd : Fix compilation error in bgpd module: Update TP_ARGS for bgp by @zzzzrf in https://github.com/FRRouting/frr/pull/19266
* EVPN Documentation for Single VXLAN Device Configuration by @kniteli in https://github.com/FRRouting/frr/pull/19263
* bgpd: CLI Changes by @krishna-samy in https://github.com/FRRouting/frr/pull/17553
* lib: compute link-state zapi message size by @mjstapp in https://github.com/FRRouting/frr/pull/19290
* tests: Allow for longer period of sysfs retry by @donaldsharp in https://github.com/FRRouting/frr/pull/19288
* tests: Fix bgp_rr_ibgp tests by @donaldsharp in https://github.com/FRRouting/frr/pull/19291
* bgpd: LL next-hop capabilty fixes (round 2) by @ton31337 in https://github.com/FRRouting/frr/pull/19277
* tests: Allow detection of core dump to grab backtrace by @donaldsharp in https://github.com/FRRouting/frr/pull/19294
* Additional test fixes by @donaldsharp in https://github.com/FRRouting/frr/pull/19293
* tests: Ensure nbr is up before adding lsa by @donaldsharp in https://github.com/FRRouting/frr/pull/19289
* zebra: Clang tells us we need larger than a uint8_t by @donaldsharp in https://github.com/FRRouting/frr/pull/19292
* Bgp dual as fixes by @donaldsharp in https://github.com/FRRouting/frr/pull/19298
* tests: Fix bgp_evpn_vxlan_topo1 in one case by @donaldsharp in https://github.com/FRRouting/frr/pull/19302
* bfdd: peer information missing in static route bfd json  by @sougata-github-nvidia in https://github.com/FRRouting/frr/pull/19237
* Weighted ecmp by @donaldsharp in https://github.com/FRRouting/frr/pull/19300
* bgpd: fix do not use import|export vpn when import vrf command used by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19034
* zebra: Fix buffer overflows found by fuzzing. by @oliverchang in https://github.com/FRRouting/frr/pull/19303
* yang: add yang type for dummy interface type by @kaffarell in https://github.com/FRRouting/frr/pull/19312
* tests: svd test cleanup by @donaldsharp in https://github.com/FRRouting/frr/pull/19314
* tests: Allow gdb decoding to hit all threads by @donaldsharp in https://github.com/FRRouting/frr/pull/19318
* bgpd: fix DEREF_OF_NULL.EX.COND in community_list_dup_check by @petrvaganoff in https://github.com/FRRouting/frr/pull/19325
* build: remove C++ version restriction for grpc build by @kaffarell in https://github.com/FRRouting/frr/pull/19313
* pim6d: fix missing packet with vrf by @anlancs in https://github.com/FRRouting/frr/pull/19335
* zebra: fix up memory leak in dplane shutdown sequences by @chiragshah6 in https://github.com/FRRouting/frr/pull/19333
* pbrd: fix disorder of rule by @anlancs in https://github.com/FRRouting/frr/pull/19332
* bgpd: fix show adj-in table for labeled-unicast by @lsang6WIND in https://github.com/FRRouting/frr/pull/19358
* bgpd: Apply RFC 7606 handling even for iBGP peers by @ton31337 in https://github.com/FRRouting/frr/pull/19364
* pbrd: DSCP-only PBR rules not installing due to incorrect family field by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/19363
* bgpd: fix overflow when decoding zapi nexthop for srv6 max segments by @petrvaganoff in https://github.com/FRRouting/frr/pull/19324
* bgpd: Handle BUM traffic per-VNI by @ton31337 in https://github.com/FRRouting/frr/pull/19331
* bgpd: fix memory leak in evpn mh  by @chiragshah6 in https://github.com/FRRouting/frr/pull/19334
* zebra: fix wrong free of nd prefix by @anlancs in https://github.com/FRRouting/frr/pull/19355
* bgpd: Implement BGPID next-hop characteristic by @ton31337 in https://github.com/FRRouting/frr/pull/19349
* Revert "bgpd: Free dup'ed attributes for aggregate routes with route-maps" by @Pdoijode in https://github.com/FRRouting/frr/pull/19352
* bgpd: Fix default vrf check while configuring md5 password for prefix on the bgp listen socket by @aprathik04 in https://github.com/FRRouting/frr/pull/19317
* bgpd: Make sure `bgp` is not NULL when changing flooding type per-VNI by @ton31337 in https://github.com/FRRouting/frr/pull/19386
* doc: Fix SRv6 configuration example in IS-IS documentation by @cscarpitta in https://github.com/FRRouting/frr/pull/19402
* staticd: Fix typo in SRv6 SIDs debug logs for interface UP/DOWN events by @cscarpitta in https://github.com/FRRouting/frr/pull/19395
* zebra: Reset encapsulation source address when `no srv6` is executed  by @cscarpitta in https://github.com/FRRouting/frr/pull/19406
* zebra: Explicitly print "exit" at the end of srv6 encap node config by @cscarpitta in https://github.com/FRRouting/frr/pull/19409
* tests: Improve bgp_lu_topo1 converge by @ton31337 in https://github.com/FRRouting/frr/pull/19398
* zebra: Add missing debug guard in rt netlink code by @cscarpitta in https://github.com/FRRouting/frr/pull/19411
* tests: Update ospf6_ecmp_inter_area topotest (#16197 regression test, unified config) by @gromit1811 in https://github.com/FRRouting/frr/pull/18549
* lib: make getloadavg() optional in late timer warnings by @maxime-leroy in https://github.com/FRRouting/frr/pull/19366
* bgpd: Allow for suppress-fib to not wait for already installed route by @donaldsharp in https://github.com/FRRouting/frr/pull/19353
* bgpd: Fix crash due to dangling pointer in bnc nht_info by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/19362
* Test run speedups by @donaldsharp in https://github.com/FRRouting/frr/pull/19356
* zebra: Add missing debug guard in if netlink code by @cscarpitta in https://github.com/FRRouting/frr/pull/19422
* pimd: fix wrong bsm case with vrf by @anlancs in https://github.com/FRRouting/frr/pull/19432
* Add addpath support to EVPN by @Tuetuopay in https://github.com/FRRouting/frr/pull/18759
* lib,ospfd: support table-direct in OSPFv2 by @rzalamena in https://github.com/FRRouting/frr/pull/19316
* pimd/pim6d: fix wrong running config by @anlancs in https://github.com/FRRouting/frr/pull/19357
* staticd: Fix SRv6 SID installation for default VRF by @cscarpitta in https://github.com/FRRouting/frr/pull/19410
* bgpd: do not crash when labels are empty by @crosser in https://github.com/FRRouting/frr/pull/18679
* doc: Show proper amount of ecmp needed for tests now by @donaldsharp in https://github.com/FRRouting/frr/pull/19435
* tools: On startup/shutdown move bfdd earlier/later by @donaldsharp in https://github.com/FRRouting/frr/pull/19442
* pbrd: fix crash by @anlancs in https://github.com/FRRouting/frr/pull/19450
* zebra: Add to `show int ..` if BGP configed RA or not by @donaldsharp in https://github.com/FRRouting/frr/pull/19449
* test: Add test for clear bgp with interface down by @soumyar-roy in https://github.com/FRRouting/frr/pull/19361
* ospf6d,tools: use json_object_object_get_ex() by @mjstapp in https://github.com/FRRouting/frr/pull/19448
* nhrpd: hash_create does not fail by @donaldsharp in https://github.com/FRRouting/frr/pull/19441
* Zebra backup nhs operation by @donaldsharp in https://github.com/FRRouting/frr/pull/19443
* Labelpool changes by @donaldsharp in https://github.com/FRRouting/frr/pull/19468
* Fix pim autorp problems by @donaldsharp in https://github.com/FRRouting/frr/pull/19472
* Fix some new coverity issues by @donaldsharp in https://github.com/FRRouting/frr/pull/19446
* lib: move `clear log cmdline-targets` to YANG RPC by @choppsv1 in https://github.com/FRRouting/frr/pull/19479
* zebra: Use zebra dplane for RTM neighbor message by @Canzovo in https://github.com/FRRouting/frr/pull/19296
* pimd: Fix Autorp del error logging by @nabahr in https://github.com/FRRouting/frr/pull/19478
* mgmtd: add be client loopback connection by @choppsv1 in https://github.com/FRRouting/frr/pull/19481
* bgpd: clean up lp_release api by @mjstapp in https://github.com/FRRouting/frr/pull/19469
* lib,doc: remove zlog tmp dirs by default at exit by @mjstapp in https://github.com/FRRouting/frr/pull/19430
* tests: Modify comparison check at test_evpn_mh.py by @ramapalleti in https://github.com/FRRouting/frr/pull/19451
* tests: fitler results so new modules don't break test by @choppsv1 in https://github.com/FRRouting/frr/pull/19445
* tests: fix grpc_basic tests by @kaffarell in https://github.com/FRRouting/frr/pull/19315
* tests: Actually look for port 179 by @donaldsharp in https://github.com/FRRouting/frr/pull/19499
* bgpd: Fix RA not re-initiated when remote-as is re-added to peer group by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19487
* docs: add build instructions for debian 13 by @kaffarell in https://github.com/FRRouting/frr/pull/19491
* ospf6d: protect LSA in vertex by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/19497
* lib: Fix SQLite DB location when using pathspace option by @gromit1811 in https://github.com/FRRouting/frr/pull/19495
* Revert l3vni optimization by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19344
* bgpd: remove the implicit EOR (keepalive message) for GR by @enkechen-panw in https://github.com/FRRouting/frr/pull/19526
* doc: Add example for "Ran out of docstring" by @mjstapp in https://github.com/FRRouting/frr/pull/19528
* *: add a more efficient zapi_route_init api by @mjstapp in https://github.com/FRRouting/frr/pull/19525
* Debian build: introduce profile "pkg.frr.asan" by @crosser in https://github.com/FRRouting/frr/pull/19519
* zebra: Allow assigning any IPv4 addresses on interfaces by @ton31337 in https://github.com/FRRouting/frr/pull/19516
* ldpd: adjust display format for one command by @anlancs in https://github.com/FRRouting/frr/pull/19515
* tests: all_protocol_startup needs some more run_and_expect by @donaldsharp in https://github.com/FRRouting/frr/pull/19533
* doc, tests: Add `--ignore-backtraces` command to pytest by @donaldsharp in https://github.com/FRRouting/frr/pull/19534
* Further enhancements for GR  by @Pdoijode in https://github.com/FRRouting/frr/pull/18305
* Nexthop weights by @donaldsharp in https://github.com/FRRouting/frr/pull/19523
* bgpd: various fixes related to VPN SRv6 entries updates by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19447
* lib: improve handling of prefix-list in route-map by @mjstapp in https://github.com/FRRouting/frr/pull/19543
* tests: Corrected unidiomatic-typecheck in ospf.py by @ramapalleti in https://github.com/FRRouting/frr/pull/19517
* zebra: Allow for NOS to initialize some zrouter values by @donaldsharp in https://github.com/FRRouting/frr/pull/19493
* ldpd: fix no sending klabels to zebra by @anlancs in https://github.com/FRRouting/frr/pull/19514
* doc: Update typesafe hash to talk about memory usage by @donaldsharp in https://github.com/FRRouting/frr/pull/19550
* tests: fix several topotests for bgp GR by @enkechen-panw in https://github.com/FRRouting/frr/pull/19563
* bgpd: don't use stale 'evpn' pointer in bgp_update() by @mjstapp in https://github.com/FRRouting/frr/pull/19561
* bgpd: fix last-reset-reason in bgp_show_failed_summary() by @enkechen-panw in https://github.com/FRRouting/frr/pull/19555
* bgpd: remove the last_reset copying in peer_xfer_conn() by @enkechen-panw in https://github.com/FRRouting/frr/pull/19556
* lib: Return a valid JSON if prefix-list is not found by @ton31337 in https://github.com/FRRouting/frr/pull/19560
* lib: cleanup doc comment formatting by @choppsv1 in https://github.com/FRRouting/frr/pull/19568
* Allow notify callback on non-presence container by @choppsv1 in https://github.com/FRRouting/frr/pull/19562
* bgpd: set last_reset for the nht change only in specific cases by @enkechen-panw in https://github.com/FRRouting/frr/pull/19559
* bgpd: record the peer down cause when sending cease notification by @enkechen-panw in https://github.com/FRRouting/frr/pull/19557
* bgpd: fix refcounts at termination by @mjstapp in https://github.com/FRRouting/frr/pull/19577
* bgpd: add NULL-check in evpn-mh code by @mjstapp in https://github.com/FRRouting/frr/pull/19542
* doc: Fix typo "echo interval" -> "each interval" by @tobiaspal in https://github.com/FRRouting/frr/pull/19586
* bgpd: Convert bmp path_info tracking from hash to rbtree by @donaldsharp in https://github.com/FRRouting/frr/pull/19548
* bgpd: Remove unnecessary code in bgp_bmp.c by @donaldsharp in https://github.com/FRRouting/frr/pull/19589
* bgpd: do not change last_reset when a peer is un-shut by @enkechen-panw in https://github.com/FRRouting/frr/pull/19558
* SRv6/MPLS L3 Services Co-existence by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19164
* bgpd: Fix illegal memory access when fetching CEASE cause by @ton31337 in https://github.com/FRRouting/frr/pull/19590
* bgpd: fix the description for PEER_DOWN_NBR_ADDR by @enkechen-panw in https://github.com/FRRouting/frr/pull/19592
* bgpd: bgp_fsm.c use bgp pointer when logical instead of peer->bgp by @donaldsharp in https://github.com/FRRouting/frr/pull/19601
* bgpd: fix clumsy boolean logic by @mjstapp in https://github.com/FRRouting/frr/pull/19594
* bgpd: initialize last_reset to PEER_DOWN_NONE for a new peer by @enkechen-panw in https://github.com/FRRouting/frr/pull/19604
* bgpd: remove the definition PEER_DOWN_WAITING_OPEN by @enkechen-panw in https://github.com/FRRouting/frr/pull/19600
* Implicit bgp by @donaldsharp in https://github.com/FRRouting/frr/pull/19591
* bgpd: Fix JSON wrapper brace consistency in neighbor commands by @rvaideesh in https://github.com/FRRouting/frr/pull/19552
* Further enhancements for Graceful restart by @Pdoijode in https://github.com/FRRouting/frr/pull/19545
* lib,zebra: replace VRF_GET_ID macro with a function by @mjstapp in https://github.com/FRRouting/frr/pull/19538
* Some improvement in NHG debuggability and code by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19488
* bgpd: use a function to set the peer reset cause by @enkechen-panw in https://github.com/FRRouting/frr/pull/19617
* tests: Fix duplicate_nexthop test to connect more often by @donaldsharp in https://github.com/FRRouting/frr/pull/19616
* nhrpd: restore ability to configure non /32 IPv4 tunnel interfaces by @louberger in https://github.com/FRRouting/frr/pull/19553
* bgpd: Reset gr_select_defer_evaluated on GR config change by @Pdoijode in https://github.com/FRRouting/frr/pull/19606
* bgpd: Do not crash with only vni configed. by @donaldsharp in https://github.com/FRRouting/frr/pull/19619
* bgpd: Fix incorrect flag checks for SRv6 SID allocation by @cscarpitta in https://github.com/FRRouting/frr/pull/19623
* doc: Fix developer/northbound/architecture links by @matthewoliver in https://github.com/FRRouting/frr/pull/19621
* Handle backend daemon config validation failure by @choppsv1 in https://github.com/FRRouting/frr/pull/19587
* bgpd: Do not override a specified rd by @donaldsharp in https://github.com/FRRouting/frr/pull/19613
* bgpd:send EOR during GR only when fib install comeplete for wfi enabled by @vijayalaxmi-basavaraj in https://github.com/FRRouting/frr/pull/19522
* bgpd: Convert the bgp->peerhash to a connectionhash by @donaldsharp in https://github.com/FRRouting/frr/pull/19599
* some more test cleanups by @donaldsharp in https://github.com/FRRouting/frr/pull/19612
* zebra: Allow usage of full range of weights by @donaldsharp in https://github.com/FRRouting/frr/pull/19630
* bgpd: Free up leaked bpme on release by @donaldsharp in https://github.com/FRRouting/frr/pull/19629
* docs: bgpd: clarify `bgp bestpath as-path multipath-relax` option by @kaffarell in https://github.com/FRRouting/frr/pull/19641
* Revert "bgpd: Free up leaked bpme on release" by @ton31337 in https://github.com/FRRouting/frr/pull/19643
* lib: Free Temporary Memory for AF_FLOWSPEC Prefix by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19658
* bgpd: Make path_valid variable name more meaningfull by @donaldsharp in https://github.com/FRRouting/frr/pull/19646
* SRv6/MPLS Coexistence in L3VPN / formatting fixes by @pguibert6WIND in https://github.com/FRRouting/frr/pull/19639
* zebra: freebsd is sending a broadcast of 0.0.0.0 by @donaldsharp in https://github.com/FRRouting/frr/pull/19657
* Fix int long issues by @mjstapp in https://github.com/FRRouting/frr/pull/19648
* bgpd: Fix bgp peer clearing logic by @mjstapp in https://github.com/FRRouting/frr/pull/19644
* zebra : Fix compilation when lttng is enabled by @raja-rajasekar in https://github.com/FRRouting/frr/pull/19660
* tests: Allow a Collision notification to not fail the test by @donaldsharp in https://github.com/FRRouting/frr/pull/19662
* tests: ospf_topo2 allow dead interval to be a bit longer by @donaldsharp in https://github.com/FRRouting/frr/pull/19661
* ldpd: fix wrong label mapping procedure by @anlancs in https://github.com/FRRouting/frr/pull/19573
* tests: Ensure multicast_pim_sm_topo2 only stops the senders by @donaldsharp in https://github.com/FRRouting/frr/pull/19666
* doc: Fixup building freebsd14 doc by @donaldsharp in https://github.com/FRRouting/frr/pull/19664
* Clang 19 on bsd sa issues by @donaldsharp in https://github.com/FRRouting/frr/pull/19665
* bgpd: Fix labelpool not being freed on allocation issues by @donaldsharp in https://github.com/FRRouting/frr/pull/19626
* tests: Change default timers to be 15s by @ton31337 in https://github.com/FRRouting/frr/pull/19669
* Revert "bgpd: Enable Link-Local Next Hop capability for unnumbered peers implicitly by @ton31337 in https://github.com/FRRouting/frr/pull/19602
* tests: msdp_topo1 not properly detecting SA limit being hit by @donaldsharp in https://github.com/FRRouting/frr/pull/19670
* pimd: Allow FreeBSD pimd to have permission to do pim by @donaldsharp in https://github.com/FRRouting/frr/pull/19675
* zebra, pimd: FreeBSD fixes (metric, IP_RECVIF) by @eqvinox in https://github.com/FRRouting/frr/pull/19671
* tests: Ensure key exists for bgp_evpn_mh (backport #19697) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19698
* tests: fix memory leaks in `make check` for ASAN run (backport #19701) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19704
* ospfd: plug leaks in TI-LFA code (backport #19700) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19707
* zebra: Cleanup early route Q when removing routes. (backport #19338) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19724
* bgpd: ensure batch clearing flags are clear (backport #19696) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19716
* doc: Fix documentation regarding capability link-local (backport #19713) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19729
* zebra: fix neighbor table name length (backport #18872) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19737
* pim6d: don't SEGV on repeated MLD records (backport #19732) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19738
* tests: correct one assert for ldp test (backport #19572) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19758
* ospf6d: Fix summary deletion dropping redistributed routes (backport #19733) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19759
* lib,zebra: make nhg nexthop show output consistent (backport #19762) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19764
* pimd/pim6d: fix router-alert crash (backport #19757) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19766
* tests: Allow --with-timestamp-precision=X to actually work w/ make check (backport #19772) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19773
* Test speedups of long running tests (backport #19770) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19785
* bgpd: EVPN fix auto derive rd when user cfg removed (backport #19779) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19781
* zebra: EVPN fix alignment of access-vlan cli output (backport #19795) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19796
* zebra: Show prefix on failed lookup (backport #19789) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19802
* pim6d: drop mismatch report packets (backport #19198) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19801
* zebra: Fix SRv6 explicit SID allocation to use the provided locator (backport #19806) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19809
* bgpd: EVPN-MH fix ES-EVI memleak during shutdown (backport #19814) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19815
* zebra: workaround for a race condition caused by if_zebra_speed_update timer (backport #19794) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19824
* bgpd: Put local BGP ID when sending NNHN TLV for NH characteristic by @ton31337 in https://github.com/FRRouting/frr/pull/19835
* bgpd: Do not complain in the logs if we intentionally withdraw specific attrs by @ton31337 in https://github.com/FRRouting/frr/pull/19837
* zebra: fix yang data for mcast-group (backport #19845) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19852
* pbrd: fix memleak during pbr map deletion (backport #19863) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19872
* bgpd: EVPN fix memleak in adv type5 cli cmd (backport #19858) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19864
* zebra: update dataplane api version for 10.5 release (backport #19856) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19877
* Frr headers (backport #19351) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19876
* bgpd: Crash due to usage of freed up evpn_overlay attr (backport #19879) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19887
* vrrpd: IPv6 VRRP macvlan doesn't have IPv6 link-local address (backport #19861) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19881
* zebra: fix missing fpm messages (backport #19807) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19892
* bgpd: Notify all incoming/outgoing on peer group notify unconfig (backport #19891) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19897
* pimd: demote a warning to a debug to avoid spamming the logs (backport #19902) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19904
* bgpd: fix routemap evpn type-5 default route check (backport #19895) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19919
* bgpd: Check L3VNI status before adv evpn vrf routes (backport #19896) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19923
* bgpd: fix BGP_ATTR_ORIGINATOR_ID flag in outbound attribute cache (backport #19918) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19928
* bgpd: fix expanded extcomm list delete by @ton31337 in https://github.com/FRRouting/frr/pull/19941
* bgpd: Check MED flag correctly in encap_attr_export() (backport #19940) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19945
* bgpd: fix BGP_ATTR_LOCAL_PREF being set appropriately (backport #19927) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19932
* doc, docker: fix Ubuntu 24.04 snmp issues and enable 24.04 github CI (backport #19483) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19964
* lib: fix memleak in nexthop label copy (backport #19959) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19966
* debian, redhat: release updates, 10.4 10.5-dev housekeeping by @Jafaral in https://github.com/FRRouting/frr/pull/19972
* ospfd: Fix crash when entering `ospf authentication key XX` (backport #19975) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19977
* Bgp keepalives data race (backport #20001) by @mergify[bot] in https://github.com/FRRouting/frr/pull/20002

## New Contributors
* @hhubb22 made their first contribution in https://github.com/FRRouting/frr/pull/19023
* @nick-bouliane made their first contribution in https://github.com/FRRouting/frr/pull/19065
* @miteshkanjariya made their first contribution in https://github.com/FRRouting/frr/pull/18697
* @cocomundo made their first contribution in https://github.com/FRRouting/frr/pull/19209
* @zzzzrf made their first contribution in https://github.com/FRRouting/frr/pull/19266
* @kniteli made their first contribution in https://github.com/FRRouting/frr/pull/19263
* @oliverchang made their first contribution in https://github.com/FRRouting/frr/pull/19303
* @Canzovo made their first contribution in https://github.com/FRRouting/frr/pull/19296
* @tobiaspal made their first contribution in https://github.com/FRRouting/frr/pull/19586
* @rvaideesh made their first contribution in https://github.com/FRRouting/frr/pull/19552
* @matthewoliver made their first contribution in https://github.com/FRRouting/frr/pull/19621

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.5-dev...frr-10.5.0

## frr-10.1.4

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](TBD)

## What's Changed

* ospf6d: Disable and delete OSPFv3 areas that no longer have interfaces or configuration. (backport #18393)
* zebra: Do not flush an existing vni configuration trying to remove wrong vni (backport #18108)
* bgpd: fix `set evpn gateway-ip ipv[46]` route-map (#18465)
* bgpd: Fix holdtime not working properly when busy (#8490)
* bgpd: Retain the routes if we do a clear with N-bit set for Graceful-Restart (backport)
* zebra: Prevent vrf table 254 being used by non-default vrf (backport #18702)
* bgpd: fix show bgp vpn rd json (backport #18802)
* Prefix list leak bfdd ldpd (backport #18830) 
* redhat: Add Workaround for inet_ntop replacement which breaks rpms (backport #18864) 
* bgpd: fix to show exist/non-exist-map in 'show run' properly (backport #18828)
* bgpd: correct no form commands (backport #18911)
* bgpd: use AS4B format for BGP loc-rib messages. (backport #18936)
* redhat: make FRR RPM build to work on RedHat 10 (backport #18920)
* build: check for libunwind.h, not unwind.h (backport #18912)
* bgpd: Force adj-rib-out updates if MRAI is kicked in (backport #18959)
* nhrpd: fix crash when accessing invalid memory zone (backport #18994)
* lib: Fix `no on-match goto NUM` command (backport #19108)
* bgpd: Fix DEREF_OF_NULL.EX.COND in bgp_updgrp_packet (backport #19126)
* bgpd: Extract link bandwidth value from extcommunity before using for WCMP (backport #19165)
* bfdd: Set bfd.LocalDiag when transitioning to AdminDown (backport #18592)
* bgpd: Do not try to reuse freed route-maps (backport #19191)
* lib: fix routemap crash (backport #19127)
* bgpd: [GR] fixed selectionDeferralTimer to display select_defer_time val (#19285)
* zebra: Fix buffer overflows found by fuzzing. (backport #19303)
* lib: compute link-state zapi message size (backport #19290) 


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.1.3...frr-10.1.4

## frr-10.0.4

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:cfcc88edb6ae95ef87589c87d26f7f0343ffbb79b6a2dafa9357f807ab81bb06)

## What's Changed

* isisd: Show correct level information for `show isis interface detail json` (backport #17732)
* tools: Add missing rpki keyword to vrf in frr-reload (backport #17750) 
* bgpd: fix a bug in peer_allowas_in_set() (backport #17780) 
* isisd: Allow full `no` form for `domain-password` and `area-password` (backport #17725)
* bgpd: fix crash in displaying json orf prefix-list (backport #17807) 
* bgpd: use igpmetric in bgp_aigp_metric_total() (backport #17813) 
* bgpd: Fix for local interface MAC cache issue in 'bgp mac hash' table (backport #17888)
* Revert "bgpd: Handle Addpath capability using dynamic capabilities" (backport #17940)
* tools: Fix frr-reload for ebgp-multihop TTL reconfiguration. (backport #17946)
* bgpd: With suppress-fib-pending ensure withdrawal is sent (backport #17971) 
* bgpd: fix route-distinguisher in vrf leak json cmd (backport #17992)
* zebra: fix evpn svd hash avoid double free (backport #17991) 
* bgpd: Send non-transitive extended communities from/to OAD peers (backport #17896)
* bgpd: Do not start BGP session if BGP identifier is not set (#18017)
* lib: actually hash all 16 bytes of IPv6 addresses, not just 4 (backport #17901)
* lib: crash handlers must be allowed on threads (backport #18060)
* zebra: include resolving nexthops in nhg hash (backport #17935) 
* bgpd: fix incorrect JSON in bgp_show_table_rd (backport #18120) 
* bgp/bfd backports for stable/10.0  (#18153)
* bgpd: When removing the prefix list drop the pointer (backport #18160)
* lib: fix false context information for SRv6 route (backport #18023)  
* bgpd: fix vty output of evpn route-target AS4 (backport #18109)
* bgpd: release manual vpn label on instance deletion (backport #18121) 
* Revert "bgpd: release manual vpn label on instance deletion (backport #18121)" 
* isisd: Correct edge insertion into TED (backport #18294) 
* bgpd: Fixed crash upon bgp network import-check command (backport #18387)
* ospf6d: Disable and delete OSPFv3 areas that no longer have interfaces or configuration. (backport #18393)
* zebra: Do not flush an existing vni configuration trying to remove wrong vni (backport #18108)
* bgpd: fix `set evpn gateway-ip ipv[46]` route-map (#18466)
* bgpd: Fix holdtime not working properly when busy (#18491)
* bgpd: Retain the routes if we do a clear with N-bit set for Graceful-Restart (#18518)
* zebra: Prevent vrf table 254 being used by non-default vrf (backport #18702)
* bgpd: fix show bgp vpn rd json (backport #18802
* redhat: Add Workaround for inet_ntop replacement which breaks rpms (backport #18864)
* bgpd: fix to show exist/non-exist-map in 'show run' properly (backport #18828)
* bgpd: correct no form commands (backport #18911)
* redhat: make FRR RPM build to work on RedHat 10 (backport #18920)
* build: check for libunwind.h, not unwind.h (backport #18912)
* bgpd: Force adj-rib-out updates if MRAI is kicked in (backport #18959)
* nhrpd: fix crash when accessing invalid memory zone (backport #18994) 
* lib: Fix `no on-match goto NUM` command (backport #19108)
* bgpd: Fix DEREF_OF_NULL.EX.COND in bgp_updgrp_packet (backport #19126)
* bgpd: Extract link bandwidth value from extcommunity before using for WCMP (backport #19165)
* bfdd: Set bfd.LocalDiag when transitioning to AdminDown (backport #18592)
* bgpd: Do not try to reuse freed route-maps (backport #19191)
* lib: fix routemap crash (backport #19127)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.0.3...frr-10.0.4

## frr-10.4.1

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:97a281a1473cae1f762ceab87cbcc53a2e102053877421e8b4606422aae45442)

## What's Changed

* bgpd: initialize local variable (backport #19233)
* ospfd: Use after free cleanup of lsa (backport #19224)
* vtysh: copy config from file should actually apply (backport #19242)
* Revert PR #18358: BGP evpn testing and bug fixes related to non default EVPN backbone  (backport #19241)
* topotests: improve embedded RP test reliability (backport #19240)
* lib, zebra: mark singleton nexthops inactive/active on link state changes for wecmp (backport #18947)
* bgpd: LL next-hop capabilty fixes (backport #19261)
* eigrp: validate hello packets and tlvs better (backport #19251)
* bgpd : Fix compilation error in bgpd module: Update TP_ARGS for bgp (backport #19266)
* bgpd: Ensure addpath does not withdraw selected route in some situations (backport #19210)
* bgpd: [GR] fixed selectionDeferralTimer to display select_defer_time val  (#19282)
* bgpd: LL next-hop capabilty fixes (round 2) (backport #19277)
* lib: compute link-state zapi message size (backport #19290)
* zebra: Fix buffer overflows found by fuzzing. (backport #19303)

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.4.0...frr-10.4.1

## frr-10.3.2

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:ada2b4c4407f9dabcca0bbf35aa32344d21de2adc5606e6df022c45032d95203)

## What's Changed

* bgpd: correct no form commands (backport #18911)
* bgpd: fix to show exist/non-exist-map in 'show run' properly 
* redhat: make FRR RPM build to work on RedHat 10 (backport #18920)
* build: check for libunwind.h, not unwind.h (backport #18912)
* bgpd: use AS4B format for BGP loc-rib messages. (backport #18936) 
* bgpd: fix for the validity and the presence of prefixes in the BGP VPN table. (backport #17370)
* bgpd: Force adj-rib-out updates if MRAI is kicked in (backport #18959)
* github: Do not cache docker foobar (backport #18909)
* zebra: Provide SID value when sending SRv6 SID release notify message (backport #18971)
* bgpd: Fix crash when fetching statistics for bgp instance (backport #19003)
* tests: add new /run/netns tmpfs to each topotest router namespace (backport #19007) 
* nhrpd: fix crash when accessing invalid memory zone (backport #18994) 
* zebra: Initialize RB tree for router tables (backport #19049)
* zebra: fix null pointer dereference in zebra_evpn_sync_neigh_del (backport #19054)
* zebra: fix stale NHG in kernel (backport #18899)
* bgpd: Fix incorrect stripping of transitive extended communities (backport #19065)
* lib: Fix `no on-match goto NUM` command (backport #19108)
* bgpd: Fix extended community check for IP non-transitive type (backport #19097)
* bgpd: Fix DEREF_OF_NULL.EX.COND in bgp_updgrp_packet (backport #19126)
* lib: revert addition of vtysh_flush() call in vty_out() (backport #19109) 
* bgpd: Extract link bandwidth value from extcommunity before using for WCMP (backport #19165)
* Use ipv4 class E addresses (240.0.0.0/4) as connected routes by default (backport #18095)
* bfdd: Set bfd.LocalDiag when transitioning to AdminDown (backport #18592)
* zebra: clean up a json object leak (backport #19192)
* bgpd: Do not try to reuse freed route-maps (backport #19191) 
* lib: fix routemap crash (backport #19127) 
* bgpd: initialize local variable (backport #19233)
* ospfd: Use after free cleanup of lsa (backport #19224)
* vtysh: copy config from file should actually apply (backport #19242)
* bgpd : Fix compilation error in bgpd module: Update TP_ARGS for bgp (backport #19266)
* bgpd: Ensure addpath does not withdraw selected route in some situations (backport #19210)
* lib, zebra: mark singleton nexthops inactive/active on link state changes for wecmp (backport #18947) 
* eigrp: validate hello packets and tlvs better (backport #19251)
* bgpd: [GR] fixed selectionDeferralTimer to display select_defer_time val (#19283)
* zebra: Fix buffer overflows found by fuzzing. (backport #19303)
* lib: compute link-state zapi message size (backport #19290)

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.3.1...frr-10.3.2

## frr-10.2.4

Debian Packages - https://deb.frrouting.org/
RPM Packages - https://rpm.frrouting.org/
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:db750084f9ef4a2e4f7f9c4132cf7df25e86ba084ac1d8808a28f81c5698b48f)

## What's Changed

* bgpd: correct no form commands (backport #18911)
* build: check for libunwind.h, not unwind.h (backport #18912)
* redhat: make FRR RPM build to work on RedHat 10 (backport #18920)
* bgpd: use AS4B format for BGP loc-rib messages. (backport #18936)
* bgpd: Force adj-rib-out updates if MRAI is kicked in (backport #18959)
* zebra: Provide SID value when sending SRv6 SID release notify message (backport #18971)
* tests: add new /run/netns tmpfs to each topotest router namespace (backport #19007)
* nhrpd: fix crash when accessing invalid memory zone (backport #18994)
* lib: Fix `no on-match goto NUM` command (backport #19108
* bgpd: Fix DEREF_OF_NULL.EX.COND in bgp_updgrp_packet (backport #19126)
* bgpd: Extract link bandwidth value from extcommunity before using for WCMP (backport #19165)
* bfdd: Set bfd.LocalDiag when transitioning to AdminDown (backport #18592)
* bgpd: Do not try to reuse freed route-maps (backport #19191)
* lib: fix routemap crash (backport #19127)
* lib, zebra: mark singleton nexthops inactive/active on link state changes for wecmp (backport #18947)
* bgpd: [GR] fixed selectionDeferralTimer to display select_defer_time val (#19284)
* zebra: Fix buffer overflows found by fuzzing. (backport #19303)
* lib: compute link-state zapi message size (backport #19290)


**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.2.3...frr-10.2.4

## frr-10.4.0

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:be6cd68d0858602d24c8ba23a6ea2dfc40ccdc25173a6f267e9120f3aaddeef3)

## Release Overview

### New Features Highlight

- BGP BFD Strict-Mode
  - `neighbor PEER bfd strict [hold-time N]`
- BGP Link-Local Next Hop Capability ([draft-ietf-idr-linklocal-capability](https://datatracker.ietf.org/doc/html/draft-ietf-idr-linklocal-capability))
  - `neighbor PEER capability link-local`
- BGP Transparent mode
  - `neighbor PEER ip-transparent`
- BGP Next Hop Dependent Characteristics Attribute ([draft-ietf-idr-entropy-label](https://datatracker.ietf.org/doc/html/draft-ietf-idr-entropy-label))
  - `neighbor PEER send-nexthop-characteristics`
- IGMP and MLD group/source limits
  - `ip igmp max-groups`
  - `ip igmp max-sources`
  - `ipv6 mld max-groups`
  - `ipv6 mld max-sources`
- PIM dense and sparse-dense mode support ([RFC3973](https://datatracker.ietf.org/doc/html/rfc3973))
  - new interface mode: dense `ip pim dm`
  - new interface mode: sparse-dense `ip pim sm-dm`
- IGMPv2/MLDv1 immediate leave
- v4-via-v6 nexthop support for static routes
- Timeout for vtysh
  - `exec-timeout`
- Discover PREF64 in Router Advertisements ([RFC8781](https://datatracker.ietf.org/doc/html/rfc8781))
  - `ipv6 nd nat64`

## What's Changed
* bgpd: Do not start BGP session if BGP identifier is not set by @ton31337 in https://github.com/FRRouting/frr/pull/17959
* bgpd: fix add label support to EVPN AD routes by @pguibert6WIND in https://github.com/FRRouting/frr/pull/17985
* isisd: 'tiebreaker' command line funtionality is inconsistent with its implementation by @baozhen-H3C in https://github.com/FRRouting/frr/pull/16593
* bgpd: Send non-transitive extended communities from/to OAD peers by @ton31337 in https://github.com/FRRouting/frr/pull/17896
* Add bgpevpn route type-2 route map filter tests by @lsang6WIND in https://github.com/FRRouting/frr/pull/17918
* lib: Remove System routes from ip protocol route map choices by @donaldsharp in https://github.com/FRRouting/frr/pull/17953
* staticd: Add CLI to support steering of IPv4 traffic over SRv6 SID list by @cscarpitta in https://github.com/FRRouting/frr/pull/17988
* Fpm problems by @donaldsharp in https://github.com/FRRouting/frr/pull/17962
* bgpd: Fix up memory leak in processing eoiu marker by @donaldsharp in https://github.com/FRRouting/frr/pull/18000
* doc: fix sbfd.rst doc warnings by @forrestchu in https://github.com/FRRouting/frr/pull/18018
* Nexthop leak by @donaldsharp in https://github.com/FRRouting/frr/pull/18014
* lib: actually hash all 16 bytes of IPv6 addresses, not just 4 by @eqvinox in https://github.com/FRRouting/frr/pull/17901
* bgpd: add L2 attr community support as per RFC8214 by @pguibert6WIND in https://github.com/FRRouting/frr/pull/17987
* tests: Remove improper pymark by @donaldsharp in https://github.com/FRRouting/frr/pull/18025
* tools: Add some more support bundle commands by @donaldsharp in https://github.com/FRRouting/frr/pull/18029
* Coverity 2024 new hotness by @donaldsharp in https://github.com/FRRouting/frr/pull/17865
* pimd: fix memory leak and assign allocation type by @rzalamena in https://github.com/FRRouting/frr/pull/18038
* isisd: Do not leak a linked list in the circuit by @donaldsharp in https://github.com/FRRouting/frr/pull/18033
* pimd: Fix for FHR mroute taking longer to age out by @routingrocks in https://github.com/FRRouting/frr/pull/14105
* pimd: fix DR election race on startup by @rzalamena in https://github.com/FRRouting/frr/pull/18048
* bgpd: rfapi: fix mem leak when killed by @gpziemba in https://github.com/FRRouting/frr/pull/18045
* bgpd: Implement Link-Local Next Hop capability by @ton31337 in https://github.com/FRRouting/frr/pull/17871
* Fix journald logging via "log stdout" by @gromit1811 in https://github.com/FRRouting/frr/pull/17775
* babeld: Improve code clarity and maintainability by @y-bharath14 in https://github.com/FRRouting/frr/pull/18077
* bgpd: fix for the validity and the presence of prefixes in the BGP VPN table. by @louis-6wind in https://github.com/FRRouting/frr/pull/17370
* bgpd: Show internal data for BGP routes by @ton31337 in https://github.com/FRRouting/frr/pull/17870
* isisd: Remove unneeded modify functions by @donaldsharp in https://github.com/FRRouting/frr/pull/18034
* bgpd: fix bgp vrf instance creation from implicit by @chiragshah6 in https://github.com/FRRouting/frr/pull/18081
* lib: crash handlers must be allowed on threads by @eqvinox in https://github.com/FRRouting/frr/pull/18060
* Bmp bgp open router id and as val by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18037
* nhrpd: fix dont consider incomplete L2 entry by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18078
* bgpd: Request SRv6 locator after zebra connection by @cscarpitta in https://github.com/FRRouting/frr/pull/18069
* zebra: Allow fpm_listener to continue to try to read by @donaldsharp in https://github.com/FRRouting/frr/pull/18049
* lib (+bfd): improve late timer warnings by @eqvinox in https://github.com/FRRouting/frr/pull/18094
* bgpd: Do not check for capability length for Link-Local Next Hop capability by @ton31337 in https://github.com/FRRouting/frr/pull/18068
* Cid 1636504 by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18062
* Bfd fixups by @donaldsharp in https://github.com/FRRouting/frr/pull/18026
* tests: clear `-Wcalloc-transposed-args` warnings by @ariel-anieli in https://github.com/FRRouting/frr/pull/17649
* bfdd: 0 is a valid fd. by @donaldsharp in https://github.com/FRRouting/frr/pull/18125
* yang: Reorder the revision statements by @y-bharath14 in https://github.com/FRRouting/frr/pull/18118
* bgpd: fix incorrect JSON in bgp_show_table_rd by @louis-6wind in https://github.com/FRRouting/frr/pull/18120
* pimd,pim6d: implement GMP group / source limits by @rzalamena in https://github.com/FRRouting/frr/pull/18032
* ospfd: Replace LSDB callbacks with LSA Update/Delete hooks. by @aceelindem in https://github.com/FRRouting/frr/pull/18046
* bgpd: Fix crash in bgp_labelpool by @donaldsharp in https://github.com/FRRouting/frr/pull/18079
* lib: fix false context information for SRv6 route by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18023
* staticd: Fix SRv6 SID installation and deletion by @cscarpitta in https://github.com/FRRouting/frr/pull/18064
* Vrf tableid debugs by @donaldsharp in https://github.com/FRRouting/frr/pull/18142
* bgpd: Some fixes/improvements for Link-Local Next Hop capability by @ton31337 in https://github.com/FRRouting/frr/pull/18080
* bgpd: release manual vpn label on instance deletion by @louis-6wind in https://github.com/FRRouting/frr/pull/18121
* watchfrr: Allow -w option to be ignored by @donaldsharp in https://github.com/FRRouting/frr/pull/18127
* bgpd: factorize bgp_table_cleanup() by @louis-6wind in https://github.com/FRRouting/frr/pull/18122
* bgpd: When removing the prefix list drop the pointer by @donaldsharp in https://github.com/FRRouting/frr/pull/18160
* sharpd: add `crashme` commands by @eqvinox in https://github.com/FRRouting/frr/pull/18163
* isisd: Request SRv6 locator after zebra connection by @cscarpitta in https://github.com/FRRouting/frr/pull/18178
* bgpd: fix vty output of evpn route-target AS4 by @mjstapp in https://github.com/FRRouting/frr/pull/18109
* tests: Fix intermittent failures in `srv6_encap_src_addr` topotest by @cscarpitta in https://github.com/FRRouting/frr/pull/18187
* yang: Default value for a key leaf to be ignored by @y-bharath14 in https://github.com/FRRouting/frr/pull/18139
* tools: add logfmt option for frr-reload.py by @gtataranni in https://github.com/FRRouting/frr/pull/16796
* lib: nb: call child destroy CBs when YANG container is deleted by @choppsv1 in https://github.com/FRRouting/frr/pull/18082
* isisd, lib: add some codepoints usually shared with other vendors by @pguibert6WIND in https://github.com/FRRouting/frr/pull/17957
* Use ipv4 class E addresses (240.0.0.0/4) as connected routes by default by @davischw in https://github.com/FRRouting/frr/pull/18095
* doc: correct `ip rip split-horizon` command in the documentation by @Shbinging in https://github.com/FRRouting/frr/pull/18189
* staticd: Failed to register nexthop after networking restart by @Pdoijode in https://github.com/FRRouting/frr/pull/18164
* pimd,pim6d: support IGMPv2/MLDv1 immediate leave by @rzalamena in https://github.com/FRRouting/frr/pull/18111
* zebra: Do not flush an existing vni configuration trying to remove wrong vni by @ton31337 in https://github.com/FRRouting/frr/pull/18108
* pimd: filter neighbors by address by @rzalamena in https://github.com/FRRouting/frr/pull/17914
* tests: Remove warning about passive command by @donaldsharp in https://github.com/FRRouting/frr/pull/18197
* bgpd: Fix another crash in orf by @donaldsharp in https://github.com/FRRouting/frr/pull/18194
* pimd: Fix for data packet loss when FHR is LHR and RP by @routingrocks in https://github.com/FRRouting/frr/pull/14227
* pimd: During prefix-list update, behave as PIM_UPSTREAM_NOTJOINED sta… by @routingrocks in https://github.com/FRRouting/frr/pull/17666
* *: Remove unneeded IPV6_JOIN|LEAVE_GROUP by @donaldsharp in https://github.com/FRRouting/frr/pull/18213
* yang: Corrected Pyang errors or warnings by @y-bharath14 in https://github.com/FRRouting/frr/pull/18218
* doc: update mgmtd list of converted by @choppsv1 in https://github.com/FRRouting/frr/pull/18223
* tests: add docstrings to frontend mgmtd client by @choppsv1 in https://github.com/FRRouting/frr/pull/18224
* bgpd: remove dmed check not required in bestpath selection by @donaldsharp in https://github.com/FRRouting/frr/pull/18210
* Fix oper-state queries that involve choice/case nodes by @choppsv1 in https://github.com/FRRouting/frr/pull/18231
* zebra: Add operational retrieval of Multipath Number by @donaldsharp in https://github.com/FRRouting/frr/pull/18236
* pim: Fix autorp group joins by @nabahr in https://github.com/FRRouting/frr/pull/18225
* pim: Fix vrf binding of autorp and mroute socket by @nabahr in https://github.com/FRRouting/frr/pull/18226
* pimd: Fix PIM VRF support (send register/register stop in VRF) by @gromit1811 in https://github.com/FRRouting/frr/pull/18216
* Drop unused code by @dksharp5 in https://github.com/FRRouting/frr/pull/18243
* bgpd: fix default instance when leaving the hidden state. by @louis-6wind in https://github.com/FRRouting/frr/pull/18119
* ripd: fix no ip rip split-horizon poisoned-reverse command by @Shbinging in https://github.com/FRRouting/frr/pull/18256
* staticd: Fix crash because registering unknown vrf by @donaldsharp in https://github.com/FRRouting/frr/pull/18235
* staticd: Add support for SRv6 uA behavior by @cscarpitta in https://github.com/FRRouting/frr/pull/18198
* fabricd: add option to treat dummy interfaces as loopback interfaces by @kaffarell in https://github.com/FRRouting/frr/pull/18242
* support pre-built oper state in libyang tree by @choppsv1 in https://github.com/FRRouting/frr/pull/18237
* tests: Fixed input dict at create_router_bgp by @y-bharath14 in https://github.com/FRRouting/frr/pull/18261
* ospf6d: Fix use after free of router in OSPFv3 ABR route calculation. by @aceelindem in https://github.com/FRRouting/frr/pull/18254
* staticd: Do not log uninitialized `nexthop` variable by @cscarpitta in https://github.com/FRRouting/frr/pull/18271
* lib: Prevent crash in getting label chunk by @donaldsharp in https://github.com/FRRouting/frr/pull/18270
* mgmtd: Prevent use after free by @donaldsharp in https://github.com/FRRouting/frr/pull/18264
* Bgp ecommlist count by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18159
* staticd: Add `no` form for `static-sids` command by @cscarpitta in https://github.com/FRRouting/frr/pull/18263
* pimd: fix null memory access on IGMP source limit by @rzalamena in https://github.com/FRRouting/frr/pull/18285
* tools: Fix `frr-reload.py` error related to `static-sids` by @cscarpitta in https://github.com/FRRouting/frr/pull/18290
* staticd: Fix `no srv6` command by @cscarpitta in https://github.com/FRRouting/frr/pull/18289
* isisd: Correct edge insertion into TED by @odd22 in https://github.com/FRRouting/frr/pull/18294
* zebra: reduce memory usage by streams when redistributing routes by @fdumontet6WIND in https://github.com/FRRouting/frr/pull/18030
* bgpd: Do not advertise aggregate routes to contributing ASes by @ton31337 in https://github.com/FRRouting/frr/pull/17961
* Allow retrieval of v4/v6 forwarding state via NB by @dksharp5 in https://github.com/FRRouting/frr/pull/18253
* Vpn prefix aggregate export and accept by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18301
* bfdd: Add "log-session-changes" command to BFD configuration and operational state via YANG Northbound API.  by @aceelindem in https://github.com/FRRouting/frr/pull/18306
* yang: Imported modules are not in use by @y-bharath14 in https://github.com/FRRouting/frr/pull/18293
* lib: Correct handling of /frr-vrf:lib/vrf/state/active by @donaldsharp in https://github.com/FRRouting/frr/pull/18268
* configure.ac: fix sed failure on FreeBSD by @rzalamena in https://github.com/FRRouting/frr/pull/18310
* More connection cleanup by @donaldsharp in https://github.com/FRRouting/frr/pull/18195
* doc: don't override automake builtin targets by @qlyoung in https://github.com/FRRouting/frr/pull/18319
* lib: Document --command-log-always in help by @donaldsharp in https://github.com/FRRouting/frr/pull/18313
* zebra: Bring up 514 BGP neighbor sessions by @soumyar-roy in https://github.com/FRRouting/frr/pull/18214
* pimd: Fix PIM6 MLD VRF support (use recvmsg() pktinfo) by @gromit1811 in https://github.com/FRRouting/frr/pull/18315
* bgpd: Fix dead code in bgp_route.c #1637664 by @donaldsharp in https://github.com/FRRouting/frr/pull/18327
* Revert "bgpd: Make keepalive pthread be connection based." by @donaldsharp in https://github.com/FRRouting/frr/pull/18337
* Documentation typesafe by @donaldsharp in https://github.com/FRRouting/frr/pull/18338
* tests: bgp_evpn_route_map_match fix invalid escape sequence by @donaldsharp in https://github.com/FRRouting/frr/pull/18344
* lib: use memcpy in bf_copy by @karthikeyav in https://github.com/FRRouting/frr/pull/18335
* Topotest startup order by @donaldsharp in https://github.com/FRRouting/frr/pull/18348
* ospfd: minor change for style by @anlancs in https://github.com/FRRouting/frr/pull/18342
* Clean up some code and bad assumptions in zebra by @donaldsharp in https://github.com/FRRouting/frr/pull/18346
* tests: Fixed NameError at bmpserver.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18362
* zebra: fix table heap-after-free crash by @louis-6wind in https://github.com/FRRouting/frr/pull/16614
* zebra: Fix neigh delete causing heap-use-after-free error by @routingrocks in https://github.com/FRRouting/frr/pull/18336
* Revert "bgpd: upon if event, evaluate bnc with matching nexthop" by @donaldsharp in https://github.com/FRRouting/frr/pull/18368
* staticd: Install known nexthops upon connection with zebra by @donaldsharp in https://github.com/FRRouting/frr/pull/18367
* Add Testing for community and Extended community match limit zero by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18366
* bgpd: Show bgp <afi> <safi> shouldn't display peers in groups by @donaldsharp in https://github.com/FRRouting/frr/pull/18380
* yang: Fixed pyang errors at frr-bgp-common.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18388
* isisd: fix bit flag collision in options field by @kaffarell in https://github.com/FRRouting/frr/pull/18377
* Fix bug with oper-state queries including list node by @choppsv1 in https://github.com/FRRouting/frr/pull/18383
* zebra: ensure proper return for failure for Sid allocation by @raja-rajasekar in https://github.com/FRRouting/frr/pull/18360
* ospf6d: Disable and delete OSPFv3 areas that no longer have interfaces or configuration. by @aceelindem in https://github.com/FRRouting/frr/pull/18393
* bgpd: Remove unnecessary stream_new/stream_copies in bgp_open_make by @donaldsharp in https://github.com/FRRouting/frr/pull/18395
* zebra: add ability to specify output file with fpm_listener by @donaldsharp in https://github.com/FRRouting/frr/pull/18394
* bgpd: Fixed crash upon bgp network import-check command by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/18387
* lib: suppress libyang logs during expected error result by @choppsv1 in https://github.com/FRRouting/frr/pull/18384
* 2 unit-test fixes by @choppsv1 in https://github.com/FRRouting/frr/pull/18399
* bgpd: Do not keep stale paths in Adj-RIB-Out if not addpath aware by @ton31337 in https://github.com/FRRouting/frr/pull/18275
* bgpd, zebra, tests: disable rtadv when bgp instance unconfiguration. by @dmytroshytyi-6WIND in https://github.com/FRRouting/frr/pull/18364
* fix(vrrp): display vrrp version by default by @echkenluo in https://github.com/FRRouting/frr/pull/18407
* bgpd: Print the real reason why the peer is not accepted (incoming) by @ton31337 in https://github.com/FRRouting/frr/pull/18410
* tests: Corrected input dict at pim.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18414
* More yang state by @donaldsharp in https://github.com/FRRouting/frr/pull/18349
* babled: reset wired/wireless internal only when wired/wireless status changed by @Shbinging in https://github.com/FRRouting/frr/pull/18413
* doc: Modify typesafe documentation by @donaldsharp in https://github.com/FRRouting/frr/pull/18419
* ripngd: Access and Prefix lists are being leaked on shutdown by @donaldsharp in https://github.com/FRRouting/frr/pull/18418
* zebra: Fix reinstalling nexthops in NHGs upon interface flaps by @raja-rajasekar in https://github.com/FRRouting/frr/pull/18374
* RedHat: Fixing for PR17793 - Allow RPM build without docs and/or rpki by @mwinter-osr in https://github.com/FRRouting/frr/pull/18426
* lib: Create VRF if needed by @nabahr in https://github.com/FRRouting/frr/pull/18430
* bgpd: fix "delete in progress" flag on default instance by @lsang6WIND in https://github.com/FRRouting/frr/pull/18412
* Fix topotest to wait for zebra connection by @donaldsharp in https://github.com/FRRouting/frr/pull/18432
* bgpd: Fix leaked memory when showing some bgp routes by @donaldsharp in https://github.com/FRRouting/frr/pull/18435
* Fpm listener reject by @donaldsharp in https://github.com/FRRouting/frr/pull/18431
* topotests: Add EVPN RT5 multipath flap test by @chdxD1 in https://github.com/FRRouting/frr/pull/18325
* Typesafe zclient by @donaldsharp in https://github.com/FRRouting/frr/pull/18409
* pimd: Skip RPF check for SA message from mesh group peer by @usrivastava-nvidia in https://github.com/FRRouting/frr/pull/18330
* tests: Catch specific exceptions by @y-bharath14 in https://github.com/FRRouting/frr/pull/18277
* lib: fix static analysis error by @dmytroshytyi-6WIND in https://github.com/FRRouting/frr/pull/17986
* zebra: zebra crash for zapi stream by @soumyar-roy in https://github.com/FRRouting/frr/pull/18359
* yang: Code inline with RFC 8407 rules by @y-bharath14 in https://github.com/FRRouting/frr/pull/18442
* tests: Change up start order of bmp tests by @donaldsharp in https://github.com/FRRouting/frr/pull/18452
* tests: add bfd_static_vrf by @louis-6wind in https://github.com/FRRouting/frr/pull/18446
* tests: Corrected typo at path_attributes.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18339
* bgpd: fix `set evpn gateway-ip ipv[46]` route-map by @Tuetuopay in https://github.com/FRRouting/frr/pull/18378
* tests: add another directory to search path for pylint by @choppsv1 in https://github.com/FRRouting/frr/pull/18475
* tests: high_ecmp creates 2 update groups by @donaldsharp in https://github.com/FRRouting/frr/pull/18469
* staticd: Fix a crash that occurs when modifying an SRv6 SID by @cscarpitta in https://github.com/FRRouting/frr/pull/18467
* babeld: Missing Validation for AE=0 and Plen!=0 by @zmw12306 in https://github.com/FRRouting/frr/pull/18473
* Bgp clear batch by @donaldsharp in https://github.com/FRRouting/frr/pull/18447
* bgpd: fix handling of configured route-targets for l2vni, l3vni by @mjstapp in https://github.com/FRRouting/frr/pull/18484
* bgpd: Fix holdtime not working properly when busy by @donaldsharp in https://github.com/FRRouting/frr/pull/18483
* babeld: add check incorrect AE value for NH TLV. by @zmw12306 in https://github.com/FRRouting/frr/pull/18471
* isisd:IS-IS hello packets not sent with configured hello timer by @Z-Yivon in https://github.com/FRRouting/frr/pull/18311
* isisd: Fix the issue where redistributed routes do not change when th… by @huchaogithup in https://github.com/FRRouting/frr/pull/18369
* babeld: Hop Count must not be 0. by @zmw12306 in https://github.com/FRRouting/frr/pull/18474
* lib: Return duplicate prefix-list entry test by @ton31337 in https://github.com/FRRouting/frr/pull/18494
* bgpd: fix SA warning in bgp clearing code by @mjstapp in https://github.com/FRRouting/frr/pull/18496
* tests: Handling potential errors gracefully by @y-bharath14 in https://github.com/FRRouting/frr/pull/18476
* babeld: fix hello packets not sent with configured hello timer by @Shbinging in https://github.com/FRRouting/frr/pull/18448
* Eigrp typesafe by @donaldsharp in https://github.com/FRRouting/frr/pull/18482
* ospf6d: Fix LSA memory leaks related to graceful restart by @gromit1811 in https://github.com/FRRouting/frr/pull/18503
* tests: Add ripng aggregate address testing by @donaldsharp in https://github.com/FRRouting/frr/pull/18506
* yang: Fixed pyang errors at frr-isisd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18500
* bgpd: Set the label for MP_UNREACH_NLRI 0x800000 instead of 0x000000 by @ton31337 in https://github.com/FRRouting/frr/pull/18502
* tests: Modify simple_snmp_test to use frr.conf by @donaldsharp in https://github.com/FRRouting/frr/pull/18508
* bgpd: Retain the routes if we do a clear with N-bit set for Graceful-Restart by @ton31337 in https://github.com/FRRouting/frr/pull/18498
* lib: `show route-map` should not print (null) by @donaldsharp in https://github.com/FRRouting/frr/pull/18515
* tests: Fix potential issues at send_bsr_packet.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18520
* tests: Irrelevant code in lutil.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18532
* tools: Add option to frr-reload to specify alternate logfile by @mwinter-osr in https://github.com/FRRouting/frr/pull/15471
* Memory leaks all over by @donaldsharp in https://github.com/FRRouting/frr/pull/18544
* Bgp packet reads conversion to a FIFO by @donaldsharp in https://github.com/FRRouting/frr/pull/18450
* babeld: Add next hop initialization by @zmw12306 in https://github.com/FRRouting/frr/pull/18470
* yang: Limit eigrp to just 1 instance per vrf by @donaldsharp in https://github.com/FRRouting/frr/pull/18524
* yang: Corrected pyang errors in frr-zebra.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18543
* bgpd: optimize attrhash_cmp calls by @louis-6wind in https://github.com/FRRouting/frr/pull/18097
* lib: Return duplicate ipv6 prefix-list entry test by @ton31337 in https://github.com/FRRouting/frr/pull/18561
* eigrpd: Fix possible use after free in nbr deletion by @donaldsharp in https://github.com/FRRouting/frr/pull/18525
* bgpd: Skip EVPN MAC processing for non-EVPN peers by @routingrocks in https://github.com/FRRouting/frr/pull/18564
* tests: Resource leaks in test_all_protocol_startup by @y-bharath14 in https://github.com/FRRouting/frr/pull/18553
* Add BGP redistribution in SRv6 BGP by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18396
* bgpd: rfapi: track outstanding rib and import timers, free mem at exit by @gpziemba in https://github.com/FRRouting/frr/pull/18546
* tests: Fix typo when configuring delayopen timer by @ton31337 in https://github.com/FRRouting/frr/pull/18572
* pimd: Initialize gm proxy to false by @nabahr in https://github.com/FRRouting/frr/pull/18567
* bgpd: Treat the peer as not active due to BFD down only if established by @ton31337 in https://github.com/FRRouting/frr/pull/18562
* bgpd: flowspec: remove sizelimit check applied to the wrong length field (issue 18557) by @spoignant-proton in https://github.com/FRRouting/frr/pull/18558
* staticd: Avoid requesting SRv6 sid from zebra when loc and sid block dont match by @raja-rajasekar in https://github.com/FRRouting/frr/pull/18580
* babeld: Hop Count must not be 0. by @zmw12306 in https://github.com/FRRouting/frr/pull/18547
* babeld: Request forwarding does not prioritize feasible routes by @zmw12306 in https://github.com/FRRouting/frr/pull/18581
* babeld: Fix starvation handling on route loss per RFC 8966 §3.8.2.1 by @zmw12306 in https://github.com/FRRouting/frr/pull/18582
* babeld: Add a check to prevent all-ones case by @zmw12306 in https://github.com/FRRouting/frr/pull/18584
* babel: fix incorrect check in known_ae() by @zmw12306 in https://github.com/FRRouting/frr/pull/18585
* doc: add a diagram for config datastore cleanup on file reads by @choppsv1 in https://github.com/FRRouting/frr/pull/18602
* pimd: Fix memory leak on shutdown by @donaldsharp in https://github.com/FRRouting/frr/pull/18526
* nhrpd: Add Hop Count Validation Before Forwarding in nhrp_peer_recv() by @zmw12306 in https://github.com/FRRouting/frr/pull/18598
* babeld: check valid babel port by @zmw12306 in https://github.com/FRRouting/frr/pull/18583
* bgpd: On shutdown free up memory leak found by topotest by @donaldsharp in https://github.com/FRRouting/frr/pull/18614
* *: expose and fix variable shadowing warnings by @mjstapp in https://github.com/FRRouting/frr/pull/17915
* yang: Pyang errors in frr-bfdd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18604
* mgmtd: remove bogus "hedge" code which corrupted active candidate DS by @choppsv1 in https://github.com/FRRouting/frr/pull/18601
* zebra: Fix shadow warning in irdp_packet.c by @donaldsharp in https://github.com/FRRouting/frr/pull/18627
* bgpd: On shutdown free up table for static routes by @donaldsharp in https://github.com/FRRouting/frr/pull/18625
* bgpd: Paths not deleted received from shutdown peer by @soumyar-roy in https://github.com/FRRouting/frr/pull/18594
* bgpd: remove useless calls to afi2family by @louis-6wind in https://github.com/FRRouting/frr/pull/18624
* bfdd: Fix demultiplexing to rely solely on Your Discriminator  by @zmw12306 in https://github.com/FRRouting/frr/pull/18586
* babeld: fix incorrect type assignment in parse_request_subtlv by @zmw12306 in https://github.com/FRRouting/frr/pull/18548
* babeld: Add input validation for update TLV. by @zmw12306 in https://github.com/FRRouting/frr/pull/18472
* bgpd: add usid behavior for bgp srv6 instructions by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18611
* bgpd: fix add prefix sent in 'show bgp neighbor' by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18376
* tools: Add pathspace option to generate_support_bundle by @mwinter-osr in https://github.com/FRRouting/frr/pull/18635
* tests: Fix potential issues in mcast-tester.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18633
* babeld: Add MBZ and Reserved field checking by @zmw12306 in https://github.com/FRRouting/frr/pull/16735
* isisd: fix asla memory leak by @louis-6wind in https://github.com/FRRouting/frr/pull/18642
* lib, staticd, isisd: add B6.ENCAPS codepoint extensions by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18597
* zebra: modify fpm_listener to display data about nhgs by @donaldsharp in https://github.com/FRRouting/frr/pull/18640
* tools: fix reload script for SRv6 locators and formats by @raja-rajasekar in https://github.com/FRRouting/frr/pull/18628
* tests: Shadowing the built-in function by @y-bharath14 in https://github.com/FRRouting/frr/pull/18574
* zebra: fix pbr_iptable memory leak by @louis-6wind in https://github.com/FRRouting/frr/pull/18645
* Rpki testing and bug fix by @donaldsharp in https://github.com/FRRouting/frr/pull/18649
* pim6d: fix missing 'use-source' interface command by @ak503 in https://github.com/FRRouting/frr/pull/18578
* zebra: Add ability to dump routes received from fpm_listener by @donaldsharp in https://github.com/FRRouting/frr/pull/18641
* Add v4-via-v6 nexthop support to staticd by @chdxD1 in https://github.com/FRRouting/frr/pull/18654
* lib,bgpd: clean up clang warnings by @mjstapp in https://github.com/FRRouting/frr/pull/18655
* bgpd: fix pbr memory leaks by @louis-6wind in https://github.com/FRRouting/frr/pull/18653
* fix yang commands that don't have yang attr by @lsang6WIND in https://github.com/FRRouting/frr/pull/18610
* lib: nb: add list_entry_done() callback to free resources by @choppsv1 in https://github.com/FRRouting/frr/pull/18540
* bfdd: Set bfd.LocalDiag when transitioning to AdminDown by @zmw12306 in https://github.com/FRRouting/frr/pull/18592
* tests: Fix northbound endian use in a unit-test by @mjstapp in https://github.com/FRRouting/frr/pull/18662
* isisd: fix srv6_sid memory leak by @louis-6wind in https://github.com/FRRouting/frr/pull/18667
* zebra: change fpm_read to batch the messages by @krishna-samy in https://github.com/FRRouting/frr/pull/18579
* zebra: show command to display metaq info by @krishna-samy in https://github.com/FRRouting/frr/pull/18497
* yang: Corrected pyang errors in frr-pathd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18665
* bgpd: fix misused rfapi conditional by @eqvinox in https://github.com/FRRouting/frr/pull/18669
* pimd: Only create and bind the autorp socket when really needed by @nabahr in https://github.com/FRRouting/frr/pull/18538
* tests: Resource leak in common_config.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18658
* lib,pimd,bgpd,bfdd: Fix clang 18 warnings by @mjstapp in https://github.com/FRRouting/frr/pull/18675
* zebra: Save event pointer for rib sweeping by @donaldsharp in https://github.com/FRRouting/frr/pull/18692
* bgpd: ensure that bgp_generate_updgrp_packets shares nicely by @donaldsharp in https://github.com/FRRouting/frr/pull/18689
* Implement RFC8781 (NAT64 prefix in RA's) by @donaldsharp in https://github.com/FRRouting/frr/pull/18626
* zebra: implement RFC8781 (NAT64 prefix in RAs) by @eqvinox in https://github.com/FRRouting/frr/pull/11224
* Update EVPN prefix routes properly instead of withdraw/install by @chdxD1 in https://github.com/FRRouting/frr/pull/18158
* bgpd: fix vty's version of show advertised-routes by @askorichenko in https://github.com/FRRouting/frr/pull/18695
* Improve notification selectors (sort, eliminate dups) by @choppsv1 in https://github.com/FRRouting/frr/pull/18683
* tests: Shadowing the built-in function by @y-bharath14 in https://github.com/FRRouting/frr/pull/18698
* bgpd: Fix deref after free in bgp_vrf_unlink by @petrvaganoff in https://github.com/FRRouting/frr/pull/18694
* doc: line vty was not documented by @donaldsharp in https://github.com/FRRouting/frr/pull/18703
* bgpd: Clean extended communities for VRF routes imported from EVPN by @leonshaw in https://github.com/FRRouting/frr/pull/18656
* zebra: Add CLI to display SRv6 SIDs allocated by @cscarpitta in https://github.com/FRRouting/frr/pull/16836
* zebra: add vtep_ip to rmac nh_list in all cases by @chdxD1 in https://github.com/FRRouting/frr/pull/18677
* doc: state correct default behaviour of VTYSH_PAGER env if unset (vtysh manpage) by @valentinbinotto in https://github.com/FRRouting/frr/pull/18691
* pimd: Fix for crash during networking restart by @usrivastava-nvidia in https://github.com/FRRouting/frr/pull/18672
* yang: Fix pyang errors in frr-interface.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18716
* Fix Pim ssmpingd by @donaldsharp in https://github.com/FRRouting/frr/pull/18652
* change to 18652 to test by @choppsv1 in https://github.com/FRRouting/frr/pull/18713
* topotests: clarify bgp evpn rt5 by @louis-6wind in https://github.com/FRRouting/frr/pull/18708
* zebra: Display nhg's afi as `No Afi` by @donaldsharp in https://github.com/FRRouting/frr/pull/18709
* *: enable the missing-noreturn compiler warning by @mjstapp in https://github.com/FRRouting/frr/pull/18720
* *: Fix MULTIPATH_NUM check in nhg encode by @karthikeyav in https://github.com/FRRouting/frr/pull/18690
* zebra: Cancel new client accept events after zsock is closed by @Pdoijode in https://github.com/FRRouting/frr/pull/18704
* tests: Proper handling of resource allocation by @y-bharath14 in https://github.com/FRRouting/frr/pull/18730
* *: Allow returns to work with --enable-undefined-behavior by @donaldsharp in https://github.com/FRRouting/frr/pull/18731
* zebra: use nexthop instead of route vrf_id for EVPN by @chdxD1 in https://github.com/FRRouting/frr/pull/18309
* bgpd: fix bmp heap use after free on non connected session by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18700
* ldpd: Option for disabled LDP hello message during TCP by @AndriiFullroot in https://github.com/FRRouting/frr/pull/18417
* Add sharp support for seg6local routes with uSID flavor by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18605
* doc: add commit message guidelines to the dev guide by @Jafaral in https://github.com/FRRouting/frr/pull/18657
* tests: Unidiomatic-typecheck in bgp.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18738
* *: Remove deprecated EVENT_OFF macro by @mjstapp in https://github.com/FRRouting/frr/pull/18739
* Isis run level issue by @donaldsharp in https://github.com/FRRouting/frr/pull/18734
* staticd: Add support for other SRv6 Headend Behaviors by @cscarpitta in https://github.com/FRRouting/frr/pull/18623
* zebra: Fixes allowing SRv6 func-bits length 0 by @raja-rajasekar in https://github.com/FRRouting/frr/pull/18737
* add total path count for bgp net in json output by @soumyar-roy in https://github.com/FRRouting/frr/pull/18740
* show ipv6 route [json] displays seg6local flavors by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18563
* ospf6d: Remove dead code by @donaldsharp in https://github.com/FRRouting/frr/pull/18752
* yang: Fix pyang errors in frr-ospfd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18756
* Remove dead code found by @donaldsharp in https://github.com/FRRouting/frr/pull/18757
* yang: Correct unidiomatic-typecheck in pim.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18764
* zebra: show nexthops count in nexthop-group command by @krishna-samy in https://github.com/FRRouting/frr/pull/18762
* Move where nhe_installed_id is set in zebra by @donaldsharp in https://github.com/FRRouting/frr/pull/18749
* staticd: Fix an issue where SRv6 SIDs may not be allocated on heavily loaded systems by @cscarpitta in https://github.com/FRRouting/frr/pull/18317
* Allow using reserved ranges in RIP by @ton31337 in https://github.com/FRRouting/frr/pull/18768
* Remove unused functions as well as cleanup a header file by @donaldsharp in https://github.com/FRRouting/frr/pull/18766
* build: fail on docstring problems by @eqvinox in https://github.com/FRRouting/frr/pull/18765
* Fix spelling error in bgp as well as clean up bgp documentation by @donaldsharp in https://github.com/FRRouting/frr/pull/18770
* tests: Unreachable code in ospf.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18767
* docker: Build with 256 way ecmp by @donaldsharp in https://github.com/FRRouting/frr/pull/18779
* eigrpd: Clean up comment to reflect reality by @donaldsharp in https://github.com/FRRouting/frr/pull/18780
* zebra: Allow `show ip route table X A.B.C.D/M` to work by @donaldsharp in https://github.com/FRRouting/frr/pull/18776
* bgpd: restart R-bit startup timer on no shutdown by @ton31337 in https://github.com/FRRouting/frr/pull/18773
* Add initial state dump on frontend datastore notify subscribe by @choppsv1 in https://github.com/FRRouting/frr/pull/18778
* Gather vtysh return codes up to report to operator by @donaldsharp in https://github.com/FRRouting/frr/pull/18783
* BGP should stay in Idle if BFD profile is in admin shutdown state by @ton31337 in https://github.com/FRRouting/frr/pull/18763
* bfdd: Adding my discriminator id in show bfd peers counters json by @sougata-github-nvidia in https://github.com/FRRouting/frr/pull/18772
* mgmtd: need to set default notify_format for protobuf message too by @choppsv1 in https://github.com/FRRouting/frr/pull/18788
* zebra: Allow nhg's to be reused when multiple interfaces are going amuck by @donaldsharp in https://github.com/FRRouting/frr/pull/18723
* Replace use of `__` as identifier prefix by @choppsv1 in https://github.com/FRRouting/frr/pull/18790
* lib/clippy: pointer offsets are signed by @eqvinox in https://github.com/FRRouting/frr/pull/18792
* zebra: Prevent vrf table 254 being used by non-default vrf by @donaldsharp in https://github.com/FRRouting/frr/pull/18702
* *: some gcc warnings clean up by @rzalamena in https://github.com/FRRouting/frr/pull/18794
* bgpd: Remove linklist.h inclusion in bgp_mpath.c by @donaldsharp in https://github.com/FRRouting/frr/pull/18800
* bgpd: fix second router-id of loc-rib peer-up message set to 0.0.0.0 by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18799
* bgpd: Not advertised to any peer in peer-group by @soumyar-roy in https://github.com/FRRouting/frr/pull/18587
* bgpd: Add support for BGP to use SRv6 SID in an explicit way by @GaladrielZhao in https://github.com/FRRouting/frr/pull/18519
* bgpd: fix show bgp vpn rd json by @louis-6wind in https://github.com/FRRouting/frr/pull/18802
* bgpd: Fix flag issue in delete_vrf_tovpn_sid_per_vrf by @GaladrielZhao in https://github.com/FRRouting/frr/pull/18808
* ripd, ripngd: Timer values by @ton31337 in https://github.com/FRRouting/frr/pull/18805
* zebra: guard against use of zapi client data during close by @mjstapp in https://github.com/FRRouting/frr/pull/18721
* docker: install correct python protobuf in ubuntu docker images by @choppsv1 in https://github.com/FRRouting/frr/pull/18816
* tests: Fix unreachable code in pim.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18817
* tests: bgp_evpn_rt5 add route-reflector by @louis-6wind in https://github.com/FRRouting/frr/pull/18733
* bgpd: Rename bgp_path_info_delete to bgp_path_info_mark_for_delete by @donaldsharp in https://github.com/FRRouting/frr/pull/18818
* isid, lib: Fix gcc 15 warnings by @mjstapp in https://github.com/FRRouting/frr/pull/18820
* Fix bestpath reason being incorrectly set in some cases by @donaldsharp in https://github.com/FRRouting/frr/pull/18819
* tests: Remove `version` (BGP version) from JSON by @ton31337 in https://github.com/FRRouting/frr/pull/18831
* ci: harden wget from github servers by @vjardin in https://github.com/FRRouting/frr/pull/18833
* doc: topotest add missing media type MIB by @vjardin in https://github.com/FRRouting/frr/pull/18832
* Ipforwarding modify by @donaldsharp in https://github.com/FRRouting/frr/pull/18316
* Prefix list leak bfdd ldpd by @donaldsharp in https://github.com/FRRouting/frr/pull/18830
* Bgp encaps reduced by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18803
* End psp flavor by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18647
* Fix up from a bunch of ubsan issues found. by @donaldsharp in https://github.com/FRRouting/frr/pull/16074
* Add PIC support in the srv6 VPN scenario. by @zice312963205 in https://github.com/FRRouting/frr/pull/16879
* bgpd: Implement BGP Next Hop Dependent Characteristics Attribute (NNHN only) by @ton31337 in https://github.com/FRRouting/frr/pull/18729
* bgpd: fix view deletion and main socket deletion by @rzalamena in https://github.com/FRRouting/frr/pull/18758
* SRv6: Allow configuring node-len 0 by @raja-rajasekar in https://github.com/FRRouting/frr/pull/18774
* bgpd: fix to show exist/non-exist-map in 'show run' properly by @krishna-samy in https://github.com/FRRouting/frr/pull/18828
* zebra: finish moving `ip[v6] forwarding` to NB/mgmtd by @choppsv1 in https://github.com/FRRouting/frr/pull/18845
* mgmtd top level root query by @choppsv1 in https://github.com/FRRouting/frr/pull/18835
* Clang-19 cleanup and removal of scheduled functionality by @donaldsharp in https://github.com/FRRouting/frr/pull/18821
* pimd: add support for group range prefix-list filter for v6 by @rzalamena in https://github.com/FRRouting/frr/pull/18260
* pimd,pim6d: require router alert configuration by @rzalamena in https://github.com/FRRouting/frr/pull/18202
* zebra: V6 RA not sent anymore after interface up-down-up by @soumyar-roy in https://github.com/FRRouting/frr/pull/18451
* redhat: Add Workaround for inet_ntop replacement which breaks rpms by @mwinter-osr in https://github.com/FRRouting/frr/pull/18864
* staticd, bgp: fix srv6 encap-value displayed with _ instead of . by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18858
* bgpd: fix PEER_FLAG_CONFIG_DAMPENING to be ULL by @vjardin in https://github.com/FRRouting/frr/pull/18869
* Revert 16879 by @ton31337 in https://github.com/FRRouting/frr/pull/18856
* build: the great war against `config.h`, issue 0 of ∞ by @eqvinox in https://github.com/FRRouting/frr/pull/18860
* yang: Fix pyang errors in frr-staticd.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18857
* Keep the original NHE associated with a re around by @donaldsharp in https://github.com/FRRouting/frr/pull/18751
* build: the war against `config.h` continues, 1 of ∞ by @eqvinox in https://github.com/FRRouting/frr/pull/18874
* bgpd: fix import all adj-rib-in and loc-rib after bmp connects by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18843
* lib: fix mis-done endian check by @eqvinox in https://github.com/FRRouting/frr/pull/18875
* Eliminate protobuf from mgmtd backend (daemon) messaging by @choppsv1 in https://github.com/FRRouting/frr/pull/18878
* *: SPDX license spring cleaning by @eqvinox in https://github.com/FRRouting/frr/pull/18883
* build: the war on `config.h` is a war of attrition, 2 of ∞ by @eqvinox in https://github.com/FRRouting/frr/pull/18877
* bgpd: two minor fixes for command by @anlancs in https://github.com/FRRouting/frr/pull/18882
* bfdd:  Only apply increased transmission interval after Poll Sequence by @zmw12306 in https://github.com/FRRouting/frr/pull/18589
* bfdd: Check for passive mode with zero discriminator by @zmw12306 in https://github.com/FRRouting/frr/pull/18591
* ospfd: Fix crash when ospf client connects before configuring an OSPF instance by @Jafaral in https://github.com/FRRouting/frr/pull/18785
* lib: fix copying of resolved addresses by @kunkku in https://github.com/FRRouting/frr/pull/18871
* *: oh no, `config.h` is mobilizing its forces! - 3 of ∞ by @eqvinox in https://github.com/FRRouting/frr/pull/18884
* doc/developer: update instructions for NetBSD by @eqvinox in https://github.com/FRRouting/frr/pull/18879
* yang: Correct pyang errors in frr-bgp-route-map.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18781
* nhrpd: ignore non-host addresses on NHRP interfaces by @kunkku in https://github.com/FRRouting/frr/pull/18873
* staticd: fix deref of NULL pointer in srv6 code by @mjstapp in https://github.com/FRRouting/frr/pull/18890
* vtysh,doc: add an idle timeout for vtysh by @mjstapp in https://github.com/FRRouting/frr/pull/18711
* pimd: add support for PIM dense and sparse-dense modes by @Jafaral in https://github.com/FRRouting/frr/pull/18648
* doc: add a note about dplane API version to the release docs by @mjstapp in https://github.com/FRRouting/frr/pull/18896
* zebra: bump the dplane api version for FRR 10.4 by @mjstapp in https://github.com/FRRouting/frr/pull/18893
* lib: fix coverity defect CID 1643927 by @choppsv1 in https://github.com/FRRouting/frr/pull/18892
* bgpd: add neighbor ip-transparent by @vjardin in https://github.com/FRRouting/frr/pull/18789
* pimd, yang: move bsr xpath to be consistent with other rp implementations by @Jafaral in https://github.com/FRRouting/frr/pull/18898
* lib: fix build failure in darr by @eqvinox in https://github.com/FRRouting/frr/pull/18863
* github: Do not cache docker foobar by @ton31337 in https://github.com/FRRouting/frr/pull/18909
* bgpd: Drop deprecated JSON field `gracefulRestartCapability` by @ton31337 in https://github.com/FRRouting/frr/pull/18900
* pimd: fix a coverity issue with state refresh by @Jafaral in https://github.com/FRRouting/frr/pull/18902
* pbrd: Fix memory leak when destroying an interface by @ton31337 in https://github.com/FRRouting/frr/pull/18906
* zebra: [SRv6] persist func-len 0 across frr restart by @raja-rajasekar in https://github.com/FRRouting/frr/pull/18847
* bgpd: correct no form commands by @anlancs in https://github.com/FRRouting/frr/pull/18911
* mgmtd simplify frontend CLI config path by @choppsv1 in https://github.com/FRRouting/frr/pull/18888
* build: check for libunwind.h, not unwind.h by @eqvinox in https://github.com/FRRouting/frr/pull/18912
* mgmtd: remove unused and unneeded code. by @choppsv1 in https://github.com/FRRouting/frr/pull/18927
* zebra: Add some more debugging when netlink read fails for a route by @donaldsharp in https://github.com/FRRouting/frr/pull/18914
* build: `autoconf` cleanup pass by @eqvinox in https://github.com/FRRouting/frr/pull/18913
* Revert "tools: ignore spaces only in macro empty line." by @donaldsharp in https://github.com/FRRouting/frr/pull/18934
* tests: Address resource leaks in bmpserver.py by @y-bharath14 in https://github.com/FRRouting/frr/pull/18935
* bgpd: do not accept a host route that matches a local address by @enkechen-panw in https://github.com/FRRouting/frr/pull/17976
* bgpd: Add Hold Time(r) for BFD strict mode by @ton31337 in https://github.com/FRRouting/frr/pull/18901
* tools: ignore spaces only in macro empty line. by @choppsv1 in https://github.com/FRRouting/frr/pull/18937
* redhat: make FRR RPM build to work on RedHat 10 by @mwinter-osr in https://github.com/FRRouting/frr/pull/18920
* tools: Fix VRF static routes deletion on config reload instead of update by @dendergunov in https://github.com/FRRouting/frr/pull/18908
* Handle VRF blackhole routes in SRv6 L3VPN setup with static routes by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18931
* bgpd: use AS4B format for BGP loc-rib messages. by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18936
* BGP evpn testing and bug fixes related to non default EVPN backbone  by @pguibert6WIND in https://github.com/FRRouting/frr/pull/18358
* bgpd: Supporting Graceful Shutdown feature for Peer-Group by @Manpreet-k0 in https://github.com/FRRouting/frr/pull/18659
* *: fix a bunch of header file / `#include` loops by @eqvinox in https://github.com/FRRouting/frr/pull/18953
* Fix up dplane handling of some edge cases by @donaldsharp in https://github.com/FRRouting/frr/pull/18919
* pimd, tests: Fix dense mode flooding/grafting, expand dense/mixed mode testing by @nabahr in https://github.com/FRRouting/frr/pull/18903
* lib: use forward-refs to remove bgp header from lib header by @mjstapp in https://github.com/FRRouting/frr/pull/18960
* zebra: Do not show SRv6 locator params when they are set to default by @cscarpitta in https://github.com/FRRouting/frr/pull/18961
* tools: Ensure that checkpatch.sh checks return code of checkpatch.pl by @donaldsharp in https://github.com/FRRouting/frr/pull/18938
* bgpd: Force adj-rib-out updates if MRAI is kicked in by @ton31337 in https://github.com/FRRouting/frr/pull/18959
* zebra: add ability to dump fpm listener nhg by @donaldsharp in https://github.com/FRRouting/frr/pull/18676
* Replace lock and commit protobuf messages with native variants by @choppsv1 in https://github.com/FRRouting/frr/pull/18928
* bgpd: Unset TOVPN_SID_EXPLICIT flag to ensure BGP can release SRv6 SIDs by @cscarpitta in https://github.com/FRRouting/frr/pull/18969
* Remove last bits of protobuf from MGMTD by @choppsv1 in https://github.com/FRRouting/frr/pull/18948
* zebra: Provide SID value when sending SRv6 SID release notify message by @cscarpitta in https://github.com/FRRouting/frr/pull/18971
* lib: fix coverity "free address-of" issues by @choppsv1 in https://github.com/FRRouting/frr/pull/18968
* zebra: Allow routes that could be considered connected to exist by @donaldsharp in https://github.com/FRRouting/frr/pull/18967
* pimd: fix coverity issues by @Jafaral in https://github.com/FRRouting/frr/pull/18985
* bgpd: Free up leaked memory in case where routemap is not used by @donaldsharp in https://github.com/FRRouting/frr/pull/18529
* bgpd: Don't send notification if IPv6 Link-Local is not assigned on the interface by @ton31337 in https://github.com/FRRouting/frr/pull/18930
* zebra: Cleanup SRv6 output of `show running-config` by @cscarpitta in https://github.com/FRRouting/frr/pull/18970
* bgpd: Set atomic aggregate attribute if we drop AS_SETs by @ton31337 in https://github.com/FRRouting/frr/pull/18983
* bgpd: Add new CLI to show the counters of each attribute by @ton31337 in https://github.com/FRRouting/frr/pull/18984
* yang: Fix pyang errors in frr-pim-rp.yang by @y-bharath14 in https://github.com/FRRouting/frr/pull/18992
* pimd: use the correct vrf with recv prune and state refresh by @Jafaral in https://github.com/FRRouting/frr/pull/18986
* bgpd: Clean up evpn mac hash on shutdown. (backport #18996) by @mergify[bot] in https://github.com/FRRouting/frr/pull/18998
* bgpd: Do not reuse the same adj->adv when flushing fifo (attributes too long) (backport #18993) by @mergify[bot] in https://github.com/FRRouting/frr/pull/18999
* pimd: add boundary checks when parsing join/graft source lists (coverity) (backport #18989) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19006
* bgpd: Fix crash when fetching statistics for bgp instance (backport #19003) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19004
* tests: add new /run/netns tmpfs to each topotest router namespace (backport #19007) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19012
* Fix some coverity issues (backport #18897) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19021
* Add frr-host yang module - fix bug with reserved IP range config (backport #19019) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19026
* static: [SRv6] Fixing uninstall and reinstall uA Sids upon Intf flaps (backport #19027) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19032
* nhrpd: fix crash when accessing invalid memory zone (backport #18994) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19035
* bgpd: [TOPOTEST] stabilize bgp_peergroup_gshut test case (backport #18991) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19046
* pathd: fix compare function overflow (backport #19050) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19053
* Nhrp redundancy ping (backport #19048) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19052
* zebra: Initialize RB tree for router tables (backport #19049) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19055
* tests: Fix `bgp_srv6_sid_explicit` test failures  (backport #19068) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19075
* debian, redhat: add missing info to changelog by @Jafaral in https://github.com/FRRouting/frr/pull/19072
* zebra: fix null pointer dereference in zebra_evpn_sync_neigh_del (backport #19054) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19081
* zebra: fix stale NHG in kernel (backport #18899) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19085
* Doc and test update (backport #19070) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19084
* bgpd: Fix incorrect stripping of transitive extended communities due … (backport #19065) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19093
* lib: Fix `no on-match goto NUM` command (backport #19108) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19112
* bgpd: fix missing BGP_ROUTE_AGGREGATE for announcing to zebra (backport #19105) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19130
* bgpd: Fix extended community check for IP non-transitive type (backport #19097) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19133
* bgpd: Fix DEREF_OF_NULL.EX.COND in bgp_updgrp_packet (backport #19126) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19142
* zebra: zebra core with v6 RA (backport #19000) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19152
* lib: revert addition of vtysh_flush() call in vty_out() (backport #19109) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19153
* bgpd: free json objects in error paths (backport #19158) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19163
* bgpd: Extract link bandwidth value from extcommunity before using for WCMP (backport #19165) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19169
* lib,bgpd,ospf6d,zebra: Free json objects in error paths (backport #19182) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19184
* zebra: clean up a json object leak (backport #19192) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19195
* bgpd: Do not try to reuse freed route-maps (backport #19191) by @mergify[bot] in https://github.com/FRRouting/frr/pull/19200

## New Contributors
* @ariel-anieli made their first contribution in https://github.com/FRRouting/frr/pull/17649
* @kaffarell made their first contribution in https://github.com/FRRouting/frr/pull/18242
* @karthikeyav made their first contribution in https://github.com/FRRouting/frr/pull/18335
* @echkenluo made their first contribution in https://github.com/FRRouting/frr/pull/18407
* @chdxD1 made their first contribution in https://github.com/FRRouting/frr/pull/18325
* @usrivastava-nvidia made their first contribution in https://github.com/FRRouting/frr/pull/18330
* @Z-Yivon made their first contribution in https://github.com/FRRouting/frr/pull/18311
* @huchaogithup made their first contribution in https://github.com/FRRouting/frr/pull/18369
* @valentinbinotto made their first contribution in https://github.com/FRRouting/frr/pull/18691
* @AndriiFullroot made their first contribution in https://github.com/FRRouting/frr/pull/18417
* @kunkku made their first contribution in https://github.com/FRRouting/frr/pull/18871
* @dendergunov made their first contribution in https://github.com/FRRouting/frr/pull/18908

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.3...frr-10.4.0

## frr-10.3.1

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr

Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:f90d26a9fd5c14fc5795a73b4254ac88bc3186c45bbeb220a225fb6182de812c)

## Bug Fixes

babeld
 - Check valid babel port
 - Fix incorrect type assignment in parse_request_subtlv

bgpd
 - Fix set evpn gateway-ip ipv[46] route-map
 - Fix bmp heap use after free on non connected session
 - Fix evpn attributes being dropped on input
 - Fix holdtime not working properly when busy
 - Fix leaked memory when showing some bgp routes
 - Fixed crash upon bgp network import-check command
 - On shutdown free up memory leak found by topotest
 - Prevent crash when issuing a show rpki connections
 - Remove unused defines from bgp_label.h
 - Retain the routes if we do a clear with n-bit set for graceful-restart
 - Set the label for mp_unreach_nlri 0x800000 instead of 0x000000
 - Treat the peer as not active due to bfd down only if established

isisd
 - Fix srv6_sid memory leak

lib
 - Create vrf if needed
 - Return duplicate ipv6 prefix-list entry test
 - Return duplicate prefix-list entry test

nhrpd
 - Add hop count validation before forwarding in nhrp_peer_recv()

ospf6d
 - Disable and delete ospfv3 areas that no longer have interfaces or configuration.
 - Fix lsa memory leaks related to graceful restart

pimd
 - Fix for crash during networking restart
 - Fix memory leak on shutdown
 - Initialize gm proxy to false

staticd
 - Avoid requesting srv6 sid from zebra when loc and sid block dont match
 - Fix crash that occurs when modifying an srv6 sid

tools
 - Fix reload script for srv6 locators and formats

zebrad
 - Do not flush an existing vni configuration trying to remove wrong vni
 - Ensure proper return for failure for sid allocation
 - Fixes allowing srv6 func-bits length 0
 

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.3...frr-10.3.1

## frr-10.2.3

Debian Packages - https://deb.frrouting.org
RPM Packages - https://rpm.frrouting.org
Snaps - https://snapcraft.io/frr
Docker - [quay.io/frrouting/frr](https://quay.io/repository/frrouting/frr/manifest/sha256:b48e58300fea8288a8ea0ce62c6f722945bb9dda532526fb9ef12f88278e4d66)

## Bug Fixes

babeld
 - Check valid babel port
 - Fix incorrect type assignment in parse_request_subtlv

bgpd
 - Do not call evpn_overlay_free no matter what
 - Fix set evpn gateway-ip ipv[46] route-map
 - Fix holdtime not working properly when busy
 - Fixed crash upon bgp network import-check command
 - In bgp_update() for mac addrs ensure we are dealing with evpn
 - Prevent crash when issuing a show rpki connections
 - Retain the routes if we do a clear with n-bit set for graceful-restart
 - Treat the peer as not active due to bfd down only if established
 - Fix incorrect bestpath reasoning in some situations
 - Fix show bgp vpn rd json
 - Fix to show exist/non-exist-map in 'show run' properly
 - Add total path count for bgp net in json output

bfdd
 - On shutdown prefix/access list memory was being leaked

isisd
 - Fix srv6_sid memory leak

lib
 - Create vrf if needed
 - Return duplicate ipv6 prefix-list entry test
 - Return duplicate prefix-list entry test

ldpd
 - Free up leaked prefix-list memory on shutdown

nhrpd
 - Add hop count validation before forwarding in nhrp_peer_recv()

ospf6d
 - Disable and delete ospfv3 areas that no longer have interfaces or configuration.
 - Fix lsa memory leaks related to graceful restart

ospfd
 - Prune duplicate next-hops when installing into zebra
 - Fix crash when ospf client connects before doing 'router ospf'

pimd
 - Fix for crash during networking restart
 - Fix memory leak on shutdown
 - Initialize gm proxy to false

zebra
 - Do not flush an existing vni configuration trying to remove wrong vni
 - Ensure proper return for failure for sid allocation
 - Prevent vrf table 254 being used by non-default vrf
 - Fixes allowing srv6 func-bits length 0

**Full Changelog**: https://github.com/FRRouting/frr/compare/frr-10.2.2...frr-10.2.3

## FRR docs — mgmtd and per-daemon configuration files (docs.frrouting.org/en/latest/bgp.html)

Prior versions of FRR supported reading and writing per-daemon config files; however, with the introduction of the centralized management daemon `mgmtd` this could no longer be supported.

In order to allow for an orderly transition from per-daemon config files to the integrated config file, FRR daemons will continue to try and read their specific per-daemon configuration file as before.

Per-daemon files will no longer be updated when the user issues a `write memory` command. Therefore these per-daemon config files should only be used as a mechanism for transitioning to the integrated config, and then removed.

Configurations should be saved in the integrated file at `/etc/frr/frr.conf`. Per-daemon files can still be loaded directly using CLI options like `-f`, but these files will not be updated when the configuration is written.
