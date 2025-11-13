### Actividad: Patrones de dependencias y módulos en IaC con Terraform y Python

La actividad busca de forma integrada, el desarrollo de  los patrones de dependencia más usados en ingeniería de software e IaC, desde flujos unidireccionales hasta inyección de dependencias, así como los patrones facade, adapter y mediator y que sepas cuándo aplicar cada uno para desacoplar, orquestar y evolucionar sistemas.

#### Estructura general de Actividad15-CC3S2

```
Actividad15-CC3S2/
├── README.md                  # Resumen general de la actividad y estructura.
├── codigo/                    # Carpeta con todo el código fuente y modificaciones.
│   ├── network/               # Módulo original de red (de Laboratorio 7), con modificaciones si aplica.
│   │   ├── network.tf.json
│   │   └── ... (otros archivos del lab)
│   ├── main.py                # Versión modificada con inyección de dependencias (Fase 2).
│   ├── facade/                # Módulo facade (Fase 3).
│   │   └── facade.tf.json
│   ├── adapter/               # Módulo adapter (Fase 4).
│   │   └── adapter.tf.json
│   ├── mediator.py            # Script mediador en Python (Fase 5).
│   └── Makefile               # Actualizado con comandos como 'release' (Fase 8).
├── documentacion/             # Carpeta con informes, explicaciones y diagramas.
│   ├── informe_fase1.pdf      # Breve informe (1 página) sobre separación unidireccional (Fase 1).
│   ├── explicacion_ioc.txt    # Explicación corta (máx. 300 palabras) de inversión de control (Fase 2).
│   ├── diagrama_facade.png    # Diagrama de alto nivel del facade (Fase 3).
│   ├── explicacion_adapter.txt# Explicación de uso del patrón adapter en producción (Fase 4).
│   ├── comparacion_mediator_facade.txt # Breve comparación entre mediator y facade (Fase 5).
│   ├── presentacion_discusion.pptx # Presentación de 5 min sobre elección de patrones en escenario complejo (Fase 6).
│   ├── tabla_mono_vs_multi.md # Tabla comparativa de monorepositorio vs multirepositorio (Fase 7).
│   ├── informe_final.pdf      # Informe final (3-4 páginas) cubriendo análisis de patrones, elecciones de diseño, comparativa mono/multi, versionado/publicación y ejercicios resueltos.
│   └── ejercicios_adicionales/ # Subcarpeta con respuestas a los 16 ejercicios adicionales.
│       ├── ejercicio1.txt     # Diferencias entre Facade, Adapter y Mediator.
│       ├── ejercicio2.txt     # Escenario real (multi-cloud) y justificación de patrones.
│       ├── ... (hasta ejercicio9 y 14.txt)
├── evidencias/                # Carpeta con capturas de pantalla, grafos y logs.
│   ├── graph.png              # Grafo de dependencias (Fase 1).
│   ├── logs_apply_destroy.txt # Logs de ejecución de terraform apply/destroy (Fase 1 y 2).
│   ├── ejemplo_release.txt    # Ejemplo de releases con al menos dos versiones (Fase 8).
│   └── captura_registro.png   # Captura de módulo instalado desde registro local (Fase 9).
└── registry/                  # Configuración de registro local (Fase 9).
    ├── providers.tf           # Configuración para registry local.
```
