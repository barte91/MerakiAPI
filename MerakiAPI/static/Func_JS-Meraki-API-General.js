// ****TUTTE LE FUNZIONI PER SEARCH ECC DI API MERAKI

//Funzione SPECIFICA--Recupera tipo Network quando si cambia dal menù
function fetchNetworks(orgID, type) {
    fetch(`/api/get_networks/${orgID}?type=${type}`)
        .then(response => response.json())
        .then(data => {
            const ntwSelect = document.getElementById('ntwID');
            ntwSelect.innerHTML = "";
            //Primo elemento vuoto
            const EmptyOpt = document.createElement('option');
            EmptyOpt.value = "";
            EmptyOpt.textContent = "";
            ntwSelect.appendChild(EmptyOpt);
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


// Funzione che restituisce il JSON richiesto (requestUrl)
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


/*
function POST_API_RadioProfile(requestUrl, field_modify_output) {
    const value_field_modify_output = document.getElementById(field_modify_output).value;
    const ntwID = document.getElementById('ntwID').value;  // Ottieni l'ID della rete
    const json_data = JSON.parse(document.getElementById(field_modify_output).value);  // Assicurati che il campo JSON sia valorizzato
    console.log('JSON-DATA', json_data)
    // Effettua la richiesta POST
    fetch(`${requestUrl}/${ntwID}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_data) // Usa il JSON modificato come body
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Errore nella creazione del profilo RF");
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            alert("Nuovo RF Profile creato con successo!");
        })
        .catch((error) => {
            console.error('Error:', error);
            alert("Si è verificato un errore nella creazione del RF Profile.");
        });
}
*/


function POST_API_General(requestUrl,ntwID, json_data) {
    // Effettua la richiesta POST
    fetch(requestUrl+'/'+ntwID, {  //`/api/post_rf_profiles/${ntwID}`
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_data) // Usa il JSON come body
    })
    .then(response => {
        if (!response.ok) {
           throw new Error("ERRORE-CREAZIONE");
        }
        return response.json();
    })
    .then(data => {
        alert('OK-CREAZIONE-ELEMENTO --> SU RETE ID: ${ntwID}');
    })
    .catch((error) => {
        alert('ERRORE-CREAZIONE-ELEMENTO --> SU RETE ID: ${ntwID}');
    });
 }

/*
function POST_API_Meraki(requestUrl, field_modify_output) {

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Accept", "application/json");
    myHeaders.append("Authorization", "f25d79a1df42dff69f5337fa61c60c2b798aa404");

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: data,
        redirect: "follow"
    };

    value_field_modify_output = document.getElementById(field_modify_output).value
    const data = JSON.stringify({ value_field_modify_output})

    fetch(requestUrl, requestOptions)
        .then((response) => response.json())
        .then((data) =>
            console.log('POST-EFFETTUATO'))
        .catch(err => console.error('Error POST data:', err));
}
*/