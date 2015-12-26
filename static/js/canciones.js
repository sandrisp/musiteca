



var table;

$(document).ready( function () {
	table = $('#table_cancion').DataTable({
					ordering: true,
					paging: false,
					info: false,
					"language": {
						"search": "",
						"zeroRecords": "No se encontraron resultados",
						"infoEmpty": "No hay canciones",
						"searchPlaceholder": "Buscar"
					},
					"columnDefs": [
						{ className: "hidden", "targets": [ 0 ] }
					],
					"columns": [
						{ "searchable": false},
						null,
						null,
						null,
						{ "searchable": false }
					]
				});
	$('div.dataTables_filter input').addClass('form-control');

	$('#table_cancion tbody').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			deselect_row($(this));

		} else {
			select_row($(this));


		}
	} );
	$('#btn_agregar').click( function () {
		$('#modalPOST').modal('show');
	} );
	$('#btn_editar').click( function () {

		accion="PUT";
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected td[name=id]').html();
		form.find("input[name=cancion_id]").attr("value", value);
		
		value = $('tr.selected td[name=titulo]').html();
		form.find("input[name=titulo]").attr("value", value);

		value = $('tr.selected td[name=artista]').html();
		form.find("input[name=artista]").attr("value", value);
		
		$('#modalPUT').modal('show');	

	} );
	$('#btn_borrar').click( function () {
		accion="DELETE";
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected td[name=id]').html();
		form.find("input[name=cancion_id]").attr("value", value);

		$('#modalDELETE').modal('show');			
	} );


} );

function deselect_row(row){

	selected = $("#table_cancion .selected");
	audio = $('#audio');

	source = $('#mp3Source');
	source.removeAttr( "src");

	row.removeClass('selected');
	$('#btn_editar').attr('disabled', true);
	$('#btn_borrar').attr('disabled', true);


}
function select_row(row){
	$('tr.selected').removeClass('selected');
	row.addClass('selected');
	$('#btn_editar').attr('disabled', false);
	$('#btn_borrar').attr('disabled', false);

	selected = $("#table_cancion .selected");
	audio = $('#audio');

	source = $('#mp3Source');
	source.attr( "src", selected.attr('data-value') );

	audio.trigger('load');
}



function acciones_cancion(accion, url){ 
	method = accion;
	form = $("form[name='form"+accion+"']");
	var formData;
	if(method=="POST"){
		formData = new FormData(form[0]);
	}else{
		formData = form.serialize();
	}
	
	var return_data = "hola";
	success = function(respuesta) { 

			if(respuesta["valido"]){
				$('#modal'+method).modal('hide');
				cancion = respuesta["cancion"];
				if(method=="POST"){
					select_row($("#cancion_"+ cancion["id"]));
					$("#table_cancion tbody").append(
							"<tr id='cancion_"+ cancion["id"] +
								"' data-value='/static/music/"+ cancion["usuario_id"] +'/'+ cancion["id"] + '.'+ cancion["formato"]+"'"+
								"titulo='"+cancion["titulo"]+"' artista='" + cancion["artista"]+"'"+
								"<td name='id'>"+ cancion["id"] + "</td>" +
								"<td name='titulo'>"+ cancion["titulo"] + "</td>" +
								"<td name='artista'>"+ cancion["artista"] + "</td>" +
								"<td name='formato'>"+ cancion["formato"] + "</td>" +
								"<td name='fecha_subida'>"+ cancion["fecha_subida"] + "</td>" +
							"</tr>");
				}else if(method=="PUT"){
					$("#cancion_"+ cancion["id"]).remove();
					$("#table_cancion tbody").append(
							"<tr id='cancion_"+ cancion["id"] +"' data-value='/static/music/"+ cancion["usuario_id"] +'/'+ cancion["id"] + '.'+ cancion["formato"]+"'"+
								"titulo='"+cancion["titulo"]+"' artista='" + cancion["artista"]+"'"+
								"<td name='id'>"+ cancion["id"] + "</td>" +
								"<td name='titulo'>"+ cancion["titulo"] + "</td>" +
								"<td name='artista'>"+ cancion["artista"] + "</td>" +
								"<td name='formato'>"+ cancion["formato"] + "</td>" +
								"<td name='fecha_subida'>"+ cancion["fecha_subida"] + "</td>" +
							"</tr>");
				}else if(method=="DELETE"){
					deselect_row($("#cancion_"+ cancion["id"]));
					$("#cancion_"+ cancion["id"]).remove();
				}
				return true;
			}

			form.find('input').closest("div").removeClass("has-error");
			error = respuesta["error"];
			$.each(error, function(i, item) {
				form.find('input[name='+i+']').closest("div").addClass("has-error");
			});

			return false;
		}
	dataType = "json";

	if(method=="POST"){
		processData=false;
		contentType=false;
	}else{
		processData=true;
		contentType='application/x-www-form-urlencoded; charset=UTF-8';
	}

	$.ajax({type: method,
			url: url, 
			data: formData, 
			success: success, 
			dataType: dataType,
			processData: processData,  // tell jQuery not to process the data
			contentType: contentType
	});

	return false;
}