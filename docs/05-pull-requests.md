# 05 - Flujo de Pull Requests y Revisiones de Código

El Pull Request (PR) es el punto formal de control de calidad, verificación de seguridad y transferencia
de conocimiento en un repositorio. Un buen proceso de PR previene la introducción de deuda técnica y fallos
en producción sin asfixiar la agilidad del equipo.

---

## 1. El Ciclo de Vida del Pull Request

```text
1. Desarrollo Local y Auto-Revisión
          │
          ▼
2. Apertura de PR con Plantilla Estructurada
          │
          ▼
3. Validación Automatizada (CI Checks: Linters, Tests, Security)
          │
          ▼
4. Revisión de Código por Pares (Peer Review)
          │
          ├── [Solicitud de Cambios] ──► Ajustes Locales ──► Push a la Rama
          │
          ▼ (Aprobado)
5. Fusión (Squash & Merge o Rebase) y Eliminación de Rama
```

---

## 2. Preparación y Auto-Revisión (Self-Review)

Antes de solicitar la revisión de otro desarrollador o mantenedor, el autor debe realizar una auto-revisión exhaustiva:

1. **Inspección del Diff**: Examinar `git diff origin/main...HEAD`. Verificar que no existan:
   - Archivos temporales o de configuración local.
   - Sentencias de depuración (`console.log`, `println!`, breakpoints).
   - Espacios en blanco innecesarios o saltos de línea modificados masivamente.
2. **Rebase con `main`**: Si la rama tiene varios días de antigüedad, actualizarla mediante
   `git fetch origin && git rebase origin/main` para garantizar que los tests corran sobre el estado real de producción.
3. **Completar la Plantilla**: Rellenar de forma honesta y técnica todos los campos de [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md).

---

## 3. Guía de Revisión de Código (Code Review)

### Responsabilidades del Revisor

El revisor debe enfocar su atención en lo que las máquinas no pueden detectar automáticamente:

- **Correctitud y Lógica**: ¿El algoritmo cubre los casos borde? ¿Hay riesgo de desbordamiento, división por
  cero o punteros nulos?
- **Concurrencia**: ¿Existen condiciones de carrera o bloqueos mutuos (*deadlocks*)?
- **Fuga de Recursos**: ¿Se cierran adecuadamente descriptores de archivo, conexiones de red o transacciones
  de base de datos?
- **Seguridad**: ¿Las entradas del usuario están sanitizadas? ¿Se respetan los principios de menor privilegio?
- **Mantenibilidad**: ¿La complejidad ciclomática es razonable? ¿Se respetó el principio de única fuente de verdad (SSOT)?

> [!TIP]
> **No gastar tiempo en discusiones cosméticas**: El formateo de espacios, sangrías o comillas dobles vs simples
> debe ser resuelto por `.editorconfig` y linters automatizados en el CI, no por revisores humanos.

### Responsabilidades del Autor

- Responder con argumentos técnicos basados en evidencia empírica.
- Si se sugiere una simplificación, evaluarla objetivamente sin apego emocional al código original.
- Si un cambio es inviable por restricciones técnicas fuera del alcance, documentar la razón con claridad.

---

## 4. Comparativa de Estrategias de Fusión (Merge Strategies)

GitHub ofrece tres métodos para fusionar un Pull Request. La política de este kit favorece
**Squash and Merge** o **Rebase and Merge**:

```text
            A ─── B ─── C  (feature)
           /
... ── 1 ── 2 ────────────────────► main
```

### A. Squash and Merge (Recomendado por defecto)

- **Comportamiento**: Condensa todos los commits de la rama del PR (`A`, `B`, `C`) en un único commit atómico nuevo en `main`.
- **Ventajas**: El historial de `main` se mantiene perfectamente lineal y limpio. Los commits de desarrollo
  iterativo intermedio ("oops typo", "wip") quedan ocultos sin ensuciar la historia principal.
- **Configuración recomendada**: Título del commit = Título del PR (`PR_TITLE`);
  cuerpo del commit = Descripción del PR (`PR_BODY`).

### B. Rebase and Merge

- **Comportamiento**: Aplica linealmente cada commit individual (`A`, `B`, `C`) al final de `main` sin
  crear un commit de merge.
- **Cuándo usar**: Solo cuando el autor ha construido intencionalmente una serie de commits atómicos
  verticales y pulidos que aportan valor histórico individualmente.

### C. Create a Merge Commit (Prohibido)

- **Comportamiento**: Genera un commit no lineal con dos padres (`Merge pull request #45 from...`).
- **Problema**: Introduce "nudos topológicos" en el grafo de Git, dificulta la lectura con `git log` y
  complica la detección de regresiones con `git bisect`.

---

## 5. Automatización de Cierre y Limpieza de Ramas

### Vinculación de Issues

Al describir el PR, utilice las palabras clave de GitHub en la descripción para cerrar automáticamente las incidencias resueltas:

- `Fixes #123` (para correcciones de bugs)
- `Closes #456` (para requerimientos generales)
- `Resolves #789`

### Eliminación Automática de Ramas

Activar en los ajustes del repositorio:
`Automatically delete head branches` (`delete_branch_on_merge: true`).
Esto previene la acumulación de ramas huérfanas en el repositorio remoto una vez que su código ya fue incorporado a `main`.

---

## Navegación

- Anterior: [04 - Convención de Commits y Atomicidad](04-commits.md)
- Siguiente: [06 - Versiones y Lanzamientos (SemVer y Changelog)](06-releases.md)
- Volver al [README principal](../README.md)
