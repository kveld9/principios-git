# 06 - Versiones y Lanzamientos (SemVer, Releases y Cadena de Suministro)

Un sistema de versionado estructurado protege a los consumidores de software frente a actualizaciones disruptivas
inesperadas, garantiza la trazabilidad de los binarios y proporciona un mapa claro de la evolución del proyecto.

Este documento detalla la aplicación de **Semantic Versioning 2.0.0**, el mantenimiento de **Keep a Changelog**,
las **estrategias de release automatizado**, la **política de checksums y firmas**, las **atestaciones de compilación**
y los **patrones de mantenimiento de repositorios**.

---

## 1. Versionado Semántico (SemVer 2.0.0)

El formato canónico de versión es:

```text
MAJOR.MINOR.PATCH
Ejemplo: 2.4.1
```

```text
       ┌────────── MAJOR: Cambios incompatibles (Breaking Changes)
       │  ┌─────── MINOR: Nuevas funcionalidades compatibles hacia atrás
       │  │  ┌──── PATCH: Correcciones de bugs compatibles hacia atrás
       ▼  ▼  ▼
       1 . 3 . 0
```

### Reglas de Incremento

1. **MAJOR (X.y.z)**: Se incrementa obligatoriamente cuando se introducen modificaciones incompatibles en la API
   pública, se eliminan funciones o endpoints, o se altera el formato de almacenamiento de datos de forma que requiera
   migración manual.
2. **MINOR (x.Y.z)**: Se incrementa cuando se agregan funcionalidades nuevas manteniendo total compatibilidad
   hacia atrás, o cuando se marca código como obsoleto (*deprecated*) sin eliminarlo.
3. **PATCH (x.y.Z)**: Se incrementa exclusivamente cuando se corrigen errores de software preservando la
   compatibilidad con versiones anteriores.

### Versiones Iniciales (0.y.z)

En versiones `0.x.x`, el software se considera en desarrollo inicial y la API pública es inestable. No obstante,
una vez que el software es adoptado en entornos de producción o por usuarios externos, se debe promover
inmediatamente a `1.0.0` para establecer el contrato formal de estabilidad.

---

## 2. Etiquetas de Git Anotadas (Annotated Tags)

Las versiones deben marcarse en el historial de Git mediante **etiquetas anotadas** que contienen la fecha,
el autor, el mensaje y opcionalmente firma criptográfica.

> [!CAUTION]
> **Nunca utilizar etiquetas ligeras (lightweight tags)** para releases de producción: `git tag v1.0.0` crea
> un puntero volátil sin metadatos.

### Creación de una Etiqueta Anotada

```bash
# Crear etiqueta anotada con mensaje explicativo
git tag -a v1.2.0 -m "Release v1.2.0: add rate limiting and security patch"

# Verificar los metadatos de la etiqueta
git show v1.2.0

# Publicar la etiqueta al repositorio remoto
git push origin v1.2.0
```

Convención de nomenclatura: Utilizar siempre el prefijo en minúscula `v` seguido del número de versión (`v1.0.0`, `v2.1.3`).

---

## 3. Gestión del Registro de Cambios (Changelog)

