# Instrucciones para Claude Code en este repo

Sitio de Germán Aquino (germanaquino.com.ar). Trabajás para Vaneh (COSMART). Hablás en español rioplatense.

## Reglas duras
- **La persona NUNCA sale de la página con un clic** (regla de Vaneh, 25/10/2026, para todas sus páginas). Los videos se reproducen embebidos en un modal dentro de la misma página; ningún botón de video, link de red social ni "Ver en…" puede llevar a Instagram/TikTok u otro sitio externo. Solo se admite abrir otra pestaña dentro del universo COSMART.
- Instagram NO reproduce sus reels embebidos (el embed siempre manda a instagram.com). Los reels se alojan como MP4 propio en `videos/` (mp4 + jpg de portada) y se reproducen con `<video>` en el modal (`data-mp4`). TikTok sí reproduce embebido por iframe sandbox.
- Mobile y tablet (horizontal y vertical) se revisan siempre. Las listas en 2 columnas muestran cantidades pares.
- Todo botón nuevo se prueba. SEO: ver `llms.txt`, `sitemap.xml` y `robots.txt`; `/shows` va sin barra final.
- El `CNAME` lo borra la sesión de migración a Cloudflare, no se toca.
