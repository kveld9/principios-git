# 11 - Convenciones de Estilo y Estándares Profesionales de Código

La consistencia de estilo y la disciplina de calidad reducen la sobrecarga cognitiva durante las revisiones de código, previenen defectos sutiles en producción y garantizan la portabilidad del repositorio entre diferentes sistemas operativos, entornos de CI y herramientas de análisis estático.

Este documento formaliza las reglas transversales de estilo, calidad y buenas prácticas de ingeniería que deben regir cualquier contribución técnica en el proyecto.

---

## 1. Política Estricta sobre Emojis

Para garantizar la fiabilidad del pipeline y preservar un entorno de ingeniería riguroso, el uso de emojis está estrictamente acotado según la superficie del repositorio.

### Superficies de Prohibición Categórica
Los emojis están **terminantemente prohibidos** en:
- Código fuente de cualquier lenguaje.
- Scripts de automatización y mantenimiento (`scripts/*.sh`, utilitarios).
- Archivos de configuración (`.yml`, `.yaml`, `.json`, `.toml`, `.ini`, `.editorconfig`, etc.).
- Mensajes y registros de terminal (CLI logs, `stdout`, `stderr`).
- Flujos de trabajo de Integración Continua (GitHub Actions workflows).
- Nombres de archivos, ramas y directorios.
- Mensajes de commit (títulos, cuerpos y pies de Conventional Commits).

### Superficies Permitidas Exclusivamente
Los emojis se permiten únicamente en:
- Documentación técnica orientada a personas (`README.md`, guías en `docs/**`).
- Portales de documentación estática y notas de versión dirigidas a usuarios finales (`CHANGELOG.md` y GitHub Releases).

### Justificación Técnica
1. **Determinismo en terminales headless y CI**: Terminales mínimas de servidores, entornos de CI sin locale UTF-8 explícito y consolas de ciertos sistemas operativos fallan al decodificar caracteres multibyte fuera del Plano Multilingüe Básico (BMP), corrompiendo pipes o interrumpiendo scripts de parsing.
2. **Robustez en herramientas de automatización**: Expresiones regulares, scripts de ingesta de logs y herramientas forenses (`grep`, `awk`, `sed`, `git log --oneline`) sufren degradación o errores de delimitación ante secuencias de variación Unicode (VS16) y caracteres de unión ZWJ (Zero Width Joiner).
3. **Sobriedad y densidad informativa**: Los registros de ejecución de producción y el historial de Git deben priorizar la precisión técnica sin elementos ornamentales que dificulten la búsqueda de patrones.

---

## 2. Convenciones de Nomenclatura (Naming Conventions)

Los nombres de identificadores, archivos y artefactos deben ser autoexplicativos, precisos y coherentes.

### Nombres de Archivos y Directorios
- Utilizar **`kebab-case`** en minúsculas para scripts, documentación técnica y recursos generales (`check-repo.sh`, `01-principios.md`).
- Respetar las excepciones históricas de la raíz del proyecto exigidas por plataformas como GitHub (`README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`).
- Si el ecosistema de un lenguaje impone una convención propia para módulos de código (como `PascalCase` para componentes React o clases en ciertos frameworks), mantener uniformidad absoluta dentro del árbol de código.

### Identificadores y Símbolos
- **Claridad sobre brevedad**: Elegir identificadores que revelen intención (`calculate_retry_delay` en lugar de `calc_del`).
- **Prohibición de variables de una sola letra**: Quedan prohibidas salvo índices aritméticos de recorrido en bucles muy reducidos (`i`, `j`).
- **Predicados booleanos**: Nombrar variables y funciones booleanas con prefijos interrogativos o de estado (`isValid`, `hasPermission`, `canRetry`, `shouldFlush`).
- **Constantes inmutables**: Definir constantes globales y valores inmutables en **`SCREAMING_SNAKE_CASE`** (`MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_MS`).
- **Evitar redundancias de contexto**: En un objeto o estructura `User`, utilizar `user.id` o `user.name`, nunca `user.userId` o `user.userName`.

---

## 3. Eliminación de Números y Cadenas Mágicas

Ningún valor numérico o literal con significado funcional debe incrustarse directamente en la lógica de negocio sin un identificador semántico.

