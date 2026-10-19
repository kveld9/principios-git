# 10 - Guía de Adopción e Integración en Repositorios Existentes

Adoptar estándares en un proyecto en blanco es trivial; el verdadero desafío de ingeniería radica en estandarizar repositorios en producción activos que carecen de `.github/`, `CONTRIBUTING.md` o políticas formales de seguridad sin interrumpir las operaciones del equipo ni provocar conflictos de merge masivos.

Este documento proporciona una guía metódica para integrar este kit en cualquier repositorio existente.

---

## 1. Plan de Adopción en 5 Fases

```text
Fase 1: Diagnóstico  ──► Fase 2: Andamiaje  ──► Fase 3: Ajustes  ──► Fase 4: Normalización  ──► Fase 5: Protección
   (Auditoría)           (Inyección Kit)        (Placeholders)        (.gitattributes)          (Branch Rules)
```

---

## 2. Fase 1: Diagnóstico del Repositorio Destino

Antes de modificar el repositorio existente, ejecute el script de auditoría provisto por el kit apuntando al directorio de dicho repositorio:

```bash
# Ejecutar auditoría sobre el repositorio destino
./scripts/check-repo.sh /ruta/al/repo-destino
```

El script listará detalladamente los archivos faltantes o vacíos organizados por categorías:
- Metadatos y licencias (`README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`).
- Configuración de entorno (`.editorconfig`, `.gitattributes`, `.gitignore`).
- Gobernanza y CI (`.github/workflows/ci.yml`, `dependabot.yml`, plantillas).

---

## 3. Fase 2: Inyección No Destructiva del Kit

Utilice el script `scripts/new-repo.sh` para copiar la infraestructura del kit hacia el repositorio destino. Por defecto, este comando **no sobreescribe** archivos que ya existan en el destino:

```bash
./scripts/new-repo.sh \
  --owner "MiOrganizacion" \
  --email "seguridad@miorganizacion.com" \
  --year "2026" \
  /ruta/al/repo-destino
```

Si el repositorio destino ya posee un archivo (por ejemplo un `README.md` con contenido del proyecto o un `.gitignore` previo), el instalador omitirá su sobreescritura y emitirá un aviso `[SKIP]`.

---

## 4. Fase 3: Personalización de Metadatos y Placeholders

Revise manualmente los siguientes puntos en el repositorio destino:

1. **`LICENSE`**: Si el proyecto no tenía licencia, el script inyectará la licencia MIT con el año y propietario configurados. Si ya existía otra licencia, asegúrese de conservarla.
2. **`SECURITY.md`**: Confirme que la dirección de correo electrónico o el enlace de contacto para reportar vulnerabilidades sea funcional.
3. **`CODE_OF_CONDUCT.md`**: Verifique que el correo de contacto para incidentes de convivencia coincida con el canal designado por el proyecto.
4. **`.github/dependabot.yml`**: Descomente el ecosistema de paquetes correspondiente al stack del proyecto (Node, Python, Go, Rust, Docker, etc.).
5. **`.github/CODEOWNERS.example`**: Renómbrelo a `.github/CODEOWNERS` y asigne los equipos o usuarios responsables de cada subdirectorio del repositorio.

---

## 5. Fase 4: Normalización de Git y Saltos de Línea

Si el repositorio previo tenía archivos con saltos de línea mixtos (CRLF en Windows y LF en Linux), la incorporación de `.gitattributes` podría generar cambios de línea no deseados en futuros commits. 

Para normalizar todo el repositorio de una sola vez en un commit dedicado:

```bash
cd /ruta/al/repo-destino

# Forzar a Git a re-evaluar todos los archivos según .gitattributes
git add --renormalize .

# Crear un commit exclusivo de normalización
git commit -m "style: normalize line endings to LF according to .gitattributes"
```

> [!IMPORTANT]
> Realice este paso en un commit separado e independiente de cualquier cambio funcional o de código. Esto mantiene limpia la historia de `git blame`.

---

## 6. Fase 5: Configuración de Protección en GitHub

Una vez que el Pull Request de adopción del kit sea fusionado en la rama principal (`main`), configure las protecciones formales:

1. Ingrese a **Settings -> Branches** en el repositorio en GitHub.
2. Agregue una regla de protección para `main`:
   - [x] **Require a pull request before merging** (1 aprobación requerida).
   - [x] **Require status checks to pass before merging** (seleccionar los checks de `CI`).
   - [x] **Require linear history** (favorece Squash & Merge).
   - [x] **Do not allow bypassing the above settings** (aplica también a administradores).
3. En **Settings -> General -> Pull Requests**:
   - [x] Permitir solo **Allow squash merging** (o Rebase).
   - [x] Marcar **Automatically delete head branches**.

---

## 7. Verificación Final de Adopción

Ejecute nuevamente la auditoría para certificar el cumplimiento:

```bash
./scripts/check-repo.sh /ruta/al/repo-destino
```

Si el resultado reporta `Result: PASSED`, el repositorio cuenta formalmente con un estándar de ingeniería de primer nivel.

---

## Navegación

- Anterior: [09 - Guía de Licencias de Software](09-licencias.md)
- Volver al [README principal](../README.md)
