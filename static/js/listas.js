



var table;
var jTable;
$(document).ready( function () {
	jTable = $('#table_lista');
	table = jTable.DataTable({
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
				});

	$('div.dataTables_filter input').addClass('form-control');

	jTable.find('tbody').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			deselect_row($(this));

		} else {
			select_row($(this));


		}
	} );

	$('#btn_editar').click( function () {

		accion="PUT";
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected td[name=id]').html();
		form.find("input[name=lista_id]").attr("value", value);
		
		value = $('tr.selected td[name=nombre]').html();
		form.find("input[name=nombre]").attr("value", value);


	} );
	
	$('#btn_borrar').click( function () {
		accion="DELETE";
		form = $("form[name='form"+accion+"']");

		value = $('tr.selected td[name=id]').html();
		form.find("input[name=lista_id]").attr("value", value);
		
	} );


} );

window.onbeforeunload = unloadPage;
function unloadPage() {
	//noneAudio();
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

	//noneAudio();
	
	row.removeClass('selected');
	$('#btn_editar').attr('disabled', true);
	$('#btn_borrar').attr('disabled', true);

	
}
function select_row(row){
	$('tr.selected').removeClass('selected');
	row.addClass('selected');
	$('#btn_editar').attr('disabled', false);
	$('#btn_borrar').attr('disabled', false);

	selected = jTable.find(".selected");

	//uploadAudio(selected);
}



function acciones_lista(accion, url){ 
	method = accion;
	form = $("form[name='form"+accion+"']");
	var formData;
	formData = form.serialize();
	
	
	var return_data = "hola";
	success = function(respuesta) { 

			if(respuesta["valido"]){
				$('#modal'+method).modal('hide');
				lista = respuesta["lista"];
				if(method=="POST"){
					jTable.find("tbody").append(createRow(lista));
					select_row($("#lista_"+ lista["id"]));
				}else if(method=="PUT"){
					$("#lista_"+ lista["id"]).remove();
					jTable.find("tbody").append(createRow(lista));
					select_row($("#lista_"+ lista["id"]));
				}else if(method=="DELETE"){
					deselect_row($("#lista_"+ lista["id"]));
					$("#lista_"+ lista["id"]).remove();
				}
				table.draw();
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


	processData=true;
	contentType='application/x-www-form-urlencoded; charset=UTF-8';
	

	//noneAudio();

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
				"<td name='nombre'>"+ lista["nombre"] + "</td>" +
			"</tr>"
}
