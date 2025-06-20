Característica: Conferencia
    Como administrador
    quiero utilizar las funcionalidades de la conferencia
    para crear conferencias

    Escenario: Crear nueva conferencia
        Dado que ingreso a la plataforma en la URL "http://127.0.0.1:8000"
        Y ingreso como administrador
        Y selecciono el listado de conferencias
        Y elijo crear una nueva conferencia
        Y modifico la duracion a "1" meses, "3" dias, "4" horas y "23" minutos en categoria "Ingeniería"
        Y modifico el nombre de la conferencia a "Conferencia Innovación 2024 - Edición" en categoria "Ingeniería"
        Cuando presiono el botón "Crear conferencia"
        Entonces podre ver la conferencia con nombre "Conferencia Innovación 2024 - Edición"