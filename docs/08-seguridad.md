# 08 - Seguridad, Análisis de Vulnerabilidades y Cadena de Suministro

La seguridad de un repositorio debe ser preventiva y abarcar todo el ciclo de vida del desarrollo: desde la estación de trabajo local del programador hasta los artefactos generados en la nube y distribuidos a los usuarios finales.

Este documento establece los protocolos de seguridad de código, detección continua de secretos con **Gitleaks**, análisis estático automatizado con **CodeQL**, inventario de credenciales y aislamiento de firmas en CI.

---

## 1. Política de Divulgación Responsable (Coordinated Disclosure)

La transparencia pública no debe comprometer a los usuarios que ejecutan el software en entornos reales.

1. **Canal Confidencial Exclusivo**: Toda vulnerabilidad de seguridad debe comunicarse a través de los canales privados definidos en [`SECURITY.md`](../SECURITY.md) (preferentemente mediante *GitHub Private Vulnerability Reporting* o correo cifrado a los mantenedores).
2. **Prohibición de Issues Públicos para Exploits**: Abrir un issue público detallando una vulnerabilidad no parcheada expone a los usuarios a ataques inmediatos.
3. **Plazos de Respuesta y Remediación**:
   - Acuse de recibo inicial: < 48 horas.
   - Evaluación y confirmación técnica: < 5 días hábiles.
   - Desarrollo de parche y publicación coordinada: tiempo razonable acordado con el investigador.

---

## 2. Prevención y Detección Continua de Fugas de Secretos

Una vez que una clave API, contraseña o certificado privado entra al árbol de Git y se empuja a un servidor remoto, **debe considerarse comprometido para siempre**, independientemente de que se elimine en el commit siguiente.

### Escaneo Automatizado en CI con Gitleaks
El kit provee una implementación activa en [`.github/workflows/gitleaks.yml`](../.github/workflows/gitleaks.yml), que audita cada push a ramas principales (`main`, `dev`) y cada Pull Request:

