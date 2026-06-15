import re, sys, os, base64, shutil
sys.stdout.reconfigure(encoding='utf-8')

src_path = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/index_github.html'
out_path = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/index.html'
img_dir  = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/images'
base_dir = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/'
os.makedirs(img_dir, exist_ok=True)

with open(src_path, encoding='utf-8') as f:
    html = f.read()
print('Original size:', len(html))

# 1. Extract base64 images
b64_names = ['hero', 'foto-cuerpo']
i = 0
for m in re.finditer(r'data:image/([a-zA-Z]+);base64,([A-Za-z0-9+/=]+)', html):
    ext = m.group(1)
    fname = b64_names[i] + '.' + ext
    fpath = img_dir + '/' + fname
    with open(fpath, 'wb') as f2:
        f2.write(base64.b64decode(m.group(2)))
    html = html.replace(m.group(0), 'images/' + fname, 1)
    print('  Imagen:', fname, '->', os.path.getsize(fpath), 'bytes')
    i += 1

print('After image extraction:', len(html))

# 2. Find section positions using regex (handles special chars)
def find_sec(html, keyword):
    m = re.search(r'<!-- [^\-]*' + re.escape(keyword) + r'[^\-]* -->', html)
    if not m:
        print('WARNING: not found -', keyword)
        return -1
    return m.start()

p_hero  = find_sec(html, 'HERO')
p_exp   = find_sec(html, 'EXPERIENCIA')
p_form  = find_sec(html, 'FORMACI')
p_foto  = find_sec(html, 'FOTO 2')
p_vid   = find_sec(html, 'VIDEOS')
p_aqts  = find_sec(html, 'A QUE TE SUENA')
p_shows = find_sec(html, 'SHOWS PARA EVENTOS')
p_cont  = find_sec(html, 'CONTACTO')
p_foot  = find_sec(html, 'FOOTER')

print('Positions:')
for n,v in [('hero',p_hero),('exp',p_exp),('form',p_form),('foto',p_foto),
            ('vid',p_vid),('aqts',p_aqts),('shows',p_shows),('cont',p_cont),('foot',p_foot)]:
    print(f'  {n}: {v}')

css    = html[0:p_hero]
s_hero = html[p_hero:p_exp]
s_exp  = html[p_exp:p_form]
s_form = html[p_form:p_foto]
s_foto = html[p_foto:p_vid]
s_vid  = html[p_vid:p_aqts]
s_aqts = html[p_aqts:p_shows]
s_show = html[p_shows:p_cont]
s_cont = html[p_cont:p_foot]
s_foot = html[p_foot:]

for n,s in [('css',css),('hero',s_hero),('exp',s_exp),('form',s_form),('foto',s_foto),
            ('vid',s_vid),('aqts',s_aqts),('show',s_show),('cont',s_cont),('foot',s_foot)]:
    print(f'  {n}: {len(s)} chars')

# 3. Copy gallery images to images/
gallery_images = [
    ('ger cantando.png',                        'German Aquino cantando'),
    ('ger cantando en evento corporativo.png',   'German Aquino en evento corporativo'),
    ('ger cantando en fiesta de 15 años.png',    'German Aquino en fiesta de 15'),
    ('ger cantando en fiesta de 15 años 1 .png', 'German Aquino show fiesta'),
    ('IMG_3460 Cuadrada.jpg',                   'German Aquino'),
    ('IMG_3421 Story.jpg',                       'German Aquino'),
    ('IMG_3395.jpg',                             'German Aquino'),
    ('IMG_3232 2.jpg',                           'German Aquino'),
    ('IMG_3246 1.jpg',                           'German Aquino'),
    ('1.png',                                    'German Aquino'),
    ('1V.png',                                   'German Aquino'),
    ('3.png',                                    'German Aquino'),
]
for fname, _ in gallery_images:
    src = base_dir + fname
    dst = img_dir + '/' + fname
    if os.path.exists(src):
        shutil.copy2(src, dst)

# 4. Gallery + video CSS
gallery_css = """
  /* GALERIA */
  .galeria-sec { padding: 60px 0; }
  .galeria-sec .sec-header { margin-bottom: 28px; }
  .galeria-wrap { position: relative; overflow: hidden; }
  .galeria-track { display: flex; transition: transform 0.6s cubic-bezier(0.4,0,0.2,1); will-change: transform; }
  .galeria-slide { flex: 0 0 100%; height: 480px; overflow: hidden; position: relative; }
  .galeria-slide img { width: 100%; height: 100%; object-fit: cover; object-position: center top; filter: grayscale(10%) contrast(1.05); display: block; }
  .galeria-slide::after { content: ""; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(13,13,13,0.3) 0%, transparent 30%), linear-gradient(to top, rgba(13,13,13,0.4) 0%, transparent 30%); pointer-events: none; }
  .galeria-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(13,13,13,0.6); border: 1px solid rgba(196,168,130,0.2); color: var(--marron-suave); width: 44px; height: 44px; border-radius: 50%; font-size: 22px; cursor: pointer; z-index: 3; display: flex; align-items: center; justify-content: center; transition: background 0.2s, border-color 0.2s; }
  .galeria-btn:hover { background: rgba(122,92,63,0.4); border-color: var(--marron-suave); }
  .galeria-btn.prev { left: 12px; }
  .galeria-btn.next { right: 12px; }
  .galeria-dots { display: flex; justify-content: center; gap: 8px; margin-top: 16px; padding: 0 24px; }
  .galeria-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--marron-suave); opacity: 0.25; cursor: pointer; transition: opacity 0.3s, transform 0.3s; border: none; }
  .galeria-dot.active { opacity: 1; transform: scale(1.4); }
  @media(min-width:768px) { .galeria-slide { height: 600px; } }
  /* VIDEO EMBED */
  .video-show-wrap { display: flex; justify-content: center; padding: 0 24px 40px; }
  .video-iframe-wrap { position: relative; width: 100%; max-width: 340px; aspect-ratio: 9/16; border-radius: 4px; overflow: hidden; background: #000; }
  .video-iframe-wrap iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: none; }
"""
css = css.replace('</style>', gallery_css + '</style>')

