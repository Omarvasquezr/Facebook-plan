# Reglas del proyecto

- Sitio estático: reutilizar HTML, CSS y JavaScript existentes.
- No publicar, usar `--deploy`, hacer push ni enviar candidaturas sin autorización explícita.
- Mantener documentos personales fuera de Git y de `dist/web`.
- Conservar los PDF existentes hasta validar los nuevos.
- Comprobar móvil y escritorio, fuentes cargadas, teclado y movimiento reducido para cambios de interfaz.
- Para la corrección de OMAR, verificar que la R cabe en su caja sin cambiar la posición o altura del título ni la posición del apellido.
- Actualizar README y ESTADO cuando cambien los pasos de trabajo.

## Preferencias e idiomas

- Mantener `preferences.js` y los textos del HTML sincronizados. Traducir también etiquetas accesibles y metadatos.
- No traducir nombres propios o niveles de idioma inventando equivalencias. Identificar siempre el idioma real de los PDF.
- Revisar tema claro y oscuro, estados hover/foco, los tres idiomas, 320 px y escritorio, almacenamiento bloqueado y movimiento reducido.
- Preparar con `python3 build.py --keep-pdfs` para conservar los documentos originales. Servir únicamente `dist/web` como raíz pública.
- Ejecutar `checks/preferences_smoke.py` contra el servidor local según README. Usar el checkout existente del entorno, sin crear worktrees salvo petición expresa.

## Identidad y vista al compartir

- Mantener los metadatos Open Graph/Twitter en el HTML inicial y sus imágenes en URLs HTTPS públicas absolutas. No depender del JavaScript de traducción para robots.
- Copiar los iconos y `assets/` en el build; no publicar `tools/`, `checks/` o documentos privados.
- Mantener la intro decorativa breve y con salida aun si falla CSS/JS. Respetar movimiento reducido y no crear un porcentaje ficticio de carga.
- Conservar el diseño editable de la tarjeta en `tools/social-card.html` y el SVG del favicon; regenerar con la herramienta documentada cuando cambien.
- Ejecutar `checks/branding_smoke.py` para cambios de entrada/metadatos/iconos. No afirmar que WhatsApp muestra la tarjeta hasta comprobarlo con la versión publicada.

## Cielo y datos personales

- Mantener fecha/hora/lugar del observador y el informe astronómico fuera de Git y de los entregables públicos. No inferir el hospital exacto desde una referencia de barrio.
- El cielo usa posiciones reales proyectadas, sin atmósfera: no llamarlo observación diurna ni mapa exacto con una ubicación aproximada.
- Conservar procedencia y BSD-3-Clause del catálogo/trazado. No sustituirlo por puntos aleatorios presentados como cielo natal.
- Virgo se revela por proximidad, hover o foco en el nombre pequeño. Por preferencia expresa de Omar, pulsar ese nombre abre la ficha personal; no debe alternar otro estado con el mismo clic. La capa decorativa no puede capturar clics ni ocultar contenido.
- Las estrellas son estáticas; respetar movimiento reducido. Solo las herramientas opcionales de generación necesitan Astropy, nunca el navegador o el build estático habitual.
- Validar `checks/sky_smoke.py` y los idiomas/temas al tocar fondo o interacción. El solapamiento parcial del lema es una preferencia expresa de Omar.

## Áreas y ficha personal

- Conservar una sola área abierta a la vez y una sola ficha personal compartida por el nombre pequeño y el enlace del pie. Mantener la firma grande y el detalle de Virgo del nombre pequeño.
- Usar únicamente capacidades y datos respaldados por lo que Omar ha contado; no inferir certificaciones ni dominio de herramientas relacionadas.
- Las áreas y la ficha deben seguir siendo legibles sin JavaScript. El diálogo debe devolver el foco al cerrar; las opciones de áreas no deben moverse mientras se eligen.
- Incluir `expertise.css/js` y `profile.css/js` en la web y en el HTML autónomo. Validar `checks/expertise_profile_smoke.py` para estos cambios.
- El retrato exacto del ZIP está en assets/omar-vasquez-portrait.jpg. No generar un sustituto ni retocarlo. Conservar sus proporciones naturales y la cabeza completa; no volver al recorte horizontal. El build admite también .webp/.jpeg/.png y lo incrusta en el HTML autónomo. Mantener el cierre del diálogo visible aunque se desplace la ficha.

## Horario y puntos diurnos

- La elección automática usa Europe/Rome: noche18:00–06:00, respetando horario de verano/invierno. Una elección manual tiene prioridad hasta pulsar «Auto · Italia». Mantener el helper temprano y el controlador posterior sincronizados, sin consultar localización del visitante.
- Incluir theme-clock.js tanto en dist/web como en el HTML autónomo. Validar checks/theme_clock_smoke.py y preferencias al modificar el horario.
- Los puntos del catálogo deben ser visibles en modo día aun sin hover; el hover los realza en blanco. Mantener sus posiciones/radios, el aspecto nocturno y el trazado de Virgo; no convertir los puntos en una distribución aleatoria.

- Las cuatro áreas editoriales son Producción, Operaciones, Negocio y Tecnología. Evitar repetir capacidades entre resúmenes y no convertir la formación en comercio exterior en una afirmación de operaciones ejecutadas. Mantener las herramientas dentro de desplegables nativos y el liderazgo en una línea compartida.

## Compatibilidad final y medición

- Conservar `compatibility.css` al final y `effects.js` en web/exportación autónoma. No reintroducir el bucle de luz continuo; respetar reposo, pestaña oculta y movimiento reducido.
- Conservar pausa/reanudación accesible de la franja de idiomas, contacto de 44 px y bloqueo/restauración del fondo al abrir/cerrar la ficha. La foto se carga de forma diferida sin modificar sus bytes o proporciones.
- La decisión expresa de Omar es `noindex,nofollow`; no habilitar indexación en una optimización.
- Para auditorías usar los comprobadores y documentar el motor real, versión y tamaños. Una UA o tamaño de iPhone emulado no equivale a Safari o Instagram real. No afirmar certificación WCAG, FPS de dispositivos ni Core Web Vitals de visitantes a partir de pruebas locales.
- Los informes de desarrollo se guardan en docs/auditoria, fuera de dist/web. Mantener los límites y la pasada nativa pendiente descritos en docs/AUDITORIA-FINAL.md.
