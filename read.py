
import csv

f = open('sub17.csv', 'r')
file = open('write.txt','w') 


#BUS_1_BUS_17KV_BUS_1_V = Param.add_variable(addspace,"BUS_1_BUS_17KV_BUS_1_V",variant2)
#BUS_1_BUS_17KV_BUS_1_V.set_writable(True)

with f:
    reader = csv.DictReader(f)
    for row in reader:
    	if row['D'] == '2':
    		#print("variant")
    		typeVar='variant'
    	elif row['D'] == '4':
    		#print("variant2")
    		typeVar='variant2'

    	Arrange1 = row['B']+" = "+"Param.add_variable(addspace,\""+row['B']+"\","+typeVar+")"+"\n"
    	Arrange2 = row['B']+".set_writable(True)"+"\n"
    	print(Arrange1)
    	file.write(Arrange1)
    	file.write(Arrange2)  

        #,\""+row['B']+","+typeVar+")"+"\n"

        #print(row['A'], row['B'], row['C'], row['D'])
        #var = 'text:'+row['A']+row['B']+row['D']+"\n"
        
        #file.write(var) 


