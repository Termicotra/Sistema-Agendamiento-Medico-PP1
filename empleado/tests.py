from django.test import TestCase
from django.urls import reverse
from .models import Empleado

class EmpleadoModelTest(TestCase):
    def test_creacion_empleado(self):
        empleado = Empleado.objects.create(
            ci='12345678',
            nombre='Juan',
            apellido='Pérez',
            fecha_nacimiento='1990-01-01',  # YYYY-MM-DD
            direccion='Calle Falsa 123',
            telefono=123456789,
            cargo='Recepcionista'
        )
        self.assertEqual(str(empleado), 'Juan Pérez - Recepcionista')
        self.assertEqual(Empleado.objects.count(), 1)

class EmpleadoViewTest(TestCase):
    def setUp(self):
        self.empleado = Empleado.objects.create(
            ci='87654321',
            nombre='Ana',
            apellido='García',
            fecha_nacimiento='1985-05-05',  # YYYY-MM-DD
            direccion='Av. Siempre Viva 742',
            telefono=987654321,
            cargo='Enfermera'
        )

    def test_listar_empleados_url(self):
        url = reverse('listar_empleados')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana')

    def test_crear_empleado_url(self):
        url = reverse('crear_empleado')
        data = {
            'ci': '11223344',
            'nombre': 'Carlos',
            'apellido': 'López',
            'fecha_nacimiento': '02/02/1992',
            'direccion': 'Calle Nueva 456',
            'telefono': 5551234,
            'cargo': 'Doctor'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirige tras crear
        self.assertEqual(Empleado.objects.count(), 2)

    def test_editar_empleado_url(self):
        url = reverse('editar_empleado', args=[self.empleado.pk])
        data = {
            'ci': '87654321',
            'nombre': 'Ana Editada',
            'apellido': 'García',
            'fecha_nacimiento': '05/05/1985',
            'direccion': 'Av. Siempre Viva 742',
            'telefono': 987654321,
            'cargo': 'Enfermera'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.empleado.refresh_from_db()
        self.assertEqual(self.empleado.nombre, 'Ana Editada')

    def test_eliminar_empleado_url(self):
        url = reverse('eliminar_empleado', args=[self.empleado.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Empleado.objects.count(), 0)

class EmpleadoURLTest(TestCase):
    def test_urls_resuelven_vistas(self):
        self.assertEqual(reverse('crear_empleado'), '/empleado/crear/')
        self.assertEqual(reverse('listar_empleados'), '/empleado/')
