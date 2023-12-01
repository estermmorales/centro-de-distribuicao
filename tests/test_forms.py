from django.test import TestCase
from protocolo.forms import ProtocoloForm

class SaveTestCase(TestCase):
    def setUp(self):
        self.protocolo = '25'
        self.emitente_nome = 'maria'
        self.destinatario_nome = 'ana'
        self.emitente = '1'
        self.destinatario = '2'

        self.dados = {
            'protocolo': self.protocolo,
            'emitente_nome': self.emitente_nome,
            'destinatario_nome': self.destinatario_nome,
            'emitente': self.emitente,
            'destinatario': self.destinatario
        }

        self.form = ProtocoloForm(data=self.dados)

    def test_save(self):
        form1 = ProtocoloForm(data=self.dados)
        form1.is_valid()
        res1 = form1.save()

        form2 = self.form
        form2.is_valid()
        res2 = form2.save()

        self.assertEquals(res1, res2)
