# Revisión visual y dirección del portfolio

Nota de continuidad: la separación completa descrita en este documento fue una propuesta anterior. Omar prefirió recuperar un solapamiento moderado y mayor translucidez; el estado actual está en `CIELO.md`.

## Contexto

El público prioritario que Omar indicó es clientes de marketing, tecnología y servicios creativos. La propuesta conserva el nombre como protagonista, baby blue/naranja, tipografías y controles actuales. No presupone que una estética expresiva perjudique la contratación ni atribuye preferencias universales al mercado.

Base revisada: commit `367e456e4d629ece3298a714e3cd937f39a4e44a` de `Omarvasquezr/Facebook-plan`, recuperado de GitHub. Se comprobó esa copia local; el acceso directo al sitio de Vercel sigue bloqueado por el proxy.

## Ajuste preparado

- La tarjeta del lema se solapaba con el apellido. Se reserva espacio para los descendentes tipográficos, sin mover ni cambiar tamaño o tipografías del nombre y apellido. El objetivo es leer la firma completa, no intentar leerla a través de desenfoque.
- El nombre nocturno recibe un degradado baby blue de más matices y una sombra luminosa estática suave. Mantiene la luz existente ligada al puntero; no añade bucles de animación.
- El lema tiene superficie semitransparente, reflejo de borde y desenfoque localizado de 14 px en ambos temas. El resto de las tarjetas conserva su tratamiento.
- Hay superficies sólidas de respaldo sin `backdrop-filter`, con preferencia de transparencia reducida, y tratamiento de alto contraste para que OMAR no quede como texto transparente.

## Retrato: propuesta, aún no integrado

La foto adjunta a la conversación combina primer plano y cuerpo entero; el archivo original no forma parte del repositorio recuperado. No se inventó ni se regeneró un retrato.

Usar el primer plano izquierdo, con encuadre de rostro y hombros y tratamiento natural, en una tarjeta secundaria junto a una presentación personal breve después del encabezado. Evitar superponer texto al rostro o añadir una tercera capa entre nombre, apellido y lema. Reservar el cuerpo entero para una futura muestra de trabajo de cámara/casting si Omar quiere ofrecer ese servicio.

Para clientes, la presentación inicial necesita una pista breve de especialidad. Propuesta editorial a validar: «Marketing, producción y tecnología aplicada». No se cambió el contenido con esta revisión.

## UGC: propuesta pendiente de revisar las piezas

Puede funcionar como evidencia de comunicación, presencia ante cámara y contenido para marcas. Revisar hasta dos o tres piezas y el derecho a mostrarlas antes de decidir. Explicar la aportación concreta de Omar sin atribuir resultados no comprobados. Usar reproducción elegida por el visitante, sin autoplay ni embeds de terceros cargados de entrada. No convertir dos trabajos en una especialidad principal automáticamente.

## Fuentes oficiales consultadas

Consulta realizada en esta revisión mediante los repositorios de sus mantenedores. Esto verifica el contenido disponible, no supone que cada documento haya sido actualizado en 2026.

- Microsoft, Acrylic material: [documentación](https://learn.microsoft.com/en-us/windows/apps/design/style/acrylic) · [fuente leída](https://raw.githubusercontent.com/MicrosoftDocs/windows-dev-docs/docs/hub/apps/design/style/acrylic.md). Su fecha declarada es 15/07/2024. Recomienda cuidar legibilidad al modificar opacidad/tinte, usar transparencia con jerarquía, evitar múltiples capas y prever fondos sólidos. Es una guía Windows/XAML; aquí se trasladan principios, no comportamientos automáticos de esa plataforma.
- MDN, backdrop-filter: [documentación](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter) · [fuente leída](https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/css/reference/properties/backdrop-filter/index.md). Requiere una superficie transparente o semitransparente para apreciar lo que se filtra detrás.
- W3C, contraste mínimo: [guía](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) · [fuente leída](https://raw.githubusercontent.com/w3c/wcag/main/understanding/20/contrast-minimum.html). El texto normal requiere 4.5:1 y el grande 3:1 en el criterio aplicable. Los fondos variables exigen revisar situaciones desfavorables; no se afirma certificación global del sitio.
- W3C, Animation from Interactions: [fuente leída](https://raw.githubusercontent.com/w3c/wcag/main/understanding/21/animation-from-interactions.html). Respeto por preferencias de movimiento y posibilidad de desactivar movimiento no esencial. Es criterio AAA; no se presenta como requisito AA.
- IBM Carbon, Tabs: [fuente leída](https://raw.githubusercontent.com/carbon-design-system/carbon-website/main/src/pages/components/tabs/usage.mdx). Etiquetas breves, contenido relacionado y evitar usar pestañas para comparar información entre grupos.
- GOV.UK Design System, Tabs: [fuente leída](https://raw.githubusercontent.com/alphagov/govuk-design-system/main/src/components/tabs/index.md). Advierte que esconden contenido: mantener visible un resumen de servicios y usar el detalle opcional con criterio.
- GOV.UK, Images: [fuente leída](https://raw.githubusercontent.com/alphagov/govuk-design-system/main/src/styles/images/index.md). El contenido debe seguir funcionando sin imágenes; el texto alternativo depende de su función. No se traslada una política de decoración de servicios públicos como veto estético a un portfolio.

No se pudieron inspeccionar los portfolios actuales de Sean Halpin, Anthony Designer, Arlen McCluskey o Devon Stank: el proxy devolvió 403. No se afirman tendencias actuales ni observaciones visuales de esos sitios no consultados.

## Comprobaciones

- 48 combinaciones: 8 anchos (320, 390, 640, 641, 768, 1024, 1440 y 1920), dos temas y tres idiomas. Sin desbordamiento horizontal; la tarjeta empieza después del área de tinta del apellido; posición y caja de OMAR y posición del apellido conservadas respecto a la base.
- Nombre visible en modo de alto contraste de Chromium.
- Regresión de preferencias, teclado, idioma, persistencia y almacenamiento bloqueado con el comprobador existente.
- Revisión visual de escritorio y móvil; sin nuevos servicios, recursos remotos ni bibliotecas de producción.
- No se midió una mejora global de rendimiento ni se pretende haber certificado WCAG o probado todos los navegadores. El desenfoque y la sombra tienen coste gráfico y deben mantenerse localizados.
- Retrato y vídeos no incorporados. Sin push, publicación o cambios en Vercel.
