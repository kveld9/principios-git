# 06 - Versiones y Lanzamientos (SemVer y Changelog)

Un sistema de versionado estructurado protege a los consumidores de software frente a actualizaciones disruptivas inesperadas y proporciona un mapa claro de la evolución del proyecto.

Este documento detalla la aplicación de **Semantic Versioning 2.0.0**, el mantenimiento de **Keep a Changelog** y el flujo de trabajo para **GitHub Releases**.

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

1. **MAJOR (X.y.z)**: Se incrementa obligatoriamente cuando se introducen modificaciones incompatibles en la API pública, se eliminan funciones o endpoints, o se altera el formato de almacenamiento de datos de forma que requiera migración manual.
2. **MINOR (x.Y.z)**: Se incrementa cuando se agregan funcionalidades nuevas manteniendo total compatibilidad hacia atrás, o cuando se marca código como obsoleto (*deprecated*) sin eliminarlo.
3. **PATCH (x.y.Z)**: Se incrementa exclusivamente cuando se corrigen errores de software preservando la compatibilidad con versiones anteriores.

### Versiones Iniciales (0.y.z)
En versiones `0.x.x`, el software se considera en desarrollo inicial y la API pública es inestable. No obstante, una vez que el software es adoptado en entornos de producción o por usuarios externos, se debe promover inmediatamente a `1.0.0` para establecer el contrato formal de estabilidad.

---

## 2. Etiquetas de Git Anotadas (Annotated Tags)

Las versiones deben marcarse en el historial de Git mediante **etiquetas anotadas** que contienen la fecha, el autor, el mensaje y opcionalmente firma criptográfica.

> [!CAUTION]
> **Nunca utilizar etiquetas ligeras (lightweight tags)** para releases de producción: `git tag v1.0.0` crea un puntero volátil sin metadatos.

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

### Categorías Obligatorias:
- `Added`: Nuevas capacidades y características.
- `Changed`: Modificaciones en comportamiento existente.
- `Deprecated`: Funcionalidades que serán removidas en próximas versiones mayores.
- `Removed`: Funcionalidades eliminadas en esta versión.
- `Fixed`: Corrección de errores.
- `Security`: Vulnerabilidades mitigadas o parches de seguridad.

---

## 4. Publicación en GitHub Releases

Al publicar una versión en GitHub:

1. **Vincular a la Etiqueta Anotada**: Asociar el release al tag `vX.Y.Z`.
2. **Generar Notas de Lanzamiento**: Extraer la sección correspondiente del `CHANGELOG.md`.
3. **Firmas y Sumas de Verificación (Checksums)**: Si el proyecto genera artefactos binarios descargables (archivos `.tar.gz`, `.zip`, ejecutables), adjuntar siempre un archivo `SHA256SUMS` con los hashes criptográficos correspondientes para que los usuarios verifiquen la integridad de la descarga:
   ```bash
   sha256sum mi-binario-linux-amd64.tar.gz > SHA256SUMS
   ```

---

## Navegación

- Anterior: [05 - Flujo de Pull Requests y Revisiones](05-pull-requests.md)
- Siguiente: [07 - Integración Continua y Automatización (CI)](07-ci.md)
- Volver al [README principal](../README.md)
