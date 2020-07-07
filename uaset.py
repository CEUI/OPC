from opcua import Client
from opcua import ua
import time

url = "opc.tcp://127.0.0.1:8899/freeopcua/server/"

client = Client(url)

client.connect()
print("client connected")

val1 = client.get_node("ns=2;i=16")
value1 = val1.get_value()
val2 = client.get_node("ns=2;i=4")
value2 = val2.get_value()
print(value1)
#print(value2)
print("--")
val1.set_value(3, ua.VariantType.Int16)
#val2.set_value(9, ua.VariantType.Float)
value1 = val1.get_value()
#value2 = val2.get_value()
print(value1)
#print(value2)

client.disconnect()

# get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type