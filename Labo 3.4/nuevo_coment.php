<?php
	require_once('libro_visitas.inc');

	// Guardar los datos del forumulario y quitar los espacios en blanco (trim)
	$nombre=trim($_POST['nombre']);
	$email=trim($_POST['email']);
	$privado=isset($_POST['privado']);
	$comentario=trim($_POST['comentario']);

	// Validar los datos del formulario
	$error = ValidarFormServ($nombre, $email, $comentario);
	if($error == '')
		// Guardar comentario en la base de datos (Fichero XML)
		if(!GuardarComentario($nombre, $email, $privado, $comentario))
			$error = '<li>No se ha podido guardar el comentario en la base de datos!</li>';

    web_header(); //cabecera: logo y menú navegación

    if($error==''){
		echo '<p>Gracias por dejar tu comentario</p></div><br>';
    }
	else{
		echo '<p>Error al recoger el comentario</p></div><br>';
    }
    web_footer(); //pie de página
?>


