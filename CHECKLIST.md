# Checklist de Adopción de Estándares de Repositorio

Esta lista de verificación condensada permite auditar el nivel de madurez y cumplimiento técnico de
cualquier repositorio en GitHub. Puede imprimirse o utilizarse como issue de seguimiento al migrar
repositorios existentes.

---

## Nivel 1: Mínimo Indispensable (Línea Base Legal y Estructural)

Este nivel es el requisito mínimo absoluto antes de publicar o compartir cualquier repositorio de código.

- [ ] **Licencia Válida (`LICENSE`)**: Archivo presente en la raíz; tipo de licencia elegido conscientemente
  y marcadores de posición `[YEAR]` y `[OWNER]` sustituidos.
- [ ] **Portal del Proyecto (`README.md`)**: Describe qué problema resuelve el software, cómo se instala
  en local y cómo se ejecuta en menos de 5 minutos.
- [ ] **Exclusión de Basura y Secretos (`.gitignore`)**: Reglas completas que impiden subir binarios, entornos
  virtuales, carpetas de dependencias (`node_modules/`, `target/`), logs y archivos de secretos (`.env`).
- [ ] **Normalización de Saltos de Línea (`.gitattributes`)**: Regla `* text=auto eol=lf` activa para evitar
  conflictos de fin de línea entre sistemas operativos.
- [ ] **Consistencia en Editores (`.editorconfig`)**: Configuración estandarizada de sangrías, codificación
  UTF-8 e inserción de salto de línea al final de archivo.
- [ ] **Rama Principal Canónica**: La rama por defecto se llama `main` (no `master` ni ramas divergentes).

---

## Nivel 2: Recomendado para Colaboración y Calidad (Salud del Repositorio)

Indispensable para repositorios colaborativos, equipos de ingeniería o proyectos abiertos a contribuciones externas.

- [ ] **Guía de Contribución (`CONTRIBUTING.md`)**: Pasos técnicos claros para compilar el proyecto, normas
  de estilo, convención de nombres de rama y requisitos de pruebas.
- [ ] **Política de Seguridad (`SECURITY.md`)**: Canal privado y directo para reportar vulnerabilidades sin
  abrir issues públicos de día cero.
- [ ] **Código de Conducta (`CODE_OF_CONDUCT.md`)**: Estándar de convivencia formal (Contributor Covenant) con
  canal de contacto definido para resolución de conflictos.
- [ ] **Plantillas de Incidencias (`.github/ISSUE_TEMPLATE/`)**:
  - [ ] `bug_report.md`: Exige pasos de reproducción, comportamiento esperado/real y versiones del entorno.
  - [ ] `feature_request.md`: Exige justificación de la necesidad técnica, diseño preliminar y casos de uso.
- [ ] **Plantilla de Pull Request (`.github/PULL_REQUEST_TEMPLATE.md`)**: Lista de control previa que obliga
  al autor a verificar atomicidad, pruebas y documentación antes de solicitar revisión.
- [ ] **Prohibición de Emojis en Superficies de Ejecución**: Emojis vetados en código, scripts, configs, logs,
  CI y commits; permitidos únicamente en documentación humana y notas de release
  ([Guía de Estilo](docs/11-estilo.md)).
- [ ] **Estándares Profesionales de Código**: Funciones pequeñas con responsabilidad única, eliminación de
  literales mágicos, manejo explícito de errores (*fail-loud*), cero código muerto y principio DRY con
  criterio ([Guía de Estilo](docs/11-estilo.md)).
- [ ] **Arquitectura Modular y Desacoplada**: Alta cohesión, bajo acoplamiento, dependencias unidireccionales
  sin ciclos, contratos explícitos y organización por feature o dominio
  ([Guía de Modularización](docs/12-modularizacion.md)).
- [ ] **Pipeline de CI Básico (`.github/workflows/ci.yml`)**:
  - [ ] Permisos restringidos a solo lectura (`permissions: contents: read`).
  - [ ] Auditoría de estándares y verificación automatizada de ausencia de emojis en ejecución.
  - [ ] Linteo de código/documentación automatizado.
  - [ ] Ejecución de pruebas unitarias en cada push y PR.
- [ ] **Limpieza de Ramas**: Opción de GitHub `Automatically delete head branches` activada.
- [ ] **Actualizaciones Agrupadas de Dependabot (`groups`)**: Lotes agrupados para versiones menores y parches
  en `.github/dependabot.yml`.
- [ ] **Automatización de Mantenimiento (`stale` y `labeler`)**: Gestión automatizada de inactividad y etiquetado
  por rutas con permisos mínimos en `.github/workflows/stale.yml.example` y `.github/labeler.yml.example`.
