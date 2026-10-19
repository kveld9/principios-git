# 10 - Guía de Adopción e Integración en Repositorios Existentes

Adoptar estándares en un proyecto en blanco es directo; el verdadero desafío de ingeniería radica en estandarizar
repositorios en producción activos que carecen de `.github/`, `CONTRIBUTING.md` o pipelines automatizados de
release y seguridad sin interrumpir las operaciones del equipo ni provocar fricción innecesaria.

Este documento proporciona una guía metódica para integrar este kit en cualquier repositorio existente a
través de **niveles de madurez (tiers)** y un **plan de ejecución en 5 fases**.

---

## 1. Modelo de Adopción por Niveles (Tiers)

Para facilitar la adopción progresiva sin sobrecargar a los equipos, el kit se estructura en tres niveles técnicos acumulativos:

```text
Nivel 1: Línea Base        ──► Nivel 2: Colaboración y CI ──► Nivel 3: Release & Supply-Chain
(Legal, Git y Formato)         (Salud, Templates y Tests)     (SemVer, Gitleaks, Checksums)
```

| Nivel | Enfoque Principal | Componentes Involucrados |
| :--- | :--- | :--- |
| **Tier 1: Base Estructural** | Garantías legales, higiene básica y consistencia de Git. | `LICENSE`, `README.md`, `.gitignore`, `.gitattributes`, `.editorconfig`. |
| **Tier 2: Colaboración y Calidad** | Protocolos de equipo, plantillas de reporte y CI básico. | `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, plantillas `.github/ISSUE_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md`, `.github/workflows/ci.yml`. |
| **Tier 3: Release y Cadena de Suministro** | Automatización de versiones, atestaciones, detección de secretos y análisis estático. | `.github/workflows/release.yml.example`, `.releaserc.js.example`, `.github/workflows/gitleaks.yml`, `.github/workflows/codeql.yml.example`, checksums `SHA256SUMS.txt`, firmas aisladas. |

---

## 2. Plan de Migración en 5 Fases

```text
Fase 1: Diagnóstico  ──► Fase 2: Andamiaje  ──► Fase 3: Personalización ──► Fase 4: Normalización ──► Fase 5: Protección y Release
   (Auditoría)           (Inyección Kit)           (Ajustes y Tiers)            (.gitattributes)            (Branch Rules y CI)
```

---

## 3. Fase 1: Diagnóstico del Repositorio Destino

Antes de modificar el repositorio existente, ejecute el script de auditoría provisto por el kit apuntando
al directorio de dicho repositorio:

```bash
# Ejecutar auditoría sobre el repositorio destino
./scripts/check-repo.sh /ruta/al/repo-destino
```

El script listará detalladamente los archivos faltantes o vacíos organizados por categorías:

- Metadatos y licencias (`README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CHECKLIST.md`).
- Configuración de entorno (`.editorconfig`, `.gitattributes`, `.gitignore`, `.releaserc.js.example`).
- Gobernanza y CI (`.github/workflows/ci.yml`, `release.yml.example`, `gitleaks.yml`, `codeql.yml.example`,
  `dependabot.yml`, plantillas).

---

## 4. Fase 2: Inyección No Destructiva del Kit

Utilice el script `scripts/new-repo.sh` para copiar la infraestructura del kit hacia el repositorio destino.
Por defecto, este comando **no sobreescribe** archivos que ya existan en el destino:

```bash
./scripts/new-repo.sh \
  --owner "MiOrganizacion" \
  --email "seguridad@miorganizacion.com" \
  --year "2026" \
  /ruta/al/repo-destino
