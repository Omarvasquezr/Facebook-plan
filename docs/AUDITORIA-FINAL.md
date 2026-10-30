# Auditoría final del portfolio de Omar Vásquez

29 de octubre de 2026. Candidata local preparada para revisión y despliegue. No se hizo push ni se publicó en Vercel.

> Actualización del 30 de octubre: este informe conserva la auditoría de la candidata anterior. La decisión posterior de quitar el botón de pausa, mantener el giro y ralentizarlo con hover, junto con la revisión actual de áreas, se documenta en [UX-AREAS-IDIOMAS.md](UX-AREAS-IDIOMAS.md). Las comprobaciones y el comportamiento de pausa descritos abajo son históricos.

## Resultado

La versión conserva la identidad, el cristal, el cielo personal y la fotografía original. Pasan las comprobaciones funcionales y de presentación en los tamaños representativos revisados. La validación automatizada se hizo en **Chromium 154.0.8037.57 sobre Linux**, con tamaños, tacto y densidades de píxel emulados. No equivale a ejecutar Safari, Brave o Instagram en dispositivos físicos.

## Cambios aplicados

- La luz conserva el seguimiento del puntero, pero deja de solicitar frames al asentarse y al ocultar la pestaña. Las lecturas de geometría se agrupan y se actualizan solo las tarjetas cercanas. El respaldo sin IntersectionObserver mantiene visible el contenido.
- Los idiomas tienen pausa/reanudación por teclado y tacto. También se pausa la franja fuera de pantalla, al enfocarla y con movimiento reducido. En este modo los tres idiomas se muestran completos, con ajuste de línea.
- Las superficies móviles evitan filtros extensos; el cristal del encabezado se conserva. Se respeta el movimiento reducido y las zonas seguras de pantalla.
- La ficha se ajusta al alto visible del navegador, mantiene el cierre accesible y bloquea/restaura el desplazamiento de fondo. Hay respaldo100vh para vistas sin unidades dinámicas y una sección normal cuando no existe diálogo nativo.
- Teléfono y correo tienen al menos44 px de altura táctil. Los PDF usan enlaces normales, sin ventanas emergentes ni descarga mediante JavaScript.
- Las dos fuentes críticas se precargan sin solicitudes duplicadas. La fotografía conserva exactamente sus bytes y proporciones; se descarga al abrir la ficha. Los PDF y la tarjeta social no se descargan automáticamente.
- Se corrigieron expresiones y equivalencias de italiano, español e inglés, sin cambiar fechas, niveles ni logros. Se mantiene Universidad Santa María como nombre propio. Los créditos reflejan el uso de herramientas de IA sin atribuir toda la versión actual a una única herramienta.
- Por elección expresa de Omar se conserva `noindex,nofollow`: no se ha habilitado su aparición en buscadores.

## Cobertura comprobada

| Familia | Tamaños CSS representativos | Resultado |
| --- | --- | --- |
| Móvil compacto |320×740,375×667 | Pasa |
| Tamaño iPhoneXS |375×812 | Pasa como emulación de tamaño/tacto |
| iPhone reciente |390×844,393×852,430×932 | Pasa como emulación de tamaño/tacto |
| Android habitual |360×800,412×915 | Pasa como emulación de tamaño/tacto |
| Tableta |768×1024,820×1180 | Pasa |
| Portátil |1366×768,1440×900 | Pasa |
| Escritorio grande |1920×1080,2560×1440 | Pasa |

La matriz suma **14 perfiles y84 estados de idioma/tema**; comprueba nombre y barra sin recorte, ausencia de desbordamiento del documento, controles, orientación, retrato completo, ficha, cierre/foco, áreas, herramientas y PDF. Hay pruebas adicionales sin JavaScript, sin diálogo nativo y sin IntersectionObserver.

También pasan las regresiones de preferencias (18 combinaciones), áreas/ficha (24), cielo (8), horario italiano (39 casos de estaciones/zonas y transiciones 18:00/06:00), entrada/metadatos y efectos.

## Accesibilidad

Axe-core 4.10.3 no detectó infracciones en las reglas A/AA ejecutadas en **10 estados**. Se revisaron además 6 tamaños, incluido 320×568 y horizontal 812×375, con navegación por teclado, pausa de idiomas, cierre tras desplazar la ficha, textos alternativos traducidos, contacto, documentos y respaldo sin JavaScript.

