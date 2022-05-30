from includes import*
from app import*

T1_PUB = 'title1_PUB'
T2_PUB = 'title2_PUB'
T_PRIV = 'title_PRIV'

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
        assert bytes(T1_PUB.encode()) in response.data

    def test_search2Itens(self):

        self.client.post('/', data=self.getItem1Pub())
        self.client.post('/', data=self.getItem2Pub())

        searchPostData = {
            'title': 'titl'
        }
        response = self.client.post('/search', data=searchPostData)
        assert all(bytes(i.encode()) in response.data for i in [T1_PUB, T2_PUB])

    def test_searchDoesNotReturnPrivateItem(self):

        self.client.post('/', data=self.getItem1Priv())
        searchPostData = {
            'title': T_PRIV
        }
        response = self.client.post('/search', data=searchPostData)
        assert bytes(T_PRIV.encode()) not in response.data

    def test_PubPrivPubReturns2Pubs(self):
        # 3 uploads (intercalados pub priv pub)
        self.client.post('/', data=self.getItem1Pub())
        self.client.post('/', data=self.getItem1Priv())
        self.client.post('/', data=self.getItem2Pub())

        searchPostData = {
            'title': 'titl'
        }
        response = self.client.post('/search', data=searchPostData)
        data = response.data
        assert all(bytes(i.encode()) in data for i in [T1_PUB, T2_PUB]) and bytes(T_PRIV.encode()) not in data