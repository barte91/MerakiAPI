const defaultSSIDJson = `{
        ...
            }`;

function setDefaultJson() {
    document.getElementById('selectedSSIDJson').value = defaultSSIDJson;
}

function fetchNetworks(orgID, type) {
    fetch(`/api/get_networks/${orgID}?type=${type}`)
        .then(response => response.json())
        .then(data => {
            const ntwSelect = document.getElementById('ntwID');
            ntwSelect.innerHTML = "";
            data.forEach(network => {
                const option = document.createElement('option');
                option.value = network[0];
                option.textContent = `${network[1]} (ID: ${network[0]})`;
                ntwSelect.appendChild(option);
            });
        });
}

function onNetworkTypeChange() {
    const orgID = document.getElementById('orgID').value;
    const type = document.getElementById('networkType').value;
    fetchNetworks(orgID, type);
}

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

// Funzione per gestire il cambiamento di SSID selezionato
function onSSIDChange() {
    const ntwID = document.getElementById('ntwID').value;
    const ssidSelect = document.getElementById('ssidSelect');
    const selectedSsidNumber = ssidSelect.value; // Ottieni il numero SSID selezionato
    if (selectedSsidNumber) {
        fetchSSIDData(ntwID, selectedSsidNumber);
    }
}

function downloadJson(jsonData) {
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'SSiD-Settings.json'; // Nome del file scaricato
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url); // Libera l'oggetto URL
}

// Funzione per chiedere conferma e scaricare il JSON
function promptDownloadJSON(jsonOutput) {
    //const jsonOutput = document.getElementsByTagName('pre')[0].innerHTML; // Ottieni il contenuto JSON
    const confirmation = confirm("Vuoi scaricare il JSON di output?");
    if (confirmation) {
        downloadJson(jsonOutput); // Chiama la funzione di download
    }
}

// Imposta il JSON di default quando la pagina viene caricata
window.onload = function () {
    setDefaultJson();
    const ssidSelect = document.getElementById('ssidSelect');
    ssidSelect.addEventListener('change', onSSIDChange); // Aggiungi ascoltatore per il cambiamento SSID
};