La revisión visual añadió 12 estados de idiomas/niveles completos con movimiento reducido y comprobó la foto completa al abrir la ficha en horizontal 812×375, con cierre accesible en ambos temas.

Los fondos translúcidos y los degradados producen comprobaciones de contraste incompletas en axe; no se presentan como una certificación de conformidad total. El reflujo a 320 px está probado; no se afirma una prueba nativa de zoom 200%, VoiceOver o TalkBack. Los PDF se conservaron, no se rehicieron ni auditaron sus etiquetas de accesibilidad.

## Rendimiento de laboratorio

Lighthouse 13.6.0, una ejecución móvil y una de escritorio sobre servidor HTTP local, tras finalizar los demás ensayos de navegador:

| Ensayo | Rendimiento | Buenas prácticas | LCP | TBT | CLS |
| --- | ---: | ---: | ---: | ---: | ---: |
| Móvil simulado |96 |100 |2,2s |50ms |0 |
| Escritorio simulado |99 |100 |0,6s |10ms |0,011 |

Móvil:150 ms RTT,1,6 Mbps y CPU 4× más lenta. Escritorio:40 ms RTT,10 Mbps y CPU sin ralentización. Son medidas locales simuladas, no métricas de visitantes ni pruebas reales de Instagram/Safari/Vercel.

La sonda de recursos midió **282.470bytes** de cuerpos iniciales sin compresión local. El retrato de925.754 bytes se solicita una sola vez al abrir la ficha; las fuentes precargadas también una sola vez. No se observaron peticiones externas del sitio, descargas automáticas de PDF/tarjeta social ni errores JavaScript. En el ensayo de efectos, la versión anterior solicitó 25 frames en 2 s de reposo; la nueva, cero. Este conteo no equivale a una promesa de FPS o de consumo en teléfonos reales.

Las recomendaciones de compresión/caché de Lighthouse corresponden al servidor Python del ensayo. No se comprobaron los encabezados del alojamiento de producción ni los Core Web Vitals de visitantes.

## Validación nativa pendiente

La descarga oficial de WebKit/Firefox fue bloqueada por el proxy del entorno con HTTP 403. No estaban disponibles binarios de Safari o Brave ni la aplicación de Instagram. No se sustituyeron por un cambio de user-agent para atribuirles resultados.

Antes de cerrar la revisión pública, realizar una pasada breve en Safari de un iPhone actualizado y dentro del navegador de Instagram, además de un Android representativo. La [lista de revisión](REVISION-DISPOSITIVOS.md) cubre orientación, zonas seguras, idioma/tema, ficha, contactos y PDF. La entrega al marcador, correo o visor depende también del sistema y de la aplicación anfitriona. Esta comprobación debe hacerse con la URL de la versión final publicada.

## Evidencia y reproducción

Los resultados completos están en [auditoria/](auditoria/), incluidos los informes Lighthouse [móvil](auditoria/lighthouse-mobile.report.html) y [escritorio](auditoria/lighthouse-desktop.report.html), las matrices JSON y los registros de regresión. Son documentos de desarrollo; el build no los copia a la carpeta pública.

```sh
python3 build.py --keep-pdfs
python3 -m http.server 4174 --bind 127.0.0.1 --directory dist/web
python3 checks/browser_matrix.py http://127.0.0.1:4174/ /tmp/browser-matrix.json
python3 checks/preferences_smoke.py http://127.0.0.1:4174/
python3 checks/expertise_profile_smoke.py http://127.0.0.1:4174/
python3 checks/sky_smoke.py http://127.0.0.1:4174/
python3 checks/theme_clock_smoke.py http://127.0.0.1:4174/
python3 checks/branding_smoke.py http://127.0.0.1:4174/
python3 checks/effects_smoke.py http://127.0.0.1:4174/
python3 checks/performance_probe.py http://127.0.0.1:4174/
```

El comprobador de accesibilidad admite `--axe /ruta/axe.min.js`; la herramienta de auditoría no es una dependencia de la web. El sitio sigue siendo estático, con recursos propios y sin servicios externos de traducción.
