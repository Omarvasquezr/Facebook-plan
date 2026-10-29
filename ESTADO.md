# Estado

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
