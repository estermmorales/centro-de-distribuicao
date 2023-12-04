

from django.test import TestCase
from model_mommy import mommy
from protocolo.models import Funcionario

class FuncionarioTestCase(TestCase):
    def setUp(self):
        self.funcionario = mommy.make('Funcionario')

    def test_str(self):
        self.assertEquals(str(self.funcionario), self.funcionario.email)


"""class FuncionarioManagerTestCase(TestCase):
    def setUp(self):
        self.email = 'teste@teste.com'
        self.user = 'teste@teste.com'

        self.dados = {
            'email': self.email,
            'user': self.user,
        }

        self.form = FuncionarioManager(data=self.dados)

    def test_funcionario_manager(self):
        form1 = FuncionarioManager(data=self.dados)
        form1.isvalid()
        res1 = form1.funcionario_manager()

        form2 = self.form
        form2.is_valid()
        res2 = form2.funcionario_manager()

        self.assertEquals(res1, res2)"""
