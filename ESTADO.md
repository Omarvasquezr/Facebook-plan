# Estado

## Revisión actual: áreas e idiomas, 30 de octubre de 2026

- Base recuperada de GitHub: `48521ec838216ac6a6f753a5f6fc59d1ca8a945d`; el checkout anterior no existe en este entorno. Se reconstruyen los ajustes pendientes.
- Áreas: pista traducida, chevrón desplegable, borde algo más visible y cuadrícula móvil 2×2. Ajustado el espacio para que las etiquetas españolas no se solapen con los cheurones a 320 px.
- Decisión final de Omar: conservar el giro de idiomas, quitar el botón y reducir la velocidad al 6 % con hover. Se conserva la posición al cambiar de velocidad; sin JS/API o con movimiento reducido se leen los tres idiomas estáticos.
- Auto · Italia incluye su texto visible en la etiqueta accesible.
- Pasan 18 combinaciones/12 selecciones de preferencias, 24 estados de áreas/ficha, cuatro modos de efectos más dos respaldos, 10 estados axe, seis tamaños de teclado y 12 estados de reflujo estático. Motor real de esta revisión: Chromium 156.0.8078.47, sin pruebas nativas de Safari/Instagram/dispositivos físicos.
- Build con `--keep-pdfs`, PDF y fotografía idénticos a la base y `noindex,nofollow` conservado. Detalle y límite WCAG del giro continuo sin control en `docs/UX-AREAS-IDIOMAS.md`.
- Publicación autorizada en `main`; Vercel sirve únicamente `dist/web`. El envío a GitHub y la coincidencia de la versión pública se comprueban por separado del build. La URL pública vuelve a responder HTTP 200 desde este entorno.

## Corrección del selector de idiomas

- Omar confirma que la versión publicada funciona y solicita corregir la selección de idiomas en otros dispositivos.
- Reproducido un cierre prematuro del menú: al perder el foco con destino nulo antes del clic en otra opción, el panel desaparecía y la selección no se registraba.
- El cierre por teclado sigue el nuevo foco fuera del selector, conservando selección por clic/tacto, Escape y clic exterior. Las traducciones locales, la persistencia y los PDF italianos se conservan.
- Pasan 18 combinaciones de idioma/tema/ancho y 12 selecciones con ratón, toque o pérdida de foco previa al clic, incluidos los 83 textos y todos los controles, textos alternativos y metadatos. La misma secuencia falla con el script anterior y funciona con la corrección. Resultado en `docs/auditoria/language-picker-fix-results.json`.
- Entregables regenerados con `--keep-pdfs`; el HTML autónomo también cambia entre los tres idiomas por toque. PDF y foto original intactos. Pruebas en Chromium con entorno móvil y secuencia de pérdida de foco emulados; no se atribuyen pruebas a Safari o Instagram nativos. La comprobación remota en Vercel sigue bloqueada por el proxy del entorno.

## Publicación autorizada

- Omar revisó la candidata final y autorizó publicarla.
- `vercel.json` fija la raíz pública en la carpeta ya revisada `dist/web`; no se ejecutan instalaciones ni generación de PDF en Vercel.
- Se prepara el envío de la versión aprobada a `main` del repositorio conectado. La aprobación del usuario no equivale a una confirmación de despliegue: el estado remoto se comprobará por separado.

## Implementado

- Rama `feat/theme-languages`, conservando la corrección previa del recorte derecho de OMAR.
- Botón con planeta dibujado en SVG y selector italiano/español/inglés. Traducciones locales del contenido, controles, metadatos y etiquetas accesibles; idiomas nativos en el selector, sin banderas.
- Tema nocturno azul profundo, baby blue y naranja; interruptor animado sol/luna/estrellas al pie y acceso sincronizado en la barra.
- Preferencias persistentes, seguimiento inicial del sistema, actualización de `lang`, sincronización entre pestañas y funcionamiento sin almacenamiento.
- Teclado, cierre del selector, anuncios accesibles y movimiento reducido.
- Ajustes de contraste en botones, tarjetas naranjas, foco y estados hover. La formación conserva su título oficial en español y se describe como título venezolano, sin atribuir equivalencia italiana.
- Generador actualizado para incluir los recursos nuevos y producir un HTML autónomo. Opción `--keep-pdfs` para conservar los PDF.
- Licencias OFL 1.1 de las dos familias incluidas con las fuentes.

