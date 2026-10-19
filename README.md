# Kit de Estándares de Repositorio y Buenas Prácticas de Git

Plantilla de ingeniería, gobernanza, automatización y cadena de suministro para establecer un estándar homogéneo, profesional y listo para producción en cualquier repositorio de GitHub.

Este kit unifica la estructura de archivos, políticas de seguridad, convenciones de commits, plantillas de colaboración, auditorías deterministas, flujos de trabajo de CI, pipelines de release, checksums, firmas criptográficas y escaneo continuo de vulnerabilidades sin requerir dependencias complejas ni herramientas externas.

---

## 🗺️ Mapa del Kit

```text
.
├── 📄 Licencias y Gobernanza
│   ├── LICENSE                       # Licencia MIT base con placeholders
│   ├── CODE_OF_CONDUCT.md            # Código de conducta (Contributor Covenant v2.1)
│   ├── SECURITY.md                   # Política de divulgación responsable de vulnerabilidades
│   ├── CONTRIBUTING.md               # Guía técnica de contribución para desarrolladores
│   └── CHECKLIST.md                  # Lista de control imprimible (Base / Colaboración / Release)
│
├── ⚙️ Configuración del Entorno
│   ├── .editorconfig                 # Reglas consistentes de indentación, UTF-8 y finales de línea
│   ├── .gitattributes                # Normalización forzada a LF y metadatos de linguist
│   ├── .gitignore                    # Plantilla políglota comentada (OS, IDEs, secretos, lenguajes)
│   └── .releaserc.js.example         # Configuración genérica para Semantic-Release y Conventional Commits
│
├── 🤖 Automatización y GitHub (.github/)
│   ├── workflows/ci.yml              # CI determinista con permisos mínimos de solo lectura
│   ├── workflows/release.yml.example # Pipeline de release automatizado con SemVer, artefactos y checksums
│   ├── workflows/gitleaks.yml        # Escaneo continuo de fuga de secretos con historial completo
│   ├── workflows/codeql.yml.example  # Análisis estático de vulnerabilidades (SAST) programado
│   ├── dependabot.yml                # Actualización periódica automatizada de dependencias
│   ├── ISSUE_TEMPLATE/               # Plantillas estructuradas de incidencias
│   │   ├── bug_report.md             # Reporte reproducible de errores y diagnóstico de entorno
│   │   └── feature_request.md        # Propuestas de funcionalidades y diseño arquitectónico
│   ├── PULL_REQUEST_TEMPLATE.md      # Lista de verificación previa para autores de PRs
│   ├── CODEOWNERS.example            # Asignación de revisores por ruta o subsistema
│   └── settings.example.yml          # Especificación de protección de ramas y políticas de merge
│
├── 🛠️ Scripts Utilitarios (scripts/)
│   ├── check-repo.sh                 # Auditor de conformidad de estándares (código de salida 0/1)
│   └── new-repo.sh                   # Instalador automatizado para repositorios nuevos o existentes
│
└── 📚 Documentación Técnica (docs/)
    ├── 01-principios.md              # Principios de ingeniería, inmutabilidad y disciplina de alcance
    ├── 02-estructura-repo.md         # Anatomía y responsabilidades de directorios y archivos
    ├── 03-branching.md               # Estrategia de ramas (Trunk-Based / GitHub Flow)
    ├── 04-commits.md                 # Conventional Commits v1.0.0 y atomicidad estricta
    ├── 05-pull-requests.md           # Flujo de PRs, auto-revisión y estrategias de merge
    ├── 06-releases.md                # SemVer, estrategias de release, firmas, checksums y atestaciones
    ├── 07-ci.md                      # Principios de seguridad en CI, permisos por job y concurrencia
    ├── 08-seguridad.md               # Detección de secretos (Gitleaks), CodeQL y modelo de firmas en PRs
    ├── 09-licencias.md               # Guía para la elección y aplicación de licencias open source
    ├── 10-adopcion.md                # Modelo de adopción por niveles (Tiers) y migración en 5 fases
    ├── 11-estilo.md                  # Convenciones de estilo, prohibición de emojis y código limpio
    └── 12-modularizacion.md          # Arquitectura de componentes, límites y desacoplamiento
```

---

