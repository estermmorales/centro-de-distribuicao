from django.test import TestCase
from model_mommy import mommy
from protocolo.models import Funcionario

class FuncionarioTestCase(TestCase):
    def setUp(self):
        self.funcionario = mommy.make('Funcionario')

    def test_str(self):
        self.assertEquals(str(self.funcionario), self.funcionario.email)
