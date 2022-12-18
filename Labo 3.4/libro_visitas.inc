<?php
// Localización del fichero de comentarios
$CMT_FILE='data/libro_visitas.xml';

// Verificar los datos del formulario de un nuevo comentario.
// RECUERDA que, aunque esta verificación se ha hecho en el cliente, es muy
//  recomendable hacerla también en el servidor.
// Si encuentra algún error devuelve un mensaje explicativo y, si no,
//  un mensaje vacío.
function ValidarFormServ($nombre, $email, $comentario)
{
	$error = '';
	// Verificar que los campos obligatorios están rellenados
	if($nombre == '')
		$error = $error.'<li>Tu nombre es obligatorio!</li>';
	if($comentario == '')
		$error = $error.'<li>No has introducido ningún comentario!</li>';
	// Verificar el formato de la dirección de correo
	if($email != '' && !VerificarFormatoCorreoServ($email))
		$error = $error.'<li>El formato de la dirección de correo no es correcto!</li>';
	return $error;
}

// Verificar el formato de una dirección de correo.
// Devuelve true si el formato de la dirección de correo es correcto y
//  false en caso contrario.
function VerificarFormatoCorreoServ($direccion)
{
	// Asegurar que '@' aparece una única vez
	$at=strpos($direccion,'@');
	if($at === false)	//  No se ha encontrado el carácter '@'
		return false;
	if($at != strrpos($direccion,'@')) // '@' ha aparecido más de una vez
		return false;
	// Asegurar que '@' no es el primer caracter
	if($at == 0)
		return false;
	// Asegurar que después de '@' hay, al menos, un punto
	$dot = strrpos($direccion,'.');
	if($dot === false) 	// No se ha encontrado un punto
		return false;
	if($dot < $at)		// No se ha encontrado un punto después de '@'
		return false;
	// Asegurar que después del último punto hay, al menos, dos caracteres
	if($dot+2 > strlen($direccion) - 1)
		return false;
	return true;
}

// Guardar un comentario nuevo en la base de datos.
// Devuelve false si ha habido algún error, y true en caso contrario.
function GuardarComentario($nombre, $email, $privado, $comentario)
{
	// Para usar $CMT_FILE como variagle global dentro de la función
	global $CMT_FILE;
      $etiq_visita = "visita"; // Etiqueta visita para los identificadores
	
	if(!file_exists($CMT_FILE)) // Si no existe el fichero XML
		// Crear nuevo fichero XML con la raíz <visitas>
		$bl=new SimpleXMLElement('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE visitas SYSTEM "libro_visitas.dtd"><visitas ult_id="' . $etiq_visita . '0"></visitas>');
	else	// Si no, cargar el fichero XML
		$bl=simplexml_load_file($CMT_FILE);
	if(!$bl)
		return false;
	// Calcular el identificador del nuevo comentario	
	$id = $etiq_visita . ((int) substr($bl['ult_id'], strlen($etiq_visita)) + 1);
	// Crear etiqueta 'visita' del nuevo comentario
	$nuevo=$bl->addChild('visita');
	$nuevo['id']=$id;
	// Crear las etiquetas asociadas a la nueva 'visita'
	$nuevo->addChild('fecha',date('r'));
	$nuevo->addChild('nombre',$nombre);
	$nuevo->addChild('comentario',$comentario);
	if($email!='')
	{
		$ep=$nuevo->addChild('email',$email);
		$ep->addAttribute('mostrar',$privado?'no':'si');
	}
	$bl['ult_id']=$id; // Actualizar el atributo 'ult_id' del libro de visitas
	return $bl->asXML($CMT_FILE); // Guardar fichero
}

function web_header(){
    echo '<!DOCTYPE html>';
    echo '<html>';
    echo '<head>';
    echo '<meta charset="utf-8">';
    echo '<title>Sitio Web SAR</title>';
    echo '<link href="css/main.css" rel="stylesheet">';
    echo '</head>';
    echo '<body>';
    echo '<div id="content">';
    echo '<!-- Logo Facultad de Informática -->';
    echo '<div id="banner">';
    echo '<img class="hr" id="logo" src="img/fakultatea.jpg" alt="Fachada exterior de la Facultad de Informatica">';
    echo '</div>';
    echo '<!-- Menú de navegación -->';
    echo '<ul id="menu">';
    echo '<li><a href="index.html">Inicio</a>';
    echo '</li>';
    echo '<div id="menu">';
    echo '<li><a href="comentario.html">Enviar Comentario</a></li>';

 

	//NOTA: Mostrar enlace a Libro de Visita

	echo '</div>';
    echo '</ul>';
    echo '<id="menu">';
	echo '</li>';
	echo '<a href="lista_coment.php">Libro de Visitas</a>';
    echo '</li>';
    echo '<div class="heading"><br><br><br>';
}

function web_footer(){
    echo '<img class="hr" src="img/line_gradient.gif">';
    echo 'Asignatura SAR. Grado en Ingeniería Informática. UPV-EHU';
    echo '</div><!--Main-->';
    echo '</div> <!-- content -->';
    echo '</body>';
    echo '</html>';
}
?>