- [ ] **Hooks Locales de Git (`core.hooksPath`)**: Validación de estándares previa al commit mediante hooks
  versionados en `.githooks/`.

---

## Nivel 3: Avanzado / Producción Crítica (Gobernanza, Release y Cadena de Suministro)

Requerido para sistemas en producción, infraestructura crítica, librerías con alto tráfico o código institucional.

- [ ] **Gobernanza con Rulesets Activos (`.github/settings.example.yml`)**:
  - [ ] Ruleset aplicado a rama default (`~DEFAULT_BRANCH`) con revisiones obligatorias, status checks
    estrictos y escaneo SAST (CodeQL).
  - [ ] Ruleset de inmutabilidad de tags de release (`refs/tags/v*`) contra borrado o force-update.
  - [ ] Bypass list acotada exclusivamente a roles esenciales o equipos de emergencia sin excepciones genéricas.
- [ ] **Control de Accesos por Menor Privilegio**: Permisos base de organización restringidos (Read/None) y
  roles de repositorio asignados por función técnica mínima (Read, Triage, Write, Maintain, Admin).
- [ ] **Revisión Periódica de Accesos**: Auditoría trimestral de miembros, colaboradores externos, permisos
  de equipos y revocación de accesos huérfanos.
- [ ] **Inventario y Rotación de Deploy Keys**: Deploy keys registradas con propósito explícito (solo lectura
  preferida) y rotación inmediata ante salida de colaboradores o cambio de infraestructura.
- [ ] **Protección Estricta de Rama `main`**:
  - [ ] Prohibido el push directo (todo entra vía Pull Request).
  - [ ] Mínimo 1 aprobación humana obligatoria.
  - [ ] Status checks de CI aprobados obligatoriamente antes de autorizar el merge.
  - [ ] Historial lineal estricto (bloqueo de merge commits desordenados; uso obligatorio de Squash o Rebase).
  - [ ] Reglas aplicadas de forma estricta a administradores (`enforce_admins: true` o bypass ausente).
- [ ] **Protección de Etiquetas (`v*`)**: Regla o ruleset de tags configurado para impedir sobreescritura o borrado de versiones.
- [ ] **Detección Continua de Fuga de Secretos (`.github/workflows/gitleaks.yml`)**: Escaneo activo en CI con
  `fetch-depth: 0` en push y PRs.
- [ ] **Análisis Estático Automatizado (`.github/workflows/codeql.yml.example`)**: Escaneo semanal programado y
  en PRs con CodeQL (SARIF upload, `security-events: write`).
- [ ] **Auditoría Continua de Dependencias (`.github/dependabot.yml`)**: Actualizaciones automatizadas semanales
  de GitHub Actions y ecosistemas de paquetes.
- [ ] **Asignación de Responsabilidades (`.github/CODEOWNERS`)**: Asignación automática de revisores por ruta,
  arquitectura o componente crítico.
- [ ] **Pipeline de Release Automatizado**:
  - [ ] Implementación de variante por artefactos con SemVer dinámico
    ([`.github/workflows/release.yml.example`](.github/workflows/release.yml.example)) o Semantic-Release
    ([`.releaserc.js.example`](.releaserc.js.example)).
  - [ ] Permisos mínimos de trabajo (`contents: write`, `id-token: write`, `attestations: write`).
  - [ ] Concurrencia con `cancel-in-progress: false` para evitar publicaciones parciales.
- [ ] **Integridad Criptográfica de Artefactos**:
  - [ ] Generación automática de sumas `SHA-256`, `SHA-512` y manifiesto unificado `SHA256SUMS.txt`
    compatible con `sha256sum -c`.
  - [ ] Atestación de procedencia de compilación Sigstore / in-toto (`actions/attest-build-provenance`).
- [ ] **Aislamiento Estricto de Firmas**:
  - [ ] Secretos de producción (`KEYSTORE_*`, `GPG_*`) restringidos a ramas protegidas / ambientes aprobados.
  - [ ] Pruebas de compilación en PRs ejecutadas con claves efímeras descartables generadas con `keytool`.
- [ ] **Commits Criptográficamente Firmados**: Configuración de firmas SSH/GPG para autores en producción (*Verified Commits*).

---

## Matriz Rápida de Evaluación

| Nivel Alcanzado | Estado del Repositorio | Calificación |
| :--- | :--- | :--- |
| **0 / 3** | Repositorio improvisado, sin garantías legales ni técnicas | Crítico / Inseguro |
| **Nivel 1 Completo** | Base legal y estructural mínima cubierta | Aceptable (Personal) |
| **Nivel 2 Completo** | Repositorio profesional apto para equipos y colaboración | Profesional / Saludable |
| **Nivel 3 Completo** | Estándar de ingeniería y cadena de suministro blindado | Blindado / Enterprise |
