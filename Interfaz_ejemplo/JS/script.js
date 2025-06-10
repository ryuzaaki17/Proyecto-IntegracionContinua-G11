// script.js
document.addEventListener("DOMContentLoaded", function() {
    // Inicializar el calendario
    const calendar = document.getElementById("calendar");
    const daysInMonth = new Date(2024, 11, 0).getDate(); // Diciembre 2024
    let selectedDate = '';

    // Crear los días del calendario
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement("div");
        dayElement.classList.add("day");
        dayElement.textContent = day;
        dayElement.addEventListener("click", function() {
            selectedDate = `2024-12-${day < 10 ? '0' + day : day}`;
            alert(`Seleccionaste el día: ${selectedDate}`);
        });
        calendar.appendChild(dayElement);
    }

    // Manejar la reserva
    const form = document.getElementById("formReserva");
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const laboratorio = document.getElementById("laboratorio").value;
        const fecha = document.getElementById("fecha").value;
        const hora = document.getElementById("hora").value;

        if (!selectedDate) {
            alert("Selecciona un día del calendario");
            return;
        }

        if (fecha !== selectedDate) {
            alert("La fecha seleccionada no coincide con la del calendario");
            return;
        }

        const reservaInfo = `
            <h3>Reserva Confirmada</h3>
            <p><strong>Nombre:</strong> ${nombre}</p>
            <p><strong>Laboratorio:</strong> ${laboratorio}</p>
            <p><strong>Fecha:</strong> ${fecha}</p>
            <p><strong>Hora:</strong> ${hora}</p>
        `;
        
        document.getElementById("confirmacion").innerHTML = reservaInfo;
    });
});
