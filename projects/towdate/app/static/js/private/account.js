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

// remover foto
const btnRemoverFoto = document.getElementById("btnRemoverFoto");
const formType = document.getElementById("formType");

if (btnRemoverFoto) {

    btnRemoverFoto.addEventListener("click", () => {

        ToDate.showConfirm({
            title: "Remover foto de perfil",
            message: "Tem certeza que deseja remover sua foto de perfil?",
            confirmText: "Remover",
            cancelText: "Cancelar"
        }).then((confirmed) => {

            if (confirmed) {

                formType.value = "remove_photo";

                photoForm.submit();
            }

        });

    });

}

// trocar senha
const changePasswordForm = document.getElementById("changePasswordForm");
const btnChangePassword = document.getElementById("btnChangePassword");

if (changePasswordForm && btnChangePassword) {
    btnChangePassword.addEventListener("click", () => {
        ToDate.showConfirm({
            title: "Alterar senha",
            message: "Tem certeza que deseja alterar sua senha?",
            confirmText: "Alterar",
            cancelText: "Cancelar"
        }).then((confirmed) => {
            if (confirmed) {
                changePasswordForm.submit();
            }
        });
    });
}
