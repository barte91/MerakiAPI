// ****TUTTE LE FUNZIONI PER PAGINA API-SSID

// Funzione che carica gli switch data la network ID (viene verificata da MenuNtwType.html)
function afterNetworksLoaded(networks) {

    const networkType = document.getElementById("networkType").value;
    const ntwSelect = document.getElementById("ntwID");

    // Se SINGLE: l'utente sceglie manualmente la network
    // → NON carichiamo SSID qui
    if (networkType === "SINGLE") {
        return;
    }

    // Se NON SINGLE:
    // prendiamo tutte le network e carichiamo direttamente gli SSID della prima rete
    if (!networks || networks.length === 0) return;

    const firstNetworkId = networks[0][0];

    // opzionale: seleziona automaticamente la prima network
    ntwSelect.value = firstNetworkId;

    fetchGeneric(
        `/api/get_ssid_settings/${this.value}`,
        "ssidSelect",
        "number",
        "name"
    );

    //loadSSIDs(firstNetworkId);
}



function loadSSIDs(networkId) {

    const ssidSelect = document.getElementById("ssidSelect");

    if (!networkId) return;

    ssidSelect.innerHTML = '<option value="">Caricamento SSID...</option>';

    fetch(`/api/get_ssid_settings/${networkId}`)
        .then(resp => resp.json())
        .then(data => {

            ssidSelect.innerHTML = '<option value="">Seleziona SSID</option>';

            // ATTENZIONE: adattare al tuo JSON reale Meraki
            data.forEach(ssid => {

                const option = document.createElement("option");

                option.value = ssid.number ?? ssid.id;
                option.textContent = ssid.name;

                ssidSelect.appendChild(option);
            });

        })
        .catch(err => {
            console.error("Errore caricamento SSID:", err);
        });
}