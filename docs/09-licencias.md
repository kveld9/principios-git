# 09 - Guía de Licencias de Software y Propiedad Intelectual

La elección de una licencia define los derechos legales de uso, modificación, distribución y comercialización
que el autor otorga al público.

> [!IMPORTANT]
> **Sin archivo LICENSE = Todos los derechos reservados**: Según el Convenio de Berna sobre propiedad intelectual,
> la ausencia de una licencia no convierte al código en dominio público. Por el contrario, reserva legalmente todos
> los derechos al autor original, impidiendo que terceros puedan legalmente clonarlo, ejecutarlo, compilarlo o
> enviar contribuciones.

---

## 1. Clasificación de Licencias de Software Libre y Código Abierto

Las licencias aprobadas por la OSI (*Open Source Initiative*) se dividen fundamentalmente en dos categorías:
**permisivas** y **recíprocas (copyleft)**.

```text
                                 LICENCIAS OPEN SOURCE
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
          Permisivas (Laxas)                           Copyleft (Recíprocas)
     (Permiten código cerrado derivado)             (Exigen que derivados sean libres)
           ├── MIT (Mínima y popular)                     ├── Débil: MPL-2.0 / LGPLv3
           ├── Apache-2.0 (Patentes explícitas)           ├── Fuerte: GPLv3
           └── BSD-3-Clause (Protección de marca)         └── Red / SaaS: AGPLv3
```

---

## 2. Comparativa Detallada de las Licencias Principales

| Licencia | Categoría | Exige Compartir Derivados | Concesión Explícita de Patentes | Obliga a Liberar Código en SaaS | Caso de Uso Ideal |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MIT** | Permisiva | No | No | No | Máxima adopción, utilidades, librerías universales, proyectos educativos. |
| **Apache 2.0** | Permisiva | No | **Sí** | No | Proyectos corporativos, SDKs, infraestructuras donde las patentes son un riesgo. |
| **BSD 3-Clause** | Permisiva | No | No | No | Proyectos académicos o de sistemas operativos que prohíben usar el nombre del autor con fines publicitarios. |
| **MPL 2.0** | Copyleft Débil | Sí (a nivel de archivo) | **Sí** | No | Componentes o módulos que deben permanecer libres pero integrarse con software propietario sin infectar el resto. |
| **GPLv3** | Copyleft Fuerte | **Sí** (todo el binario/link) | **Sí** | No | Aplicaciones de escritorio o utilidades donde se busca garantizar que nadie cierre el código. |
| **AGPLv3** | Copyleft de Red | **Sí** | **Sí** | **Sí** | Servicios web, bases de datos o plataformas en la nube donde se busca evitar que proveedores ofrezcan el software como SaaS propietario sin contribuir cambios. |

---

## 3. Matriz de Decisión: ¿Qué Licencia Elegir?

1. **"Quiero que cualquier persona o empresa use, modifique y venda mi código con la menor fricción posible":**
   - Elija **MIT** (la licencia provista por defecto en este kit).
2. **"Quiero permitir uso comercial libre, pero requiero protección explícita contra demandas de patentes":**
   - Elija **Apache 2.0**.
3. **"Quiero una aplicación que siempre sea libre; si alguien la mejora y la distribuye, debe compartir el código fuente":**
   - Elija **GPLv3**.
4. **"Estoy creando un servicio o backend en la nube y no quiero que empresas de hosting ofrezcan mi trabajo como
   servicio privativo sin aportar código":**
   - Elija **AGPLv3**.

---

## 4. Personalización del Archivo `LICENSE` en este Kit

Por defecto, este kit incluye la licencia **MIT** en [`LICENSE`](../LICENSE) con los siguientes marcadores de posición (*placeholders*):

```text
Copyright (c) [YEAR] [OWNER]
```

### Pasos para Configurar su Licencia

1. Abra el archivo `LICENSE` en la raíz.
2. Reemplace `[YEAR]` con el año actual (ejemplo: `2026`).
3. Reemplace `[OWNER]` con su nombre completo, pseudónimo habitual o razón social de su organización (ejemplo: `Acme Corporation`).
4. Si decide utilizar otra licencia (como Apache 2.0 o GPLv3), reemplace el contenido completo del archivo `LICENSE`
   con el texto oficial correspondiente obtenido de [choosealicense.com](https://choosealicense.com/).

---

## Navegación

- Anterior: [08 - Seguridad y Vulnerabilidades](08-seguridad.md)
- Siguiente: [10 - Guía de Adopción en Repositorios Existentes](10-adopcion.md)
- Volver al [README principal](../README.md)