## ⏱️ Guía de Adopción en 10 Minutos

### 1. Auditar el Repositorio Actual
Para verificar qué archivos o estándares faltan en un proyecto:

```bash
./scripts/check-repo.sh /ruta/al/proyecto
```

### 2. Inyectar el Kit en el Proyecto
Para aplicar el kit completo sustituyendo marcadores de posición de forma automática:

```bash
./scripts/new-repo.sh \
  --owner "Nombre del Propietario u Organización" \
  --email "seguridad@ejemplo.com" \
  --year "2026" \
  /ruta/al/proyecto
```

> [!NOTE]
> `new-repo.sh` respeta archivos preexistentes por defecto. Si el proyecto destino ya posee un `README.md` o `.gitignore`, el script lo omitirá para no destruir su contenido. Para forzar el reemplazo completo, use `--force`.

### 3. Personalizar Dependencias y Código
1. Edite `.github/dependabot.yml` y descomente los ecosistemas correspondientes a su stack (npm, pip, cargo, gomod, docker).
2. Si el repositorio contenía archivos con saltos de línea mezclados (CRLF/LF), normalice el historial en un commit dedicado:
   ```bash
   git add --renormalize .
   git commit -m "style: normalize line endings to LF according to .gitattributes"
   ```
3. Si requiere releases automatizados, adapte `.github/workflows/release.yml.example` o `.releaserc.js.example` según su ecosistema de empaquetado.

### 4. Activar Protección de Ramas y Secretos en GitHub
Siga las especificaciones documentadas en [`.github/settings.example.yml`](.github/settings.example.yml) o en la [Guía de Ramas](docs/03-branching.md) para bloquear pushes directos a `main`, exigir revisiones de código, activar el escaneo de secretos y requerir que los checks de CI pasen de forma obligatoria.

---

## 📖 Índice de Documentación Detallada

1. [**Principios de Ingeniería y VCS**](docs/01-principios.md): Inmutabilidad, reproducibilidad y disciplina de alcance.
2. [**Estructura Estándar**](docs/02-estructura-repo.md): Anatomía física y lógica de directorios.
3. [**Estrategias de Ramas**](docs/03-branching.md): Trunk-Based Development, nomenclaturas y branch protection.
4. [**Commits y Atomicidad**](docs/04-commits.md): Conventional Commits v1.0.0, formato de mensajes y cortes verticales.
5. [**Pull Requests y Revisiones**](docs/05-pull-requests.md): Proceso de auto-revisión, revisión por pares y políticas de merge.
6. [**Versiones, Lanzamientos y Cadena de Suministro**](docs/06-releases.md): SemVer 2.0.0, estrategias de release, firmas, checksums y atestaciones Sigstore.
7. [**Integración Continua (CI)**](docs/07-ci.md): Principio de menor privilegio, permisos granulares por job y políticas de concurrencia.
8. [**Seguridad y Vulnerabilidades**](docs/08-seguridad.md): Detección de secretos con Gitleaks, análisis con CodeQL y firmas descartables en PRs.
9. [**Guía de Licencias**](docs/09-licencias.md): Clasificación de licencias (MIT, Apache, GPL, AGPL) y propiedad intelectual.
10. [**Guía de Adopción e Integración**](docs/10-adopcion.md): Modelo de adopción por niveles (Tiers) y migración metódica en 5 fases.
11. [**Estilo y Estándares Profesionales**](docs/11-estilo.md): Prohibición de emojis en ejecución, convenciones de nombres, funciones pequeñas y fail-loud.
12. [**Modularización y Arquitectura**](docs/12-modularizacion.md): Responsabilidad única por módulo, contratos desacoplados, dependencias acíclicas y organización por feature.

---

## 🛠️ Herramientas de Verificación Incluidas

- **`./scripts/check-repo.sh`**: Evalúa la presencia, tamaño y consistencia de todos los componentes del kit. Retorna código de salida `0` si todos los requisitos se cumplen o `1` si detecta omisiones críticas. Ideal para incluirse como paso obligatorio en pipelines de CI.
- **`./scripts/new-repo.sh`**: Inicializa nuevos repositorios o actualiza proyectos existentes con reemplazo configurable de variables de entorno y metadatos.