```

Si el repositorio destino ya posee un archivo (por ejemplo un `README.md` con contenido del proyecto o un
`.gitignore` previo), el instalador omitirá su sobreescritura y emitirá un aviso `[SKIP]`.

---

## 5. Fase 3: Personalización por Tiers y Placeholders

Revise manualmente los siguientes puntos en el repositorio destino según el nivel de madurez deseado:

### Nivel 1 y 2: Gobernanza y Colaboración

1. **`LICENSE`**: Si el proyecto no tenía licencia, el script inyectará la licencia MIT con el año y
   propietario configurados. Si ya existía otra licencia, asegúrese de conservarla.
2. **`SECURITY.md`**: Confirme que la dirección de correo electrónico o el enlace de contacto para
   reportar vulnerabilidades sea funcional.
3. **`CODE_OF_CONDUCT.md`**: Verifique que el correo de contacto para incidentes de convivencia coincida
   con el canal designado por el proyecto.
4. **`.github/dependabot.yml`**: Descomente el ecosistema de paquetes correspondiente al stack del proyecto
   (Node, Python, Go, Rust, Docker, etc.).
5. **`.github/CODEOWNERS.example`**: Renómbrelo a `.github/CODEOWNERS` y asigne los equipos o usuarios
   responsables de cada subdirectorio del repositorio.

### Nivel 3: Release, Seguridad y Cadena de Suministro

1. **Secret Scanning Activo**: El archivo `.github/workflows/gitleaks.yml` queda inmediatamente activo
   para escanear push a `main`/`dev` y PRs.
2. **Estrategia de Release**:
   - Si genera artefactos compilados (binarios, APKs, bundles): renombre `.github/workflows/release.yml.example`
     a `release.yml` y configure las variables de entorno iniciales (`ARTIFACT_GLOB`, `ASSET_PREFIX`, `BUILD_CMD`).
   - Si distribuye paquetes mediante conventional commits: active `.releaserc.js.example` como `.releaserc.js`.
3. **Análisis Estático (CodeQL)**: Renombre `.github/workflows/codeql.yml.example` a `codeql.yml` y
   ajuste la matriz de lenguajes (`matrix.include`) según el stack del proyecto.
4. **Secretos de Firma**: En caso de requerir firma de paquetes, configure los secretos en
   **Settings -> Secrets and variables -> Actions** (`KEYSTORE_*`, `GPG_*`) y verifique que las pruebas en
   PRs utilicen claves efímeras descartables.

---

## 6. Fase 4: Normalización de Git y Saltos de Línea

Si el repositorio previo tenía archivos con saltos de línea mixtos (CRLF en Windows y LF en Linux),
la incorporación de `.gitattributes` podría generar cambios de línea no deseados en futuros commits.

Para normalizar todo el repositorio de una sola vez en un commit dedicado:

```bash
cd /ruta/al/repo-destino

# Forzar a Git a re-evaluar todos los archivos según .gitattributes
git add --renormalize .

# Crear un commit exclusivo de normalización
git commit -m "style: normalize line endings to LF according to .gitattributes"
```

> [!IMPORTANT]
> Realice este paso en un commit separado e independiente de cualquier cambio funcional o de código.
> Esto mantiene limpia la historia de `git blame`.

---

## 7. Fase 5: Configuración de Protección en GitHub

Una vez que el Pull Request de adopción del kit sea fusionado en la rama principal (`main`), configure
las protecciones formales:

1. Ingrese a **Settings -> Branches** en el repositorio en GitHub.
2. Agregue una regla de protección para `main`:
   - [x] **Require a pull request before merging** (1 aprobación requerida).
   - [x] **Require status checks to pass before merging** (seleccionar los checks de `CI` y `Secret Scanning`).
   - [x] **Require linear history** (favorece Squash & Merge).
   - [x] **Do not allow bypassing the above settings** (aplica también a administradores).
3. En **Settings -> Tags**:
   - [x] Crear regla de protección para `v*` restringiendo la creación a mantenedores y GitHub Actions.
4. En **Settings -> General -> Pull Requests**:
   - [x] Permitir solo **Allow squash merging** (o Rebase).
   - [x] Marcar **Automatically delete head branches**.

---

## 8. Verificación Final de Adopción

Ejecute nuevamente la auditoría para certificar el cumplimiento:

```bash
./scripts/check-repo.sh /ruta/al/repo-destino
```

Si el resultado reporta `Result: PASSED`, el repositorio cuenta formalmente con un estándar de ingeniería
de primer nivel que abarca desde la higiene de código hasta la publicación segura de artefactos.

---

## 9. Caso Práctico y Dogfooding en Este Repositorio

Este repositorio aplica su propio kit de estándares de forma integral (*dogfooding*):

- **Visibilidad pública**: Configurado como repositorio público en GitHub para habilitar las capacidades
  completas de Repository Rulesets y protecciones avanzadas sin restricciones de plan.
- **`CODEOWNERS` real**: Posee un archivo `.github/CODEOWNERS` activo (`* @kveld9`) que define la propiedad
  técnica directa del repositorio, mientras que `scripts/new-repo.sh` sustituye automáticamente dicho handle
  por el propietario adoptante al instanciar nuevos proyectos.
- **`CHANGELOG.md` activo**: Mantiene un registro de cambios histórico estructurado bajo el estándar
  *Keep a Changelog* y versionado semántico (SemVer).
- **Ruleset mínimo aplicado**: Implementa un subconjunto pragmático de las especificaciones descritas en
  [`.github/settings.example.yml`](../.github/settings.example.yml). Al tratarse de un repositorio unipersonal
  con autor único, el ruleset activo prioriza la inmutabilidad de tags (`refs/tags/v*`), la linealidad del
  historial y la ejecución de checks de CI/Gitleaks, permitiendo pushes directos a la rama principal sin exigir
  la apertura de Pull Requests obligatorios para cada cambio.

---

## Navegación

- Anterior: [09 - Guía de Licencias de Software](09-licencias.md)
- Siguiente: [11 - Convenciones de Estilo y Calidad de Código](11-estilo.md)
- Volver al [README principal](../README.md)
