from django.test import TestCase
from django.urls import reverse
from .models import Paciente

class PacienteModelTest(TestCase):
    def test_creacion_paciente(self):
        paciente = Paciente.objects.create(
            ci='12345678',
            nombre='Juan',
            apellido='Pérez',
            fecha_nacimiento='1990-01-01',  # YYYY-MM-DD
            direccion='Calle Falsa 123',
            telefono='123456789',
            otro_contacto='Contacto X'
        )
        self.assertEqual(str(paciente), 'Juan Pérez 12345678')
        self.assertEqual(Paciente.objects.count(), 1)

class PacienteViewTest(TestCase):
    def setUp(self):
        self.paciente = Paciente.objects.create(
            ci='87654321',
            nombre='Ana',
            apellido='García',
            fecha_nacimiento='1985-05-05',  # YYYY-MM-DD
            direccion='Av. Siempre Viva 742',
            telefono='987654321',
            otro_contacto='Contacto Y'
        )

    def test_listar_pacientes_url(self):
        url = reverse('listar_pacientes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana')

    def test_crear_paciente_url(self):
        url = reverse('crear_paciente')
        data = {
            'ci': '11223344',
            'nombre': 'Carlos',
            'apellido': 'López',
            'fecha_nacimiento': '02/02/1992',
            'direccion': 'Calle Nueva 456',
            'telefono': '5551234',
            'otro_contacto': 'Contacto Z'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Paciente.objects.count(), 2)

    def test_editar_paciente_url(self):
        url = reverse('editar_paciente', args=[self.paciente.pk])
        data = {
            'ci': '87654321',
            'nombre': 'Ana Editada',
            'apellido': 'García',
            'fecha_nacimiento': '05/05/1985',
            'direccion': 'Av. Siempre Viva 742',
            'telefono': '987654321',
            'otro_contacto': 'Contacto Y'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.paciente.refresh_from_db()
        self.assertEqual(self.paciente.nombre, 'Ana Editada')

    def test_eliminar_paciente_url(self):
        url = reverse('eliminar_paciente', args=[self.paciente.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Paciente.objects.count(), 0)

class PacienteURLTest(TestCase):
    def test_urls_resuelven_vistas(self):
        self.assertEqual(reverse('crear_paciente'), '/paciente/crear/')
        self.assertEqual(reverse('listar_pacientes'), '/paciente/')
