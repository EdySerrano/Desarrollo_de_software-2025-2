**Parte C. Preguntas adicionales**

C1. Gobernanza vs velocidad

Permitir autonomia de los equipos sin sacrificar politicas duras requiere guardrails automaticos y propiedad clara. Separar modulos en repositorios distintos con dueños naturales (OWNERS) da responsabilidad local y acota blast radius; cada cambio se publica como un artefacto versionado semanticamente con notas de version para rastrear cambios y responsabilidades. Los gates automaticos (OPA, escaneo de secretos, SBOM) deben estar integrados en la CI bloqueando solo en preflight critico y ofreciendo feedback rapido para que la politica sea inmutable pero el proceso sea agil. Manten defaults seguros (encriptado, IAM mínimo, TLS 1.3+) en plantillas y modulos, asi los desarrolladores aceleran sobre buenos presets.

Para medir y mejorar, combina metricas DORA (lead time, deployment frequency, MTTR) con KPIs de IaC: tiempo medio de revision, locks concurrentes, y porcentaje de rechazos por politica (ideal bajo pero >0 para detectar violaciones). Usa esas metricas para equilibrar reglas y velocidad: si las politicas frenan demasiado, invierte en mejor feedback y en tests automaticos que reduzcan friccion.
