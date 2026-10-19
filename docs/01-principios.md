# 01 - Principios Fundamentales de Ingeniería y Control de Versiones

Un repositorio de Git no es un respaldo pasivo ni un basurero de código temporal; es el registro histórico, legal y técnico de la evolución de un sistema de software. Cada commit, rama y etiqueta constituye un documento auditable que debe explicar con precisión técnica qué cambió, por qué cambió y cómo verificarlo.

Este documento establece los principios de ingeniería aplicados en este kit de estándares.

---

## 1. El Historial como Registro de Auditoría

Un historial de Git limpio permite:
- **Localizar regresiones con precisión** mediante `git bisect`. Si un commit contiene cinco cambios distintos, identificar el commit culpable no revela qué línea o decisión introdujo el fallo.
- **Auditoría forense y de seguridad**: determinar cuándo y por qué se alteró un algoritmo criptográfico, una dependencia o un flujo de autorización.
- **Reversión quirúrgica**: ejecutar `git revert <hash>` sin desmantelar funcionalidades no relacionadas ni provocar conflictos masivos.

### Invariantes del Historial
1. **Compilabilidad y coherencia**: Cada commit en la rama principal (`main`) debe compilar, superar las pruebas automatizadas y dejar el sistema en un estado funcional.
2. **Determinismo**: Dos desarrolladores o entornos de CI que clonen el repositorio en el mismo commit deben obtener exactamente el mismo comportamiento binario y de ejecución.
3. **Linealidad preferente**: Un historial lineal o con ramas de integración limpias minimiza nudos topológicos y facilita la lectura cronológica.

---

## 2. Disciplina Estricta de Alcance (Scope Discipline)

La causa primaria de deuda técnica en control de versiones es el "acoplamiento oportunista": modificar dependencias, corregir formato o refactorizar archivos ajenos mientras se implementa un requerimiento funcional.

### Separación de Capas de Trabajo
- **TASK SCOPE**: El conjunto delimitado de archivos y componentes necesarios para cumplir el requerimiento actual.
- **COMMIT SCOPE**: La unidad atómica individual de ese alcance (por ejemplo, el modelo de datos, la lógica del servicio o la interfaz).
- **FOREIGN WORK**: Cualquier archivo modificado o no rastreado presente en el árbol de trabajo previo al inicio de la tarea. No debe mezclarse ni commitearse por accidente.

```text
Árbol de Trabajo
├── Modificaciones previas no relacionadas (FOREIGN WORK -> Preservar / Omitir de stage)
└── Cambios del requerimiento actual (TASK SCOPE)
    ├── Unidad 1: Fix validación entrada -> Commit 1 (fix)
    └── Unidad 2: Actualización de documentación -> Commit 2 (docs)
```

### Reglas de Operación
1. **Prohibido el bundle de formateo y funcionalidad**: Si un archivo requiere reindentación o linteo general, ese formateo se realiza en un commit independiente (`style` o `refactor`), nunca mezclado con lógica de negocio.
2. **Revisión obligatoria del diff antes de indexar**: Antes de ejecutar `git add`, verificar qué líneas cambiaron con `git diff` para evitar incluir artefactos temporales, saltos de línea indeseados o depuraciones (`console.log`, `print`).

---

## 3. Principio del Cambio Mínimo

Toda modificación debe aspirar al cambio más pequeño que:
1. Resuelva el problema técnico planteado.
2. Preserve el comportamiento preexistente y los invariantes del sistema.
3. No introduzca abstracciones prematuras ni sobreingeniería.
4. No requiera limpieza colateral en componentes no relacionados.

Si un cambio mayor o refactor estructural es indispensable, debe justificarse empíricamente demostrando por qué una alternativa de menor impacto es insuficiente o técnicamente inviable.

---

## 4. Evidencia Empírica y Reproducibilidad

Ningún cambio se considera concluido sin validación observable.

```text
JERARQUÍA DE EVIDENCIA TÉCNICA:
REPRODUCCIÓN DIRECTA / EJECUCIÓN
  ↓
PRUEBA AUTOMATIZADA CONTROLADA
  ↓
OBSERVACIÓN EN RUNTIME / LOGS
  ↓
ANÁLISIS ESTÁTICO / LINTERS
  ↓
INFERENCIA TÉCNICA
  ↓
HIPÓTESIS
```

- Si se reporta o soluciona un bug, debe existir un procedimiento exacto para reproducirlo antes del fix y confirmar su ausencia tras el fix.
- Si se afirma una mejora de rendimiento, debe respaldarse con métricas reproducibles o benchmarks controlados, no con suposiciones teóricas.

---

## 5. Mantenibilidad y Dependencia del Entorno (Anti-Hardcoding)

Un repositorio debe ser portable entre máquinas de desarrollo, entornos de CI y contenedores de producción.

- **Cero rutas absolutas locales**: No incorporar rutas dependientes del sistema de archivos local (`/home/usuario/...` o `C:\Users\...`). Las rutas relativas o variables de entorno estándar deben gobernar la configuración.
- **Única fuente de verdad (SSOT)**: Constantes de versión, identificadores de red, puertos y configuraciones deben definirse en un punto canónico (archivo de configuración o manifiesto) y ser derivados por el resto del sistema, evitando duplicación manual.

---

## 6. Documentación Sincronizada con el Código

La documentación desactualizada es peor que la ausencia de documentación: induce a errores en producción.

- Si un commit altera una bandera de línea de comandos, un endpoint de API, una variable de entorno o un paso de instalación, la documentación correspondiente (`README.md`, `docs/`, man pages) **debe actualizarse en ese mismo commit**.
- El cambio documental es parte integral de la unidad de trabajo (corte vertical), no una tarea postergable para después del despliegue.

---

## Navegación

- Siguiente: [02 - Estructura Estándar de Repositorio](02-estructura-repo.md)
- Volver al [README principal](../README.md)
