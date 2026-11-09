# Laboratorio: Lenguajes de Programación con Aspectos de Seguridad (LAS)

## Datos del Estudiante
* **Nombre:** Fernando Ariel Montoya Hernández
* **Carrera:** Técnico Superior Universitario en Ciberseguridad
* **Institución:** Escuela Superior de Innovación y Tecnología (ESIT)
* **Módulo:** Lenguajes de Programación con Aspectos de Seguridad

---

## 1. Descripción del Proyecto
Implementación de un sistema web seguro en Flask integrado con base de datos SQLite para la gestión de credenciales, autenticación robusta y mitigación de ataques por fuerza bruta mediante monitoreo activo y cálculo de métricas MTTD/MTTR.

### Mecanismos de Seguridad Implementados
* **Validación de entradas:** Requisitos estrictos de longitud y formato en registro y login.
* **Almacenamiento seguro:** Hashing criptográfico de contraseñas mediante `werkzeug.security` (Scrypt/PBKDF2) sin persistencia de texto plano.
* **Mitigación de SQL Injection:** Consultas parametrizadas en SQLite (`?`).
* **Trazabilidad y auditoría:** Registro de eventos de autenticación con marcas de tiempo en `eventos.log`.

---

## 2. Estructura del Repositorio
```text
lab-las/
├── app.py                 # Servidor web Flask y rutas de autenticación
├── crearDB.py             # Script de inicialización de la base de datos
├── detector.py            # Analizador de logs, contención y cálculo MTTD/MTTR
├── usuarios.db            # Base de datos SQLite
├── eventos.log            # Registro de auditoría de intentos de inicio de sesión
├── respuesta.log          # Registro de acciones defensivas ejecutadas
├── templates/
│   ├── login.html         # Formulario de autenticación
│   └── registro.html      # Formulario de alta de credenciales
└── README.md              # Documentación técnica del laboratorio