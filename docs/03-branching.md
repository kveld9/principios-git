# 03 - Estrategias de Ramas (Branching)

Una estrategia de ramificación caótica produce "el infierno de la integración": ramas de larga duración
que divergen durante semanas, provocando conflictos de merge masivos, pérdida accidental de código y bloqueos
en los despliegues.

Este documento formaliza la política de ramas recomendada: **Trunk-Based Development con ramas de vida corta**
(variante optimizada de GitHub Flow).

---

## 1. Comparativa de Modelos de Ramificación

### Git Flow Clásico vs GitHub Flow Moderno

| Criterio | Git Flow Tradicional | Trunk-Based / GitHub Flow (Estándar) |
| :--- | :--- | :--- |
| **Ramas principales** | `master`, `develop`, `release/*`, `hotfix/*` | `main` (única fuente de verdad) |
| **Vida útil de ramas** | Semanas o meses | Horas o máximo 2-3 días |
| **Frecuencia de integración** | Baja (al final del sprint) | Continua (múltiples veces al día) |
| **Riesgo de conflictos** | Extremo (requiere "merge days") | Casi nulo (cambios atómicos continuos) |
| **Alineación con CI/CD** | Pobre (frecuentes estados no desplegables) | Total (cada commit en `main` es desplegable) |

**Conclusión técnica**: A menos que se mantengan múltiples versiones incompatibles en producción simultáneamente
(como versiones legacy de sistemas operativos embebidos o librerías corporativas con soporte extendido), el
modelo Git Flow clásico introduce sobrecarga burocrática injustificada. Se adopta el modelo Trunk-Based /
GitHub Flow.

---

## 2. Nomenclatura Estricta de Ramas

Toda rama creada fuera de `main` debe seguir el formato:

```text
<tipo>/<alcance-o-identificador-kebab-case>
```

### Tipos Permitidos

- `feat/`: Nueva funcionalidad, endpoint o capacidad (`feat/oauth2-login`, `feat/export-csv`).
- `fix/`: Corrección de un defecto o fallo detectado (`fix/null-pointer-session`, `fix/db-connection-leak`).
- `refactor/`: Reestructuración de código sin alterar comportamiento (`refactor/extract-auth-middleware`).
- `perf/`: Optimización cuantificable de rendimiento (`perf/batch-sqlite-inserts`).
- `docs/`: Actualización exclusiva de documentación (`docs/update-install-guide`).
- `chore/`: Tareas de mantenimiento, actualización de dependencias o CI (`chore/update-actions-node20`).

### Patrones Prohibidos

- Nombres vagos o personales: `parche`, `prueba`, `mi-rama`, `dev-juan`, `fix-bug`.
- Caracteres incompatibles: espacios, tildes, signos de puntuación extraños o mayúsculas (`feat/Mi_Super_Fix!`).

---

## 3. Ciclo de Vida de una Rama

```text
       (git checkout -b feat/x)
main  ───────────────────────────────────────────► (Merge Squash) ──► main
        \                                         /
         └── Commit 1 ──► Commit 2 ──► CI Pass ──┘
```

1. **Creación**: Partir siempre del estado más reciente de la rama principal:

   ```bash
   git checkout main
   git pull --ff-only origin main
   git checkout -b feat/nueva-capacidad
   ```

2. **Desarrollo**: Ejecutar commits atómicos que compilen y pasen validaciones en local.
3. **Sincronización Continua**: Si la rama dura más de 24 horas o `main` avanzó significativamente,
   rebasar localmente para resolver conflictos temprano:

   ```bash
   git fetch origin
   git rebase origin/main
   ```

4. **Publicación y PR**: Subir la rama y abrir el Pull Request correspondiente.
5. **Merge y Eliminación**: Una vez aprobado y superado el CI, fusionar a `main` y eliminar la rama
   remota y local inmediatamente para no dejar ramas muertas ("stale branches").

---

## 4. Políticas de Protección de Ramas (Branch Protection)

La rama `main` debe ser declarada como rama protegida en GitHub.

### Invariantes de Protección

1. **Prohibido el Push Directo**: Nadie (incluidos administradores) debe empujar commits directamente a
   `main`. Todo cambio debe ingresar vía Pull Request.
2. **Revisión de Código Obligatoria**: Al menos una aprobación (`required_approving_review_count: 1`)
   antes de autorizar el merge.
3. **CI en Verde Requerido**: Los checks de GitHub Actions deben reportar estado exitoso de forma estricta (`strict: true`).
4. **Historial Lineal Requerido**: Prohibir merges recursivos de 3 vías con commits tipo `Merge branch 'main' of ...`.
   El historial debe avanzar limpiamente mediante **Squash and merge** o **Rebase and merge**.
5. **Prohibición de Force Push**: Prohibir `git push --force` sobre `main` para salvaguardar la inmutabilidad histórica.

La especificación completa de estas reglas se encuentra lista para aplicar en [`.github/settings.example.yml`](../.github/settings.example.yml).

---

## Navegación

- Anterior: [02 - Estructura Estándar de Repositorio](02-estructura-repo.md)
- Siguiente: [04 - Convención de Commits y Atomicidad](04-commits.md)
- Volver al [README principal](../README.md)
