import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent/".env")
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY","dev-only-change-me")
DEBUG=os.getenv("DEBUG","True").lower()=="true"
ALLOWED_HOSTS=[h.strip() for h in os.getenv("ALLOWED_HOSTS","127.0.0.1,localhost").split(",") if h.strip()]
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","corsheaders","rest_framework","automations"]
MIDDLEWARE=["corsheaders.middleware.CorsMiddleware","django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="config.wsgi.application"
DATABASES={"default":{"ENGINE":"django.db.backends.postgresql","NAME":os.getenv("POSTGRES_DB","automation"),"USER":os.getenv("POSTGRES_USER","postgres"),"PASSWORD":os.getenv("POSTGRES_PASSWORD","postgres"),"HOST":os.getenv("POSTGRES_HOST","localhost"),"PORT":os.getenv("POSTGRES_PORT","5432")}}
if os.getenv("DATABASE_URL"):
    import dj_database_url
    DATABASES={"default":dj_database_url.parse(os.environ["DATABASE_URL"],conn_max_age=600)}
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE="en-us"; TIME_ZONE="Asia/Kolkata"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATIC_ROOT=BASE_DIR/"staticfiles"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS=[x.strip() for x in os.getenv("CORS_ALLOWED_ORIGINS","http://localhost:5173").split(",") if x.strip()]
CSRF_TRUSTED_ORIGINS=[x.strip() for x in os.getenv("CSRF_TRUSTED_ORIGINS","").split(",") if x.strip()]
if not DEBUG:
    SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")
    SECURE_SSL_REDIRECT=os.getenv("SECURE_SSL_REDIRECT","True").lower()=="true"
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
    SECURE_HSTS_SECONDS=int(os.getenv("SECURE_HSTS_SECONDS","31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS=True
    SECURE_HSTS_PRELOAD=True
REST_FRAMEWORK={"DEFAULT_PERMISSION_CLASSES":["rest_framework.permissions.AllowAny"],"DEFAULT_AUTHENTICATION_CLASSES":["rest_framework.authentication.SessionAuthentication"],"DEFAULT_THROTTLE_CLASSES":["rest_framework.throttling.AnonRateThrottle","rest_framework.throttling.UserRateThrottle"],"DEFAULT_THROTTLE_RATES":{"anon":"30/min","user":"120/min"}}
