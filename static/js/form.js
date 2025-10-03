const form = document.getElementById("formAviso");
const submitBtn = document.getElementById("submit-btn");
let contactoIndex = document.querySelectorAll("#contactosContainer .contacto-item").length; 
let fotos = 1;





const regionSelect = document.getElementById("region");
const comunaSelect = document.getElementById("comuna");
regionSelect.addEventListener("change" , () => {
  const regionId = regionSelect.value;

  [...comunaSelect.options].forEach(opt => {
    if (opt.value == ""){
      opt.hidden = false;
      opt.disabled = false;
    } else{
      opt.hidden = opt.dataset.region !== regionId;
      opt.disabled = opt.dataset.region !== regionId;
    }
  });

  comunaSelect.value = "";
});



function agregarFoto(){
    if(fotos < 5){
        fotos++
        const div = document.getElementById("masFotos");
        const input = document.createElement("input");
        input.type = "file";
        input.name="fotos";
        input.accept = "image/*";
        div.appendChild(document.createElement("br"));
        div.appendChild(input);
    }else{
        alert("Maximo 5 fotos");
        return;
    }
}



function agregarOtroContacto(){
    if (contactoIndex < 5){
        const wrap = document.getElementById("contactosContainer");

        const div = document.createElement("div");
        div.classList.add("contacto-item");

        const select = document.createElement("select");
        select.name = `contactos[${contactoIndex}][nombre]`;
        select.innerHTML = 
        `<option value="">Seleccione</option>
          <option value="whatsapp">WhatsApp</option>
          <option value="telegram">Telegram</option>
          <option value="X">X</option>
          <option value="instagram">Instagram</option>
          <option value="tiktok">TikTok</option>
          <option value="otro">Otro</option>`;
          const input =  document.createElement("input");
          input.type = "text";
          input.name = `contactos[${contactoIndex}][identificador]`;
          input.placeholder = "ID o URL (4-50 caracteres)";
          div.appendChild(document.createElement("br"));
          div.appendChild(select);
          div.appendChild(input);
          wrap.appendChild(div);
          contactoIndex++;    
    } else{
        alert("Maximo 5 contactos permitidos");
        return;
    }
}



const validateRegion = (region) => region && region.trim() !== "";
const validateComuna = (comuna) => comuna && comuna.trim() !== "";

const validateName = (name) => {
  if(!name) return false;
  let lengthValid =  name.trim().length >= 3 && name.trim().length <= 200;
  
  return lengthValid;
}



const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length > 15;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};


const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return true;
  // validación de longitud
  let lengthValid = phoneNumber.length >= 8;

  // validación de formato
  let re = /^\+\d{3}\.\d{8,9}$/;
  let formatValid = re.test(phoneNumber);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};


const validateTipo = (tipo) => tipo && tipo.trim() != "";

const validateCantidad = (cantidad) => cantidad && cantidad >= 1;

const validateEdad = (edad) => edad && edad >= 1;

const validateFechaEntrega = (fecha) => {
    if(!fecha) return false;

    let fechaSeleccionada = new Date(fecha);
    let fehcaMinima= new Date();
    return fechaSeleccionada >= fehcaMinima
};

const validateContactoId = (contacto, contactoId) => {
  if (!contacto || contacto.trim() === "") return true; // opcional
  if (!contactoId || contactoId.trim() === "") return false;
  return contactoId.length >= 4 && contactoId.length <= 50;
};

const validateFiles = (inputsNodeList) => {
  const files = [];
  Array.from(inputsNodeList).forEach(inp => {
    if (inp.files && inp.files.length > 0) files.push(...inp.files);
  });
  if (files.length < 1 || files.length > 5) return false;
  return files.every(f => f.type.startsWith("image/"));
};





const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.forms["myForm"];
  let region= myForm["region"].value;
  let comuna= myForm["comuna"].value;
  let name= myForm["nombre"].value;
  let email= myForm["email"].value;
  let phone= myForm["telefono"].value;
  let tipo= myForm["tipo"].value;
  let cantidad= myForm["cantidad"].value;
  let edad= myForm["edad"].value;
  let fecha= myForm["fechaEntrega"].value;
  
  

  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName, reason) => {
    invalidInputs.push(`${inputName}: ${reason}`);
    isValid = false;
  };

  // lógica de validación
  if (!validateRegion(region)) setInvalidInput("Region", "Debes elegir al menos una region");
  if (!validateComuna(comuna)) setInvalidInput("Comuna","Debes elegir al menos una comuna");
  if (!validateName(name)) setInvalidInput("Nombre","El nombre debe tener entre 3 y 20 caracteres");
  if (!validateEmail(email)) setInvalidInput("Email","Debe colocar un email valido");
  if (phone && !validatePhoneNumber(phone)) setInvalidInput("Telefono", "Teléfono inválido. Ejemplo: +569.12345678");
  if (!validateTipo(tipo)) setInvalidInput("Tipo","Debes elegir al menos un tipo");
  if (!validateCantidad(cantidad)) setInvalidInput("Cantidad", "Cantidad debe ser al menos 1");
  if (!validateEdad(edad)) setInvalidInput("Edad","Edad debe ser al menos 1");
  if (!validateFechaEntrega(fecha)) setInvalidInput("Fecha de Entrega", "Debe ser igual o posterior a hoy");
  

  const filas = document.querySelectorAll("#contactosContainer .contacto-item");
  filas.forEach((fila, i) => {
    const sel = fila.querySelector("select");
    const inp = fila.querySelector("input[type='text']");
    if (!validateContactoId(sel.value, inp.value)) {
      setInvalidInput(`Contacto #${i + 1}`, "Si eliges un medio, debes ingresar un identificador de 4-50 caracteres");
    }
  });

  
  const fotosInputs = document.querySelectorAll('input[type="file"][name="fotos"]');
  if (!validateFiles(fotosInputs)) {
    setInvalidInput("Fotos", "Debes subir entre 1 y 5 fotos válidas");
  }

  

  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  
  validationListElem.textContent = "";
  if (!isValid) {
    // agregar elementos inválidos al elemento val-list.
    for (let input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";
    // hacer visible el mensaje de validación
    validationBox.hidden = false;
    return;
  } 
  // Ocultar el formulario
  form.style.display = "none";
    

  // establecer mensaje de éxito
  validationMessageElem.innerText = "“¿Está seguro que desea agregar este aviso de adopción?";
  validationListElem.textContent = "";

  // aplicar estilos de éxito
  validationBox.style.backgroundColor = "#ddffdd";
  validationBox.style.borderLeftColor = "#4CAF50";
  validationBox.hidden = false;

    

  // Agregar botones para enviar el formulario o volver
  let yesBtn = document.createElement("button");
  yesBtn.innerText = "“Sí, estoy seguro";
  yesBtn.type = "button";
  yesBtn.addEventListener("click", () => {
    form.submit();
  });

  let noBtn = document.createElement("button");
  noBtn.innerText = "No, no estoy seguro, quiero volver al formulario";
  noBtn.type = "button";
  noBtn.addEventListener("click", () => {
      // Mostrar el formulario nuevamente
    form.style.display = "block";
    validationBox.hidden = true;
  });

    
  validationListElem.appendChild(yesBtn);
  validationListElem.appendChild(noBtn);

};



submitBtn.addEventListener("click", validateForm);
