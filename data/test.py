from ase.io import read, write


atoms = read('ORCA_DATA.xyz', ':')


alkanes = []
cumulenes = []
for a in atoms:
	print(a.info['config_type'])
	if 'alkane' in a.info['config_type']:
		alkanes.append(a)
	elif 'cumulene' in a.info['config_type']:
		cumulenes.append(a)

write('data/ALKANES.xyz', alkanes)
write('data/CUMULENES.xyz', cumulenes)