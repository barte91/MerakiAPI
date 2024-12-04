//****TUTTE LE FUNZIONI CHE SI RIFERISCONO A 

//Funzione SPECIFICA--Recupera tipo Network quando si cambia dal menù
function onNetworkTypeChange() {
    const orgID = document.getElementById('orgID').value;
    const type = document.getElementById('networkType').value;
    fetchNetworks(orgID, type);
}

/* -----TEST DISABLE FUNCTION ----****START*****
//Recupera tipo Network quando si cambia dal menù
function onOptionChange(param1,param2,requestUrl) {
    const value_param1 = document.getElementById(param1).value;
    const value_param2 = document.getElementById(param2).value;
    console.log('ON-OPTION-CHANGE', value_param1, value_param2)
    fetchGenericFromOption(value_param1, value_param2,requestUrl);
}
/* -----TEST DISABLE FUNCTION ----****END*****  */
//Setta un JSON di Default nel Form
const defaultSSIDJson = `{
        ...
            }`;
function setDefaultJson() {
    document.getElementById('ModifyJson').value = defaultSSIDJson;
}
// Imposta il JSON di default quando la pagina viene caricata
window.onload = function () {
    setDefaultJson();
    const CurrentSettings = document.getElementById('CurrentSettings');
    CurrentSettings.addEventListener('change', onElementChange('ntwID', 'CurrentSettings')); // Aggiungi ascoltatore per il cambiamento SSID
};

//Funzione per fare il DOWNLOAD del JSON
function downloadJson(jsonData,name_file) {
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name_file; // Nome del file scaricato
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url); // Libera l'oggetto URL
}
// Funzione per chiedere conferma e scaricare il JSON
function promptDownloadJSON(jsonOutput,name_file) {
    //const jsonOutput = document.getElementsByTagName('pre')[0].innerHTML; // Ottieni il contenuto JSON
    const confirmation = confirm("Vuoi scaricare il JSON di output?");
    if (confirmation) {
        downloadJson(jsonOutput,name_file); // Chiama la funzione di download
    }
}

/* -----TEST DISABLE FUNCTION ----****START*****

// Funzione per gestire il cambiamento di SSID selezionato
function onSSIDChange() {
    const ntwID = document.getElementById('ntwID').value;
    const ssidSelect = document.getElementById('ssidSelect');
    const selectedSsidNumber = ssidSelect.value; // Ottieni il numero SSID selezionato
    if (selectedSsidNumber) {
        fetchSSIDData(ntwID, selectedSsidNumber);
    }
}

// Funzione per gestire il cambiamento di RF selezionato
function onRFChange() {
    const ntwID = document.getElementById('ntwID').value;
    const RFSelect = document.getElementById('RFSelect');
    const selectedRFNumber = RFSelect.value; // Ottieni il numero RF selezionato
    if (selectedRFNumber) {
        fetchRFData(ntwID, selectedRFNumber);
    }
}

/* -----TEST DISABLE FUNCTION ----****END*****  */

// Funzione per gestire il cambiamento di un campo in HTML-Generalizzato
function onElementChange(field1, field2, field_visual_output, field_modify_output, url) {
    // field_visual output è dove verrà mostrato il risultato es. CurrentSettings
    // field_modify output è dove verrà mostrato e si può modificare output per inviare il risultato es. ModifyJson
    //di solito ntwID
    const value_field1 = document.getElementById(field1).value;
    //esempio RFSelect
    const select_field2 = document.getElementById(field2);
    // Ottieni il numero RF selezionato
    const value_field2 = select_field2.value;
    if (value_field2) {
        request_url = url + value_field1 + '/' + value_field2
        //console.log('onElementChange', value_field1, 'URL=', url, 'REQ_URL=', request_url)
        fetchGenericData(request_url, field_visual_output, field_modify_output);
    }
}

//Recupera le info data NtwID e OrgID del parametro richiesto
function fetch_Settings(ntwID, request_url, el_select, el_JSON,pkey) {
    request_url_full = request_url + ntwID
    fetch(request_url_full)
        .then(response => response.json())
        .then(data => {
            const element_Select = document.getElementById(el_select);
            element_Select.innerHTML = ""; // Pulisce le element_select precedente
            data.forEach(element => {
                const option = document.createElement('option');
                option.value = element[pkey];
                option.textContent = `${element.name} (ID: ${element[pkey]})`;
                element_Select.appendChild(option);
                //console.log('*****ELEMENT-NAME*****:', element.name + '*****ELEMENT-NUMBER*****:', element.id)
            });

            // Recupera le impostazioni element per il primo element per fornire una visualizzazione iniziale
            if (data.length > 0) {
                fetchElementData(ntwID, data[0][pkey], request_url, 'CurrentSettings', el_JSON);
            }
        })
        .catch(err => console.error('Error fetching Elements settings:', err));
}

// Funzione che restituisce il JSON del SSID
function fetchElementData(ntwID, el_id, request_url,el_settings,el_JSON) {
    //fetch(request_url +'${ntwID}/${el_id}') // Aggiorna endpoint per includere il numero
    fetch(request_url + ntwID+'/'+el_id)
        .then(response => response.json())
        .then(data => {
            const jsonContainer = document.getElementById(el_settings);
            jsonContainer.innerHTML = ""; // Pulisce il contenuto precedente

            const pre = document.createElement('pre');
            pre.textContent = JSON.stringify(data, null, 4); // Formatta il JSON
            jsonContainer.appendChild(pre);
            document.getElementById(el_JSON).value = JSON.stringify(data); // Aggiorna il campo JSON da inviare
            console.log('Return',data)
        })
        .catch(err => console.error('Error fetching Elements data:', err));
}