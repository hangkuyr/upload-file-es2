from pch import*

def SaveFile(id, data, optTitle=None, optDesc=None):
	with open(PRIV_DIR + id, 'wb') as f:
		f.write(data)
	# todo save in database the entries instead of the filesystem