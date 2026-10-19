# 04 - Convención de Commits y Atomicidad

Los mensajes de commit son la documentación más duradera de un proyecto. El código fuente muestra el estado presente del sistema, pero el historial de commits es el único registro que explica la intención del autor, las alternativas descartadas y el contexto de las decisiones críticas.

Este proyecto sigue estrictamente la especificación **Conventional Commits v1.0.0** y el principio de **atomicidad estricta**.

---

## 1. La Regla de Oro: Atomicidad Estricta

Un commit atómico representa **una única unidad lógica indivisible de cambio**.

### El Test de Atomicidad
Un commit es atómico si y solo si:
1. **Compila y pasa pruebas**: El repositorio no queda roto si se hace checkout directamente en ese hash.
2. **Es revertible limpiamente**: Puede revertirse con `git revert <hash>` sin desmantelar código o características no relacionadas.
3. **Se puede describir en una sola oración sin usar conjunciones**: Si el mensaje necesita decir *"agrega autenticación y arregla padding del botón y actualiza dependencias"*, son al menos tres commits distintos.

### Corte Vertical (Vertical Slice)
Un commit atómico no separa artificialmente el frontend del backend cuando forman parte de la misma funcionalidad. Debe incluir verticalmente:
- La lógica interna.
- Las pruebas asociadas.
- La documentación afectada por ese cambio específico.

---

## 2. Estructura de Conventional Commits

```text
<tipo>[alcance opcional]: <descripción en imperativo>

[cuerpo explicativo opcional: contexto técnico, motivación y trade-offs]

[pie opcional: referencias a issues y breaking changes]
```

### Tipos Permitidos

| Tipo | Propósito | Ejemplo |
| :--- | :--- | :--- |
| `feat` | Nueva funcionalidad visible para el usuario o API | `feat(auth): add rate limiting to login endpoint` |
| `fix` | Corrección de un defecto o comportamiento anómalo | `fix(parser): prevent panic on malformed JSON tokens` |
| `docs` | Cambios exclusivos en documentación | `docs(readme): clarify local installation prerequisites` |
| `refactor` | Cambio de código que no altera el comportamiento externo | `refactor(db): extract connection pool initialization` |
| `perf` | Optimización de rendimiento cuantificable | `perf(router): replace linear regex matching with trie` |
| `test` | Incorporación o corrección de pruebas sin tocar código de producción | `test(auth): add boundary tests for token expiration` |
| `build` | Cambios que afectan el sistema de empaquetado o dependencias | `build(deps): bump openssl from 3.1 to 3.2` |
| `ci` | Cambios en flujos de integración continua o scripts de automatización | `ci(actions): pin checkout action to v4 with sha` |
| `chore` | Tareas rutinarias que no modifican código ni pruebas | `chore: update license copyright year to 2026` |
| `revert` | Reversión de un commit previo | `revert: "feat(api): enable experimental websocket support"` |

---

## 3. Reglas de Estilo para el Mensaje

1. **Idioma Estrictamente en Inglés**: Todo mensaje de commit debe redactarse en inglés técnico. Esto maximiza la interoperabilidad global y permite herramientas automatizadas de release y changelog.
2. **Modo Imperativo en Tiempo Presente**:
   - Correcto: `fix: handle timeout on remote connection`
   - Incorrecto: `fixed timeout` o `fixing timeouts` o `handles timeout`
3. **Límite de Longitud**:
   - Título: Máximo 72 caracteres.
   - Sin punto final en el título.
4. **Cuerpo Técnico Detallado**:
   - Explica el *por qué* y no solo el *qué*.
   - Describe efectos secundarios relevantes, restricciones de hardware o razones por las que se descartó una alternativa obvia.
5. **Cero Atribución de Herramientas**: No contaminar los mensajes con pies automáticos tipo `Co-authored-by: bot` o slogans promocionales de asistentes de IA. El autor y committer deben ser identidades válidas y rastreables.
6. **Prohibición Estricta de Emojis**: Queda vetado el uso de emojis en títulos, cuerpos o pies de commits (por ejemplo, redactar `feat: add login` en lugar de `feat: 🚀 add login`). Esto asegura compatibilidad con terminales headless, herramientas de diff/patch por email y generadores deterministas de changelog (véase [11 - Convenciones de Estilo](11-estilo.md)).

---

## 4. Cambios Rompedores (Breaking Changes)

Cuando un cambio rompe la compatibilidad hacia atrás (requiere incremento de versión MAJOR en SemVer), debe indicarse explícitamente:

### Opción A: Signo de Exclamación en el Tipo
```text
feat(api)!: drop support for deprecated v1 endpoints
```

### Opción B: Pie BREAKING CHANGE
```text
feat(auth): require Ed25519 signatures for session tokens

BREAKING CHANGE: RSA-1024 and RSA-2048 keys are no longer accepted.
Clients must migrate to Ed25519 or ECDSA P-256 before upgrading.
```

---

## 5. Ejemplos de Comparación: Malos vs Buenos Commits

### Ejemplo 1: Corrección de un Bug
- **Malo**:
  ```text
  Arreglado el bug raro
  ```
- **Bueno**:
  ```text
  fix(http): resolve race condition in websocket keepalive ping

  The ping timer was not cancelled when the client initiated an orderly
  close handshake, resulting in duplicate write attempts on closed sockets.
  Cancels the timer immediately upon receiving CLOSE frame.

  Fixes #142
  ```

### Ejemplo 2: Actualización de Alcance Múltiple (Anti-Patrón)
- **Malo (Mega-commit)**:
  ```text
  feat: finish user profile, fix database bug, update css and clean up code
  ```
- **Bueno (Secuencia Atómica)**:
  - Commit 1: `fix(db): add missing foreign key index on user_sessions`
  - Commit 2: `feat(profile): implement avatar upload endpoint`
  - Commit 3: `style(profile): align form padding with design tokens`
  - Commit 4: `docs(api): document avatar upload payload constraints`

---

## Navegación

- Anterior: [03 - Estrategias de Ramas (Branching)](03-branching.md)
- Siguiente: [05 - Flujo de Pull Requests y Revisiones](05-pull-requests.md)
- Volver al [README principal](../README.md)
