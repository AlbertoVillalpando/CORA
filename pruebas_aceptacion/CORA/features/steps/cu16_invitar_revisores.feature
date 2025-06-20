Característica: Invitar revisores manualmente
    Como organizador
    quiero asignar revisores a documentos manualmente
    para controlar el proceso de revisión

    Escenario: Invitar a Autor a una conferencia
        Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
        Y ingreso como organizador
        Y selecciono el listado de conferencias
        Y selecciono la conferencia "Conferencia Innovación 2024 - Edición" presionando el boton Invitaciones
        Y selecciono del listado de revisores a "autorP" de apellido "autorP"
        Cuando presiono el botón "Invitar"
        Entonces el sistema muestra en el listado de autores invitados a "autorP" de apellido "autorP"
