from django.test import TestCase
from django.urls import reverse
from .models import Insumo

class InsumoModelTest(TestCase):
    def test_creacion_insumo(self):
        insumo = Insumo.objects.create(
            nombre='Paracetamol',
            descripcion='Analgésico',
            cantidad=100,
            fecha_caducidad='2025-12-31',  # YYYY-MM-DD
            laboratorio='LabX'
        )
        self.assertEqual(str(insumo), 'Paracetamol LabX')
        self.assertEqual(Insumo.objects.count(), 1)

class InsumoViewTest(TestCase):
    def setUp(self):
        self.insumo = Insumo.objects.create(
            nombre='Ibuprofeno',
            descripcion='Antiinflamatorio',
            cantidad=50,
            fecha_caducidad='2024-11-30',  # YYYY-MM-DD
            laboratorio='LabY'
        )

    def test_listar_insumos_url(self):
        url = reverse('listar_insumos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ibuprofeno')

    def test_crear_insumo_url(self):
        url = reverse('crear_insumo')
        data = {
            'nombre': 'Amoxicilina',
            'descripcion': 'Antibiótico',
            'cantidad': 30,
            'fecha_caducidad': '01/01/2026',
            'laboratorio': 'LabZ'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Insumo.objects.count(), 2)

    def test_editar_insumo_url(self):
        url = reverse('editar_insumo', args=[self.insumo.pk])
        data = {
            'nombre': 'Ibuprofeno Editado',
            'descripcion': 'Antiinflamatorio',
            'cantidad': 50,
            'fecha_caducidad': '30/11/2024',
            'laboratorio': 'LabY'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.nombre, 'Ibuprofeno Editado')

    def test_eliminar_insumo_url(self):
        url = reverse('eliminar_insumo', args=[self.insumo.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Insumo.objects.count(), 0)

class InsumoURLTest(TestCase):
    def test_urls_resuelven_vistas(self):
        self.assertEqual(reverse('crear_insumo'), '/inventario/crear/')
        self.assertEqual(reverse('listar_insumos'), '/inventario/')
