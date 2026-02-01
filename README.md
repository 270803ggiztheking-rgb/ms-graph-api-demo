![Microsoft Graph API Integration](banner.png)

# 🔗 Microsoft Graph API Demo

Demo de integración con Microsoft Graph API usando Python (FastAPI).

## 🚀 Características

- ✅ Autenticación OAuth 2.0 con Azure AD
- ✅ Lectura de emails (Outlook)
- ✅ Envío de emails
- ✅ Gestión de calendario
- ✅ Acceso a OneDrive (subir/descargar archivos)
- ✅ Información del usuario

## 📋 Requisitos Previos

1. Cuenta de Microsoft 365 / Azure AD
2. Aplicación registrada en Azure Portal
3. Python 3.9+

## ⚙️ Configuración Azure

1. Ve a [Azure Portal](https://portal.azure.com)
2. Navega a **Azure Active Directory** > **App registrations**
3. Click en **New registration**
4. Configura:
   - Name: `MS Graph Demo`
   - Redirect URI: `http://localhost:8000/callback`
5. Copia el **Application (client) ID** y **Directory (tenant) ID**
6. En **Certificates & secrets**, crea un nuevo **Client secret**
7. En **API permissions**, agrega:
   - `User.Read`
   - `Mail.Read`
   - `Mail.Send`
   - `Calendars.ReadWrite`
   - `Files.ReadWrite`

## 🛠️ Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/ms-graph-api-demo.git
cd ms-graph-api-demo

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Azure
```

## 🔐 Variables de Entorno

```env
CLIENT_ID=tu-client-id
CLIENT_SECRET=tu-client-secret
TENANT_ID=tu-tenant-id
REDIRECT_URI=http://localhost:8000/callback
```

## 🚀 Uso

```bash
# Iniciar servidor
uvicorn src.main:app --reload

# Abrir navegador
# http://localhost:8000
```

## 📚 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página principal |
| GET | `/login` | Iniciar autenticación OAuth |
| GET | `/callback` | Callback de Azure AD |
| GET | `/me` | Información del usuario |
| GET | `/emails` | Listar emails |
| POST | `/send-email` | Enviar email |
| GET | `/calendar` | Eventos del calendario |
| GET | `/files` | Archivos de OneDrive |

## 📁 Estructura

```
ms-graph-api-demo/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── auth.py           # OAuth 2.0 logic
│   ├── graph_client.py   # Microsoft Graph client
│   └── routes/
│       ├── __init__.py
│       ├── mail.py       # Email endpoints
│       ├── calendar.py   # Calendar endpoints
│       └── files.py      # OneDrive endpoints
├── .env.example
├── requirements.txt
└── README.md
```

## 📄 Licencia

MIT License

## 👤 Autor

**Gael L. Chulim G.**  
Freelance Developer & Automation Specialist  
[LinkedIn](https://linkedin.com/in/tu-perfil) | [GitHub](https://github.com/tu-usuario)
