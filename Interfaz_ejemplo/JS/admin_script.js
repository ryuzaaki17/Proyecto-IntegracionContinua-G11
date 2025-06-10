// admin_script.js

// Simulación de datos en memoria
let laboratorios = [
    { id: 1, nombre: "Laboratorio A", capacidad: 30 },
    { id: 2, nombre: "Laboratorio B", capacidad: 25 }
];
let horarios = [];
let reservas = [];

// Cargar laboratorios en el formulario de gestión
function cargarLaboratorios() {
    const labSelect = document.getElementById("labSeleccionado");
    laboratorios.forEach(lab => {
        const option = document.createElement("option");
        option.value = lab.id;
        option.textContent = lab.nombre;
        labSelect.appendChild(option);
    });
}

// Añadir laboratorio
document.getElementById("formLab").addEventListener("submit", function(event) {
    event.preventDefault();
    const nombreLab = document.getElementById("nombreLab").value;
    const capacidadLab = document.getElementById("capacidadLab").value;

    const nuevoLaboratorio = {
        id: laboratorios.length + 1,
        nombre: nombreLab,
        capacidad: parseInt(capacidadLab)
    };

    laboratorios.push(nuevoLaboratorio);
    alert("Laboratorio añadido con éxito.");
    cargarLaboratorios();
});

// Añadir horario
document.getElementById("formHorario").addEventListener("submit", function(event) {
    event.preventDefault();
    const labId = document.getElementById("labSeleccionado").value;
    const fecha = document.getElementById("fechaHorario").value;
    const horaInicio = document.getElementById("horaInicio").value;
    const horaFin = document.getElementById("horaFin").value;

    if (!labId || !fecha || !horaInicio || !horaFin) {
        alert("Por favor complete todos los campos.");
        return;
    }

    const horario = {
        laboratorio_id: labId,
        fecha,
        horaInicio,
        horaFin
    };

    horarios.push(horario);
    alert("Horario añadido con éxito.");
});

// Mostrar reservas
function mostrarReservas() {
    const tablaReservas = document.getElementById("tablaReservas").getElementsByTagName('tbody')[0];
    tablaReservas.innerHTML = "";

    reservas.forEach(reserva => {
        const fila = document.createElement("tr");

        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = reserva.nombre;
        fila.appendChild(celdaNombre);

        const celdaLab = document.createElement("td");
        celdaLab.textContent = reserva.laboratorio;
        fila.appendChild(celdaLab);

        const celdaFecha = document.createElement("td");
        celdaFecha.textContent = reserva.fecha;
        fila.appendChild(celdaFecha);

        const celdaHora = document.createElement("td");
        celdaHora.textContent = `${reserva.horaInicio} - ${reserva.horaFin}`;
        fila.appendChild(celdaHora);

        tablaReservas.appendChild(fila);
    });
}

// Simular reservas para mostrar en la tabla (esto vendría de la base de datos en un escenario real)
reservas = [
    { nombre: "Juan Pérez", laboratorio: "Laboratorio A", fecha: "2024-12-05", horaInicio: "09:00", horaFin: "11:00" },
    { nombre: "Ana López", laboratorio: "Laboratorio B", fecha: "2024-12-06", horaInicio: "12:00", horaFin: "14:00" }
];

// Inicialización
cargarLaboratorios();
mostrarReservas();
