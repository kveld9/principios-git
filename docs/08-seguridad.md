# 08 - Seguridad y Gestión de Vulnerabilidades

La seguridad de un repositorio debe ser preventiva y abarcar todo el ciclo de vida del desarrollo: desde la estación de trabajo local del programador hasta los artefactos generados en la nube.

Este documento establece los protocolos de seguridad de código, prevención de fugas y respuesta ante incidentes.

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

## 2. Prevención y Detección de Fugas de Secretos

Una vez que una clave API, contraseña o certificado privado entra al árbol de Git y se empuja a un servidor remoto, **debe considerarse comprometido para siempre**, independientemente de que se elimine en el commit siguiente.

### Mecanismos de Prevención
- **`.gitignore` Exhaustivo**: El archivo [`.gitignore`](../.gitignore) de este kit excluye automáticamente patrones de secretos habituales (`.env`, `*.pem`, `*.key`, `id_rsa`, etc.).
- **Push Protection de GitHub**: Habilite en los ajustes de seguridad del repositorio la opción **Secret scanning -> Push protection** para que GitHub bloquee inmediatamente cualquier push que contenga patrones de tokens conocidos (AWS, GitHub, Stripe, Slack, etc.).
- **Escaneo Local con Pre-commit**: Se recomienda instalar utilidades como `gitleaks` o `detect-secrets` en la máquina local para interceptar credenciales antes del commit:
  ```bash
  # Escanear el repositorio completo en busca de secretos históricos
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

## 3. Seguridad de Dependencias y Cadena de Suministro

La mayoría de las brechas modernas no se originan en el código propio, sino en dependencias transitivas comprometidas (*supply chain attacks*).

### Monitoreo Continuo con Dependabot
Este kit incluye [`.github/dependabot.yml`](../.github/dependabot.yml), configurado para auditar semanalmente acciones de GitHub y manifiestos de paquetes.

### Auditorías Locales Obligatorias
Antes de realizar releases importantes, ejecute las herramientas de análisis de dependencias de su ecosistema:
- **Rust**: `cargo audit`
- **Node.js**: `npm audit` o `pnpm audit`
- **Python**: `pip-audit`
- **Go**: `govulncheck ./...`

---

## 4. Integridad de Autoría: Commits Firmados (GPG / SSH)

Para garantizar que un commit fue efectivamente creado por quien dice ser (y no suplantado mediante `git config user.name`), se recomienda firmar criptográficamente los commits utilizando claves SSH o GPG:

```bash
# Configurar Git para firmar con clave SSH moderna
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global gpg.format ssh
git config --global commit.gpgsign true
```

Los commits firmados lucirán el distintivo verde **Verified** en la interfaz web de GitHub, impidiendo la falsificación de identidad en entornos corporativos o proyectos de código abierto de alto impacto.

---

## Navegación

- Anterior: [07 - Integración Continua y Automatización](07-ci.md)
- Siguiente: [09 - Guía de Licencias de Software](09-licencias.md)
- Volver al [README principal](../README.md)
