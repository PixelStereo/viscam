zoom = '\x90'+'\x50'+'\x0F'+'\x05'
zoom = zoom.encode('hex')
print type(zoom),len(zoom),zoom

def hex_unpack(zoom,L):
	part = zoom[:2]
	zoom=zoom[2:]
	L.append(part)
	if zoom:
		hex_unpack(zoom,L)
	return L

zoom = hex_unpack(zoom,[])
print zoom


value = 52719
print 'DEPART' , value
ViscaLongMsg = []
valuea = value & 15 
valuebZ = value >> 4 
valuecZ = value >> 8 
valuedZ = value >> 12 
valueb = valuebZ & 15 
valuec = valuecZ & 15 
valued = valuedZ & 15 
valuea = chr(valuea).encode('hex')
valueb = chr(valueb).encode('hex')
valuec = chr(valuec).encode('hex')
valued = chr(valued).encode('hex')
value = valuea+valueb+valuec+valued
print 'CONVERTED' , value
value = hex_unpack(value,[])
print 'BEFORE',value,len(value)
a = value[0]
b = value[1]
c = value[2]
d = value[3]
a=int(a,16)
b=int(b,16)
c=int(c,16)
d=int(d,16)
value = [a,b,c,d]
print 'COME BACK' , value
value = ((((((16*d)+c)*16)+b)*16)+a)
print 'FINAL' , value


