# Monorepositorio vs Multirepositorio

Fase 7: Estructura y compartición de módulos — tabla comparativa y debate

| Aspecto | Monorepositorio (Mono) | Multirepositorio (Multi) |
|---|---:|---:|
| Alcance del repo | Todo el código (varios proyectos/módulos) en un único repositorio. | Cada proyecto o módulo en su propio repositorio independiente. |
| Visibilidad del código | Alta: fácil ver y cambiar dependencias internas y módulos. | Limitada: dependencias externas requieren publicación/versionado y revisión. |
| Consistencia y coordinación | Fácil coordinación de cambios cross-cutting (refactorings, cambios de API). | Cambios que afectan a varios repos requieren coordinación entre repos/PRs y versiones. |
| Control de versiones | Un solo historial; se suelen usar herramientas de monorepo para scopes/paths. | Versionado independiente por repositorio; release management aislado. |
| CI/CD | Pipelines monolíticos o por paquete; a veces optimizados por rutas de cambio. | Pipelines independientes; puedes desplegar por separado y con distintas cadencias. |
| Escalabilidad del equipo | Bueno para equipos estrechamente integrados; puede crecer con reglas y herramientas. | Bueno para organizaciones grandes con equipos autónomos que necesitan aislamiento. |
| Aislamiento de fallos | Riesgo mayor: mal cambio puede afectar todo el repositorio si no hay controles. | Mejor aislamiento: cambios en un repo no rompen otros hasta que se integren vía versiones. |
| Gestión de dependencias internas | Más simple: referencias directas al código; refactorings en un PR. | Necesita publicación de paquetes/artifacts y compatibilidad semántica (semver). |
| Overhead operativo | Repos únicos: menor overhead de gestión (una sola política, CI). | Mayor overhead (múltiples repos, permisos, pipelines, releases). |
| Casos de uso típicos | Plataformas integradas, monolitos modulares, librerías estrechamente acopladas. | Microservicios independientes, productos con ciclos de vida distintos, equipos autónomos. |

## Debate—Ventajas y desventajas

Monorepositorio — Ventajas
- Coordinación simple: refactorings y cambios cross-cutting se hacen en un único PR.
- Reutilización y descubrimiento: es más fácil encontrar y compartir módulos internos.
- Políticas centralizadas: linters, formateo, configuración CI y políticas son más homogéneas.

Monorepositorio — Desventajas
- Escala y rendimiento: historial y tamaño del repo pueden crecer mucho; CI puede volverse lento.
- Riesgo de blast radius: errores en cambios comunes pueden afectar muchos proyectos.
- Gobernanza: mantener límites claros entre equipos y permisos puede requerir herramientas adicionales.

Multirepositorio — Ventajas
- Aislamiento y seguridad: acceso y permisos por proyecto; errores locales no rompen todo.
- Autonomía: cada equipo decide ciclo de release y stack de CI/CD.
- Escalabilidad operativa: repos pequeños más manejables y pipelines más rápidos por repo.

Multirepositorio — Desventajas
- Mayor fricción para cambios cross-cutting: implica version bumps, coordinación y PRs encadenados.
- Descubrimiento y duplicación: más riesgo de duplicar código si no hay buenas librerías internas.
- Gestión de dependencias: requiere buen sistema de versiones, registro de paquetes y compatibilidad.

## Recomendaciones prácticas
- Pequeños/medios proyectos con alta interdependencia: monorepo suele ser más productivo.
- Organizaciones grandes con equipos autónomos y productos independientes: multirepo aporta aislamiento.
- En ambos modelos, invertir en automatización: CI que detecte qué cambiar (affected tests), linters compartidos, plantillas y políticas.
- Si eliges multi, tener un registro de paquetes interno, políticas de semver y tooling para coordinar cambios.
- Si eliges mono, usar herramientas de monorepo (p. ej. bazel, nx, repo-tools) para gestionar escalado y pipelines parciales.

## Conclusión
No existe una única respuesta: elegir entre monorepo y multirepo depende de la organización, tamaño del equipo, acoplamiento entre módulos y requisitos operativos. Evalúa trade-offs y prototipa con una estructura pequeña antes de comprometerte a gran escala.
