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
