import tempfile, unittest
from pathlib import Path
import app
class Workflow(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        app.DB=str(Path(self.tmp.name)/'test.db')
        self.client=app.app.test_client()
    def test_approval_and_exports(self):
        self.assertEqual(self.client.post('/draft',data={'title':'Late arrival','steps':'Check reservation\nLeave welcome packet'}).status_code,302)
        self.assertEqual(self.client.get('/export/1/checklist').status_code,404)
        self.assertEqual(self.client.post('/approve/1').status_code,302)
        self.assertIn(b'Leave welcome packet',self.client.get('/export/1/checklist').data)
        self.assertIn(b'S0 --> S1',self.client.get('/export/1/diagram').data)
        self.client.post('/draft',data={'title':'Late arrival','steps':'New procedure'})
        self.assertEqual(self.client.get('/export/2/checklist').status_code,404)
        self.assertIn(b'Leave welcome packet',self.client.get('/export/1/checklist').data)
    def test_validation(self):
        self.assertEqual(self.client.post('/draft',data={'title':'','steps':''}).status_code,400)
        self.assertEqual(self.client.post('/approve/999').status_code,404)
        self.assertEqual(self.client.get('/health').status_code,200)
if __name__=='__main__': unittest.main()
