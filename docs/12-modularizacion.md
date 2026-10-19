# 12 - Modularización y Arquitectura de Componentes

La modularización es la disciplina de descomponer un sistema de software en componentes cohesivos, autónomos y acoplados de forma débil. Una modularización adecuada permite que múltiples colaboradores desarrollen características simultáneamente sin bloqueos, facilita el reemplazo de subsistemas y garantiza que los errores queden contenidos sin provocar fallos en cascada.

Este documento establece las directrices arquitectónicas para organizar el código y definir fronteras claras entre módulos en cualquier proyecto.

---

## 1. Principio de Responsabilidad por Módulo

Un módulo es una unidad lógica de empaquetado (directorio, librería, paquete o subsistema) que agrupa elementos relacionados con una frontera explícita.

### Invariantes de Modularidad
1. **Alta Cohesión Interna**: Todos los archivos y funciones dentro de un módulo deben colaborar estrechamente para resolver un único subproblema del dominio del sistema. Si una pieza del módulo cambia, es porque el requerimiento de ese subproblema cambió.
2. **Bajo Acoplamiento Externo**: Un módulo debe conocer lo mínimo indispensable sobre el funcionamiento interno de otros módulos. Las interacciones entre ellos deben reducirse al mínimo necesario para cumplir el flujo de negocio.
3. **Una Sola Razón para Cambiar**: Si un módulo acumula modificaciones tanto cuando cambia la pasarela de pagos como cuando cambia el formato de reportes de clientes, el módulo sufre de acoplamiento espurio y debe dividirse.

---

## 2. Contratos e Interfaces Explícitas

Los módulos deben comunicarse exclusivamente a través de interfaces bien definidas y estables, ocultando sus detalles de implementación internos.

### Encapsulamiento y Fronteras de Visibilidad
- **Superficie Pública Mínima**: Cada módulo debe exponer únicamente los puntos de entrada, tipos o firmas estrictamente requeridos por sus consumidores externos. Las estructuras internas, algoritmos auxiliares y manejadores privados deben permanecer inaccesibles desde fuera del módulo.
- **Invariancia del Contrato**: Los consumidores del módulo deben depender de abstracciones o contratos (APIs públicas), nunca de detalles de persistencia (como una consulta SQL directa a tablas de otro módulo) ni de variables globales mutables.
- **Evolución sin Ruptura**: Si se refactoriza o reemplaza la implementación interna de un módulo sin modificar sus contratos públicos, ningún consumidor externo debe requerir ajustes.

---

## 3. Dependencias Unidireccionales y Prevención de Ciclos

El grafo de dependencias entre los módulos de un sistema debe ser estrictamente un **Grafo Acíclico Dirigido (DAG)**.

```text
CORRECTO (Grafo Acíclico Dirigido - DAG):
[Interfaz de Usuario / CLI] ──► [Casos de Uso / Dominio] ──► [Servicios / Persistencia]

INCORRECTO (Dependencia Circular):
[Módulo A] ──► [Módulo B] ──► [Módulo C] ──► [Módulo A]  (Fallo arquitectónico)
```

### Reglas de Dependencia
1. **Flujo Unidireccional**: Las dependencias siempre deben apuntar en una única dirección. Está estrictamente prohibido que un módulo `A` dependa de un módulo `B` si `B` a su vez depende directa o indirectamente de `A`.
2. **Impacto de los Ciclos**:
   - Imposibilitan compilar o empaquetar módulos de forma aislada.
   - Provocan condiciones de carrera y deadlocks en el orden de inicialización de runtime.
   - Impiden la reutilización independiente de cualquier módulo del ciclo.
3. **Resolución de Ciclos**: Ante un ciclo de dependencias, debe aplicarse una de dos soluciones arquitectónicas:
   - **Inversión de dependencias**: Introducir una interfaz o contrato intermedio.
   - **Extracción de un tercer módulo**: Mover los tipos o funciones compartidas a un módulo base común del cual dependan los dos anteriores.

---

## 4. Límites de Tamaño y Criterios para Dividir Archivos

Los umbrales cuantitativos de líneas son orientativos, pero sirven como detectores tempranos de acumulación excesiva de responsabilidades.

### Umbrales Prácticos Recomendados
- **Archivo individual**: Archivos que superen las 300-500 líneas de código deben ser objeto de escrutinio técnico para identificar oportunidades de modularización.
- **Módulo o paquete**: Módulos con más de 7-10 archivos densos suelen ser candidatos para subdividirse en submódulos temáticos.

