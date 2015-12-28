



var table;
var jTable;
var parametros_table = {
					ordering: true,
					paging: false,
					info: false,
					"language": {
						"search": "",
						"zeroRecords": "No se encontraron resultados",
						"infoEmpty": "No hay listas",
						"searchPlaceholder": "Buscar"
					},
					"columnDefs": [
						{ className: "hidden", "targets": [ 0 ] }
					],
					"columns": [
						{ "searchable": false},
						null
					]
				};
$(document).ready( function () {
	jTable = $('#table_lista');
	table = jTable.DataTable(parametros_table);

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
		noneAudio();
		limpia_input();
		accion="PUT";
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected').attr("listaId");
		form.find("input[name=lista_id]").val(value);
		
		value = $('tr.selected').attr("nombre");
		form.find("input[name=nombre]").attr("value",value);

		editar_lista();

	} );
	
	$('#btn_borrar').click( function () {
		cleanError();
		noneAudio();

		accion="DELETE";
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected td[name=id]').html();
		form.find("input[name=lista_id]").val(value);
		
	} );


} );

window.onbeforeunload = unloadPage;
function unloadPage() {
	noneAudio();
}

function uploadAudio(selected ){

	$.ajax({type: "GET",
		url: "/lista/"+selected.attr('listaId'),
		success: function(respuesta){
			$("#Audio_Col").html(respuesta);
		}, 
		dataType: "html",
	});
}
function uploadAudioShuffle( ){

	$.ajax({type: "GET",
		url: "/lista/"+$("tbody .selected").attr('listaId'),
		success: function(respuesta){
			$("#Audio_Col").html(respuesta);
		}, 
		dataType: "html",
		data: "orden=1"
	});
}
function noneAudio(){
	audio = $('audio');
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

	$("#Audio_Col").html('<div class="wrapper">Seleccion una lista.</div>')
	
}
function select_row(row){
	noneAudio();
	if(row.attr("listaid")==undefined){
		return
	}
	$('tr.selected').removeClass('selected');
	row.addClass('selected');
	$('#btn_editar').attr('disabled', false);
	$('#btn_borrar').attr('disabled', false);

	uploadAudio(row);
}

function editar_lista(){
	selected = jTable.find(".selected");
	$.ajax({type: "PUT",
		url: "/lista/"+selected.attr('listaId'),
		success: function(respuesta){
			$("#extraDivPUT").html(respuesta);
		}
	});
}

function acciones_lista(accion, url){ 
	noneAudio();
	method = accion;
	form = $("form[name='form"+accion+"']");
	var formData;
	formData = form.serialize();
	
	
	var return_data = "hola";
	success = function(respuesta) { 
			table_lista = $('#table_lista');
			if(respuesta["valido"]){
				$('#modal'+method).modal('hide');
				lista = respuesta["lista"];
				
				if(method=="POST"){
					jRow = $(createRow(lista));
					table.row.add(jRow).draw();
					select_row($("#lista_"+ lista["id"]));
				}else if(method=="PUT"){

					table.row($("#lista_"+ lista["id"])).remove();
					jRow = $(createRow(lista));
					table.row.add(jRow).draw();
					select_row($("#lista_"+ lista["id"]));
				}else if(method=="DELETE"){
					deselect_row($("#lista_"+ lista["id"]));
					table.row($("#lista_"+ lista["id"])).remove();
					table.draw();
				}
				
				return true;
			}

			cleanError();
			error = respuesta["error"];
			$.each(error, function(i, item) {
				form.find('input[name='+i+']').closest("div").addClass("has-error");
				form.find('input[name='+i+']').closest("div").after(createAlert(item));
			});

			return false;
		}
	dataType = "json";


	processData=true;
	contentType='application/x-www-form-urlencoded; charset=UTF-8';
	

	

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

function createRow(lista){
	return "<tr id='lista_"+ lista["id"] + "' " +
				"listaId='"+ lista["id"] +"' nombre='"+ lista["nombre"] + "' >"+
				"<td name='id'>"+ lista["id"] + "</td>" +
				"<td name='nombre'>"+ 
					'<span class="glyphicon glyphicon glyphicon-list" aria-hidden="true"></span>&nbsp;' +lista["nombre"] + 
				"</td>" +
			"</tr>";
}
function createAlert(error){
	return 	"<div class='alert alert-danger' role='alert' style='margin-top:25px'>"+
				"<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>"+
				"<span class='sr-only'>Error:</span>"+
				"&nbsp;" + error + 
			"</div>";
}
function cleanError(){
	$(".alert").remove();
	$("form").find('input').closest("div").removeClass("has-error");
}
function limpia_input(){
	$("input").val("");
	$('form[name=formPOST]')[0].reset();
	$('form[name=formPUT]')[0].reset();
	$('form[name=formDELETE]')[0].reset();
}