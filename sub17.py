from opcua import Server
from opcua import ua
from opcua import Client
from random import randint
import datetime
import time

server = Server()
url = "opc.tcp://0.0.0.0:8899/freeopcua/server/"
server.set_endpoint(url)

name="OPC_UA_SERVER"
addspace = server.register_namespace(name)

#Define Variant Data Type  2 = Integer ; 4 = float
variant = None
variant = ua.Variant(0, ua.VariantType.Int16)

variant2 = None
variant2 = ua.Variant(0, ua.VariantType.Float)



node = server.get_objects_node()
Param = node.add_object(addspace,"Substation17Bus01")

Temp = Param.add_variable(addspace,"Temperature",0)

BUS_01_V_RES = Param.add_variable(addspace,"BUS_01_V_RES",variant2)
BUS_01_V_RES.set_writable(True)
LINE_01_02_I_RES = Param.add_variable(addspace,"LINE_01_02_I_RES",variant2)
LINE_01_02_I_RES.set_writable(True)
LINE_01_02_P_RES = Param.add_variable(addspace,"LINE_01_02_P_RES",variant2)
LINE_01_02_P_RES.set_writable(True)
LINE_01_02_Q_RES = Param.add_variable(addspace,"LINE_01_02_Q_RES",variant2)
LINE_01_02_Q_RES.set_writable(True)
LINE_01_02_V_RES = Param.add_variable(addspace,"LINE_01_02_V_RES",variant2)
LINE_01_02_V_RES.set_writable(True)
LINE_01_02_f_RES = Param.add_variable(addspace,"LINE_01_02_f_RES",variant2)
LINE_01_02_f_RES.set_writable(True)
LINE_01_39_I_RES = Param.add_variable(addspace,"LINE_01_39_I_RES",variant2)
LINE_01_39_I_RES.set_writable(True)
LINE_01_39_P_RES = Param.add_variable(addspace,"LINE_01_39_P_RES",variant2)
LINE_01_39_P_RES.set_writable(True)
LINE_01_39_Q_RES = Param.add_variable(addspace,"LINE_01_39_Q_RES",variant2)
LINE_01_39_Q_RES.set_writable(True)
LINE_01_39_V_RES = Param.add_variable(addspace,"LINE_01_39_V_RES",variant2)
LINE_01_39_V_RES.set_writable(True)
SWT_LINE_01_02 = Param.add_variable(addspace,"SWT_LINE_01_02",variant)
SWT_LINE_01_02.set_writable(True)
SWT_LINE_01_02_RES = Param.add_variable(addspace,"SWT_LINE_01_02_RES",variant)
SWT_LINE_01_02_RES.set_writable(True)
SWT_LINE_01_39 = Param.add_variable(addspace,"SWT_LINE_01_39",variant)
SWT_LINE_01_39.set_writable(True)
SWT_LINE_01_39_RES = Param.add_variable(addspace,"SWT_LINE_01_39_RES",variant)
SWT_LINE_01_39_RES.set_writable(True)




server.start()

print("Server start at {}".format(url))

i = 1
while i < 5:
    """
    print(

        BUS_1_BUS_17KV_BUS_1_V_RES.get_value(),
        BUS_2_BUS_18KV_BUS_2_V_RES.get_value(),
        BUS_3_BUS_14KV_BUS_3_V_RES.get_value(),
        BUS_4_LNE_230KV_LINE_1_P_RES.get_value(),
        BUS_5_LNE_230KV_LINE_1_P.get_value(),
        BUS_6_LNE_230KV_LINE_5_Q.get_value(),
        BUS_7_LNE_230KV_LINE_2_P.get_value(),
        BUS_8_LNE_230KV_LINE_3_P.get_value(),
        BUS_9_LNE_230KV_LINE_4_P.get_value(),

        )
    """

    time.sleep(1)

 

server.stop()



"""
idx = server.register_namespace(uri)
server.start()
objects = server.get_objects_node()
self.pfGroup = objects.add_object(idx, "PF")
pfVar = self.pfGroup.add_variable(idx, var.aliasName, variant)

"""

