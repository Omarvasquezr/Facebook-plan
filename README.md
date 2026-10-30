# Portfolio de Omar Vásquez

Sitio estático, sin dependencias de producción ni servicios externos de traducción. Base importada del ZIP proporcionado por Omar. Los documentos privados y los identificadores de Vercel no forman parte del proyecto.

## Preparar y revisar

```sh
python3 build.py --keep-pdfs
python3 -m http.server 4174 --bind 127.0.0.1 --directory dist/web
```

La única carpeta de publicación es `dist/web`. `--keep-pdfs` reutiliza los PDF originales y prepara la web sin regenerarlos. No publica nada. Para revisar en esta máquina, hacer solicitudes locales al servidor; no asumir que sus procesos sobreviven al reinicio del entorno.

`vercel.json` publica la carpeta ya generada `dist/web`, sin instalar dependencias ni ejecutar un build remoto. Antes de subir cambios de código o de imágenes, preparar `python3 build.py --keep-pdfs` e incluir también los archivos generados. La documentación, comprobadores y herramientas permanecen fuera de la raíz pública. Se conserva `noindex,nofollow` por elección de Omar.

`dist/allegati/Omar-Vasquez-CV.html` es una vista autónoma: incluye fuentes, CSS y JavaScript, y se puede abrir sin conexión. Como en el generador original, omite la sección de descargas. Los dos PDF conservados también están en esa carpeta.

## Preferencias

- Planeta de la barra: italiano, español e inglés. Traducción local de textos, metadatos y etiquetas accesibles, sin cambiar fechas o nombres propios.
- Italiano inicial; elección recordada en `localStorage` (`ov-language`). El atributo `lang` acompaña la elección.
- Interruptor sol/luna al pie y acceso en la barra, sincronizados. Inicialmente sigue el horario de Italia (`Europe/Rome`): noche de 18:00 a 05:59 y día de 06:00 a 17:59, con cambio de horario de verano/invierno. Una elección manual se recuerda en `ov-theme`; «Auto · Italia» la borra y vuelve al horario.
- Las preferencias se sincronizan entre pestañas. Si el navegador bloquea el almacenamiento, los controles siguen funcionando en la pestaña actual.
- Respeta movimiento reducido. Selector operable con Tab, Enter/Espacio, flechas, Inicio/Fin y Escape; se cierra al recibir otro elemento el foco o pulsar fuera. Una pérdida de foco sin destino no cancela la selección táctil o con ratón.
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

La comprobación cubre 18 combinaciones de idioma/tema/ancho (320, 390 y 1440 px), traducciones, geometría, teclado, persistencia, horario italiano, elección manual, almacenamiento bloqueado y recursos descargables. Incluye selección táctil y el caso en que el navegador desenfoca un botón sin asignar el foco al siguiente antes del clic. No sustituye la revisión en navegadores nativos.

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

## Revisión de luz y cristal

La rama `review/hero-light-glass` conserva el diseño y añade una propuesta local de halo nocturno y cristal para el lema. El recuadro deja libre el apellido completo, incluidos sus descendentes. Se mantienen los idiomas y los archivos PDF originales. Las decisiones, referencias oficiales consultadas, límites de la investigación y propuesta para el retrato/UGC están en `docs/REVISION-VISUAL.md`.

Preparar con `python3 build.py --keep-pdfs` y revisar `dist/web` como antes. Estos ajustes no están publicados; no se añadió la foto de casting ni vídeos.

## Cielo personal y Virgo

La rama `review/birth-sky-glass` añade puntos calculados de un catálogo real, trazado interactivo de Virgo y halo situado a partir de la posición solar de referencia. El público recibe solo el gráfico; el archivo natal permanece fuera del proyecto. Los detalles, procedencia BSD, aproximaciones y regeneración están en `docs/CIELO.md`.

El recuadro vuelve a un solapamiento moderado con cristal más transparente (6 px de blur); las preferencias de transparencia reducida conservan superficies sólidas y más espacio. El trazado es un detalle oculto: se revela por proximidad y al pasar o enfocar el nombre pequeño **Omar Vásquez** del encabezado. Según la preferencia más reciente de Omar, pulsar ese nombre o usar Enter abre la ficha personal. No hay botón Virgo visible ni nota al pie. No hay animación de estrellas ni servicios astronómicos cargados desde el navegador.

