function jsEnviar(){
    alert("hola mundo")
}

function jsVentanaModal(Titulo,Header,Contenido,Botones){
	var MODAL = document.getElementById("ModalSistema");
	var ContenidoModal = '';
	ContenidoModal += '<div class="modal-dialog">';
	ContenidoModal += '<div class="modal-content">';
	ContenidoModal += '<div class="modal-header '+Header+'">';
	ContenidoModal += '<h1 class="modal-title fs-5" id="exampleModalLabel">'+Titulo+'</h1>';
	ContenidoModal += '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>';
	ContenidoModal += '</div>';
	ContenidoModal += '<div class="modal-body">';
	///////////// C O N T E N I D O ///////////////
	ContenidoModal += Contenido;
	///////////// C O N T E N I D O ///////////////
	ContenidoModal += '</div>';
	ContenidoModal += '<div class="modal-footer">';
	///////////// B O T O N E S ///////////////	
	VecBotones = Botones.split("@"); // Parsea o divide la cadena en un array, según el carácter que le proporcionemos.
	for(i=0; i<VecBotones.length; i++){
		var Boton = VecBotones[i];
		VecPartesBoton 	= Boton.split("|");
		var TextoBoton 	= VecPartesBoton[0];
		var ColorBoton 	= VecPartesBoton[1];
		var MetodoBoton = VecPartesBoton[2];
		if(TextoBoton == "Cancelar" || TextoBoton == "Cerrar"){
			ContenidoModal += '<button type="button" class="btn btn-'+ColorBoton+'" data-bs-dismiss="modal">'+TextoBoton+'</button>';
		}else{
			ContenidoModal += '<button type="button" class="btn btn-'+ColorBoton+'" onclick="'+MetodoBoton+'">'+TextoBoton+'</button>';
		}
	}
	///////////// B O T O N E S ///////////////	
	ContenidoModal += '</div>';
	ContenidoModal += '</div>';
	ContenidoModal += '</div>';
	MODAL.innerHTML = ContenidoModal;
	
	var myModal = new bootstrap.Modal(document.getElementById('ModalSistema'), {
        keyboard: true,
        backdrop: 'static'
    });
	myModal.show();
	$("#ModalSistema").draggable(); // permite a la ventana modal arrastrar con el método DRAG
	if (!$(".modal.in").length) { // reacomoda el modal en la pantalla de inicio.
        $(".modal").css({
            inset: "revert-layer"
        });
    }
}

function jsModalCrearCliente(){
	var ContenidoModal = "";
	ContenidoModal += '<label class="col-form-label">Nombres:</label>';
	ContenidoModal += '<input type="text" autocomplete="off" class="form-control" id="Nombres">';
	ContenidoModal += '<label class="col-form-label">Apellidos:</label>';
	ContenidoModal += '<input type="text" autocomplete="off" class="form-control" id="Apellidos">';
	ContenidoModal += '<label class="col-form-label">Edad:</label>';
	ContenidoModal += '<input type="number" autocomplete="off" class="form-control" id="Edad">';
	jsVentanaModal("Cliente Nuevo","Header-Verde",ContenidoModal,"Cerrar|danger|@Crear|primary|jsCrearUsuario()");
}

function jsCrearUsuario(){
    var Nombres     = document.getElementById("Nombres").value;
    var Apellidos   = document.getElementById("Apellidos").value;
    var Edad        = document.getElementById("Edad").value;

    var url_ruta = "/crear-cliente";

	var Datos = new FormData();
	Datos.append('Nombres', Nombres);	
	Datos.append('Apellidos', Apellidos);	
	Datos.append('Edad', Edad);	

    $.ajax({
		url: url_ruta,
		data: Datos,
		type: "post",
		dataType:"json",
		cache: false,
		processData: false,  // tell jQuery not to process the data
		contentType: false,  // tell jQuery not to set contentType		
		success: function(cJSON){
			if (cJSON.Resultado == 'ok'){
                $('#ModalSistema').modal('hide');
                
            }
		},
		error: function(obj1,TipoError,Error){
		}
	});	
}