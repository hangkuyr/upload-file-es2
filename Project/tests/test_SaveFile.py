from includes import*
from db import*

def test_SaveFile():
	id = 'id teste'
	filename = 'teste.txt'
	data = b'teste bytes'
	title = 'título teste'
	desc = 'desc teste'
	SaveFileImpl(id, filename, data, title, desc)
	d = TryReadContents(id)
	assert d['title'] == title