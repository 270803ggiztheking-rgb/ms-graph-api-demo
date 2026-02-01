"""
=============================================================================
EJEMPLO DE INTEGRACIÓN - Software Empresarial
=============================================================================
Este ejemplo muestra cómo integrar Microsoft Graph API en un sistema
empresarial existente para sincronizar emails, calendario y archivos.

Autor: Gael L. Chulim G.
Cliente: [Tu Empresa]
=============================================================================
"""
import asyncio
from datetime import datetime, timedelta

# Importar el cliente de Graph API
from src.graph_client import GraphClient
from src.auth import MSGraphAuth


class EmpresaSoftwareIntegration:
    """
    Ejemplo de integración de MS Graph API en software empresarial.
    
    Este módulo demuestra cómo:
    1. Sincronizar emails de empleados
    2. Crear eventos de calendario automáticamente
    3. Subir reportes a OneDrive compartido
    """
    
    def __init__(self, access_token: str):
        self.graph = GraphClient(access_token)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CASO DE USO 1: Sistema de Notificaciones por Email
    # ═══════════════════════════════════════════════════════════════════════
    
    async def enviar_notificacion_cliente(
        self,
        email_cliente: str,
        nombre_cliente: str,
        tipo_notificacion: str,
        detalles: dict
    ):
        """
        Envía notificación automática a cliente vía Outlook.
        
        Ejemplo de uso en sistema de facturación:
        - Notificar pago recibido
        - Recordatorio de vencimiento
        - Confirmación de pedido
        """
        plantillas = {
            "pago_recibido": f"""
                <h2>¡Pago Recibido!</h2>
                <p>Hola {nombre_cliente},</p>
                <p>Confirmamos la recepción de tu pago por <strong>${detalles.get('monto', 0):.2f}</strong></p>
                <p>Factura: {detalles.get('factura', 'N/A')}</p>
                <p>Gracias por tu preferencia.</p>
            """,
            "recordatorio_pago": f"""
                <h2>Recordatorio de Pago</h2>
                <p>Hola {nombre_cliente},</p>
                <p>Tu factura <strong>{detalles.get('factura', 'N/A')}</strong> vence en {detalles.get('dias', 0)} días.</p>
                <p>Monto pendiente: <strong>${detalles.get('monto', 0):.2f}</strong></p>
            """,
            "pedido_confirmado": f"""
                <h2>Pedido Confirmado</h2>
                <p>Hola {nombre_cliente},</p>
                <p>Tu pedido <strong>#{detalles.get('pedido_id', 'N/A')}</strong> ha sido confirmado.</p>
                <p>Fecha estimada de entrega: {detalles.get('fecha_entrega', 'Por confirmar')}</p>
            """
        }
        
        cuerpo = plantillas.get(tipo_notificacion, "<p>Notificación del sistema</p>")
        asunto = {
            "pago_recibido": "✅ Confirmación de Pago",
            "recordatorio_pago": "⏰ Recordatorio de Pago Pendiente",
            "pedido_confirmado": "📦 Tu Pedido ha sido Confirmado"
        }.get(tipo_notificacion, "Notificación")
        
        await self.graph.send_email(
            to=[email_cliente],
            subject=asunto,
            body=cuerpo
        )
        
        print(f"✅ Notificación enviada a {email_cliente}")
        return {"status": "sent", "to": email_cliente, "type": tipo_notificacion}
    
    # ═══════════════════════════════════════════════════════════════════════
    # CASO DE USO 2: Sincronización de Calendario
    # ═══════════════════════════════════════════════════════════════════════
    
    async def agendar_reunion_automatica(
        self,
        titulo: str,
        participantes: list[str],
        duracion_minutos: int = 60,
        descripcion: str = ""
    ):
        """
        Agenda reunión automáticamente en calendario de Microsoft 365.
        
        Ejemplo de uso:
        - CRM agenda llamada de seguimiento con cliente
        - Sistema de RRHH agenda entrevistas
        - Helpdesk agenda visitas técnicas
        """
        # Calcular próximo slot disponible (ejemplo: mañana a las 10am)
        inicio = datetime.now().replace(hour=10, minute=0, second=0) + timedelta(days=1)
        fin = inicio + timedelta(minutes=duracion_minutos)
        
        evento = await self.graph.create_event(
            subject=titulo,
            start=inicio.isoformat(),
            end=fin.isoformat(),
            attendees=participantes,
            body=f"""
                <h3>{titulo}</h3>
                <p>{descripcion}</p>
                <p><em>Esta reunión fue agendada automáticamente por el sistema.</em></p>
            """
        )
        
        print(f"📅 Reunión agendada: {titulo}")
        return evento
    
    # ═══════════════════════════════════════════════════════════════════════
    # CASO DE USO 3: Almacenamiento de Documentos en OneDrive
    # ═══════════════════════════════════════════════════════════════════════
    
    async def subir_reporte_mensual(
        self,
        mes: str,
        año: int,
        contenido_csv: str
    ):
        """
        Sube reportes mensuales a OneDrive corporativo.
        
        Ejemplo de uso:
        - Reportes de ventas automáticos
        - Backups de base de datos
        - Logs del sistema
        """
        nombre_archivo = f"reportes/{año}/reporte_{mes}_{año}.csv"
        
        resultado = await self.graph.upload_file(
            file_name=nombre_archivo,
            content=contenido_csv.encode('utf-8')
        )
        
        print(f"☁️ Reporte subido: {nombre_archivo}")
        return resultado
    
    async def obtener_inbox_resumen(self, limite: int = 5):
        """
        Obtiene resumen de emails recientes para dashboard.
        """
        emails = await self.graph.get_emails(top=limite)
        
        resumen = []
        for email in emails.get('value', []):
            resumen.append({
                "de": email.get('from', {}).get('emailAddress', {}).get('name', 'Desconocido'),
                "asunto": email.get('subject', 'Sin asunto'),
                "fecha": email.get('receivedDateTime', '')[:10],
                "leido": email.get('isRead', False)
            })
        
        return resumen


# ═══════════════════════════════════════════════════════════════════════════
# EJEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════════

async def demo():
    """
    Demostración de la integración.
    
    Para usar en producción:
    1. Obtener access_token via OAuth flow (ver src/auth.py)
    2. Instanciar EmpresaSoftwareIntegration con el token
    3. Llamar los métodos según necesidad del sistema
    """
    # NOTA: En producción, el token viene del flujo OAuth
    # access_token = "tu_token_aqui"
    # integracion = EmpresaSoftwareIntegration(access_token)
    
    print("=" * 60)
    print("DEMO: Integración Microsoft Graph API")
    print("=" * 60)
    print()
    print("CASO 1: Enviar notificación de pago")
    print("  await integracion.enviar_notificacion_cliente(")
    print('      email_cliente="cliente@empresa.com",')
    print('      nombre_cliente="Juan Pérez",')
    print('      tipo_notificacion="pago_recibido",')
    print('      detalles={"monto": 1500.00, "factura": "F-2024-001"}')
    print("  )")
    print()
    print("CASO 2: Agendar reunión automática")
    print("  await integracion.agendar_reunion_automatica(")
    print('      titulo="Revisión de Proyecto",')
    print('      participantes=["socio@empresa.com"],')
    print("      duracion_minutos=30")
    print("  )")
    print()
    print("CASO 3: Subir reporte a OneDrive")
    print('  await integracion.subir_reporte_mensual("enero", 2024, csv_data)')
    print()
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
