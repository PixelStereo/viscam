def scale(value, old_min, old_max, new_min, new_max):
	return (((value - old_min) * (new_max - new_min)) / (old_max - old_min)) + new_min

def degree_to_visca(value, what, flip=False):
	if what == 'pan':
		# value must be between -170 & 170
		old_min = -170
		old_max = 170
		new_min = 45537
		new_max = 24094
	elif what == 'tilt':
		# value must be between -20 & 90
		old_min = -20
		old_max = 90
		new_min = 22479
		new_max = 4080
		if flip:
			# value must be between -90 & 20
			old_min = -90
			old_max = 20
			new_min = 271
			new_max = 47152
	return scale(value, old_min, old_max, new_min, new_max)

def visca_to_degree(value, what, flip=False):
	if what == 'pan':
		# value must be between -170 & 170
		old_min = 45537
		old_max = 24094
		new_min = -170
		new_max = 170
	elif what == 'tilt':
		# value must be between -20 & 90
		old_min = 22479
		old_max = 4080
		new_min = -20
		new_max = 90
		if flip:
			# value must be between -90 & 20
			old_min = 271
			old_max = 47152
			new_min = -90
			new_max = 20
	return scale(value, old_min, old_max, new_min, new_max)

print degree_to_visca(0, 'tilt', True)
print visca_to_degree(38628, 'tilt', True)