# 5. Gallery HTML
slides_html = '\n'.join(
    f'      <div class="galeria-slide"><img src="images/{fn}" alt="{alt}" loading="lazy"></div>'
    for fn, alt in gallery_images
)
galeria = f"""
<!-- GALERIA -->
<section class="galeria-sec">
  <div class="sec-header reveal" style="padding:0 24px;">
    <span class="sec-num">02</span>
    <h2>Galería</h2>
    <div class="sec-linea"></div>
  </div>
  <div class="galeria-wrap">
    <div class="galeria-track" id="galeriaTrack">
{slides_html}
    </div>
    <button class="galeria-btn prev" onclick="galeriaMove(-1)" aria-label="Anterior">&#8249;</button>
    <button class="galeria-btn next" onclick="galeriaMove(1)" aria-label="Siguiente">&#8250;</button>
  </div>
  <div class="galeria-dots" id="galeriaDots"></div>
</section>

<hr class="sep">

"""

# 6. YouTube embed inside Shows section (centered, before shows-grid)
video_embed = """
  <!-- VIDEO SHOW EN VIVO -->
  <div class="video-show-wrap reveal">
    <div class="video-iframe-wrap">
      <iframe
        src="https://www.youtube.com/embed/wW26FPcQF0w?rel=0&modestbranding=1"
        title="German Aquino Show en Vivo Cantante y Animador para Eventos"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen loading="lazy">
      </iframe>
    </div>
  </div>

"""
s_show = s_show.replace('<div class="shows-grid">', video_embed + '  <div class="shows-grid">', 1)

# 7. Clean contacts
s_cont = re.sub(r'<a[^>]*whatsapp[^>]*>.*?</a>', '', s_cont, flags=re.DOTALL)
s_cont = re.sub(r'<div[^>]*c-fila[^>]*>[\s\S]*?akinogerman[\s\S]*?</div>\s*</div>', '', s_cont)
s_cont = re.sub(r'<a[^>]*contactosmart[^>]*>.*?</a>', '', s_cont, flags=re.DOTALL)
s_cont = re.sub(r'<a[^>]*aquivaneh[^>]*>.*?</a>', '', s_cont, flags=re.DOTALL)
s_cont = re.sub(
    r'Consultas y cotizaciones a través de COSMART[^<]*',
    'Contrataciones: <a href="https://shows.cosmart.com.ar" target="_blank" style="color:var(--marron-suave);">shows.cosmart.com.ar</a>',
    s_cont
)
s_foot = s_foot.replace('<span class="if">@akinogerman</span>', '')

# 8. Gallery JS before </body>
gallery_js = """
<script>
(function(){
  var track = document.getElementById("galeriaTrack");
  var dotsWrap = document.getElementById("galeriaDots");
  if (!track) return;
  var slides = track.children.length, cur = 0, timer;
  for (var i = 0; i < slides; i++) {
    var d = document.createElement("button");
    d.className = "galeria-dot" + (i===0 ? " active" : "");
    d.setAttribute("data-i", String(i));
    d.onclick = function(){ goTo(parseInt(this.getAttribute("data-i"))); reset(); };
    dotsWrap.appendChild(d);
  }
  function goTo(n) {
    cur = (n + slides) % slides;
    track.style.transform = "translateX(-" + (cur*100) + "%)";
    dotsWrap.querySelectorAll(".galeria-dot").forEach(function(d,i){ d.classList.toggle("active", i===cur); });
  }
  window.galeriaMove = function(dir){ goTo(cur+dir); reset(); };
  function reset(){ clearInterval(timer); timer = setInterval(function(){ goTo(cur+1); }, 3500); }
  reset();
})();
</script>
"""
s_foot = s_foot.replace('</body>', gallery_js + '</body>')

# 9. Renumber visible section numbers
s_exp  = s_exp.replace('>01<', '>03<', 1)
s_form = s_form.replace('>02<', '>04<', 1)
s_vid  = s_vid.replace('>03<', '>01<', 1)
s_aqts = s_aqts.replace('>04<', '>06<', 1)

# 10. New order: css > hero > videos(01) > galeria(02) > exp(03) > form(04) > foto > shows(05) > aqts(06) > cont > foot
new_html = css + s_hero + s_vid + galeria + s_exp + s_form + s_foto + s_show + s_aqts + s_cont + s_foot

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print('\nFINAL FILE:', out_path)
print('Size:', len(new_html), 'bytes')

# Verify section order
print('\nSection order check:')
positions = []
for keyword in ['HERO', 'VIDEOS', 'GALERIA', 'EXPERIENCIA', 'FORMACI', 'FOTO 2', 'SHOWS', 'A QUE TE SUENA', 'CONTACTO', 'FOOTER']:
    m = re.search(r'<!-- [^\-]*' + keyword + r'[^\-]* -->', new_html)
    if m:
        positions.append((m.start(), keyword))
positions.sort()
for pos, name in positions:
    print(f'  {pos:6d}: {name}')
