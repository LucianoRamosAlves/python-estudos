const form = document.querySelector(".reg-form");
const btnSalvar = document.getElementById("btnSalvar");

if (form && btnSalvar) {
    btnSalvar.addEventListener("click", () => {
        ToDate.showConfirm({
            title: "Salvar alterações",
            message: "Tem certeza que deseja salvar as alterações?",
            confirmText: "Salvar",
            cancelText: "Cancelar"
        }).then((confirmed) => {
            if (confirmed) {
                form.submit();
            }
        });
    });
}