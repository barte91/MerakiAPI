document.addEventListener("DOMContentLoaded", function () {

    const uploadForm = document.getElementById("uploadConfigForm");
    if (!uploadForm) return;

    uploadForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(uploadForm);

        fetch("/api/LM-CatMeraki-upload-switches", {
            method: "POST",
            body: formData
        })
            .then(response => {
                if (!response.ok) throw new Error("Errore upload");
                return response.json();
            })
            .then(data => {

                /* ───────────── TABELLA ORDINATA ───────────── */
                if (data.results && Array.isArray(data.results)) {
                    renderResultsTable(data.results);
                }

                /* ───────────── DOWNLOAD AUTOMATICO CSV COMPLETO ───────────── */
                if (data.full_csv) {
                    const blob = new Blob([data.full_csv], { type: "text/csv;charset=utf-8;" });
                    const url = URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = "LM-CatMeraki-Results.csv";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    URL.revokeObjectURL(url);
                }

            })
            .catch(err => {
                alert("Errore durante upload");
                console.error(err);
            });

    });

});

/* =========================================================
   RENDER TABLE
   ========================================================= */

const RESULT_COLUMNS = [
    "serial",
    "port_id",
    "port_name",
    "status",
    "enabled",
    "poeEnabled",
    "type",
    "vlan",
    "allowedVlans"
];

function renderResultsTable(results) {

    let table = document.getElementById("resultsTable");

    if (!table) {
        table = document.createElement("table");
        table.id = "resultsTable";
        table.style.borderCollapse = "collapse";
        table.style.marginTop = "20px";
        table.style.width = "100%";
        document.body.appendChild(table);
    }

    table.innerHTML = "";

    // HEADER
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    RESULT_COLUMNS.forEach(col => {
        const th = document.createElement("th");
        th.textContent = col;
        th.style.border = "1px solid black";
        th.style.padding = "6px";
        th.style.background = "#f0f0f0";
        th.style.position = "sticky";
        th.style.top = "0";
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // BODY
    const tbody = document.createElement("tbody");

    results.forEach(row => {
        const tr = document.createElement("tr");

        // colori righe
        if (row.status?.startsWith("NO-PROFILE")) {
            tr.style.backgroundColor = "#ffe0e0";
        } else if (row.status?.includes("SHUT")) {
            tr.style.backgroundColor = "#e6e6e6";
        } else if (row.status?.startsWith("PROFILE-APPLIED")) {
            tr.style.backgroundColor = "#e0ffe0";
        }

        RESULT_COLUMNS.forEach(col => {
            const td = document.createElement("td");
            td.textContent = row[col] ?? "";
            td.style.border = "1px solid black";
            td.style.padding = "6px";
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
}