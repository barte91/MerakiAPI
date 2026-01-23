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
                if (!response.ok) {
                    throw new Error("Errore upload");
                }
                return response.json();
            })
            .then(data => {
                // Mostra JSON risultato
                const output = document.getElementById("uploadResult");
                if (output) {
                    output.textContent = JSON.stringify(data, null, 2);
                }

                //  Download automatico CSV NO-PROFILE
                if (data.no_profile_count && data.no_profile_count > 0) {
                    window.location.href =
                        "/api/LM-CatMeraki-download-no-profile";
                }
            })
            .catch(err => {
                alert("Errore durante upload");
                console.error(err);
            });
    });

});
