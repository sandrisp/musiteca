



var table;
var jTable;
$(document).ready( function () {
	jTable = $('#table_cancion');
	table = jTable.DataTable({
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

	jTable.find('tbody').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			deselect_row($(this));

		} else {
			select_row($(this));


		}
	} );

	$('#btn_agregar').click( function () {
		cleanError();
		noneAudio();
		limpia_input();

	} );

	$('#btn_editar').click( function () {

		cleanError();

		accion="PUT";
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected').attr("cancionid");
		form.find("input[name=cancion_id]").val(value);
		
		value = $('tr.selected').attr("titulo");
		form.find("input[name=titulo]").val(value);

		value = $('tr.selected').attr("artista");
		form.find("input[name=artista]").val(value);
		

	} );
	
	$('#btn_borrar').click( function () {
		accion="DELETE";
		cleanError();
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected td[name=id]').html();
		form.find("input[name=cancion_id]").val(value);

	} );


} );


window.onbeforeunload = unloadPage;
function unloadPage() {
	noneAudio();
}

function uploadAudio(selected){
	audio = $('#mp3Source');
	var timestamp = new Date().getTime();
	audio.attr( "src", selected.attr('data-value')+ "?i=" +timestamp);
	audio.trigger('load');

}

function noneAudio(){
	audio = $('#mp3Source');
	audio.trigger("pause");
	audio.removeAttr( "src");
	audio.trigger('load');
}

function deselect_row(row){

	selected = jTable.find(".selected");

	noneAudio();
	
	row.removeClass('selected');
	$('#btn_editar').attr('disabled', true);
	$('#btn_borrar').attr('disabled', true);

	
}
function select_row(row){
	if(row.attr("cancionid")==undefined){
		return
	}
	$('tr.selected').removeClass('selected');
	row.addClass('selected');
	$('#btn_editar').attr('disabled', false);
	$('#btn_borrar').attr('disabled', false);

	selected = jTable.find(".selected");

	uploadAudio(selected);
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
					jRow = $(createRow(cancion));
					table.row.add(jRow).draw();
					select_row($("#cancion_"+ cancion["id"]));
				}else if(method=="PUT"){
					table.row($("#cancion_"+ cancion["id"])).remove();
					jRow = $(createRow(cancion));
					table.row.add(jRow).draw();
					select_row($("#cancion_"+ cancion["id"]));
				}else if(method=="DELETE"){
					deselect_row($("#cancion_"+ cancion["id"]));
					table.row($("#cancion_"+ cancion["id"])).remove();
					table.draw();
				}
				return true;
			}
			$(".alert").remove();
			form.find('input').closest("div").removeClass("has-error");
			error = respuesta["error"];
			$.each(error, function(i, item) {
				form.find('input[name='+i+']').closest("div").addClass("has-error");
				form.find('input[name='+i+']').closest("div").after(createAlert(item));
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

	noneAudio();

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

function createRow(cancion){
	return "<tr id='cancion_"+ cancion["id"] +
				"' data-value='/static/music/"+ cancion["usuario_id"] +'/'+ cancion["id"] + '.'+ cancion["formato"]+"'"+
				"titulo='"+cancion["titulo"]+"' artista='" + cancion["artista"]+"' cancionId='"+ cancion["id"] +"' >"+
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

function cleanError(){
	$(".alert").remove();
	$("form").find('input').closest("div").removeClass("has-error");
}
function limpia_input(){
	$("input").val("");
}