## Validación

- 18 combinaciones de 3 idiomas × 2 temas × 3 anchos (320, 390, 1440 px): pasan traducciones, atributos y ausencia de desbordamiento horizontal del documento.
- Pasan apertura/selección/cierre por teclado, recuperación de foco, persistencia tras recarga, cambio de preferencia del sistema, elección manual y almacenamiento bloqueado.
- Pasan sincronización entre pestañas y vista HTML autónoma sin peticiones de recursos adicionales.
- Sin errores JavaScript observados; fuentes y archivos descargables disponibles.
- Auditoría axe-core 4.10.3: sin infracciones detectadas en los seis estados idioma/tema de escritorio para las reglas WCAG A/AA ejecutadas. El contraste sobre fondos con degradados y transparencias queda parcialmente sin resolver por axe; no se afirma conformidad total. Se revisaron capturas de móvil y escritorio, menú y pie, en ambos temas.
- PDF raíz y copias de entrega idénticos byte por byte a los originales. `dist/web` contiene solo HTML, CSS, JavaScript, fuentes/licencias y los dos PDF públicos.
- Capturas y resultados en `/workspace/review/`. Ninguna publicación en Vercel ni push.

## Límites y próximos pasos

- La página de referencia y la comparación con producción siguen bloqueadas por la política de red observada (403 del proxy). El interruptor es una implementación propia inspirada en la interacción solicitada, no una copia inspeccionada de Sean Halpin.
- PDF existentes únicamente en italiano; no se alteraron para esta solicitud.
- Las ampliaciones anteriores de créditos independientes y CV editorial trilingüe no forman parte de esta etapa y siguen pendientes; también falta fotografía de perfil y confirmar las discrepancias de fechas señaladas en el diagnóstico previo.
- No se emprendió una optimización general del rendimiento ni se atribuyen mejoras numéricas a estos cambios.

## Etapa: entrada y vista al compartir

- Rama actual `feat/intro-social-card`.
- Sustituida la cortina original por una intro con lámpara articulada, haz que busca y firma OV. Implementación original SVG/CSS; no es un personaje de Pixar ni un porcentaje de carga simulado.
- Duración visual aproximada 1,9 s, una vez por sesión; parámetro de revisión `?intro=1`. Omisión por movimiento reducido, cierre por interacción y salidas independientes CSS/JS.
- Favicon OV azul/naranja en SVG con trazados, ICO multirresolución, PNG 32 px y Apple Touch Icon 180 px.
- Tarjeta social propia 1200×630 PNG, diseño fuente HTML conservado. Open Graph y Twitter Card completos en el HTML inicial, URL de imagen absoluta HTTPS y canonical del sitio existente. No se cambiaron robots ni documentos PDF.
- El generador copia explícitamente iconos/intro/imagen a `dist/web`, mantiene las fuentes y sus licencias e integra iconos, CSS y JS en el HTML autónomo.
- Pasan pruebas locales de intro a 320/1440 px, una vez por sesión, repetición, Escape, sin JavaScript, movimiento reducido y fallos aislados de CSS/JS. Pasan validación del HTML crudo de metadatos, acceso HTTP/MIME y tamaños de recursos, PNG bajo 1 MB y tamaños ICO 16/32/48.
- Regresión: vuelven a pasar las 18 combinaciones de idiomas/temas/anchos y los controles de persistencia, sistema, teclado y almacenamiento bloqueado. HTML autónomo, sincronización entre pestañas, estados hover, PDF intactos y carpeta pública verificados después de añadir los recursos.
- Revisión visual: capturas `/workspace/review/intro-mobile.png`, `/workspace/review/intro-desktop.png`, tarjeta y favicon. Sin documentos privados ni herramientas de desarrollo en `dist/web`.
- Pendiente externo: publicar los cambios en Vercel para validar la vista real al compartir. El acceso al sitio publicado desde este entorno sigue devolviendo 403 del proxy. No se ha publicado, hecho push ni enviado enlaces por mensajería. La tarjeta estática del enlace raíz usa italiano; las preferencias guardadas del visitante no llegan a los robots de mensajería.

