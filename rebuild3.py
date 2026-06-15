import re, sys, os, base64, shutil
sys.stdout.reconfigure(encoding='utf-8')

src_path = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/index_github.html'
out_path = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/index.html'
img_dir  = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/images'
base_dir = 'C:/Users/vfernandez/Downloads/Sitio Web Germán Aquino/'
os.makedirs(img_dir, exist_ok=True)

with open(src_path, encoding='utf-8') as f:
    html = f.read()

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
    i += 1

# 2. Copy gallery images to images/
gallery_images = [
    ('ger cantando.png',                        'German Aquino cantando'),
    ('ger cantando en evento corporativo.png',   'German Aquino en evento corporativo'),
    ('ger cantando en fiesta de 15 años.png',    'German Aquino en fiesta de 15'),
    ('ger cantando en fiesta de 15 años 1 .png', 'German Aquino show fiesta'),
    ('IMG_3460 Cuadrada.jpg',                    'German Aquino'),
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

# 3. Find sections
def find_sec(html, keyword):
    m = re.search(r'<!-- [^\-]*' + keyword + r'[^\-]* -->', html)
    return m.start() if m else -1

p_hero  = find_sec(html, 'HERO')
p_exp   = find_sec(html, 'EXPERIENCIA')
p_form  = find_sec(html, 'FORMACI')
p_foto  = find_sec(html, 'FOTO 2')
p_vid   = find_sec(html, 'VIDEOS')
p_aqts  = find_sec(html, 'A QUE TE SUENA')
p_shows = find_sec(html, 'SHOWS PARA EVENTOS')
p_cont  = find_sec(html, 'CONTACTO')
p_foot  = find_sec(html, 'FOOTER')

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

# 4. Gallery CSS — horizontal strip, portrait photos, slow scroll
gallery_css = """
  /* GALERIA HORIZONTAL */
  .galeria-sec { padding: 60px 0; }
  .galeria-sec .sec-header { margin-bottom: 28px; padding: 0 24px; }
  .galeria-wrap { position: relative; }
  .galeria-track-outer { overflow: hidden; }
  .galeria-track {
    display: flex;
    gap: 10px;
    padding: 0 24px;
    transition: transform 0.7s cubic-bezier(0.4,0,0.2,1);
    will-change: transform;
  }
  .galeria-slide {
    flex: 0 0 200px;
    height: 300px;
    overflow: hidden;
    position: relative;
    border-radius: 2px;
  }
  .galeria-slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center top;
    filter: grayscale(10%) contrast(1.05);
    display: block;
    transition: transform 0.4s ease;
  }
  .galeria-slide:hover img { transform: scale(1.03); }
  .galeria-slide::after {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(13,13,13,0.35) 0%, transparent 40%);
    pointer-events: none;
  }
  .galeria-nav {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 20px;
    padding: 0 24px;
  }
  .galeria-btn {
    background: rgba(13,13,13,0.6);
    border: 1px solid rgba(196,168,130,0.25);
    color: var(--marron-suave);
    width: 40px; height: 40px;
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: background 0.2s, border-color 0.2s;
  }
  .galeria-btn:hover { background: rgba(122,92,63,0.4); border-color: var(--marron-suave); }
  .galeria-dots { display: flex; justify-content: center; gap: 6px; margin-top: 12px; }
  .galeria-dot {
    width: 4px; height: 4px; border-radius: 50%;
    background: var(--marron-suave); opacity: 0.25;
    cursor: pointer; transition: opacity 0.3s, transform 0.3s; border: none;
  }
  .galeria-dot.active { opacity: 1; transform: scale(1.5); }
  @media(min-width:768px) {
    .galeria-slide { flex: 0 0 240px; height: 360px; }
  }
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
  <div class="sec-header reveal">
    <span class="sec-num">03</span>
    <h2>Galería</h2>
    <div class="sec-linea"></div>
  </div>
  <div class="galeria-wrap">
    <div class="galeria-track-outer">
      <div class="galeria-track" id="galeriaTrack">
{slides_html}
      </div>
    </div>
    <div class="galeria-nav">
      <button class="galeria-btn prev" onclick="galeriaMove(-1)" aria-label="Anterior">&#8249;</button>
      <button class="galeria-btn next" onclick="galeriaMove(1)" aria-label="Siguiente">&#8250;</button>
    </div>
    <div class="galeria-dots" id="galeriaDots"></div>
  </div>
</section>

<hr class="sep">

"""

# 6. YouTube embed in Shows section
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

# 8. Gallery JS — moves by visible width, auto every 6 seconds
gallery_js = """
<script>
(function(){
  var outer = document.querySelector('.galeria-track-outer');
  var track = document.getElementById('galeriaTrack');
  var dotsWrap = document.getElementById('galeriaDots');
  if (!track || !outer) return;

  var slides = track.children.length;
  var cur = 0, timer;
  var slideW = track.children[0].offsetWidth + 10; // width + gap

  // Build dots (one per slide)
  for (var i = 0; i < slides; i++) {
    var d = document.createElement('button');
    d.className = 'galeria-dot' + (i===0 ? ' active' : '');
    d.setAttribute('data-i', String(i));
    d.onclick = function(){ goTo(parseInt(this.getAttribute('data-i'))); reset(); };
    dotsWrap.appendChild(d);
  }

  function goTo(n) {
    cur = Math.max(0, Math.min(n, slides - 1));
    track.style.transform = 'translateX(-' + (cur * slideW) + 'px)';
    dotsWrap.querySelectorAll('.galeria-dot').forEach(function(d,i){ d.classList.toggle('active', i===cur); });
  }

  window.galeriaMove = function(dir){
    var next = cur + dir;
    if (next >= slides) next = 0;
    if (next < 0) next = slides - 1;
    goTo(next); reset();
  };

  function reset(){ clearInterval(timer); timer = setInterval(function(){ window.galeriaMove(1); }, 6000); }
  reset();
})();
</script>
"""
s_foot = s_foot.replace('</body>', gallery_js + '</body>')

# 9. Renumber sections
# ORDER: hero(no num) > exp(01) > form(02) > foto > vid(03) > galeria(03 in HTML) > shows(04) > aqts(05) > cont > foot
# Keep original numbers, just set galeria=03, shows=04, aqts=05, vid stays 03, exp=01, form=02
s_aqts = re.sub(r'(<span class="sec-num">)0[0-9](<)', r'\g<1>05\2', s_aqts, count=1)
s_show = re.sub(r'(<span class="sec-num">)0[0-9](<)', r'\g<1>04\2', s_show, count=1)

# NEW ORDER: hero > exp(01) > form(02) > foto > vid(03) > galeria(03) > shows(04) > aqts(05) > cont > foot
new_html = css + s_hero + s_exp + s_form + s_foto + s_vid + galeria + s_show + s_aqts + s_cont + s_foot

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print('LISTO:', len(new_html), 'bytes')
positions = []
for kw in ['HERO','EXPERIENCIA','FORMACI','FOTO 2','VIDEOS','GALERIA','SHOWS','A QUE TE SUENA','CONTACTO','FOOTER']:
    m = re.search(r'<!-- [^\-]*' + kw + r'[^\-]* -->', new_html)
    if m:
        positions.append((m.start(), kw))
    elif kw == 'GALERIA':
        idx = new_html.find('<!-- GALERIA -->')
        if idx > 0: positions.append((idx, kw))
positions.sort()
for pos, name in positions:
    print(f'  {pos:6d}: {name}')

# Verify contacts
bad = ['whatsapp','akinogerman','contactosmart','aquivaneh']
for c in bad:
    if c in new_html: print('FAIL: found', c)
print('Contacts: OK' if not any(c in new_html for c in bad) else 'Some contacts remain')
