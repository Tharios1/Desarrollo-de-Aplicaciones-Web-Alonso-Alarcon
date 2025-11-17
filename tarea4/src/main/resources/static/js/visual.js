function abrirModal(id) { document.getElementById("id-aviso").value = id;
    document.getElementById("modal").style.display = "flex";
}

function cerrarModal() {
    document.getElementById("modal").style.display = "none";
}

function enviarNota() {
    let id = document.getElementById("id-aviso").value;
    let nota = document.getElementById("valor-nota").value;
    
    fetch("/nota",{
        method: "POST",
        headers: { "Content-Type":"application/x-www-form-urlencoded" },
        body: "id=" + id + "&nota=" + nota
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error al enviar la nota");
        }
        return response.text();
    })
    .then(() => {
        location.reload();
    })
    .catch(error => {
        alert("No se puede guardar la nota: Error" + error.message);
        console.error("Detalle del error: ", error);
    });
}