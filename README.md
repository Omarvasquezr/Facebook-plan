# Portfolio de Omar Vásquez

Sitio estático, sin dependencias de producción ni servicios externos de traducción. Base importada del ZIP proporcionado por Omar. Los documentos privados y los identificadores de Vercel no forman parte del proyecto.

## Preparar y revisar

```sh
python3 build.py --keep-pdfs
python3 -m http.server 4174 --bind 127.0.0.1 --directory dist/web
```

La única carpeta de publicación es `dist/web`. `--keep-pdfs` reutiliza los PDF originales y prepara la web sin regenerarlos. No publica nada. Para revisar en esta máquina, hacer solicitudes locales al servidor; no asumir que sus procesos sobreviven al reinicio del entorno.

`dist/allegati/Omar-Vasquez-CV.html` es una vista autónoma: incluye fuentes, CSS y JavaScript, y se puede abrir sin conexión. Como en el generador original, omite la sección de descargas. Los dos PDF conservados también están en esa carpeta.

## Preferencias

- Planeta de la barra: italiano, español e inglés. Traducción local de textos, metadatos y etiquetas accesibles, sin cambiar fechas o nombres propios.
- Italiano inicial; elección recordada en `localStorage` (`ov-language`). El atributo `lang` acompaña la elección.
- Interruptor sol/luna al pie y acceso en la barra, sincronizados. Inicialmente sigue al sistema; después recuerda la elección (`ov-theme`). Se adapta a cambios del sistema mientras no haya elección manual.
- Las preferencias se sincronizan entre pestañas. Si el navegador bloquea el almacenamiento, los controles siguen funcionando en la pestaña actual.
- Respeta movimiento reducido. Selector operable con Tab, Enter/Espacio, flechas, Inicio/Fin y Escape; también se cierra al salir o pulsar fuera.
- Los PDF existentes están en italiano y se identifican así en los tres idiomas. No se han generado documentos traducidos.

`preferences.js` centraliza las traducciones: las filas de `content` siguen el orden italiano, español, inglés; `ui` contiene los textos de controles. Si cambia un texto italiano en HTML, actualizar su entrada. `preferences.css` contiene los controles, los estados y el tema nocturno. El script temprano del HTML aplica el tema guardado antes del primer pintado.

## Comprobaciones

Con Python, Chromium y Playwright disponibles:

```sh
# Si se sirve la raíz del proyecto:
python3 checks/preferences_smoke.py http://127.0.0.1:4174/dist/web/
# Si se sirve directamente dist/web como arriba:
python3 checks/preferences_smoke.py http://127.0.0.1:4174/
```

La comprobación cubre 18 combinaciones de idioma/tema/ancho (320, 390 y 1440 px), traducciones, geometría, teclado, persistencia, preferencia del sistema, almacenamiento bloqueado y recursos descargables. No sustituye la revisión visual.

## PDF y publicación

`python3 build.py` utiliza Chromium para regenerar las presentaciones originales desde `deck.html`. Conservar los originales antes de hacerlo. La opción heredada `--deploy` publica en producción y requiere autorización expresa; no se ha utilizado.

Las fuentes Jost y Cormorant Garamond se distribuyen con sus textos OFL 1.1 en `fonts/`, obtenidos de las carpetas oficiales correspondientes de Google Fonts. El planeta es un SVG local y el interruptor usa CSS. La referencia de Sean Halpin sirve de inspiración solicitada; no hay código extraído ni colaboración atribuida a ese diseñador. La red de esta máquina no permitió inspeccionar la página de referencia.

## Entrada, favicon y tarjeta para compartir

- `intro.css` / `intro.js` y el SVG del HTML dibujan una lámpara articulada propia: busca con el haz y revela OV. Es una entrada decorativa de unos 1,9 segundos, no un indicador ficticio de descarga. No usa vídeos ni librerías.
- Se muestra una vez por sesión; se omite con movimiento reducido y desaparece al interactuar con teclado/puntero. Tiene salida CSS y temporizador de respaldo; no bloquea la navegación ni anuncia una carga falsa a lectores de pantalla.
- Para repetirla durante una revisión, abrir el servidor local con `?intro=1`. El HTML autónomo también admite ese parámetro al abrirlo localmente.
- `favicon.svg` contiene trazados de OV basados en Jost, azul y naranja sobre fondo claro; no necesita fuentes cargadas. Se distribuyen ICO de 16/32/48 px, PNG de 32 px y Apple Touch Icon de 180 px.
- `assets/omar-vasquez-social-v1.png`: tarjeta PNG de 1200×630 px. `tools/social-card.html` conserva su diseño editable con las fuentes locales. La imagen no añade una descarga a la carga habitual de la web: la referencian los metadatos.
- Open Graph y Twitter Card están presentes en el HTML inicial, con URL HTTPS absoluta, dimensiones, tipo MIME, texto alternativo y canonical. Los robots de mensajería no necesitan ejecutar JavaScript.
- El enlace canónico es `https://omar-vasquez.vercel.app/`. La tarjeta del enlace raíz está en italiano, el idioma inicial; cambiar de idioma en el navegador traduce los metadatos en esa pestaña, pero no cambia lo que recibe un robot que consulta el mismo enlace raíz. No se prometen tarjetas por idioma sin rutas públicas distintas.
- Publicar **todo** `dist/web` es necesario para que WhatsApp y otros servicios puedan leer los metadatos y descargar la imagen. El archivo HTML enviado por chat no publica la tarjeta. La apariencia real en cada servicio y su caché solo se podrán comprobar después de publicar; no se ha publicado ni enviado ningún mensaje.
- Si se sustituye la imagen más adelante, cambiar su nombre/versionado en los metadatos para distinguir el recurso nuevo de las copias en caché. Se conserva la política `noindex, nofollow` original; no se ha cambiado la visibilidad en buscadores.

Para regenerar los PNG e ICO desde los diseños locales, con Chromium, Playwright y Pillow instalados, servir la raíz del proyecto en desarrollo y ejecutar:

```sh
python3 tools/generate_brand_assets.py http://127.0.0.1:4174/
python3 build.py --keep-pdfs
```

Los diseños y los archivos generados están incluidos, por lo que el build habitual no necesita esas herramientas de diseño. La lámpara es un dibujo propio, sin personajes ni recursos extraídos de Pixar.

Comprobación adicional de entrada, iconos y metadatos (mismo argumento de URL base que la comprobación de preferencias):

```sh
python3 checks/branding_smoke.py http://127.0.0.1:4174/dist/web/
```
