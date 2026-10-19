# 02 - Estructura Estándar de un Repositorio

La arquitectura de directorios de un repositorio debe ser autoexplicativa, predecible y uniforme a lo largo de toda una organización o portafolio de proyectos. Cualquier desarrollador o sistema de CI debe ser capaz de ubicar la configuración de linters, las pruebas, los puntos de entrada y las políticas de contribución sin requerir inducción verbal.

---

## 1. Anatomía Canónica del Repositorio

A continuación se detalla la estructura física que este kit estandariza:

```text
.
├── .editorconfig               # Configuración uniforme de formato para editores e IDEs
├── .gitattributes              # Normalización de saltos de línea (LF) y reglas de Linguist
├── .gitignore                  # Reglas exhaustivas de exclusión de binarios, SO y secretos
├── .github/                    # Automatización y gobernanza nativa de GitHub
│   ├── CODEOWNERS.example      # Matriz de responsabilidad por ruta y componente
│   ├── dependabot.yml          # Auditoría periódica y actualización de dependencias
│   ├── ISSUE_TEMPLATE/         # Formularios estructurados para issues
│   │   ├── bug_report.md       # Plantilla para reporte reproducible de errores
│   │   └── feature_request.md  # Plantilla para propuestas de arquitectura y features
│   ├── PULL_REQUEST_TEMPLATE.md# Lista de control previa a revisión de PRs
│   ├── settings.example.yml    # Especificación de protección de ramas y reglas de merge
│   └── workflows/              # Pipelines de Integración Continua (GitHub Actions)
│       └── ci.yml              # Pipeline determinista con privilegios mínimos (read-only)
├── CHECKLIST.md                # Lista de verificación imprimible de adopción del kit
├── CODE_OF_CONDUCT.md          # Código de conducta para colaboradores (Contributor Covenant)
├── CONTRIBUTING.md             # Guía técnica paso a paso para contribuir al proyecto
├── docs/                       # Documentación técnica modular y decisiones de diseño
│   ├── 01-principios.md
│   ├── 02-estructura-repo.md
│   ├── 03-branching.md
│   ├── 04-commits.md
│   ├── 05-pull-requests.md
│   ├── 06-releases.md
│   ├── 07-ci.md
│   ├── 08-seguridad.md
│   ├── 09-licencias.md
│   └── 10-adopcion.md
├── LICENSE                     # Licencia legal del software (MIT por defecto)
├── README.md                   # Portal de entrada, descripción general y guía de inicio rápido
├── scripts/                    # Scripts utilitarios y herramientas de automatización
│   ├── check-repo.sh           # Auditor estricto de cumplimiento de estándares
│   └── new-repo.sh             # Herramienta de andamiaje para nuevos repositorios
└── SECURITY.md                 # Política de reporte confidencial de vulnerabilidades
```

---

## 2. Descripción de Componentes Críticos

### Raíz del Repositorio (Root Files)
- **`README.md`**: Es la tarjeta de presentación técnica. Debe responder en los primeros 30 segundos: ¿qué problema resuelve el proyecto?, ¿cómo se instala/ejecuta?, y ¿cuál es el estado de la build?
- **`LICENSE`**: Todo repositorio público o compartido sin licencia explícita es, por defecto de copyright internacional, de uso privativo exclusivo del autor, lo que impide legalmente que terceros lo utilicen o contribuyan.
- **`CONTRIBUTING.md`**: Define el contrato entre mantenedores y colaboradores: normas de commits, flujo de ramas, requerimientos de pruebas y pasos para compilar en local.
- **`SECURITY.md`**: Canal formal para reportar fallos de seguridad sin exponer al proyecto a exploits de día cero.
- **`CHECKLIST.md`**: Matriz condensada para auditar rápidamente si un repositorio cumple los niveles Mínimo, Recomendado y Avanzado de calidad.

### Configuración del Entorno de Desarrollo
- **`.editorconfig`**: Neutraliza discrepancias entre editores (espacios vs tabuladores, final de línea CRLF vs LF, espacios sobrantes al final de línea). Respaldado nativamente por prácticamente todos los IDEs modernos.
- **`.gitattributes`**: Garantiza que los saltos de línea se conviertan a LF en Linux/macOS y Windows al momento del commit (`* text=auto eol=lf`). Evita que commits gigantescos se ensucien por diferencias invisibles de retorno de carro (`\r\n`).
- **`.gitignore`**: Evita la filtración accidental de secretos (`.env`), paquetes pesados (`node_modules/`, `target/`, `venv/`), artefactos binarios o metadatos del sistema operativo (`.DS_Store`, `Thumbs.db`).

### Directorio de Gobernanza (`.github/`)
- **`workflows/`**: Almacena los pipelines declarativos de GitHub Actions. Cada pipeline debe operar bajo el principio de menor privilegio (`permissions: contents: read`).
- **`ISSUE_TEMPLATE/`**: Filtra reportes ambiguos o incompletos, exigiendo pasos de reproducción y especificaciones concretas de entorno.
- **`PULL_REQUEST_TEMPLATE.md`**: Fuerza al autor del PR a autoevaluar su impacto antes de solicitar la atención de un revisor.
- **`dependabot.yml`**: Monitorea automáticamente vulnerabilidades de dependencias y las mantiene al día.

### Documentación Modular (`docs/`)
La documentación no debe concentrarse en un único `README.md` monolítico de miles de líneas.
- La raíz contiene el resumen ejecutivo y arranque rápido.
- El directorio `docs/` contiene guías especializadas organizadas secuencialmente con numeración prefijada (`01-...`, `02-...`), facilitando su lectura tanto en la web como en navegadores de archivos locales.

### Scripts Utilitarios (`scripts/`)
Los scripts deben ser deterministas, ejecutables (`chmod +x`), poseer encabezados bash seguros (`set -euo pipefail`) y permitir su invocación tanto en local por el desarrollador como en los pipelines de CI.

---

## 3. Invariantes de Higiene Estructural

1. **Cero archivos huérfanos o temporales**: No deben commitearse archivos `.bak`, `.tmp`, notas personales o borradores en la raíz del repositorio.
2. **Nombres de archivo predecibles**: Todo en minúsculas y separado por guiones medios para scripts y documentación (`mi-documento.md`, `mi-script.sh`), excepto los archivos estándar de GitHub que usan mayúsculas por convención histórica (`README.md`, `LICENSE`, `SECURITY.md`).
3. **Independencia de compilación**: La documentación en markdown debe ser legible directamente en GitHub y navegadores de texto, sin obligar al usuario a instalar generadores de sitios estáticos pesados (como MkDocs o Docusaurus) a menos que la escala del proyecto lo justifique formalmente.

---

## Navegación

- Anterior: [01 - Principios Fundamentales](01-principios.md)
- Siguiente: [03 - Estrategias de Ramas (Branching)](03-branching.md)
- Volver al [README principal](../README.md)
