
function ampliarFoto(img){
    const modal = document.getElementById("modalFoto");
    const modalImg = document.getElementById("imgGrande");
    modal.style.display = "block";
    modalImg.src = img.src;
    
}

function cerrarFoto(){
  const modal = document.getElementById("modalFoto")
  modal.style.display= "none"
  
}






const comentariosDiv = document.getElementById("comentarios");
const avisoId = Number(comentariosDiv.dataset.avisoId);
const formComentario = document.getElementById("formComentario")

function cargarComentarios(){
  const url = `/api/comentarios/${avisoId}`;
  fetch(url)
    .then((response) => {
      if (!response.ok){
        throw new Error("Error al obtener los comentarios");
      }
      return response.json();
    })
    .then((comentarios) => {
      comentariosDiv.innerHTML = "";
      if(comentarios.length == 0){
        comentariosDiv.innerHTML = "<p> No hay comentarios aun.</p>";
        return;
      }

      comentarios.forEach((c) => {
        const p = document.createElement("p");
        p.innerHTML = `<strong>${c.nombre}</strong> (${c.fecha}):<br>${c.texto}`;
        comentariosDiv.appendChild(p);
      });
    })
    .catch((error) => {
      console.error("Hubo un problema al cargar los comentarios:", error);
      comentariosDiv.innerHTML = "<p>Error al cargar los comentarios.</p>";
    });
}

formComentario.addEventListener("submit", (e) => {
  e.preventDefault();
  const nombre = document.getElementById("nombreComentario").value.trim();
  const texto = document.getElementById("textoComentario").value.trim();
  if (nombre.length < 3 || texto.length < 5){
    alert("El nombre deber tener al menos 3 caracteres y el comentario 5.");
    return;
  }

  const url = "/api/comentarios";
  const data = {
    nombre: nombre,
    texto: texto,
    aviso_id: avisoId,
  };

  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if(!response.ok){
        throw new Error("Error al enviar el comentario");
      }
      return response.json();
    })
    .then((nuevoComentario) => {
      formComentario.reset();
      const p = document.createElement("p");
      p.innerHTML = `<strong>${nuevoComentario.nombre}</strong> (${nuevoComentario.fecha}):<br>${nuevoComentario.texto}`;
      comentariosDiv.prepend(p); 

      console.log("Comentario agregado:", nuevoComentario);

    })
    .catch((error) => {
      console.error("Hubo un problema con el envío del comentario:", error);
      alert("No se pudo enviar el comentario. Inténtalo de nuevo.");
    });

});

cargarComentarios()
