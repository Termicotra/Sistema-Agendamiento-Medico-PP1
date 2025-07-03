from django.test import TestCase
from django.urls import reverse
from .models import Facturacion
from turno.models import Turno
from profesional.models import Profesional
from paciente.models import Paciente
from empleado.models import Empleado

class FacturacionModelTest(TestCase):
    def setUp(self):
        self.profesional = Profesional.objects.create(
            ci='111', nombre='Pro', apellido='Fesional', fecha_nacimiento='1980-01-01', direccion='Calle', telefono='123', especialidad='Cardiología', registro_profesional='REG1', otro_contacto='X')
        self.paciente = Paciente.objects.create(
            ci='222', nombre='Pa', apellido='Ciente', fecha_nacimiento='1990-01-01', direccion='Calle', telefono='456', otro_contacto='X')
        self.empleado = Empleado.objects.create(
            ci='333', nombre='Em', apellido='pleado', fecha_nacimiento='1985-01-01', direccion='Calle', telefono=789, cargo='Admin')
        self.turno = Turno.objects.create(
            fecha='2024-01-01', hora='10:00', modalidad='Presencial', estado='Activo', motivo='Consulta', fue_notificado=True,
            profesional=self.profesional, paciente=self.paciente, empleado=self.empleado)

    def test_creacion_facturacion(self):
        facturacion = Facturacion.objects.create(
            fecha='2024-01-01', monto_total=100, metodo_pago='Efectivo', tipo_facturacion=1, estado='Pendiente', turno=self.turno)
        self.assertIn('Factura', str(facturacion))
        self.assertEqual(Facturacion.objects.count(), 1)

class FacturacionViewTest(TestCase):
    def setUp(self):
        self.profesional = Profesional.objects.create(
            ci='111', nombre='Pro', apellido='Fesional', fecha_nacimiento='1980-01-01', direccion='Calle', telefono='123', especialidad='Cardiología', registro_profesional='REG1', otro_contacto='X')
        self.paciente = Paciente.objects.create(
            ci='222', nombre='Pa', apellido='Ciente', fecha_nacimiento='1990-01-01', direccion='Calle', telefono='456', otro_contacto='X')
        self.empleado = Empleado.objects.create(
            ci='333', nombre='Em', apellido='pleado', fecha_nacimiento='1985-01-01', direccion='Calle', telefono=789, cargo='Admin')
        self.turno = Turno.objects.create(
            fecha='2024-01-01', hora='10:00', modalidad='Presencial', estado='Activo', motivo='Consulta', fue_notificado=True,
            profesional=self.profesional, paciente=self.paciente, empleado=self.empleado)
        self.facturacion = Facturacion.objects.create(
            fecha='2024-01-01', monto_total=100, metodo_pago='Efectivo', tipo_facturacion=1, estado='Pendiente', turno=self.turno)

    def test_listar_facturaciones_url(self):
        url = reverse('listar_facturaciones')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Factura')

    def test_crear_facturacion_url(self):
        url = reverse('crear_facturacion')
        data = {
            'fecha': '02/01/2024',
            'monto_total': 200,
            'metodo_pago': 'Efectivo',
            'tipo_facturacion': 2,
            'estado': 'Pendiente',
            'turno': self.turno.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Facturacion.objects.count(), 2)

    def test_editar_facturacion_url(self):
        url = reverse('editar_facturacion', args=[self.facturacion.pk])
        data = {
            'fecha': '01/01/2024',
            'monto_total': 150,
            'metodo_pago': 'Efectivo',
            'tipo_facturacion': 1,
            'estado': 'Pagado',
            'turno': self.turno.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.facturacion.refresh_from_db()
        self.assertEqual(self.facturacion.monto_total, 150)
        self.assertEqual(self.facturacion.estado, 'Pagado')

    def test_eliminar_facturacion_url(self):
        url = reverse('eliminar_facturacion', args=[self.facturacion.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Facturacion.objects.count(), 0)

class FacturacionURLTest(TestCase):
    def test_urls_resuelven_vistas(self):
        self.assertEqual(reverse('crear_facturacion'), '/facturacion/crear/')
        self.assertEqual(reverse('listar_facturaciones'), '/facturacion/')