```yaml
steps:
  - name: Check out repository with full history
    uses: actions/checkout@v4
    with:
      fetch-depth: 0 # OBLIGATORIO: descarga todo el historial de Git

  - name: Run Gitleaks scanner
    uses: gitleaks/gitleaks-action@v2
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

> [!IMPORTANT]
> **Por qué `fetch-depth: 0` es Mandatorio**:
> Por defecto, `actions/checkout` descarga únicamente el commit más reciente (`fetch-depth: 1`). Si un atacante o desarrollador comete un secreto en un commit y luego intenta "remediarlo" borrándolo en el siguiente commit del mismo PR, un escaneo superficial no detectará la fuga. `fetch-depth: 0` garantiza que Gitleaks audite todos los deltas del árbol histórico.

### Prevención Local y Push Protection
- **`.gitignore` Exhaustivo**: El archivo [`.gitignore`](../.gitignore) de este kit excluye automáticamente patrones de secretos habituales (`.env`, `*.pem`, `*.key`, `id_rsa`, etc.).
- **Push Protection de GitHub**: Habilite en los ajustes de seguridad del repositorio la opción **Secret scanning -> Push protection** para que GitHub bloquee inmediatamente cualquier push que contenga patrones de tokens conocidos (AWS, GitHub, Stripe, Slack, etc.).
- **Escaneo Local**: Ejecute `gitleaks` en su máquina local antes de crear un commit:
  ```bash
  gitleaks detect --source . --verbose
  ```

### Procedimiento de Emergencia ante Filtración de Secretos
Si accidentalmente se empuja una clave o secreto al repositorio:
1. **Paso Inmediato: Revocar e Invalidar el Secreto**: Asuma que bots automatizados ya clonaron el secreto. Invalide la credencial en el proveedor de nube inmediatamente. **Este paso es prioritario sobre la limpieza de Git**.
2. **Purgar el Historial**: Un commit posterior con `git rm .env` **no** borra el archivo del historial previo. Utilice `git-filter-repo` (la herramienta oficial recomendada por Git, reemplazante de `git filter-branch`):
   ```bash
   git-filter-repo --path .env --invert-paths
   ```
3. **Forzar Actualización y Notificar**: Tras reescribir el historial, realizar push forzado coordinado y alertar a los miembros del equipo para que re-clonen o rebasen sus copias locales.

---

## 3. Análisis Estático de Vulnerabilidades con CodeQL

El análisis semántico de código (*SAST*) permite interceptar vulnerabilidades como inyecciones SQL, Cross-Site Scripting (XSS), escalado de privilegios y desreferencia de punteros nulos antes de llegar a producción.

Este kit provee una plantilla de integración en [`.github/workflows/codeql.yml.example`](../.github/workflows/codeql.yml.example).

### Aspectos Clave de CodeQL en el Pipeline:

1. **Escaneo Programado Semanal (`schedule`)**:
   Las bases de datos de vulnerabilidades (CVEs) se actualizan constantemente. Un flujo que corre semanalmente (ej. lunes a las 06:00 UTC) permite detectar fallos en código que no ha sido modificado recientemente, ante nuevas reglas publicadas por investigadores de seguridad.
2. **Permisos Restringidos (`security-events: write`)**:
   El token de GitHub Actions solo necesita permisos para publicar los reportes SARIF resultantes en la interfaz de seguridad del repositorio, manteniendo `contents: read`.
3. **Soporte Políglota y de Acciones**:
   CodeQL permite auditar tanto los lenguajes principales del repositorio (`javascript-typescript`, `python`, `go`, `java-kotlin`, `c-cpp`, `csharp`, `ruby`) como las propias acciones de GitHub (`actions`), previniendo vulnerabilidades en los workflows de CI.

---

## 4. Inventario de Secretos y Aislamiento de Firmas en Pull Requests

Un repositorio maduro requiere credenciales protegidas para tareas de publicación, firma y notificaciones.

### Inventario Estándar de Secretos

| Categoría | Nombre del Secreto | Uso y Restricción |
| :--- | :--- | :--- |
| **Firma Android / Java** | `KEYSTORE_BASE64` | Keystore binario codificado en Base64 para firmar APKs/JARs. |
| **Firma Android / Java** | `KEYSTORE_PASSWORD` | Contraseña maestra del archivo keystore. |
| **Firma Android / Java** | `KEY_ALIAS` | Alias de la llave privada dentro del almacén. |
| **Firma Android / Java** | `KEY_PASSWORD` | Contraseña individual de la llave privada. |
| **Firma Criptográfica GPG** | `GPG_PRIVATE_KEY` | Clave privada GPG para firma de tags o tarballs de binarios. |
| **Firma Criptográfica GPG** | `GPG_PASSPHRASE` | Frase de paso para desbloquear la clave privada GPG. |
| **Notificaciones** | `TELEGRAM_BOT_TOKEN` | Token para alertas de despliegue a canales o chats. |
| **Notificaciones** | `TELEGRAM_CHAT_ID` | Identificador de chat o canal receptor de alertas. |

---

### Por qué los PRs Jamás Deben Recibir Secretos de Firma

> [!CAUTION]
> **Modelo de Amenazas en Entornos de Integración Continua**:
> Los flujos de trabajo disparados por `pull_request` **nunca deben tener acceso a secretos de producción ni de firma**.

Cuando un usuario envía un Pull Request (especialmente desde un fork público), el código introducido aún no ha sido revisado ni auditado por los mantenedores. Si los secretos de producción estuviesen disponibles en dicho entorno:

1. **Exfiltración Directa de Certificados**:
   Un actor malicioso podría alterar una tarea de compilación en `build.gradle`, `Makefile`, `package.json` o scripts de tests para volcar el contenido de `KEYSTORE_BASE64` o `GPG_PRIVATE_KEY` mediante una petición HTTP externa.
2. **Generación de Binarios Maliciosos Firmados**:
   El atacante podría modificar el código fuente para inyectar un troyano o backdoor y forzar al runner de GitHub Actions a firmarlo legítimamente con el certificado oficial del proyecto.

#### Solución Robusta: Firmas Descartables (*Ephemeral Keys*)
Para validar en un PR que los pasos de empaquetado y firma funcionan sin comprometer secretos reales:
- El pipeline de PR genera en tiempo de ejecución un almacén de claves descartable (*throwaway*) mediante `keytool`:
  ```bash
  keytool -genkey -v \
    -keystore ephemeral.keystore \
    -alias ephemeral \
    -keyalg RSA \
    -keysize 2048 \
    -validity 1 \
    -storepass android \
    -keypass android \
    -dname "CN=PR-Build, OU=CI, O=Disposable, L=Ephemeral, S=Ephemeral, C=US"
  ```
- El proceso de build compila y firma el artefacto de prueba usando esta clave ficticia.
- Se verifica la integridad estructural del binario sin exponer credenciales de producción.

---

## 5. Seguridad de Dependencias y Cadena de Suministro

La mayoría de las brechas modernas se originan en dependencias transitivas comprometidas (*software supply chain*).

### Monitoreo Continuo con Dependabot
Este kit incluye [`.github/dependabot.yml`](../.github/dependabot.yml), configurado para auditar semanalmente acciones de GitHub y manifiestos de paquetes.

### Auditorías Locales Obligatorias
Antes de realizar releases importantes, ejecute las herramientas de análisis de dependencias de su ecosistema:
- **Rust**: `cargo audit`
- **Node.js**: `npm audit` o `pnpm audit`
- **Python**: `pip-audit`
- **Go**: `govulncheck ./...`

---

## 6. Integridad de Autoría: Commits Firmados (GPG / SSH)

Para certificar que un commit proviene del autor legítimo y no fue suplantado alterando `git config user.name`:

```bash
# Configurar Git para firmar con clave SSH moderna
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global gpg.format ssh
git config --global commit.gpgsign true
```

Los commits firmados lucirán el distintivo verde **Verified** en la interfaz web de GitHub, impidiendo la falsificación de identidad en entornos colaborativos y garantizando una auditoría forense inalterable.

---

## Navegación

- Anterior: [07 - Integración Continua y Automatización](07-ci.md)
- Siguiente: [09 - Guía de Licencias de Software](09-licencias.md)
- Volver al [README principal](../README.md)
