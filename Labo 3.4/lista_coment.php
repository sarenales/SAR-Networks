<?php
	require_once("libro_visitas.inc");
	web_header();
?>

		<p>Libro de Visita</p><br></div>
		<?php
			if(!file_exists($CMT_FILE))
			{
				echo('<p><br><br>El libro de visitas está vacío.</p>');
			}
			elseif(!($bl=simplexml_load_file($CMT_FILE)))
			{
				echo('<p><br><br>Ha habido algún error al leer el libro de visitas. Perdona las molestias.</p>');
			}
			else
			{

				echo '<p><br>';
				$cont=0;
				foreach($bl->visita as $visita)
				{
					// Para mostrar el comentario en curso se ha de cumplir alguna de estas 2 condiciones:
					//  (si se cumple la primera, la segunda no será evaluada)
					//   · No se ha especificado ningun nombre de usuario en 'nombre_busq'
					//   · Coincide el nombre de usuario de 'nombre_busq' y el del comentario en curso
					//      (se pasan los dos a minúsculas antes de comparar)
					if(!isset($_POST['nombre_busq']) ||
					   (strtolower($_POST['nombre_busq']) == strtolower($visita->nombre)) )
					{
						$cont++;
						echo('Fecha: '.$visita->fecha.'<br>');
						echo('Nombre: '.$visita->nombre.'<br>');
						if($visita->email && $visita->email['mostrar']=="si")
							echo('Email: '.$visita->email.'<br>');

						echo('Comentario: '.$visita->comentario.'<br>');

					}
					echo '<br><br>';
				}
				// Mostrar un mensaje de aviso si no se ha encontrado ningún comentario del usuario especificado
				if($cont==0)
					echo('No se ha encontrado ningún comentario del usuario: '.$_POST['nombre_busq']);
			}
			echo '</p></div><br>';

	web_footer();
	?>
