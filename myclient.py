import asyncio
import sys
sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua

import time

async def main():
    url = 'opc.tcp://CX-385DB1:4840'
    # url = 'opc.tcp://commsvr.com:51234/UA/CAS_UA_Server'
    async with Client(url=url) as client:
        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        root = await root.get_children()

        # 'main.xxx' is the node name, 4 is the namespace (ns) , E.G. in uaexpert/objects/plcbeckhoff/MAIN/o_rxd
        O_RXD = client.get_node(ua.NodeId('MAIN.O_RXD', 4))
        M_RXD = client.get_node(ua.NodeId('MAIN.M_RXD', 4))
        M_RIF = client.get_node(ua.NodeId('MAIN.M_RIF', 4))
        M_FOOD = client.get_node(ua.NodeId('MAIN.M_FOOD', 4))

        out = await O_RXD.get_value()
        print('RXD out is {v} '.format(v=out))

        dt = 0.2
        while True:
            await M_RXD.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(dt)
            await M_RXD.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
            time.sleep(dt)
            await M_RIF.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(dt)
            await M_RIF.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
            time.sleep(dt)
            await M_FOOD.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
            time.sleep(dt)
            await M_FOOD.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))
            time.sleep(dt)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    loop.run_until_complete(main())
    loop.close()