// Verificar los datos del formulario de un nuevo comentario.
// Si encuentra algún error muestra una ventana de alerta y devuelve false.
// Si todo ha ido bien, devuelve true.
function ValidarForm(f)
{
	// Leer valores del formulario
	var nombre = f.nombre.value;
	var email = f.email.value;
	var privado = f.privado.checked;
	var comentario = f.comentario.value;
	
	var error = "";
	// Verificar que los campos obligatorios están rellenados
	if(nombre=="")
		error += "\tTu nombre es obligatorio!\n";
	if(comentario=="")
		error += "\tNo has introducido ningún comentario!\n";
	
	// Verificar el formato de la dirección de correo
	if(email != "" && !VerificarFormatoCorreo(email))
		error += "\tEl formato de la dirección de correo no es correcto!\n";
		
	// Si hay algún error, mostrar el mensaje
	if(error != "")
	{
		alert("Validación del formulario:\n" + error);
		return false;
	}
	else
		return true;
}

// Verificar el formato de una dirección de correo
// Devuelve true si el formato de la dirección de correo es correcto y false en caso contrario
function VerificarFormatoCorreo(direccion)
{
	// Asegurar que '@' aparece una única vez
	if(direccion.split("@").length != 2)
		return false;
	// Asegurar que '@' no es el primer caracter
	if(direccion.indexOf("@") == 0)
		return false;
	// Asegurar que después de '@' hay, al menos, un punto
	if(direccion.lastIndexOf(".") < direccion.lastIndexOf("@"))
		return false;
	// Asegurar que después del último punto hay, al menos, dos caracteres
	if(direccion.lastIndexOf(".") + 2 > direccion.length - 1)
		return false;
	return true;
}
