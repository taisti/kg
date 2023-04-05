import re

def convert_quantity(input):
    pattern1 = '^([0-9]+) ([0-9]+)/([0-9]+)$'
    pattern2 = '^([0-9]+(\.[0-9]+)?) ([0-9]+(\.[0-9]+)?)$'
    pattern3 = '^([0-9]+)/([0-9]+) ([0-9]+)/([0-9]+)$'
    pattern4 = '^([0-9]+)/([0-9]+) ([0-9]+)$'
    if re.match(pattern1,input):
       result = re.match(pattern1,input)
       whole_number = float(result[1])
       nominator = float(result[2])
       denominator = float(result[3])
       return whole_number + (nominator/denominator)
    if re.match(pattern2,input):
       result = re.match(pattern2,input)
       n1 = float(result[1])
       n2 = float(result[3])
       return n1 * n2
    if re.match(pattern3,input):
       result = re.match(pattern3,input)
       nominator1 = float(result[1])
       denominator1 = float(result[2])
       nominator2 = float(result[3])
       denominator2 = float(result[4])
       return (nominator1/denominator1) * (nominator2/denominator2)
    if re.match(pattern4,input):
       result = re.match(pattern4,input)
       nominator1 = float(result[1])
       denominator1 = float(result[2])  
       whole_number = float(result[3])
       return (nominator1/denominator1) * whole_number
    
print(convert_quantity('1 1/2'))
print(convert_quantity('1/2 1/2'))
print(convert_quantity('2 4'))
print(convert_quantity('2.5 4'))
print(convert_quantity('4.5 4.5'))
print(convert_quantity('1/2 3'))