Preparar con `python3 build.py --keep-pdfs`. Validar con `python3 checks/sky_smoke.py URL_LOCAL` y el comprobador existente de preferencias. No hay cambios publicados en GitHub/Vercel.

## Áreas de trabajo y ficha personal

`Competenze` sustituye la lista de programas por cuatro áreas: Producción, Operaciones, Negocio y Tecnología. Cada botón abre un único panel con un resumen, cuatro capacidades y herramientas de apoyo; volver a pulsarlo o usar Escape lo cierra. Las flechas e Inicio/Fin recorren los botones. En móvil los cuatro botones están visibles en una cuadrícula 2×2; los controles no se mueven solos. Una indicación breve y un chevrón que gira al abrir hacen explícito el desplegable.

`expertise.css/js` gestionan las áreas. Los textos nuevos están en `ui` de `preferences.js`, en italiano, español e inglés. Los programas se conservan en un desplegable nativo «Herramientas y recursos» dentro de cada área; la lectura inicial no repite la lista de software. El liderazgo operativo, la coordinación multidisciplinar y las decisiones bajo presión se expresan una sola vez en una línea compartida, visible al abrir un área. Sin JavaScript se muestran las cuatro áreas completas y se ocultan los controles inactivos.

`profile.css/js` convierten la sección `#about-omar` en un único diálogo nativo. Se abre desde el nombre pequeño «Omar Vásquez», con pista de clic y flecha subrayada, o el acceso al pie; Escape, el cierre visible y el fondo exterior permiten cerrarlo y devolver el foco al acceso original. La firma tipográfica mantiene su tamaño y posición. El nombre pequeño conserva la revelación de Virgo por hover/foco. Sin JavaScript los enlaces llevan a la misma sección al pie.

La ficha contiene residencia, intereses y valores expresados por Omar. El retrato original del ZIP de Omar está en `assets/omar-vasquez-portrait.jpg`, sin retoques ni sustitución generada. El build lo añade a la ficha y lo incrusta en el HTML autónomo, con texto alternativo traducido. Para reemplazarlo, conservar ese nombre o usar `.webp`, `.jpeg` o `.png`; el bloque marcado `profile:portrait:start/end` se normaliza durante el build. Si falta el archivo, el build omite la imagen. No se publican fecha de nacimiento o coordenadas. Las nuevas interacciones y sus recursos están incluidos también en el HTML autónomo.

Después del build, comprobar con `python3 checks/expertise_profile_smoke.py URL_LOCAL`, además de las pruebas de preferencias y cielo cuando corresponda. La revisión local no publica la web ni actualiza GitHub.

Las herramientas confirmadas más recientes se distribuyen por contexto: Canva y productos Google de publicidad/SEO/medición en marketing; Adobe Creative Cloud para fotografía, AutoCAD para dibujo técnico, fotografía/cámaras y edición profesional de audio en producción; Google Workspace y ofimática en operaciones; Windows, Fedora Linux y macOS avanzados, Google Flow, automatización y trabajo con iOS/Android en tecnología. La experiencia móvil incluye configuración, diagnóstico, reparación, modificaciones, privacidad, accesibilidad para mayores y desarrollo de aplicaciones asistido por IA. Los programas sugeridos para refrescar la memoria no se incorporan como experiencia sin confirmación.

## Horario italiano y estrellas diurnas

`theme-clock.js` se carga antes del primer pintado y resuelve el tema con la zona IANA `Europe/Rome`, sin ubicación del visitante ni peticiones externas. Sin elección manual, actualiza al llegar las 18:00/06:00 y al volver a la pestaña. El interruptor conserva una elección manual; «Auto · Italia» restablece el horario y se sincroniza con las demás pestañas. Si el navegador carece de datos IANA, el respaldo es el tema del sistema. No añade cookies.

