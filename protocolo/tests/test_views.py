from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy

class ProtocoloTestCase(TestCase):
    def setUp(self):
        self.dados={
            'protocolos': '10',
            'total_retirado': '5',
            'total_pendente':'4',
            'total_cancelado':'1',
            #colocar todos os campos

        }

        self.cliente = Client()

    def test_protocolo_valid(self):
        request = self.cliente.post(reverse_lazy('protocolo'), data=self.dados )
        self.assertEquals(request.status_code, 302)

    def test_protocolo_invalid(self):
        dados = {
            'protocolos': '5',
        }
        request = self.cliente.post(reverse_lazy('protocolo'), data=dados)
        self.assertEquals(request.status_code, 302)
