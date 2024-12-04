// ****TUTTE LE FUNZIONI PER API MERAKI SPECIFICHE SU SSID


/* -----TEST DISABLE FUNCTION ----****START*****
//Recupera le info dell' SSID
function fetchRFSettings(ntwID) {
    const orgID = document.getElementById('orgID').value;
    fetch(`/api/get_rf_settings/${ntwID}`)
        .then(response => response.json())
        .then(data => {
            const RFSelect = document.getElementById('RFSelect');
            RFSelect.innerHTML = ""; // Pulisce le SSID precedenti

            data.forEach(rf => {
                const option = document.createElement('option');
                option.value = rf.number;
                option.textContent = `${rf.name} (ID: ${rf.number})`;
                RFSelect.appendChild(option);
            });

            // Recupera le impostazioni SSID per la prima SSID per fornire una visualizzazione iniziale
            if (data.length > 0) {
                fetchRFData(ntwID, data[0].number);
            }
        })
        .catch(err => console.error('Error fetching RF settings:', err));
}

// Funzione che restituisce il JSON del SSID
function fetchRFData(ntwID, RFid, field_visual_output, field_modify_output) {
    fetch(`/api/get_rf_settings/${ntwID}/${RFid}`) // Aggiorna endpoint per includere il numero
        .then(response => response.json())
        .then(data => {
            const jsonContainer = document.getElementById(field_visual_output);
            jsonContainer.innerHTML = ""; // Pulisce il contenuto precedente

            const pre = document.createElement('pre');
            pre.textContent = JSON.stringify(data, null, 4); // Formatta il JSON
            jsonContainer.appendChild(pre);
            document.getElementById(field_modify_output).value = JSON.stringify(data); // Aggiorna il campo JSON da inviare
        })
        .catch(err => console.error('Error fetching RF data:', err));
}

/* -----TEST DISABLE FUNCTION ----****END*****  */