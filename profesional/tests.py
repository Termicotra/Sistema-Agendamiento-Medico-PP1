from django.test import TestCase
from django.urls import reverse
from .models import Profesional

class ProfesionalModelTest(TestCase):
    def test_creacion_profesional(self):
        profesional = Profesional.objects.create(
            ci='12345678',
            nombre='Juan',
            apellido='Pérez',
            fecha_nacimiento='1990-01-01',
            direccion='Calle Falsa 123',
            telefono='123456789',
            especialidad='Cardiología',
            registro_profesional='REG123',
            otro_contacto='Contacto X'
        )
        self.assertEqual(str(profesional), 'Juan Pérez - Cardiología ')
        self.assertEqual(Profesional.objects.count(), 1)

class ProfesionalViewTest(TestCase):
    def setUp(self):
        self.profesional = Profesional.objects.create(
            ci='87654321',
            nombre='Ana',
            apellido='García',
            fecha_nacimiento='1985-05-05',
            direccion='Av. Siempre Viva 742',
            telefono='987654321',
            especialidad='Pediatría',
            registro_profesional='REG456',
            otro_contacto='Contacto Y'
        )

    def test_listar_profesionales_url(self):
        url = reverse('listar_profesionales')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana')

    def test_crear_profesional_url(self):
        url = reverse('crear_profesional')
        data = {
            'ci': '11223344',
            'nombre': 'Carlos',
            'apellido': 'López',
            'fecha_nacimiento': '1992-02-02',
            'direccion': 'Calle Nueva 456',
            'telefono': '5551234',
            'especialidad': 'Dermatología',
            'registro_profesional': 'REG789',
            'otro_contacto': 'Contacto Z'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profesional.objects.count(), 2)

    def test_editar_profesional_url(self):
        url = reverse('editar_profesional', args=[self.profesional.pk])
        data = {
            'ci': '87654321',
            'nombre': 'Ana Editada',
            'apellido': 'García',
            'fecha_nacimiento': '1985-05-05',
            'direccion': 'Av. Siempre Viva 742',
            'telefono': '987654321',
            'especialidad': 'Pediatría',
            'registro_profesional': 'REG456',
            'otro_contacto': 'Contacto Y'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.profesional.refresh_from_db()
        self.assertEqual(self.profesional.nombre, 'Ana Editada')

    def test_eliminar_profesional_url(self):
        url = reverse('eliminar_profesional', args=[self.profesional.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profesional.objects.count(), 0)

class ProfesionalURLTest(TestCase):
    def test_urls_resuelven_vistas(self):
        self.assertEqual(reverse('crear_profesional'), '/profesional/crear/')
        self.assertEqual(reverse('listar_profesionales'), '/profesional/')
