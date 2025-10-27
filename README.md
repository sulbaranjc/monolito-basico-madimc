# 🏥 MEDIMIC - Sistema de Gestión Médica de IMC

## 📋 Descripción del Proyecto

**MEDIMIC** es un sistema monolítico educativo para la gestión de pacientes y cálculo de Índice de Masa Corporal (IMC), desarrollado con **FastAPI** y **Jinja2**. Este proyecto está diseñado como una herramienta de aprendizaje que demuestra las mejores prácticas de desarrollo web moderno, arquitectura de componentes y diseño responsivo.

### 🎯 Objetivos Educativos

- **Arquitectura Monolítica**: Comprensión de aplicaciones web completas en un solo repositorio
- **Patrones de Diseño**: Implementación de MVC, componentes reutilizables y separación de responsabilidades
- **CSS Moderno**: Flexbox, CSS Grid, responsive design y metodologías de organización
- **Validación de Datos**: Pydantic para validación robusta del lado servidor
- **UX/UI Moderno**: Modales personalizados, animaciones y accesibilidad

## 🏗️ Arquitectura del Sistema

### 📂 Estructura del Proyecto

```
medimic/
├── app/                          # 🐍 Aplicación principal
│   ├── main.py                   # 🚀 Punto de entrada FastAPI
│   ├── models/                   # 📊 Modelos de datos Pydantic
│   │   └── patient.py           # 👤 Modelo de paciente con validaciones
│   ├── routers/                  # 🛤️ Rutas organizadas por módulos
│   │   └── patients.py          # 🏥 CRUD completo de pacientes
│   ├── data/                     # 💾 Datos seed y persistencia
│   │   └── patients_seed.py     # 🌱 Datos de ejemplo para desarrollo
│   ├── templates/                # 🎨 Templates Jinja2
│   │   ├── patients_list.html   # 📋 Vista de listado
│   │   ├── patients_create.html # ➕ Vista de creación
│   │   ├── patients_edit.html   # ✏️ Vista de edición
│   │   └── components/          # 🧩 Componentes reutilizables
│   │       ├── header.html      # 🔝 Cabecera común
│   │       └── footer.html      # 🔻 Pie de página común
│   └── static/                   # 📁 Recursos estáticos
│       ├── css/                  # 🎨 Hojas de estilo
│       │   ├── main.css         # 🏠 Estilos globales
│       │   ├── main_commented.css # 📖 Versión educativa comentada
│       │   ├── patients_list.css # 📋 Estilos específicos de listado
│       │   └── patients_create.css # 📝 Estilos específicos de formularios
│       ├── js/                   # ⚡ Scripts JavaScript
│       │   ├── patients_list.js # 🗑️ Modal de confirmación personalizado
│       │   ├── patients_edit.js # ✏️ Funcionalidades de edición
│       │   └── patients_create.js # ➕ Validación en tiempo real
│       └── img/                  # 🖼️ Imágenes y logos
├── requirements.txt              # 📦 Dependencias Python
├── CSS_GUIDE.md                 # 📚 Guía educativa de CSS
└── .vscode/                     # ⚙️ Configuración de desarrollo
    └── settings.json            # 🔧 Prettier y formateo automático
```

## 🚀 Tecnologías Implementadas

### 🐍 Backend (Python)

