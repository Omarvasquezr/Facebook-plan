# Áreas e idiomas: ajuste de interacción

30 de octubre de 2026. Continuación desde `48521ec838216ac6a6f753a5f6fc59d1ca8a945d`, sin recuperar el entorno anterior. Se reconstruyen los ajustes no confirmados, sin cambiar la identidad del portfolio.

## Comportamiento final elegido por Omar

- Las áreas muestran «Elige un área para ver los detalles», traducido a italiano e inglés, un chevrón que gira al abrir y un borde ligeramente más visible en ambos temas. En móvil las cuatro opciones se ven en una cuadrícula 2×2, sin desplazamiento horizontal para descubrirlas. Se conservan los botones nativos, `aria-expanded`, `aria-controls`, teclado y selección exclusiva.
- El botón de pausa de idiomas se elimina por petición expresa posterior de Omar. La franja conserva su giro original de 22 segundos; al pasar el puntero por la franja, la velocidad baja al 6 %. Al salir vuelve a la velocidad original. `updatePlaybackRate()` conserva la posición, sin modificar la duración CSS ni reiniciar el ciclo. No se añade un bucle JavaScript de animación.
- Fuera de pantalla o con la pestaña oculta el giro se suspende. Con movimiento reducido, sin JavaScript o sin Web Animations se muestran los tres idiomas estáticos y completos. La copia del bucle es decorativa, `aria-hidden` e `inert`, y se oculta con movimiento reducido.
- La etiqueta accesible de Auto incluye «Auto · Italia» / «Auto · Italy», el texto visible del control.

## Comprobaciones de esta revisión

Chromium **156.0.8078.47 sobre Linux**, mediante Playwright. Los tamaños y el tacto son emulados; no se atribuyen pruebas físicas a Safari, Instagram, iPhone o Android.

- Preferencias: 18 combinaciones de idioma/tema/ancho y 12 selecciones de idioma, persistencia, teclado y almacenamiento bloqueado.
- Áreas/ficha: 24 combinaciones, apertura exclusiva, herramientas nativas, foto completa, foco y respaldo sin JavaScript. Comprobación añadida de las dos filas de botones a 320/390 px y de que el texto no se solape con el chevrón. Se afina el espacio del chevrón móvil para que «Operaciones» quepa a 320 px.
- Efectos: cuatro combinaciones de movimiento/IntersectionObserver, más los respaldos sin Web Animations y sin JavaScript. Se mide el avance real al 6 %, su continuidad al entrar/salir del hover y la ausencia de solicitudes RAF continuas en reposo.
- Axe-core 4.10.3: 10 estados sin infracciones detectadas por las reglas ejecutadas; además seis tamaños de teclado/ficha y 12 estados de reflujo estático de idiomas.
- Los mismos seis modos de efectos pasan también en el HTML autónomo abierto por `file://`.
- Build `python3 build.py --keep-pdfs`; los seis PDF conservados y las dos copias de la foto son idénticos byte por byte a la base. Se conserva `noindex,nofollow` y únicamente `dist/web` es raíz pública.

Evidencia actual: `docs/auditoria/disclosure-motion-accessibility.json` y `docs/auditoria/disclosure-motion-regressions.json`.

## Alcance de accesibilidad

El hover lento ayuda a seguir el texto, pero no es un mecanismo de pausa. La preferencia de movimiento reducido tampoco sustituye un control explícito para cualquier visitante. La elección de giro continuo sin botón no acredita el criterio WCAG 2.2.2; los resultados de axe no cubren por sí solos ese requisito ni el contraste completo sobre degradados y transparencias. No se afirma conformidad WCAG total.

Referencias consultadas: [W3C, desplegables](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/), [W3C, pausa y movimiento](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html), [MDN, cambio de velocidad sin salto de posición](https://developer.mozilla.org/en-US/docs/Web/API/Animation/updatePlaybackRate).
