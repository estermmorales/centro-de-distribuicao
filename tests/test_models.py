from django.test import TestCase
from model_mommy import mommy

class FuncionarioManagerTestCase(TestCase):
    def setUp(self):
        self.funcionario = mommy.make('FuncionarioManager')

    def test_str(self):
        self.assertEquals(str(self.funcionario), self.funcionario.funcionario)


