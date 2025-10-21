# Actividad 8: Gestión ágil de proyectos con GitHub Projects, configuración de Kanban Board y creación de historias de usuario

* **Repositorio:** [Repositorio de GitHub](https://github.com/EdySerrano/Desarrollo_de_software-2025-2)
* **Proyecto Kanban:** [Tablero de GitHub Projects](https://github.com/users/EdySerrano/projects/7)


## Parte 1: Kanban Board
* **Tablero inicial:** Captura de "Devops-agile" con columnas predeterminadas.

![alt text](capturas/tablero-inicial.png)

* **Columnas renombradas:** 
    * Ready -> Icebox
    
    ![alt text](capturas/icebox.png)

    * In Review -> Review/QA.

    ![alt text](capturas/review-qa.png)

* **Tablero final:** Columnas Product Backlog y Sprint Backlogs, orden correcto.

![alt text](capturas/tablero-final-parte1.png)

## Parte 2: Issue template
* **Configuración:** *Settings > Features > Custom template.*

![alt text](capturas/template-config.png)

* **Template User Story:** Markdown de ejemplo.
    * **Enlace:** [.github/ISSUE_TEMPLATE/user-story.md](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/blob/main/.github/ISSUE_TEMPLATE/user-story.md)

    * **Commit:** 

    ![alt text](capturas/commit-template.png)


## Parte 3: Historias de usuario
* **7 Issues:**
    * **Enlaces:** 
        * [Counter](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/1)
        * [Multiple-Counters](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/2)
        * [Persist](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/3)
        * [Reset](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/4)
        * [Deploy](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/5)
        * [Remove](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/6)
        * [Update](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/7)

    * **Creación:**

        ![alt text](capturas/creacion-issue.png)


* **Límite:** New Issues con límite 7.

    ![alt text](capturas/limite-new-issues.png)

* **Priorización:** Counter al inicio de Product Backlog, Multiple Counters en Icebox, resto en New Issues.

    ![alt text](capturas/tablero-parte3.png)

## Parte 4: Refinamiento y labels

* **Triage:**

    * **Deploy bajo Persist:**

        ![alt text](capturas/triage-deploy.png)

    * **Remove a Icebox:**

        ![alt text](capturas/triage-remove.png)

    * **Update tras Reset:**

        ![alt text](capturas/triage-update.png)

* **Edición:** Detalles y criterios para todas las historias en Product Backlog.

    ![alt text](capturas/edit-counter.png)

* **Label Technical Debt:** Amarillo #FBCA04.

    ![alt text](capturas/label-technical-debt.png)

* **Labels Asignados:** enhancement para la mayoría, technical debt para Deploy.

    ![alt text](capturas/labels-visibles.png)

## Ejercicios
### Ejercicio 1: Epic

* **Enlace:** [Epic: Implementar servicio de contador](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/issues/10)

    ![alt text](capturas/epic.png)

### Ejercicio 2: Etiquetas
* **Labels:** High/Medium/Low Priority, In Review, Blocked, Ready for Testing.

    ![alt text](capturas/nuevas-labels.png)

* **Tablero:**

    ![alt text](capturas/tablero-labels-ej2.png)

### Ejercicio 3: GitHub Actions
* **Enlace:** [.github/workflows/kanban-automation.yml](https://github.com/EdySerrano/Desarrollo_de_software-2025-2/blob/main/.github/workflows/project-automation.yml)
* **Evidencia:**
    ![alt text](capturas/automation-proof.png)

* **Archivo de automatizacion:**
    ![alt text](capturas/workflow.png)


### Ejercicio 4: Tiempo
* Esfuerzo estimado en (horas)
    ![alt text](capturas/campo-esfuerzo.png)

### Ejercicio 5: Stakeholder Feedback
* **Enlace:** [Exportar a CSV](https://github.com/users/EdySerrano/projects/7/views/1?pane=issue&itemId=134828550&issue=EdySerrano%7CDesarrollo_de_software-2025-2%7C12)

* Historia priorizada
    ![alt text](capturas/export-csv.png)

### Ejercicio 6: Análisis

* **Métricas:** Cycle time, cuellos de botella (Review/QA: 3 días).

    ![alt text](capturas/metricas.png)

* **Reporte:**

    [reporte-metricas.txt](capturas/reporte-metricas.txt)