## Revisión de identidad, luz y cristal

- Base actual recuperada de GitHub: `367e456e4d629ece3298a714e3cd937f39a4e44a`; rama local `review/hero-light-glass`.
- Preferencia confirmada por Omar: público prioritario de clientes de marketing, tecnología y servicios creativos.
- Ajuste localizado en `preferences.css`: halo/degradado nocturno de OMAR, cristal real del lema en ambos temas y espacio para leer el apellido completo, conservando sus posiciones tipográficas.
- Respaldo sólido sin filtro/transparencia y tratamiento del título en alto contraste.
- 48 combinaciones de ancho/tema/idioma verifican separación del apellido, título y posición del apellido conservados, sin desbordamiento. Regresión del comprobador existente de preferencias y revisión de capturas móvil/escritorio.
- `docs/REVISION-VISUAL.md` contiene las fuentes oficiales leídas mediante repositorios y las limitaciones: los sitios de diseñadores y Vercel siguen inaccesibles desde el proxy. No se inventó una investigación de tendencias de 2026.
- Foto: se recomienda primer plano izquierdo en una tarjeta secundaria; no se integró al no estar el original en los archivos recuperados. UGC pendiente de revisar piezas y permisos.
- No se reestructuraron las áreas, ni se cambiaron loader/favicon o contenido en esta etapa. Sin push ni publicación.

## Cielo personal y recuperación del solapamiento

- Rama `review/birth-sky-glass`, conservando el trabajo previo.
- Catálogo real XHIP/d3-celestial, versión fijada y BSD-3-Clause conservada; 280 estrellas sobre el horizonte y 13 vértices de Virgo. Cálculo de horizonte y Sol mediante Astropy offline.
- Referencia geográfica aproximada, no edificio verificado. Fecha/hora y configuración detallada fuera del proyecto; sin campos personales en el SVG público. Es un diagrama de posiciones sin atmósfera, no visibilidad diurna real.
- Halo ambiental situado según el mismo punto solar proyectado que el cielo. Estrellas estáticas; Virgo aparece por proximidad y se fija con botón accesible al pie, en los tres idiomas.
- Lema recupera parte del solapamiento de escritorio; mayor translucidez y blur6. Se mantiene la separación móvil y el respaldo sólido accesible.
- Pasan las pruebas de 8 combinaciones de ancho/tema, 13 vértices encuadrados, posición Sol/halo, tacto/teclado/proximidad, movimiento reducido, sin JS y sin errores JavaScript observados. Regresión de 18 combinaciones de preferencias también pasa.
- Exportación y privacidad revisadas; documentación en `docs/CIELO.md`. Sin push ni cambios en Vercel.

## Contraste de cursos y detalle oculto

- Rama `review/course-contrast-easter-egg`.
- Corrección limitada a dos colores en los cursos: Claude 101 usa `var(--paper)` sobre `var(--ink)`; Digital Marketing usa `#141821` sobre baby blue. Los fondos y la disposición permanecen.
- Comprobación de estilos computados: contraste mínimo superior a 11:1 para ambos cursos en los dos temas. Capturas de Formazione en móvil y escritorio.
- Retirados botón Virgo y nota del pie. El nombre pequeño del encabezado conserva su apariencia y actúa como entrada discreta con área táctil ampliada, foco visible y etiqueta accesible traducida. Proximidad, tacto, Enter/Espacio y Escape conservan la interacción. Sin JS el nombre permanece visible e inactivo.
- Actualizados el comprobador de cielo y las instrucciones. El resto de la composición no cambia. Sin push ni publicación.

## Áreas de trabajo y ficha personal

