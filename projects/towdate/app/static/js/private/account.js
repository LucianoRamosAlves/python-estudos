const form = document.getElementById("profileForm");
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


// foto 

const photoForm = document.getElementById("photoForm");
const fotoInput = document.getElementById("fotoPerfil");
const btnAlterarFoto = document.getElementById("btnAlterarFoto");

if (photoForm && fotoInput) {

    if (btnAlterarFoto) {
        btnAlterarFoto.addEventListener("click", () => {
            fotoInput.click();
        });
    }

    fotoInput.addEventListener("change", () => {

        if (!fotoInput.files.length) {
            return;
        }

        ToDate.showConfirm({
            title: "Alterar foto de perfil",
            message: "Tem certeza que deseja alterar sua foto de perfil?",
            confirmText: "Alterar",
            cancelText: "Cancelar"
        }).then((confirmed) => {

            if (confirmed) {
                photoForm.submit();
            } else {
                fotoInput.value = "";
            }

        });

    });

}