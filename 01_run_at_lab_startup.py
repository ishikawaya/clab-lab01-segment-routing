import pexpect

# ラボ名
labname = "lab01"

# ノードとAS番号の対応表
nodes = {
    "pe1": 65001,
    "pe2": 65001,
    "pe3": 65002,
    "pe4": 65002,
}

for host, asn in nodes.items():
    print(f"=== Configuring {host} (AS{asn}) ===")

    # docker execでvtyshを起動
    cmd = f"docker exec -ti clab-{labname}-{host} bash -c vtysh"
    child = pexpect.spawn(cmd)

    # プロンプト待ち: peX>
    child.expect(f"{host}#")

    # conf t
    child.sendline("conf t")
    child.expect(f"{host}\\(config\\)#")

    # router bgp <ASN> vrf red
    child.sendline(f"router bgp {asn} vrf red")
    child.expect(f"{host}\\(config-router\\)#")

    # address-family ipv4 unicast
    child.sendline("address-family ipv4 unicast")
    child.expect(f"{host}\\(config-router-af\\)#")

    # rt vpn both 65000:20
    child.sendline("rt vpn both 65000:20")
    child.expect(f"{host}\\(config-router-af\\)#")

    # 終了
    child.sendline("exit")
    child.sendline("exit")
    child.sendline("exit")

    child.close()