- Rama `review/areas-personal-profile`, conservando los cambios anteriores.
- Sustituida la franja de programas por cuatro áreas desplegables con capacidades y herramientas de apoyo. Un solo panel abierto; controles estables con desplazamiento manual móvil, foco visible y acceso con teclado. Liderazgo, negociación y hospitalidad aparecen en su contexto de trabajo.
- Ficha personal única con residencia, intereses y valores, accesible desde OMAR, «Chi sono» y el pie. Diálogo nativo con cierre, Escape, fondo exterior, foco restaurado y transición breve que respeta movimiento reducido.
- La composición de OMAR y del apellido conserva sus medidas. El apellido decorativo deja pasar los clics al nombre que tiene debajo. El nombre pequeño mantiene Virgo.
- Todos los textos y etiquetas nuevos traducidos en italiano, español e inglés. Sin JavaScript se leen las cuatro áreas y la presentación personal como secciones de la página.
- Build web y HTML autónomo incluyen los recursos nuevos; PDF originales conservados. El retrato queda pendiente de que Omar adjunte la imagen como archivo recuperable; no se publica una foto ficticia ni una imagen rota.
- Pasan 24 combinaciones de ancho/idioma/tema para las áreas y la ficha: selección exclusiva, traducciones, tres accesos al diálogo, teclado/tacto, foco, modalidad y lectura sin JavaScript. Regresión de preferencias (18 combinaciones) y cielo (8 estados) también pasa.
- HTML autónomo verificado sin solicitudes adicionales; los dos PDF siguen idénticos. Verificados además enlace directo a la ficha, cierre desde el fondo, colores forzados y movimiento normal.
- Sin push, cambios en Vercel ni servicios externos nuevos.

## Nombre personal y ampliación de herramientas

- Por petición expresa de Omar, el nombre pequeño reúne la entrada a la ficha personal con la revelación de Virgo al pasar/enfocar. Incluye un cursor pequeño y una flecha subrayada. Se eliminan «Chi sono» separado y el enlace de OMAR grande; se conserva el acceso del pie. No hay dos acciones alternantes en un mismo clic.
- Añadidos los niveles avanzados declarados para Windows, Fedora Linux y macOS; Canva, Adobe Creative Cloud para fotografía y AutoCAD para dibujo técnico. Producción incluye fotografía, cámaras profesionales y edición profesional de audio.
- Tras aclaración expresa, añadidos Search Console, Tag Manager, Google Ads Manager/MCC y Google Flow. Tecnología incorpora configuración/diagnóstico/reparación/modificaciones de iOS/Android, ayuda con privacidad y accesibilidad para mayores y desarrollo de aplicaciones con asistencia de IA.
- El original del retrato es visible en el chat pero no recuperable como binario en este entorno. El build detecta un archivo assets/omar-vasquez-portrait.{webp,jpg,jpeg,png} y lo integra en web y HTML autónomo; sin archivo no hay petición ni imagen rota. Hace falta recibirlo dentro de un ZIP o recuperarlo del repositorio.
- Las sugerencias adicionales de programas se mantienen fuera del perfil publicado hasta confirmación. Sin push ni cambios en Vercel.
- Validación de esta etapa: pasan 24 estados de áreas/ficha, 8 de cielo con el acceso reunido, traducciones de las últimas ampliaciones a 320 px y la regresión de preferencias. Se revisaron las capturas del nombre y de los paneles ampliados en móvil/escritorio.

## Retrato, puntos diurnos y horario italiano

