[README.md](https://github.com/user-attachments/files/21904774/README.md)
# 📝 Mi API de Tareas - Semana 3

## ¿Qué hice?
Creé una API super práctica para organizar mis tareas usando FastAPI. Ahora puedo guardar, ver, actualizar y eliminar mis pendientes fácilmente.

## Características que implementé

### Validaciones
- Los títulos no pueden estar vacíos o ser solo espacios
- La prioridad va del 1 al 5
- Las descripciones son opcionales pero si las pongo, tienen límite de 500 caracteres
- No se pueden repetir títulos

### Manejo de errores
- Si busco una tarea que no existe → Error 404 "No encontrado"
- Si pongo prioridad incorrecta → Error 400 "Datos inválidos"
- Si hay error del servidor → Error 500 con mensaje claro

### Cosas útiles extras
- Cada tarea tiene ID único, no se pueden repetir
- Fechas automáticas de creación y última actualización
- Filtros para ver solo tareas completadas o por prioridad
- Documentación automática en /docs

## Endpoints que funcionan

| Método | URL | ¿Qué hace? |
|--------|-----|------------|
| `GET` | `/` | Muestra info de la API |
| `GET` | `/tareas` | Trae todas mis tareas |
| `GET` | `/tareas/{id}` | Busca una tarea específica |
| `POST` | `/tareas` | Crear nueva tarea |
| `PUT` | `/tareas/{id}` | Actualizar tarea |
| `DELETE` | `/tareas/{id}` | Eliminar tarea |

## Cómo ejecutarlo

# Instalar (si es necesario)
pip install fastapi uvicorn

# Ejecutar
uvicorn main:app --reload

# Abrir en el navegador
http://localhost:8000/docs

## Lo que aprendí haciendo esto

### Lo que me salió bien:
- FastAPI es fácil de entender y usar
- Los validadores de Pydantic sirven bastante para revisar datos
- Manejar errores hace que mi API se vea profesional
- UUIDs son mejores que números secuenciales

### Mis aprendizajes:
1. Validar temprano es mejor que arreglar después
2. Los códigos HTTP importan mucho para que el cliente sepa qué pasó
3. La documentación automática me ahorró mucho tiempo
4. Middleware suena complicado pero es útil para medir tiempos

### Dificultades que tuve:
- Al principio me confundía con los tipos de datos (UUID vs string)
- Los validadores custom requieren pensar en todos los casos posibles
- Manejar los errores específicos fue un reto al inicio

## Conclusión

Aprendí que con poco código se puede hacer una API potente y profesional. FastAPI es perfecto para proyectos personales porque:

- Documenta automáticamente → No tengo que escribir manual
- Valida todo → Menos errores tontos
- Es rápido → Perfecto para prototipos

Ahora tengo mi propio organizador de tareas y entendí cómo funcionan las APIs de verdad. Estoy listo para proyectos más grandes.

**Nota para mí:** La próxima vez agregaré usuarios y login.
