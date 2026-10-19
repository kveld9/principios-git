# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-10-19

### Added

- **Kit inicial de estándares de repositorio**: Estructura canónica con licencias, metadatos y gobernanza (`LICENSE`,
  `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHECKLIST.md`), exclusión y normalización de
  archivos (`.gitignore`, `.gitattributes`, `.editorconfig`) y guías técnicas de arquitectura (documentos 01 a 05).
- **Instalador y auditor auto-verificable**: Herramientas de automatización en `scripts/` (`new-repo.sh` para
  andamiaje determinista no destructivo con sustitución de metadatos y `check-repo.sh` para auditoría de cumplimiento
  con códigos de salida 0/1).
- **Estándares profesionales de código y estilo**: Guías de diseño y arquitectura (`docs/11-estilo.md` y
  `docs/12-modularizacion.md`), principio de responsabilidad única, eliminación de literales mágicos, manejo explícito
  fail-loud y prohibición estricta de emojis en superficies de ejecución.
- **Nivel de release y cadena de suministro (Tier 3)**: Guía exhaustiva de versionado (`docs/06-releases.md`),
  configuración para Semantic-Release y Conventional Commits (`.releaserc.js.example`) y pipeline automatizado con
  atestaciones Sigstore y manifiestos `SHA256SUMS.txt`.
- **Gobernanza de seguridad y control de accesos**: Detección continua de fuga de secretos con Gitleaks
  (`.github/workflows/gitleaks.yml`), plantilla de análisis estático SAST con CodeQL
  (`.github/workflows/codeql.yml.example`), especificación de rulesets modernos en `.github/settings.example.yml`
  y plantilla `.github/CODEOWNERS.example`.

### Changed

- **Actualización de dependencias de automatización**: Actualización de acciones oficiales en GitHub Actions y
  Dependabot (`actions/checkout@v7` y `DavidAnson/markdownlint-cli2-action@v24`).

### Fixed

- **Estabilización de CI y calidad de documentación**: Restricción de permisos mínimos en el flujo de Gitleaks,
  ajuste de configuración y límites de línea en `.markdownlint.yaml` para asegurar validaciones deterministas.
