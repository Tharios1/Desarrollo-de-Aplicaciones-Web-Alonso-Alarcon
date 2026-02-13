
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