- **[FastAPI 0.120.0](https://fastapi.tiangolo.com/)**: Framework web moderno y rápido
- **[Pydantic](https://pydantic.dev/)**: Validación de datos con Python types
- **[Jinja2](https://jinja.palletsprojects.com/)**: Motor de templates para renderizado server-side
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI de alta performance

### 🎨 Frontend

- **HTML5 Semántico**: Estructura accesible y SEO-friendly
- **CSS3 Moderno**: Flexbox, CSS Grid, Custom Properties
- **JavaScript Vanilla**: Sin frameworks, enfoque en fundamentos
- **Responsive Design**: Mobile-first approach

### 🛠️ Herramientas de Desarrollo

- **[Prettier](https://prettier.io/)**: Formateo automático de código
- **VS Code**: Configuración optimizada para desarrollo
- **Cache-busting**: Estrategias para desarrollo sin caché

### 📊 Dependencias Extendidas

El proyecto incluye un stack completo de librerías para funcionalidades avanzadas:

- **Científicas**: `numpy`, `pandas`, `torch` (preparado para ML/AI)
- **Datos**: `mysql-connector-python`, `openpyxl` (persistencia y export)
- **Validación**: `email-validator`, `python-multipart`
- **Audio/AI**: `openai-whisper` (preparado para funcionalidades de voz)

## 📊 Modelo de Datos

### 👤 Entidad Paciente

```python
class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=60)
    last_name: str = Field(..., min_length=1, max_length=60)
    date_of_birth: date
    sex_at_birth: Literal["Masculino", "Femenino", "Otro"]
    gender_identity: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^[0-9+\-() ]{7,20}$")
    notes: Optional[str] = Field(None, max_length=500)
    consent_data_processing: bool = True
```

### 🧮 Cálculos Automáticos

- **IMC**: Peso (kg) / (Altura (m))²
- **Categoría IMC**: Bajo peso, Normal, Sobrepeso, Obesidad
- **Edad**: Calculada automáticamente desde fecha de nacimiento
- **Datos Computados**: Nombre completo, estado adulto, contactabilidad

## 🎨 Sistema de Diseño CSS

### 🏗️ Arquitectura CSS Modular

1. **`main.css`** - Estilos globales y componentes base
2. **`patients_list.css`** - Estilos específicos para tablas
3. **`patients_create.css`** - Sistema de formularios
4. **`main_commented.css`** - Versión educativa con documentación

### 🎭 Patrones de Diseño Implementados

#### 🔄 Sticky Footer Pattern

```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main {
  flex: 1 0 auto;
}
.site-footer {
  margin-top: auto;
}
```

#### 📊 CSS Grid para Formularios

```css
.grid-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
@media (max-width: 820px) {
  .grid-form {
    grid-template-columns: 1fr;
  }
}
```

#### 🎨 Sistema de Botones Semánticos

- **`.btn-primary`**: Acciones principales (azul)
- **`.btn-secondary`**: Acciones secundarias (gris)
- **`.btn-danger`**: Acciones destructivas (rojo)

### 📱 Responsive Design

- **Breakpoint principal**: 820px
- **Mobile-first approach**
- **Flexbox** para componentes unidimensionales
- **CSS Grid** para layouts bidimensionales

## ⚡ Funcionalidades JavaScript

### 🗑️ Sistema de Modal Personalizado

Reemplaza `window.confirm()` nativo con un modal elegante:

```javascript
function confirmDelete(formEl) {
  const name = formEl?.dataset?.displayName || "este paciente";
  const modal = createDeleteModal(name);
  // ... implementación completa con animaciones y accesibilidad
}
```

**Características**:

- Animaciones CSS con transiciones suaves
- Múltiples formas de cerrar (click overlay, ESC, botones)
- Accesibilidad con focus management
- Escape HTML para seguridad

### 🔧 Cache-busting Dinámico

```javascript
// Carga JS con timestamp para evitar caché en desarrollo
const s = document.createElement("script");
s.src =
  "{{ url_for('static', path='js/patients_list.js') }}" + "?v=" + Date.now();
```

## 🏥 Funcionalidades del Sistema

### 📋 Gestión de Pacientes (CRUD Completo)

#### ➕ **Crear Paciente**

- Formulario con validación server-side
- Campos obligatorios y opcionales
- Validación de email y teléfono con regex
- Cálculo automático de IMC
- Consentimiento para tratamiento de datos

#### 📊 **Listar Pacientes**

- Tabla responsive con datos esenciales
- Ordenamiento alfabético por apellido
- Display de IMC y categoría
- Botones de acción (Modificar/Eliminar)
- Estados para datos faltantes (valores "—")

#### ✏️ **Editar Paciente**

- Pre-carga de datos existentes
- Recálculo de IMC al modificar peso/altura
- Mantenimiento del estado de consentimiento
- Validación consistente con creación

#### 🗑️ **Eliminar Paciente**

- Modal de confirmación personalizado
- Prevención de eliminación accidental
- Feedback visual claro
- Acciones irreversibles claramente marcadas

### 🧮 Cálculo de IMC

#### Fórmulas Implementadas

```python
def _calc_bmi(weight_kg: float, height_cm: float) -> float:
    h = height_cm / 100.0
    return round(weight_kg / (h * h), 2)

def _bmi_category(bmi: float) -> str:
    if bmi < 18.5: return "bajo peso"
    if bmi < 25.0: return "normal"
    if bmi < 30.0: return "sobrepeso"
    return "obesidad"
```

#### Características

- Cálculo automático al crear/editar
- Categorización según estándares OMS
- Timestamp de última medición
- Manejo de casos sin datos suficientes

### ✅ Sistema de Validación

#### Server-side (Pydantic)

- Validación de tipos de datos
- Longitud de campos
- Formato de email
- Patrón de teléfono
- Fechas válidas

#### Traducción de Mensajes

```python
traducciones = {
    "String should have at least 1 character": "El texto debe tener al menos 1 carácter.",
    "Input should be a valid email address": "Debe ingresar un correo electrónico válido.",
    # ... más traducciones
}
```

## 🛠️ Instalación y Configuración

### 📋 Prerrequisitos

- **Python 3.9+**
- **pip** (gestor de paquetes Python)
- **Git** (opcional, para clonar el repositorio)

### 🚀 Instalación Paso a Paso

1. **Clonar el repositorio**:

```bash
git clone <repository-url>
cd monolito-basico-medimc
```

2. **Crear entorno virtual**:

```bash
python -m venv .venv
```

3. **Activar entorno virtual**:

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

### ▶️ Ejecución del Proyecto

#### Desarrollo

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 🌐 Acceso a la Aplicación

- **URL principal**: http://127.0.0.1:8000
- **Lista de pacientes**: http://127.0.0.1:8000/patients
- **Crear paciente**: http://127.0.0.1:8000/patients/create
- **API Docs**: http://127.0.0.1:8000/docs (Swagger UI automático)
- **Health Check**: http://127.0.0.1:8000/health

## 👥 Uso del Sistema

### 📋 Flujo de Trabajo Típico

1. **Acceder al sistema** → Redirección automática a lista de pacientes
2. **Ver pacientes existentes** → 3 pacientes seed precargados
3. **Crear nuevo paciente** → Formulario con validación
4. **Editar datos** → Modificación con recálculo de IMC
5. **Eliminar paciente** → Confirmación con modal personalizado

### 🎯 Casos de Uso Específicos

#### ➕ Registro de Paciente Nuevo

1. Click en "Agregar paciente"
2. Llenar campos obligatorios (nombre, apellido, fecha nacimiento, sexo, peso, altura)
3. Campos opcionales (email, teléfono, notas)
4. Aceptar consentimiento de datos
5. Sistema calcula IMC automáticamente
6. Redirección a lista actualizada

#### 📊 Consulta de IMC

- El sistema muestra IMC calculado en la tabla
- Categoría automática (bajo peso/normal/sobrepeso/obesidad)
- Timestamp de última medición
- Valores "—" para datos incompletos

#### ✏️ Actualización de Datos

1. Click en "Modificar" en la fila del paciente
2. Formulario pre-poblado con datos actuales
3. Modificar campos necesarios
4. Sistema recalcula IMC si cambia peso/altura
5. Validación y guardado

## 📚 Recursos Educativos

### 📖 Documentación Incluida

- **`CSS_GUIDE.md`**: Guía completa del sistema CSS con ejercicios
- **`main_commented.css`**: CSS educativo con comentarios detallados
- **Código comentado**: Explicaciones técnicas en cada archivo

### 🎓 Conceptos Enseñados

#### 🎨 Frontend

- **Flexbox vs CSS Grid**: Cuándo usar cada uno
- **Responsive Design**: Mobile-first con breakpoints estratégicos
- **Accesibilidad**: Focus states, ARIA, navegación por teclado
- **Animaciones CSS**: Transiciones suaves y micro-interacciones

#### 🐍 Backend

- **FastAPI**: Decoradores, dependencias, validación automática
- **Pydantic**: Modelos de datos, validación, serialización
- **Jinja2**: Templates, herencia, componentes
- **Arquitectura**: Separación de responsabilidades, modularidad

#### 📊 Patrones de Diseño

- **MVC**: Modelo-Vista-Controlador en web apps
- **Component Architecture**: Reutilización y mantenibilidad
- **Form Handling**: Validación, estado, UX
- **State Management**: Persistencia en memoria, ciclo de vida

## 🔧 Configuración de Desarrollo

### 🎨 Prettier (Formateo Automático)

Configuración en `.prettierrc`:

```json
{
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": false,
  "printWidth": 80,
  "overrides": [
    {
      "files": "*.css",
      "options": { "printWidth": 100 }
    }
  ]
}
```

### ⚙️ VS Code

Settings en `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[css]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### 🔄 Cache-busting para Desarrollo

- CSS: `?v={{ range(1000000) | random }}`
- JS: Timestamp dinámico con `Date.now()`

## 🎯 Ejercicios Sugeridos

### 🔰 Nivel Básico

1. **Modificar colores del sistema**:

   - Cambiar la paleta de colores corporativa
   - Crear un tema dark mode

2. **Agregar campos al modelo**:

   - Campo "dirección"
   - Campo "número de historia clínica"

3. **Mejorar validaciones**:
   - Validar que la fecha de nacimiento no sea futura
   - Agregar validación de peso/altura mínimos

### 🔵 Nivel Intermedio

1. **Implementar búsqueda**:

   - Buscador por nombre o email
   - Filtros por categoría de IMC

2. **Agregar exportación**:

   - Export a CSV
   - Report de estadísticas

3. **Mejorar UX**:
   - Loading states
   - Notificaciones toast
   - Breadcrumbs

### 🔴 Nivel Avanzado

1. **Persistencia real**:

   - Integrar base de datos SQLite
   - Migrations con Alembic

2. **API REST completa**:

   - Endpoints JSON separados
   - Documentación OpenAPI extendida

3. **Funcionalidades avanzadas**:
   - Histórico de IMC con gráficos
   - Sistema de usuarios y autenticación
   - Upload de imágenes/documentos

## 🤝 Contribución

### 📝 Guías de Estilo

- **Python**: Seguir PEP 8
- **HTML**: Semántico y accesible
- **CSS**: Metodología BEM-inspired
- **JavaScript**: ESLint standard

### 🔀 Flujo de Desarrollo

1. Fork del repositorio
2. Crear branch feature/bugfix
3. Implementar cambios con tests
4. Documentar nuevas funcionalidades
5. Pull request con descripción detallada

## 📄 Licencia

Este proyecto está diseñado con fines educativos. Consultar con el instructor para uso comercial.

## 👨‍🏫 Autor

**Ing. Juan Carlos Sulbaran**  
_Monolito FastAPI + Jinja2 — MVP educativo_

---

## 🔗 Enlaces Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic.dev/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

---

_📚 Este README es parte del sistema educativo y se actualiza continuamente con mejoras pedagógicas._
