// ****TUTTE LE FUNZIONI PER API MERAKI SPECIFICHE SU SSID
/* -----TEST DISABLE FUNCTION ----****START*****
//Recupera le info dell' SSID
function fetchSSIDSettings(ntwID) {
    const orgID = document.getElementById('orgID').value;
    fetch(`/api/get_ssid_settings/${ntwID}`)
        .then(response => response.json())
        .then(data => {
            const ssidSelect = document.getElementById('ssidSelect');
            ssidSelect.innerHTML = ""; // Pulisce le SSID precedenti

            data.forEach(ssid => {
                const option = document.createElement('option');
                option.value = ssid.number;
                option.textContent = `${ssid.name} (NUMBER: ${ssid.number})`;
                ssidSelect.appendChild(option);
            });

            // Recupera le impostazioni SSID per la prima SSID per fornire una visualizzazione iniziale
            if (data.length > 0) {
                fetchSSIDData(ntwID, data[0].number);
            }
        })
        .catch(err => console.error('Error fetching SSID settings:', err));
}

// Funzione che restituisce il JSON del SSID
function fetchSSIDData(ntwID, ssidNumber) {
    fetch(`/api/get_ssid_settings/${ntwID}/${ssidNumber}`) // Aggiorna endpoint per includere il numero
        .then(response => response.json())
        .then(data => {
            const jsonContainer = document.getElementById('ssidSettings');
            jsonContainer.innerHTML = ""; // Pulisce il contenuto precedente

            const pre = document.createElement('pre');
            pre.textContent = JSON.stringify(data, null, 4); // Formatta il JSON
            jsonContainer.appendChild(pre);
            document.getElementById('selectedSSIDJson').value = JSON.stringify(data); // Aggiorna il campo JSON da inviare
        })
        .catch(err => console.error('Error fetching SSID data:', err));
}
 -----TEST DISABLE FUNCTION ----****END*****   */