Todo repositorio mantenido debe incluir un archivo `CHANGELOG.md` basado en el estándar [Keep a Changelog](https://keepachangelog.com/).

### Secciones Estándar por Versión

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Experimental WebSocket keepalive support.

## [1.2.0] - 2026-10-18

### Added
- Rate limiting middleware on `/auth/login` endpoint (#104).

### Changed
- Migrated default password hashing to Argon2id (#108).

### Fixed
- Prevent memory leak on unclosed client connections (#112).

### Security
- Updated dependency `openssl` to patch CVE-2026-XXXX (#115).
```

### Categorías Obligatorias

- `Added`: Nuevas capacidades y características.
- `Changed`: Modificaciones en comportamiento existente.
- `Deprecated`: Funcionalidades que serán removidas en próximas versiones mayores.
- `Removed`: Funcionalidades eliminadas en esta versión.
- `Fixed`: Corrección de errores.
- `Security`: Vulnerabilidades mitigadas o parches de seguridad.

---

## 4. Estrategias de Release y Tabla de Decisión

El kit contempla tres estrategias operativas de publicación de versiones, adaptables según la naturaleza del software,
la frecuencia de despliegue y el nivel de automatización deseado.

### Comparativa y Tabla de Decisión

| Estrategia | Mecanismo de Disparo | Cálculo de Versión | Generación de Notas | Casos de Uso Recomendados |
| :--- | :--- | :--- | :--- | :--- |
| **Manual (Línea Base)** | Push manual de etiqueta anotada `git push origin vX.Y.Z` | Decisión manual del mantenedor según SemVer | Edición manual de `CHANGELOG.md` | Proyectos iniciales, utilidades internas simples, repositorios documentales. |
| **Artefactos con Tags Computados** | Push directo o merge a `main` | Inspección de rango de conventional commits desde último `v*` | Automatizada en cuerpo de release con tabla de hashes | Aplicaciones compiladas (Android APKs, binarios Go/Rust, bundles CLI), proyectos que distribuyen binarios descargables. |
| **Semantic-Release Total** | Push o merge a `main` (estable) o `dev` (experimental) | `@semantic-release/commit-analyzer` | `@semantic-release/release-notes-generator` + `@semantic-release/changelog` | Librerías compartidas (npm, Python, paquetes), monorepos, APIs continuas, proyectos morphe/gold-standard. |

---

### Estrategia A: Manual (Etiquetas Anotadas)

El mantenedor actualiza manualmente `CHANGELOG.md`, crea un commit con `chore: prepare release vX.Y.Z`, genera
la etiqueta anotada firmada (`git tag -s -a vX.Y.Z -m "..."`) y la empuja a GitHub. Si existe un workflow de
publicación, este se activa al detectar el tag `v*`.

---

### Estrategia B: Artefactos con Tags Computados (Patrón `.github/workflows/release.yml.example`)

Utilizado en proyectos que generan artefactos físicos (como APKs, binarios, paquetes comprimidos) donde no
se requiere una suite pesada de Node.js en CI para calcular versiones:

1. **Inspección de Rango Git**:
   Un paso de shell ejecuta `git describe --tags --abbrev=0 --match "v[0-9]*"` para hallar el tag base más reciente.
2. **Evaluación de Conventional Commits**:
   - Si el rango `LATEST_TAG..HEAD` contiene commits con `!` (ej. `feat!:`) o la leyenda `BREAKING CHANGE:`,
     se incrementa **MAJOR**.
   - Si contiene prefijos `feat:`, se incrementa **MINOR**.
   - En cualquier otro caso (`fix:`, `perf:`, `refactor:`), se incrementa **PATCH**.
   - Si no hay nuevos commits en el rango, el paso marca `skip_release=true` y finaliza sin error.
3. **Compilación y Renombrado**:
   Los artefactos generados por el comando de build se renombran incorporando el prefijo del proyecto y la
   versión exacta (`[ASSET_PREFIX]-[VERSION]-[ORIGINAL]`).
4. **Cálculo de Checksums**:
   Se generan hashes SHA-256, SHA-512 y el manifiesto unificado `SHA256SUMS.txt`.
5. **Publicación en GitHub**:
   Se emplea la acción comunitaria [`softprops/action-gh-release`](https://github.com/softprops/action-gh-release)
   con `generate_release_notes: false`, adjuntando los artefactos y construyendo dinámicamente una tabla Markdown
   con las sumas de verificación.

---

### Estrategia C: Semantic-Release Total (Patrón `.releaserc.js.example`)

Diseñado para pipelines sin intervención humana basada en el estándar *Conventional Commits*:

1. **Configuración de Ramas**:
   - Rama principal: `main` (publica releases formales `vX.Y.Z`).
   - Rama de desarrollo/pre-release: `dev` (publica releases preliminares `vX.Y.Z-experimental.N` en canal `experimental`).
2. **Plugins de Semantic-Release**:
   - `@semantic-release/commit-analyzer`: Determina el tipo de incremento. Se configuran reglas explícitas para
     ignorar scopes puramente de mantenimiento como `docs`, `ci`, `test`, `tooling`, `scripts` y `chore` evitando
     la publicación de versiones innecesarias.
   - `@semantic-release/release-notes-generator`: Extrae las notas estructuradas a partir de los commits.
   - `@semantic-release/changelog`: Actualiza automáticamente `CHANGELOG.md`.
   - `@semantic-release/git`: Realiza un commit con los assets modificados (`CHANGELOG.md`, `package.json`,
     `version.txt`) con el mensaje canónico:

     ```text
     chore: Release vX.Y.Z [skip ci]
     ```

   - `@semantic-release/github`: Sube los artefactos al release de GitHub y asigna el tag remoto.
3. **Notificaciones y Fallback**:
   - Notificación opcional a canales de mensajería (como bots de Telegram mediante `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`).
   - Paso de fallback en CI: Cuando ningún commit amerita un nuevo release, el workflow ejecuta una verificación
     de compilación básica para asegurar que la rama `main` compila limpiamente.

---

## 5. Política y Estándares de Checksums (Sumas de Verificación)

La distribución de archivos descargables exige salvaguardas contra alteraciones en tránsito y ataques de suplantación.

```text
Distribución de Artefactos
├── Archivo Binario:     my-app-1.2.0-linux-amd64.tar.gz
├── Hash Individual:     my-app-1.2.0-linux-amd64.tar.gz.sha256
├── Hash Alta Seguridad: my-app-1.2.0-linux-amd64.tar.gz.sha512
├── Hash Corrupción:     my-app-1.2.0-linux-amd64.tar.gz.md5 (Solo diagnóstico de red)
└── Manifiesto Canónico: SHA256SUMS.txt (Compatible con sha256sum -c)
```

### Directrices de Algoritmos Criptográficos

1. **SHA-256 (Mandatorio)**:
   Es el estándar de la industria para verificación de autenticidad e integridad criptográfica. Cada binario o
   tarball debe contar con su hash correspondiente y estar listado en `SHA256SUMS.txt`.
2. **SHA-512 (Recomendado)**:
   Proporciona una capa superior de resistencia a colisiones en entornos de alta seguridad o sistemas operativos
   de misión crítica.
3. **MD5 (Uso Restringido)**:
   **Prohibido para seguridad y autenticidad** debido a vulnerabilidades de colisión conocidas. Se permite
   únicamente como verificación rápida contra corrupción accidental de paquetes en transferencias de red lentas
   o descargadores legados.

### Formato de `SHA256SUMS.txt`

El archivo debe contener el hash hexadecimal seguido de dos espacios (o un espacio y asterisco en modo binario)
y el nombre relativo del archivo:

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  my-app-1.2.0-x86_64.apk
a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e  my-app-1.2.0-arm64.apk
```

Esto permite al usuario final o a scripts de aprovisionamiento auditar la descarga en un solo comando:

```bash
sha256sum -c SHA256SUMS.txt
```

---

## 6. Firma de Artefactos y Seguridad de la Cadena de Suministro

Para garantizar que un artefacto compilado provino de una fuente autorizada y no fue adulterado durante el
empaquetado en CI, se aplican protocolos estrictos de firma y atestación.

### Inventario de Secretos de Firma

Los flujos de trabajo de publicación consumen credenciales que deben residir exclusivamente en
**GitHub Repository Secrets** o **Environment Secrets**:

| Secreto | Propósito | Formato / Tipo |
| :--- | :--- | :--- |
| `KEYSTORE_BASE64` | Almacén de claves binarias para firma de paquetes (Android APK, JARs) | Cadena codificada en Base64 (`base64 -w 0 release.jks`) |
| `KEYSTORE_PASSWORD` | Contraseña maestra para descifrar el almacén de claves | Texto plano cifrado en secret |
| `KEY_ALIAS` | Alias de la clave privada dentro del keystore | Identificador alfanumérico |
| `KEY_PASSWORD` | Contraseña específica para la clave privada seleccionada | Texto plano cifrado en secret |
| `GPG_PRIVATE_KEY` | Clave privada GPG para firma de binarios y commits de release | Bloque de texto ASCII Armored (`-----BEGIN PGP PRIVATE KEY BLOCK-----`) |
| `GPG_PASSPHRASE` | Contraseña de protección de la clave GPG | Texto plano cifrado en secret |
| `TELEGRAM_BOT_TOKEN` | Token para notificaciones automáticas de release | Identificador de API de Telegram Bot |
| `TELEGRAM_CHAT_ID` | Identificador del canal o grupo receptor de notificaciones | Número entero o identificador de canal |

### Aislamiento Estricto: Por qué los PRs Jamás Reciben Secretos de Firma

> [!CAUTION]
> **Regla de Oro de Seguridad en CI**:
> Los flujos de trabajo de Pull Request (`pull_request`) **nunca** deben tener acceso a secretos de firma ni de producción.

Si un flujo ejecutado en un Pull Request tuviera acceso a `KEYSTORE_BASE64` o `GPG_PRIVATE_KEY`, cualquier
colaborador externo o atacante podría enviar un PR modificando los scripts de compilación (como `build.gradle`,
`Makefile` o `package.json`) para exfiltrar las claves maestras a un servidor remoto, o para generar versiones
maliciosas firmadas con el certificado legítimo del proyecto.

#### Solución para Pruebas en PRs: Firmas Descartables (Ephemeral Keys)

Cuando un pipeline de PR necesita compilar y verificar que el empaquetado funciona correctamente, debe generar
una clave efímera descartable en memoria durante el paso de CI mediante `keytool`:

```bash
# Generación de keystore de usar y tirar en el runner de CI para PRs
keytool -genkey -v \
  -keystore ephemeral.keystore \
  -alias ephemeral \
  -keyalg RSA \
  -keysize 2048 \
  -validity 1 \
  -storepass android \
  -keypass android \
  -dname "CN=PR-Validation, OU=CI, O=Disposable, L=Ephemeral, S=Ephemeral, C=US"
```

El binario resultante se somete a validación interna y se descarta al finalizar el trabajo, garantizando que
el entorno de desarrollo sea 100% testeable sin arriesgar los activos de producción.

---

### Atestación de Procedencia de Compilación (Build Attestations)

GitHub proporciona atestaciones criptográficas basadas en el estándar abierto [Sigstore](https://www.sigstore.dev/)
e [in-toto](https://in-toto.io/), vinculando el artefacto compilado con el commit exacto, el workflow y el runner
de GitHub Actions que lo generó.

Para habilitar atestaciones en el job de publicación:

```yaml
permissions:
  contents: write
  id-token: write       # Requerido para firmar OIDC con Sigstore
  attestations: write   # Requerido para registrar la atestación en GitHub

steps:
  - name: Generate Artifact Attestation
    uses: actions/attest-build-provenance@v1
    with:
      subject-path: 'release_assets/*'
```

Los usuarios pueden verificar la autenticidad del binario utilizando el CLI de GitHub
(`gh attestation verify my-app.tar.gz --owner [OWNER]`).

---

## 7. Canales de Distribución y Pre-releases

Los proyectos con ciclos activos de retroalimentación deben segregar sus entregas en canales diferenciados:

```text
Flujo de Canales
├── Rama 'main' ──► Tag 'v1.2.0'                 ──► Canal Estable (Latest en GitHub / Tiendas)
└── Rama 'dev'  ──► Tag 'v1.3.0-experimental.1'  ──► Canal Pre-release (Marcado como Prerelease)
```

1. **Canal Estable (`main`)**:
   - Genera versiones inmutables `vX.Y.Z`.
   - Se marca como el release formal predeterminado (`latest`).
2. **Canal Experimental / Beta (`dev`)**:
   - Genera versiones con sufijo SemVer (por ejemplo `vX.Y.Z-experimental.1` o `vX.Y.Z-rc.1`).
   - Se marca en GitHub Releases con la bandera `prerelease: true`.
   - Permite que los probadores auditen cambios sin afectar a los usuarios en producción.

---

## 8. Patrones de Mantenimiento Avanzado

A continuación se documentan los cuatro patrones arquitectónicos comunes en infraestructuras maduras. Se describen
conceptualmente para ser adoptados a medida sin atar al kit a dependencias específicas de cada proyecto.

### 1. Monitoreo Programado de Upstream (Update-Check)

En proyectos derivados, wrappers o clientes de servicios de terceros, un workflow programado periódicamente
(vía `schedule` cron en GitHub Actions) consulta la API de releases del repositorio o librería *upstream*. Si se
detecta una nueva versión superior a la soportada, el bot abre automáticamente un Issue estructurado en el
repositorio para que los mantenedores evalúen la compatibilidad.

### 2. Espejos en Forjas Secundarias (Forge Mirroring)

Para mitigar el riesgo de dependencia exclusiva de un único proveedor de Git (*single point of failure*),
un workflow activado ante cada push a `main` o tags ejecuta un empuje autenticado hacia una forja secundaria
(como GitLab, Codeberg o un servidor Gitea/Forgejo propio). Este mecanismo utiliza SSH keys privadas restringidas
almacenadas en los secretos del repositorio.

### 3. Sincronización Post-Release (`main` -> `dev`)

Cuando se utiliza una estrategia de doble rama (`main` y `dev`), la publicación de un release en `main` genera
commits automáticos (como la actualización de `CHANGELOG.md` o el incremento de versión). Para evitar que la rama
`dev` diverja y sufra conflictos de fusión posteriores, un paso final en el pipeline de release ejecuta una
sincronización automática *fast-forward* de `main` sobre `dev`.

### 4. Salvaguardas de Canal Pre-release (Pre-release Guard)

Para evitar accidentes donde un artefacto inestable o compilado en una rama de pruebas sea indexado por
administradores de paquetes públicos (npm, crates.io, PyPI) como la versión recomendada, se implementa una
condición de guardia (*channel guard*) que inspecciona si el nombre de la versión contiene guiones o sufijos
(`-experimental`, `-alpha`, `-beta`). Ante la presencia de un sufijo, se obliga al uso de tags de distribución
específicos (`npm publish --tag experimental`) o se previene la ejecución de comandos de publicación en producción.

---

## Navegación

- Anterior: [05 - Flujo de Pull Requests y Revisiones](05-pull-requests.md)
- Siguiente: [07 - Integración Continua y Automatización (CI)](07-ci.md)
- Volver al [README principal](../README.md)
