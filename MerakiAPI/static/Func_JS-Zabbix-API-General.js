console.log("ZABBIX JS CARICATO");

document.addEventListener("DOMContentLoaded", function () {

    const buSelect = document.getElementById("bu");
    const typeSelect = document.getElementById("group_type");
    const locationSelect = document.getElementById("location");

    console.log("BU:", buSelect);
    console.log("TYPE:", typeSelect);
    console.log("LOCATION:", locationSelect);
    console.log("HIERARCHY:", hierarchy);


    function updateTypes() {

        const bu = buSelect.value;

        console.log("BU SELEZIONATA:", bu);

        typeSelect.innerHTML = "";
        locationSelect.innerHTML = "";

        // BU = ALL
        if (bu === "ALL") {

            const option = document.createElement("option");

            option.value = "ALL";
            option.textContent = "ALL";

            typeSelect.appendChild(option);

            const locationOption = document.createElement("option");

            locationOption.value = "ALL";
            locationOption.textContent = "ALL";

            locationSelect.appendChild(locationOption);

            return;
        }

        const types = hierarchy[bu].types;

        console.log("TIPI:", types);

        for (const typeName in types) {

            const option = document.createElement("option");

            option.value = typeName;
            option.textContent = typeName;

            typeSelect.appendChild(option);
        }

        updateLocations();
    }


    function updateLocations() {

        const bu = buSelect.value;
        const type = typeSelect.value;

        locationSelect.innerHTML = "";

        const locations = hierarchy[bu].types[type].locations;

        for (const locationName in locations) {

            const option = document.createElement("option");

            option.value = locationName;
            option.textContent = locationName;

            locationSelect.appendChild(option);
        }
    }


    // EVENTI
    buSelect.addEventListener("change", updateTypes);

    typeSelect.addEventListener("change", updateLocations);


    // CARICAMENTO INIZIALE
    updateTypes();

});