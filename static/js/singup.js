
		function valid_insert_user(url, exito){ 

			data = $("form[name='singup']").serialize();

			var return_data = "hola";
			success = function(respuesta) { 
					$(".alert").remove();

					if(respuesta["valido"]){

						

						action=exito;
						$("form[name=singup]").attr("action", action);
						$("form[name=singup]").removeAttr("onsubmit");
						$("form[name=singup]").submit();

						return true;
					}

					$('form[name=singup] input').closest("div").removeClass("has-error");
					error = respuesta["error"];
					$.each(error, function(i, item) {
						$('input[name='+i+']').closest("div").addClass("has-error");
						$('input[name='+i+']').closest("div").after(createAlert(item));
					});

					$("form[name=singup]").removeAttr("action");
					return false;
				}
			dataType = "json";

			$.ajax({method: "POST",url: url, data: data, success: success, dataType: dataType});

			return false;
		}

function createAlert(error){
	return 	"<div class='alert alert-danger' role='alert' style='margin-top:25px'>"+
				"<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>"+
				"<span class='sr-only'>Error:</span>"+
				error + 
			"</div>";
}