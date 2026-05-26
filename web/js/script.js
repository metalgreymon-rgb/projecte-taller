const API = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', carregarCites);

document.getElementById('citaForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const client_id        = document.getElementById('client_id').value;
    const vehicle_id       = document.getElementById('vehicle_id').value;
    const data_cita        = document.getElementById('data_cita').value;
    const servei_sollicitat = document.getElementById('servei_sollicitat').value;

    try {
        const response = await fetch(`${API}/appointments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ client_id, vehicle_id, data_cita, servei_sollicitat })
        });

        const result = await response.json();

        if (response.ok) {
            mostrarMissatge(result.message, 'ok');
            document.getElementById('citaForm').reset();
            carregarCites();
        } else {
            mostrarMissatge(result.error || 'Error desconegut', 'error');
        }
    } catch (err) {
        mostrarMissatge('No s\'ha pogut connectar amb l\'API', 'error');
    }
});

async function carregarCites() {
    const contenidor = document.getElementById('llistatCites');
    contenidor.innerHTML = '<p class="loading">Carregant cites...</p>';

    try {
        const response = await fetch(`${API}/appointments`);
        const cites = await response.json();

        if (cites.length === 0) {
            contenidor.innerHTML = '<p class="no-data">No hi ha cites programades.</p>';
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Client</th>
                        <th>Vehicle</th>
                        <th>Data</th>
                        <th>Servei</th>
                    </tr>
                </thead>
                <tbody>
        `;

        cites.forEach(c => {
            html += `
                <tr>
                    <td data-label="#">${c.id}</td>
                    <td data-label="Client">${c.client_nom}<br><small>${c.telefon}</small></td>
                    <td data-label="Vehicle">${c.matricula} - ${c.model}</td>
                    <td data-label="Data">${c.data_cita}</td>
                    <td data-label="Servei">${c.servei_sollicitat}</td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        contenidor.innerHTML = html;

    } catch (err) {
        contenidor.innerHTML = '<p class="no-data">Error carregant les cites. Comprova que l\'API està en marxa.</p>';
    }
}

function mostrarMissatge(text, tipus) {
    const div = document.getElementById('missatge');
    div.textContent = text;
    div.className = `missatge ${tipus}`;
    setTimeout(() => { div.className = 'missatge hidden'; }, 4000);
}
