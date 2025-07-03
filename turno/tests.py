from django.test import TestCase
from django.urls import reverse
from .models import Turno
from profesional.models import Profesional
from paciente.models import Paciente
from empleado.models import Empleado

class TurnoModelTest(TestCase):
    def setUp(self):
        self.profesional = Profesional.objects.create(
            ci='111', nombre='Pro', apellido='Fesional', fecha_nacimiento='1980-01-01', direccion='Calle', telefono='123', especialidad='Cardiología', registro_profesional='REG1', otro_contacto='X')
        self.paciente = Paciente.objects.create(
            ci='222', nombre='Pa', apellido='Ciente', fecha_nacimiento='1990-01-01', direccion='Calle', telefono='456', otro_contacto='Y')
        self.empleado = Empleado.objects.create(
            ci='333', nombre='Em', apellido='pleado', fecha_nacimiento='1985-01-01', direccion='Calle', telefono=789, cargo='Admin')

    def test_creacion_turno(self):
        turno = Turno.objects.create(
            fecha='2024-01-01', hora='10:00', modalidad='Presencial', estado='Activo', motivo='Consulta', fue_notificado=True,
            profesional=self.profesional, paciente=self.paciente, empleado=self.empleado)
        self.assertIn(self.paciente.nombre, str(turno))
        self.assertEqual(Turno.objects.count(), 1)

class TurnoViewTest(TestCase):
    def setUp(self):
        self.profesional = Profesional.objects.create(
            ci='111', nombre='Pro', apellido='Fesional', fecha_nacimiento='1980-01-01', direccion='Calle', telefono='123', especialidad='Cardiología', registro_profesional='REG1', otro_contacto='X')
        self.paciente = Paciente.objects.create(
            ci='222', nombre='Pa', apellido='Ciente', fecha_nacimiento='1990-01-01', direccion='Calle', telefono='456', otro_contacto='Y')
        self.empleado = Empleado.objects.create(
            ci='333', nombre='Em', apellido='pleado', fecha_nacimiento='1985-01-01', direccion='Calle', telefono=789, cargo='Admin')
        self.turno = Turno.objects.create(
            fecha='2024-01-01', hora='10:00', modalidad='Presencial', estado='Activo', motivo='Consulta', fue_notificado=True,
            profesional=self.profesional, paciente=self.paciente, empleado=self.empleado)

    def test_listar_turnos_url(self):
        url = reverse('listar_turnos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pa')

    def test_crear_turno_url(self):
        url = reverse('crear_turno')
        data = {
            'fecha': '02/01/2024',
            'hora': '11:00',
            'modalidad': 'Presencial',
            'estado': 'Activo',
            'motivo': 'Control',
            'fue_notificado': True,
            'profesional': self.profesional.pk,
            'paciente': self.paciente.pk,
            'empleado': self.empleado.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Turno.objects.count(), 2)

    def test_editar_turno_url(self):
        url = reverse('editar_turno', args=[self.turno.pk])
        data = {
            'fecha': '01/01/2024',
            'hora': '10:00',
            'modalidad': 'Virtual',
            'estado': 'Cancelado',
            'motivo': 'Consulta',
            'fue_notificado': False,
            'profesional': self.profesional.pk,
            'paciente': self.paciente.pk,
            'empleado': self.empleado.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.modalidad, 'Virtual')
        self.assertEqual(self.turno.estado, 'Cancelado')

    def test_eliminar_turno_url(self):
        url = reverse('eliminar_turno', args=[self.turno.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Turno.objects.count(), 0)

class TurnoURLTest(TestCase):
    def test_urls_resuelven_vistas(self):
        self.assertEqual(reverse('crear_turno'), '/turno/crear/')
        self.assertEqual(reverse('listar_turnos'), '/turno/')
