from includes import*
from saveFile import*

def test_SaveFile():
	id = 'abc'
	content = b'hello'
	SaveFile(id, content)
	with open(PRIV_DIR + id, 'rb') as f:
		writtenContent = f.read()
		assert writtenContent == content