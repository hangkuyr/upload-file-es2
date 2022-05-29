from includes import*
from app import*

T1_PUB = b'title1_PUB'
T2_PUB = b'title2_PUB'
T_PRIV = b'title_PRIV'

class TestSearch:

    def getDict(self, fileName, title, desc, password = ''):
        return {
            'file': (Path(__file__).parent / 'files' / fileName).open('rb'),
            'title': title,
            'desc': desc,
            'password': password
        }

    def getItem1Pub(self):
        return self.getDict(MP3_PATH, T1_PUB, 'desc1')

    def getItem2Pub(self):
        return self.getDict(MP3_PATH, T2_PUB, 'desc2')

    def getItem1Priv(self):
        return self.getDict(MP3_PATH, T_PRIV, 'desc1', 'pass1')

    def setup_method(self):
        self.app = CreateApp()
        self.client = self.app.test_client()

    def test_search1Item(self):
        item1 = self.getItem1Pub()
        self.client.post('/', data=item1)
        searchPostData = {
            'title': T1_PUB
        }
        response = self.client.post('/search', data=searchPostData)
        assert T1_PUB in response.data

    def test_search2Itens(self):

        self.client.post('/', data=self.getItem1Pub())
        self.client.post('/', data=self.getItem2Pub())

        searchPostData = {
            'title': 'titl'
        }
        response = self.client.post('/search', data=searchPostData)
        assert all(i in response.data for i in [T1_PUB, T2_PUB])

    def test_searchDoesNotReturnPrivateItem(self):
        pass

    def test_pubPrivPubReturns2Pubs(self):
        pass