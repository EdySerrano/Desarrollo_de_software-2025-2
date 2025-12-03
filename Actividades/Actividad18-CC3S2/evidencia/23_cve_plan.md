# Plan de acción CVE (HIGH/CRITICAL) - Imagen: etl-app:1.0.0 @ sha256:9e0c716edb106992a9ebace60e5c23542732e47fb10bc5cb1e0bb865649e22c3

- Hallazgos clave:
  - (Sin hallazgos HIGH/CRITICAL en el escaneo actual. Se mantiene la plantilla como referencia para futuros incidentes).
  - CVE-YYYY-XXXX en <paquete> (<versión>) - Severidad: HIGH - Componente: sistema/biblioteca
  - CVE-YYYY-YYYY en <paquete> (<versión>) - Severidad: CRITICAL

- Remediación técnica:
  1) Actualizar base image a <nueva_base:tag> (ETA: <fecha>).
  2) Fijar versión de <paquete> a >= X.Y.Z donde el CVE está parchado.
  3) Ejecutar re-build y re-scan. Adjuntar nuevo SBOM y scan.

- Excepción temporal (si aplica):
  - Justificación: el paquete no se ejecuta en ruta explotable (argumento técnico).
  - Ticket: <ID/enlace interno> - Revisión: <fecha límite> (<= 30 días).

- Criterios de cierre:
  - Trivy/Grype sin HIGH/CRITICAL en imagen final.
  - Documentación de digest nuevo y evidencia de remediación.
