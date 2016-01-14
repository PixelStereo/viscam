zoom = '\x90'+'\x50'+'\x0F'+'\x05'
zoom = zoom.encode('hex')
print type(zoom),len(zoom),zoom

def hex_unpack(zoom,L=[]):
	part = zoom[:2]
	zoom=zoom[2:]
	L.append(part)
	if zoom:
		hex_unpack(zoom,L)
	return L

zoom = hex_unpack(zoom)
print zoom
for item in zoom:
	print item,int(item,16)
