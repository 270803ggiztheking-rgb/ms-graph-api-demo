"""
=============================================================================
EJEMPLO RÁPIDO - Quick Start
=============================================================================
Script minimalista para probar la conexión con Microsoft Graph API.
Ideal para verificar que las credenciales funcionan correctamente.

Autor: Gael L. Chulim G.
=============================================================================
"""
import asyncio
import httpx


async def quick_test(access_token: str):
    """
    Test rápido de conexión con Graph API.
    
    Pasos para obtener access_token:
    1. Registrar app en Azure Portal
    2. Ejecutar el servidor: uvicorn src.main:app
    3. Navegar a http://localhost:8000/login
    4. Copiar el token de la sesión
    """
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        # Test 1: Información del usuario
        print("🔍 Obteniendo información del usuario...")
        response = await client.get(
            "https://graph.microsoft.com/v1.0/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Usuario: {user.get('displayName')}")
            print(f"   Email: {user.get('mail') or user.get('userPrincipalName')}")
            print(f"   Job Title: {user.get('jobTitle', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return
        
        # Test 2: Últimos 3 emails
        print("\n📧 Últimos 3 emails:")
        response = await client.get(
            "https://graph.microsoft.com/v1.0/me/messages?$top=3",
            headers=headers
        )
        
        if response.status_code == 200:
            emails = response.json().get('value', [])
            for i, email in enumerate(emails, 1):
                sender = email.get('from', {}).get('emailAddress', {}).get('name', 'Unknown')
                subject = email.get('subject', 'Sin asunto')[:40]
                print(f"   {i}. De: {sender}")
                print(f"      Asunto: {subject}...")
        
        print("\n✅ Conexión exitosa con Microsoft Graph API!")


if __name__ == "__main__":
    # Reemplazar con tu token
    TOKEN = "PEGAR_TU_ACCESS_TOKEN_AQUI"
    
    if TOKEN == "PEGAR_TU_ACCESS_TOKEN_AQUI":
        print("⚠️  Por favor, reemplaza TOKEN con tu access_token")
        print("   Obtener token: http://localhost:8000/login")
    else:
        asyncio.run(quick_test(TOKEN))