### Reglas
- **Constantes con significado**: Extraer valores escalares a constantes nombradas antes de utilizarlos en comparaciones, operaciones o temporizadores.
- **Centralización de literales repetidos**: Si una cadena de texto, ruta relativa, clave de diccionario o mensaje de error se utiliza en más de un punto, debe definirse en un punto canónico.
- **Configuración desacoplada**: Valores sujetos a variación entre entornos (tiempos de espera, límites de paginación, URLs de servicios) deben residir en configuración externa, nunca quemados en el código.

---

## 4. Funciones Pequeñas y Responsabilidad Única

Cada función, método o procedimiento debe resolver un único problema lógico en un único nivel de abstracción.

### Complejidad Ciclomática y Tamaño
- Mantener las funciones breves y enfocadas. Si una función supera los 20-30 renglones o acumula múltiples bifurcaciones anidadas, es candidata prioritaria para descomposición.
- **Cláusulas de Guarda (Guard Clauses)**: Validar precondiciones y retornar o abortar inmediatamente al inicio de la función. Evitar el anti-patrón de flecha (*arrow anti-pattern*) producido por anidamiento profundo de bloques `if/else`.
- **Extracción de funciones auxiliares**: Aislar transformaciones de datos o cálculos matemáticos en funciones puras auxiliares sin efectos secundarios.

---

## 5. Manejo de Errores Explícito y Filosofía Fail-Loud

Un fallo silencioso es el origen de corrupciones de datos y comportamientos erráticos difíciles de diagnosticar.

### Principios Fundamentales
1. **Prohibido enmascarar errores**:
   - Cero bloques de captura de excepciones vacíos (`catch (e) {}` o `except Exception: pass`).
   - Cero silenciamiento indiscriminado de salidas en scripts mediante `|| true` o redirecciones ciegas a `/dev/null` para encubrir comandos defectuosos.
   - Cero omisión deliberada de errores devueltos por el sistema o APIs (`_ = err`).
2. **Filosofía Fail-Loud**: Ante una condición inesperada, violación de invariantes o falla en un paso crítico, el sistema debe fallar de inmediato y de forma ruidosa, interrumpiendo el flujo antes de propagar estados inválidos.
3. **Contexto enriquecido en errores**: Todo mensaje de error debe responder a tres interrogantes: ¿qué falló?, ¿qué entrada o estado lo provocó?, y ¿cuál fue la causa raíz detectable?

> [!IMPORTANT]
> Este estándar complementa directamente las directrices de ejecución de pipelines documentadas en [07 - Integración Continua (CI)](07-ci.md#1-principio-de-menor-privilegio-security-first-ci).

---

## 6. Prohibición de Código Comentado Muerto

El árbol de código debe contener únicamente lógica activa en producción o pruebas vigentes.

### Reglas
- **Git como única memoria histórica**: Nunca conservar bloques de código deshabilitados mediante comentarios bajo la justificación de "por si se necesita después". El historial de commits de Git es la herramienta diseñada para consultar implementaciones anteriores.
- **Eliminación sistemática**: Durante refactorizaciones o sustitución de algoritmos, el código obsoleto debe borrarse por completo del archivo.
- **Comentarios orientados a la intención**: Los comentarios deben explicar el *por qué* de una decisión no obvia o una restricción externa de hardware/negocio, nunca relatar lo que el código ya describe explícitamente ni contener código muerto.

---

## 7. Principio DRY con Criterio (Don't Repeat Yourself)

La duplicación indiscriminada genera inconsistencias de mantenimiento; sin embargo, la abstracción prematura produce sistemas rígidos e incomprensibles.

### Aplicación Práctica
- **Duplicación de conocimiento vs coincidencia estructural**: El principio DRY busca unificar el conocimiento de negocio y las fuentes de verdad (SSOT). Dos bloques de código que lucen estructuralmente idénticos pero representan conceptos de dominio distintos no deben fusionarse precipitadamente.
- **La regla de tres**: Antes de extraer una abstracción genérica o framework interno, esperar a observar al menos tres instancias reales de duplicación idéntica.
- **Preferencia por el desacoplamiento**: Una duplicación controlada y local es preferible a una abstracción incorrecta que acople fuertemente módulos independientes.

---

## Navegación

- Anterior: [10 - Guía de Adopción e Integración](10-adopcion.md)
- Siguiente: [12 - Modularización y Arquitectura de Componentes](12-modularizacion.md)
- Volver al [README principal](../README.md)
