
def translate(reply):
	reply = reply.encode('hex')
	def hex_unpack(zoom, L, size=2):
		part = zoom[:size]
		zoom = zoom[size:]
		L.append(part)
		if zoom:
			hex_unpack(zoom, L)
			return L
	reply = hex_unpack(reply, [])
	a = reply[0]
	b = reply[1]
	c = reply[2]
	d = reply[3]
	a=int(a,16)
	b=int(b,16)
	c=int(c,16)
	d=int(d,16)
	reply = ((((((16*d)+c)*16)+b)*16)+a)
	return reply

reply = '\x0E'+'\x01'+'\x0E'+'\x05'
print 'E1E5 ->', translate(reply)
reply = '\x01'+'\x0E'+'\x01'+'\x0B'
print '1E1B ->', translate(reply)

reply = '\x0F'+'\x0C'+'\x07'+'\x05'
print 'FC75 ->', translate(reply)
reply = '\x00'+'\x0F'+'\x0F'+'\x00'
print '0FF0 ->', translate(reply)

reply = '\x0F'+'\x00'+'\x01'+'\x00'
print 'F010 ->', translate(reply)
reply = '\x00'+'\x03'+'\x08'+'\x0B'
print '038B ->', translate(reply)

OldValue = 0
OldMin = -170
OldMax = 170
NewMax = 24094
NewMin = 45537
OldRange = (OldMax - OldMin)  
NewRange = (NewMax - NewMin)  
NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
print NewValue

"""
This is the result code
"""
reply = 127
# convert degree to visca pan
NewValue = (((reply - -170) * (24094 - 45537)) / (170 - -170)) + 45537
# convert visca pan to degree
NewValue = (((NewValue - 45537) * (170 - -170)) / (24094 - 45537)) + -170

print NewValue