En modo día, los puntos reales del catálogo permanecen visibles en azul gris y se iluminan en blanco cerca del cursor, con un borde azul definido. La máscara sigue la misma transformación SVG y se oculta al salir. La capa es decorativa, no captura clics y no altera las estrellas nocturnas ni el color de Virgo.

Validar el horario con `python3 checks/theme_clock_smoke.py URL_LOCAL`, además de preferencias, áreas/ficha y cielo. Los nuevos grupos de herramientas incluyen las aplicaciones confirmadas; REAPER, Ahrefs, Tailscale y Revit no se incorporaron.

## Pulido de competencias y retrato

La organización más reciente sigue los bloques elegidos por Omar: Producción (integración audiovisual, recursos técnicos, medios y hospitalidad), Operaciones (logística, proveedores, costes y contingencias), Negocio (clientes, negociación, marketing y formación en comercio exterior) y Tecnología (automatización, sistemas, desarrollo asistido por IA y soporte accesible). El comercio exterior se presenta como formación, sin atribuir operaciones realizadas. Las herramientas confirmadas se conservan dentro de desplegables.

El retrato usa sus proporciones originales9:16, altura automática y `object-fit:contain`: se ve completo, sin cortar la cabeza ni deformarlo. En escritorio se sitúa junto a la presentación; en móvil aparece centrado sobre ella. Se conserva el archivo original y el cierre accesible de la ficha.

## Candidata final: compatibilidad y auditoría

La revisión completa está en [docs/AUDITORIA-FINAL.md](docs/AUDITORIA-FINAL.md), con resultados en `docs/auditoria/` y una pasada manual breve en [docs/REVISION-DISPOSITIVOS.md](docs/REVISION-DISPOSITIVOS.md). La preferencia explícita de Omar es conservar `noindex,nofollow`. No se publica al ejecutar el build.

`effects.js` sustituye el antiguo bloque de efectos inline: la luz se detiene al asentarse, suspende trabajo en segundo plano y conserva un respaldo sin IntersectionObserver. Por la preferencia más reciente de Omar, la franja de idiomas conserva el giro continuo y no tiene botón de pausa. Al pasar el puntero baja al 6 % de velocidad, conservando la posición mediante Web Animations; vuelve a la velocidad original al salir. Se suspende fuera de pantalla y en segundo plano. Con movimiento reducido, sin JavaScript o sin la API necesaria se muestran los tres idiomas estáticos y completos.

`compatibility.css` debe cargarse al final: aplica zonas seguras, altura visible/vh para la ficha, contacto de 44 px, respaldo de filtros y menor coste de superficies en móvil. `profile.js` bloquea/restaura el desplazamiento de fondo y adapta el alto de la ficha al viewport visible. La foto original se carga al abrir la ficha; se precargan Jost y Cormorant italic sin duplicación. El HTML autónomo integra los nuevos recursos y elimina las precargas de archivos externos.

Comprobadores nuevos: `checks/browser_matrix.py`, `checks/accessibility_smoke.py`, `checks/effects_smoke.py` y `checks/performance_probe.py`. Cubren tamaños representativos y comportamientos; la emulación no acredita dispositivos físicos ni Safari/Instagram. Los motores WebKit/Firefox no estuvieron disponibles por bloqueo 403 de su descarga. La web no incorpora las herramientas de desarrollo ni bibliotecas de auditoría.

Laboratorio local Lighthouse 13.6: rendimiento 96 en móvil / 99 en escritorio, buenas prácticas 100 en ambos; carga inicial 282.470 bytes sin la foto ni los PDF. No son métricas de visitantes ni del alojamiento Vercel. Consultar el informe para condiciones, límites y resultados completos.

## Ajustes de interacción del 30 de octubre de 2026

Las áreas tienen una pista traducida, cheurones y bordes algo más visibles; en móvil se muestran las cuatro opciones. El nombre accesible de «Auto · Italia» incluye el texto visible. El detalle de implementación, las comprobaciones actuales y el límite de accesibilidad del giro continuo sin control están en [docs/UX-AREAS-IDIOMAS.md](docs/UX-AREAS-IDIOMAS.md).
