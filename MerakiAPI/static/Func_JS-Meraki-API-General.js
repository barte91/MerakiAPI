// ****TUTTE LE FUNZIONI PER SEARCH ECC DI API MERAKI

//Funzione SPECIFICA--Recupera tipo Network quando si cambia dal menù
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

// Recuepra Generic by URL for 2 elements
function fetchGeneric(requestUrl, FieldOutput) {
    //console.log('^^^^^^^^URL^^^^^',requestUrl)
    fetch(requestUrl)
        .then(response => response.json())
        .then(data => {
            const FieldSelect = document.getElementById(FieldOutput);
            FieldSelect.innerHTML = "";
            data.forEach(element => {
                const option = document.createElement('option');
                option.value = element[0];
                option.textContent = `${element[1]} (ID: ${element[0]})`;
                FieldSelect.appendChild(option);
            });
        });
}


/* -----TEST DISABLE FUNCTION ----****START*****
// Recuepra Generic by URL for 2 elements FROM Option
function fetchGenericFromOption(requestUrl, FieldOutput) {
    fetch(requestUrl)
        .then(response => response.json())
        .then(data => {
            const FieldSelect = document.getElementById(FieldOutput);
            FieldSelect.innerHTML = "";
            data.forEach(element => {
                const option = document.createElement('option');
                option.value = element[0];
                option.textContent = `${element[1]} (ID: ${element[0]})`;
                FieldSelect.appendChild(option);
            });
        });
}
 -----TEST DISABLE FUNCTION ----****END***** */
// Funzione che restituisce il JSON del SSID
function fetchGenericData(requestUrl, field_visual_output, field_modify_output) {
    //console.log('^^^^^^^^URL-GEN-DATA^^^^^', requestUrl)
    fetch(requestUrl) // Aggiorna endpoint per includere il numero
        .then(response => response.json())
        .then(data => {
            const jsonContainer = document.getElementById(field_visual_output);
            jsonContainer.innerHTML = ""; // Pulisce il contenuto precedente

            const pre = document.createElement('pre');
            pre.textContent = JSON.stringify(data, null, 4); // Formatta il JSON
            jsonContainer.appendChild(pre);
            document.getElementById(field_modify_output).value = JSON.stringify(data); // Aggiorna il campo JSON da inviare
        })
        .catch(err => console.error('Error fetching data:', err));
}