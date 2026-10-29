# Cielo personal, luz y cristal

## Qué representa

El fondo utiliza un catálogo real: XHIP, en coordenadas J2000, mediante los archivos de ofrohn/d3-celestial. Se seleccionaron estrellas hasta magnitud 4 y todos los vértices necesarios para el trazado de Virgo. Astropy transforma las coordenadas al horizonte del observador y al instante de referencia proporcionado por Omar. En esta configuración quedan 280 estrellas y las 13 de Virgo por encima del horizonte geométrico.

Es una representación de posiciones astronómicas, sin atmósfera. El instante corresponde a horas diurnas: esos puntos no se habrían podido observar a simple vista durante el día. No representa meteorología, contaminación lumínica ni visibilidad fotográfica. Se usa una referencia aproximada del lugar: no se verificó por geocodificación el edificio indicado. No se aplican movimientos propios individuales del catálogo; la transformación sí utiliza el marco celeste y orientación terrestre mediante Astropy/IERS.

El Sol resulta aproximadamente a 79,20° de altura y 150,58° de acimut (desde el norte hacia el este). Su punto proyectado controla el centro del halo ambiental en ambos temas. El foco interactivo del puntero es una capa artística independiente que ya existía en la web; no se presenta como una simulación física completa de iluminación.

## Composición

Proyección azimutal equidistante, girada −90° para la composición. Se mantiene la misma transformación para todas las estrellas, Virgo y el Sol. La imagen se recorta según la ventana; en móvil se centra horizontalmente la región de Virgo. No es un mapa de navegación ni una carta astronómica completa.

Los puntos conservan sus posiciones. En modo día, su azul gris tiene contraste suficiente para reconocer el cielo sin pasar el cursor. Una máscara cercana al cursor ilumina copias de los mismos puntos en blanco con un borde azul definido; desaparece al salir del área y no cambia el aspecto nocturno. El puntero se transforma al mismo sistema de coordenadas del SVG, también tras cambiar el ancho. El trazado de Virgo aparece por proximidad del puntero y al pasar o enfocar el nombre pequeño «Omar Vásquez» del encabezado. Por preferencia expresa de Omar, ese nombre es ahora también el enlace a la ficha personal: pulsarlo o usar Enter abre la ficha; no alterna un segundo estado. El enlace tiene una pista de clic y una flecha subrayada. No se muestra un botón Virgo ni una nota explicativa al pie. La capa gráfica no captura clics. Con movimiento reducido cambia sin animación; en alto contraste se omite el detalle decorativo.

Se recuperó el solapamiento moderado del lema en escritorio, sin alterar las posiciones tipográficas de OMAR o Vásquez. Transparencia más alta y blur de 6 px permiten ver el apellido bajo el borde. En móvil se conserva la separación. Cuando se solicita transparencia reducida o el filtro no está disponible, una superficie sólida y mayor separación protegen la lectura.

## Privacidad

El archivo de fecha/hora/localización y el informe del cálculo están **fuera del checkout público**. El generador rechaza un archivo de configuración situado dentro del proyecto. No se distribuyen esos archivos en Git, `dist/web`, el HTML autónomo o el ZIP de revisión. El público recibe las posiciones dibujadas y el punto solar, sin campos de fecha, hora, hospital ni coordenadas del observador.

El navegador no consulta un servicio astronómico, no usa geolocalización del visitante y no envía el puntero a ningún servidor. El estado de Virgo solo vive en la pestaña; no añade almacenamiento de preferencias ni cookies. Los registros habituales del alojamiento son una cuestión separada.

## Archivos y regeneración

- `tools/data/bright-stars-virgo.json`: subconjunto de catálogo y trazado.
- `tools/generate_sky.py`: cálculo opcional de diseño; requiere `tools/requirements-sky.txt`.
- `assets/sky/sky-fragment.html`: SVG generado, también insertado en `index.html` entre marcadores.
- `assets/sky/solar.css`: posición solar inicial.
- `sky.css` / `sky.js`: aspecto e interacción local.

El build habitual no instala Astropy ni NumPy: usa los archivos ya generados. Para cambiar el instante de referencia, crear un JSON privado **fuera** del repositorio con `date` ISO, `local_time`, `timezone` IANA, `latitude`, `longitude`, `elevation_m` y una nota `location_accuracy`. No asumir que la hora actual de Venezuela es válida para toda su historia: la zona IANA resuelve el desfase histórico.

Instalar las dependencias opcionales en un entorno Python de desarrollo y ejecutar:

```sh
python3 tools/generate_sky.py /ruta/privada/sky-config.json
python3 build.py --keep-pdfs
```

El proceso funciona sin descargas de efemérides: utiliza `get_sun` de Astropy y datos IERS instalados, con la descarga automática desactivada. La ubicación no debe tener una precisión mayor de la que realmente se verificó.

## Procedencia y licencia

Fuente fijada: ofrohn/d3-celestial, commit `7e720a3de062059d4c5400a379146a601d9010e0`.

- [Catálogo de estrellas](https://raw.githubusercontent.com/ofrohn/d3-celestial/7e720a3de062059d4c5400a379146a601d9010e0/data/stars.6.json): fuente XHIP, Anderson y Francis (2012), según README del proyecto.
- [Trazado de constelaciones](https://raw.githubusercontent.com/ofrohn/d3-celestial/7e720a3de062059d4c5400a379146a601d9010e0/data/constellations.lines.json): adaptación del proyecto; no se afirma que exista una forma oficial única para unir las estrellas.
- [Licencia](https://raw.githubusercontent.com/ofrohn/d3-celestial/7e720a3de062059d4c5400a379146a601d9010e0/LICENSE): BSD-3-Clause. Texto completo distribuido en `assets/sky/LICENSE-d3-celestial.txt` y en los metadatos SVG del HTML autónomo.

## Validación

`checks/sky_smoke.py` comprueba los 280 puntos y 13 vértices, transformaciones concordantes entre Sol y halo, encuadre de Virgo, interacción de proximidad/tacto/teclado, movimiento reducido, ausencia de capa que capture enlaces y fallback sin JS. Acepta como primer argumento la URL local donde se sirve `dist/web`.

La regresión de preferencias conserva las 18 combinaciones de idioma/tema/ancho. Capturas revisadas en móvil y escritorio, noche/día y con/sin trazado. La fecha, hora y geografía de la configuración no se han publicado ni se ha hecho push.
