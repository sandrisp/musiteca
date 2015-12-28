



var table;
var jTable;




function acciones_usuario(url){ 
	method = "PUT";
	form = $("form[name='form"+method+"']");
	var formData = form.serialize();
	
	var return_data = "hola";
	success = function(respuesta) { 
			$(".alert").remove();
			if(respuesta["valido"]){
				if(method=="PUT"){
					
				}
				return true;
			}

			form.find('input').closest("div").removeClass("has-error");
			error = respuesta["error"];
			$.each(error, function(i, item) {
				form.find('input[name='+i+']').closest("div").addClass("has-error");
				form.find('input[name='+i+']').closest("div").after(createAlert(item));
			});

			return false;
		}
	dataType = "json";


	$.ajax({type: method,
			url: url, 
			data: formData, 
			success: success, 
			dataType: dataType
	});

	return false;
}

function createRow(cancion){
	return "<tr id='cancion_"+ cancion["id"] +
				"' data-value='/static/music/"+ cancion["usuario_id"] +'/'+ cancion["id"] + '.'+ cancion["formato"]+"'"+
				"titulo='"+cancion["titulo"]+"' artista='" + cancion["artista"]+"' >"+
				"<td name='id'>"+ cancion["id"] + "</td>" +
				"<td name='titulo'>"+ 
					'<span class="glyphicon glyphicon glyphicon-music" aria-hidden="true"></span>&nbsp;'+
					cancion["titulo"] + "</td>" +
				"<td name='artista'>"+ cancion["artista"] + "</td>" +
				"<td name='formato'>"+ cancion["formato"] + "</td>" +
				"<td name='fecha_subida'>"+ cancion["fecha_subida"] + "</td>" +
			"</tr>"
}

function createAlert(error){
	return 	"<div class='alert alert-danger' role='alert' style='margin-top:25px'>"+
				"<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>"+
				"<span class='sr-only'>Error:</span>"+
				error + 
			"</div>";
}