- Recuperado IMG_4095_Original.JPG del ZIP aportado por Omar y copiado sin retoques a assets/omar-vasquez-portrait.jpg. Visible en la ficha desde el nombre pequeño y el pie, texto alternativo traducido, incrustado en la versión autónoma. El cierre permanece visible fuera del contenido desplazable y cada apertura vuelve al inicio.
- Herramientas actualizadas con las aplicaciones confirmadas de fotografía/diseño (incluido Photopea) y las restantes sugeridas salvo las descartadas. No se añadieron REAPER, Ahrefs, Tailscale ni Revit. Las herramientas se agrupan para no convertir el panel en una lista indiscriminada.
- Corrección explícita del alcance: el hover blanco corresponde a los puntos de estrellas del modo día. Se mantienen las 280 posiciones/radios reales, el aspecto nocturno y el color de Virgo; máscara radial local sin bucle de animación añadido ni captura de clics.
- Nuevo theme-clock.js: modo automático según Europe/Rome, noche18:00–06:00 con horario estacional; elección manual persistente y botón «Auto · Italia» para volver al reloj. Comprobación periódica y al volver a la pestaña. Sin servicios externos ni geolocalización del visitante.
- Pasan39casos de horario/zonas/estaciones y la prueba integrada de transición18:00/06:00, elección manual y retornoAuto;18combinaciones de preferencias,24de ficha/áreas con el retrato cargado/alt traducido/cierre al desplazarse y8estados de cielo.
- Sin push ni publicación en Vercel.

## Pulido final solicitado por Omar

- Contraste diurno de los puntos aumentado: se reconocen sin hover y se realzan en blanco al pasar el cursor. Radios y posiciones originales, aspecto nocturno y trazado de Virgo conservados. Comparación visual de móvil/escritorio realizada.
- Retrato completo en proporción9:16, sin recorte ni deformación. Presentación en dos columnas de escritorio y una columna móvil; archivo original intacto.
- Nueva organización editorial: Producción, Operaciones, Negocio y Tecnología. Cada área contiene una frase breve y cuatro capacidades distintas; hospitalidad se sitúa en Producción y comercio exterior se identifica como formación.
- Liderazgo operativo, coordinación multidisciplinar y decisiones bajo presión se expresan una sola vez en un párrafo compartido. Todos los programas confirmados se conservan en desplegables nativos inicialmente cerrados.
- Pasan24estados de áreas/ficha (incluidos proporción natural del retrato y herramientas por teclado),18combinaciones de preferencias y8estados de cielo. Traducciones, foco, móvil, foto, ausencia de desbordamiento y versión sin JS verificados.
- Sin push ni publicación en Vercel.

## Auditoría para candidata de despliegue

- Revisión de compatibilidad, accesibilidad, rendimiento y lenguaje solicitada por Omar. No se cambió la arquitectura estática ni la identidad visual.
- Nuevo effects.js reemplaza el bloque inline: movimiento finito del foco, lecturas por lotes, cero solicitudes RAF en reposo comprobado, suspensión en segundo plano y respaldo sin IntersectionObserver. Pausa de idiomas accesible.
- Nuevo compatibility.css: zonas seguras, altura visible/vh de la ficha, bloqueo/restauración del fondo, contacto de 44 px y reducción de filtros móviles. Intro sin dependencia de señales AbortController y con respaldo MediaQueryList antiguo.
- Retrato original diferido hasta abrir la ficha; precarga de dos fuentes críticas. Exportación autónoma integra todos los recursos y no solicita archivos adicionales.
- Diez entradas lingüísticas corregidas y seis textos italianos iniciales sincronizados. Créditos actualizados a herramientas de IA; no se alteraron logros, fechas o niveles.
- Por respuesta expresa de Omar se conserva noindex,nofollow.
- Pasan 84 estados en 14 perfiles Chromium 154, 10 estados axe sin infracciones detectadas, 6 tamaños de reflujo/teclado, regresiones18/24/8 y horario de 39 casos, entrada/metadatos y efectos.
- Laboratorio Lighthouse 13.6: rendimiento 96 en móvil / 99 en escritorio, buenas prácticas 100/100; LCP 2,2 s / 0,6 s, TBT 50 ms / 10 ms, CLS 0 / 0,011. Recursos iniciales 282.470 bytes; foto de 925.754 bytes diferida; no peticiones externas/PDF/tarjeta social automáticas. Medición local, no producción ni dispositivos reales.
- WebKit/Firefox no se instalaron por rechazo403 del proxy; Safari/Brave/Instagram nativos no disponibles. La pasada real de Safari/Instagram/iPhone/Android está documentada antes de cerrar la entrega pública.
- Informe completo docs/AUDITORIA-FINAL.md y evidencia docs/auditoria. Sin push ni publicación en Vercel.