### Señales Técnicas para Dividir un Archivo
Más allá de la cantidad de renglones, un archivo debe dividirse de inmediato si presenta cualquiera de los siguientes síntomas:
1. **Imposibilidad de resumir su rol en una frase concisa**: Si la descripción del archivo contiene conjunciones ("valida usuarios, genera tokens JWT y envía correos de bienvenida"), contiene más de una responsabilidad.
2. **Mezcla de niveles de abstracción**: El archivo combina simultáneamente orquestación de alto nivel con detalles de bajo nivel (como manipulación directa de sockets, serialización cruda de bytes o formateo de strings).
3. **Frecuentes conflictos de merge concurrentes**: Múltiples desarrolladores colisionan habitualmente en el mismo archivo mientras trabajan en tareas funcionales no relacionadas.
4. **Acumulación excesiva de importaciones dispares**: El archivo requiere decenas de librerías o dependencias de dominios heterogéneos para operar.

---

## 5. Organización del Proyecto: Por Feature vs Por Capa

La estructura de carpetas física de un repositorio debe facilitar la navegación y reflejar la modularidad de la arquitectura lógica.

### Comparativa de Patrones Organizativos

| Modelo | Definición | Adecuado para | Riesgo a Escala |
| :--- | :--- | :--- | :--- |
| **Package by Layer** (Por Capa Técnica) | Agrupar archivos por su tipo tecnológico (`controllers/`, `models/`, `views/`, `services/`). | Proyectos pequeños (< 10-15 archivos) o prototipos iniciales. | Fragmenta el conocimiento de cada feature en 4 o 5 directorios distantes, aumentando la fricción en cada cambio funcional. |
| **Package by Feature** (Por Funcionalidad) | Agrupar todos los componentes relacionados con un mismo caso de uso o dominio en un único módulo (`auth/`, `billing/`, `reports/`). | Aplicaciones medianas, grandes y sistemas en producción sostenida. | Requiere disciplina inicial para definir fronteras de dominio precisas. |

### Ejemplos Agnósticos de Estructura de Directorios

#### Escala Pequeña / Mediana (Por Feature o Dominio Central)
```text
src/
├── auth/
│   ├── api.ext           # Punto de entrada y controladores de autenticación
│   ├── service.ext       # Lógica de verificación de credenciales y tokens
│   ├── repository.ext    # Acceso a almacenamiento de cuentas
│   └── types.ext         # Tipos y contratos públicos del módulo
│
├── billing/
│   ├── api.ext           # Endpoints de facturación
│   ├── service.ext       # Procesamiento de pagos y cálculo impositivo
│   ├── provider.ext      # Integración con pasarelas externas
│   └── types.ext         # Contratos públicos de cobro
│
└── shared/
    ├── config.ext        # Carga de variables de entorno y configuración
    └── database.ext      # Manejador genérico de conexiones
```

#### Escala Modular Amplia (Monorepo o Subsistemas Independientes)
```text
modules/
├── identity/
│   ├── public/           # Contratos e interfaces exportables a otros módulos
│   └── internal/         # Implementación privada oculta para terceros
│
├── notification/
│   ├── public/
│   └── internal/
│
└── storage/
    ├── public/
    └── internal/
```

---

## 6. Qué NO es Modularización (Anti-Patrones Habituales)

La modularización auténtica se mide por el desacoplamiento y la claridad de fronteras, no por la cantidad de subcarpetas creadas.

### Anti-Patrones Críticos
1. **El Directorio "Cajón de Sastre" (`utils/`, `helpers/`, `common/`)**:
   - Crear una carpeta `utils/` sin cohesión semántica es una renuncia al diseño modular. Termina acumulando algoritmos de criptografía, formateadores de fechas, llamadas a red y constantes dispersas.
   - **Regla**: Todo código utilitario debe pertenecer al módulo de negocio que lo necesita o constituir un paquete especializado con nombre descriptivo (`date-formatting/`, `crypto-primitives/`).
2. **Micro-Fragmentación Prematura**:
   - Descomponer un archivo de 80 líneas en 10 archivos de 8 líneas cada uno no es modularizar; es introducir dispersión cognitiva y sobrecarga de navegación sin aportar aislamiento funcional.
3. **Módulos con Fronteras Porosas**:
   - Crear carpetas separadas pero permitir que los archivos importen directamente variables internas o estados mutables privados de otros módulos anula cualquier beneficio de modularidad.

---

## Navegación

- Anterior: [11 - Convenciones de Estilo y Calidad de Código](11-estilo.md)
- Volver al [README principal](../README.md)
