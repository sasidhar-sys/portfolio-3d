import os
import re

html_path = r'c:\Projects\Attempt-1\alche-download\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Title & Meta Tags
content = content.replace('<title>Alche, Inc</title>', '<title>Sasidhar | 3D WebGL Portfolio</title>')
content = content.replace('<meta name="description" content="Alcheは、デジタルネイティブ時代にこれまでにないエンターテイメント体験を生み出すクリエイティブスタジオです。">', '<meta name="description" content="Portfolio of Sasidhar (Sasi) — 3D WebGL Developer specializing in React Three Fiber, custom GLSL shaders, and interactive web experiences.">')
content = content.replace('content="Alche, Inc"', 'content="Sasidhar | 3D WebGL Portfolio"')
content = content.replace('Alcheは、デジタルネイティブ時代にこれまでにないエンターテイメント体験を生み出すクリエイティブスタジオです。', 'Portfolio of Sasidhar (Sasi) — 3D WebGL Developer specializing in React Three Fiber, custom GLSL shaders, and interactive web experiences.')

# 2. Hero Tagline
new_loading = '''<div id="loading-text" class="Loading__text">
  Crafting immersive digital spaces<br>with code, shaders, and 3D optics.
</div>'''
content = re.sub(r'<div id="loading-text" class="Loading__text">.*?</div>', new_loading, content, flags=re.DOTALL)

# 3. Header Logo
header_logo_new = '''<div class="Header__logo" style="display: flex; align-items: center;">
  <a href="index.html">
    <img src="images/sasidhar_logo.png" alt="SASIDHAR" style="height: 60px; max-height: 80px; width: auto; display: block; padding-left: 10px;">
  </a>
</div>'''
content = re.sub(r'<div class="Header__logo">.*?</div>', header_logo_new, content, flags=re.DOTALL, count=1)

# 4. Footer Logo
footer_logo_new = '''<div class="Footer__logo">
  <img src="images/sasidhar_logo.png" alt="SASIDHAR" style="max-width: 280px; width: 100%; height: auto; opacity: 0.9;">
</div>'''
content = re.sub(r'<div class="Footer__logo">.*?</div>', footer_logo_new, content, flags=re.DOTALL)

# 5. Footer copyright
content = content.replace('©2025 Alche, inc.', '©2026 Sasidhar. All Rights Reserved.')

# 6. Social Links
social_links_new = '''<div class="SideMenu__social_links">
  <a href="https://github.com/sasidhar-sys" target="_blank" class="SideMenu__social_link"><span>GitHub</span></a>
  <a href="https://linkedin.com/in/your-linkedin" target="_blank" class="SideMenu__social_link"><span>LinkedIn</span></a>
  <a href="mailto:mailtosasi.official@gmail.com" class="SideMenu__social_link"><span>Contact Me</span></a>
</div>'''
content = re.sub(r'<div class="SideMenu__social_links">.*?</div>', social_links_new, content, flags=re.DOTALL)

# 7. Footer Contact
footer_contact_old = '''<a href="https://alche.notion.site/2488a66d791180af8037c174b9cee8ab" class="Footer__contact_button" target="_blank" rel="noopener noreferrer"> <span class="Footer__contact_button_text" data-scramble="">Contact</span>'''
footer_contact_new = '''<a href="mailto:mailtosasi.official@gmail.com" class="Footer__contact_button" target="_blank" rel="noopener noreferrer"> <span class="Footer__contact_button_text" data-scramble="">Contact</span>'''
content = content.replace(footer_contact_old, footer_contact_new)

# 8. Works List Items
works_list_new = '''<div class="Works__list">
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/ai_nexus.html" class="Works__item_title_link">AI Nexus 3D Portal</a>
    </h3>
    <p class="Works__item_title_ja">Interactive WebGL Experience</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>React Three Fiber</a></li>
      <li class="Works__item_categoryList_item"><a>GLSL Shaders</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/cyberpunk_metaverse.html" class="Works__item_title_link">Cyberpunk Metaverse City</a>
    </h3>
    <p class="Works__item_title_ja">Realtime 3D Virtual World</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Unreal Engine 5</a></li>
      <li class="Works__item_categoryList_item"><a>WebGL</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/crystal_shading.html" class="Works__item_title_link">Optical Crystal Shading</a>
    </h3>
    <p class="Works__item_title_ja">Physically Based Refraction</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Custom GLSL</a></li>
      <li class="Works__item_categoryList_item"><a>Three.js Optics</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/uefn_virtual_studio.html" class="Works__item_title_link">UEFN Virtual Studio</a>
    </h3>
    <p class="Works__item_title_ja">Interactive Concert Stage</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Fortnite Creative</a></li>
      <li class="Works__item_categoryList_item"><a>UEFN</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/unreal_engine_showcase.html" class="Works__item_title_link">Unreal Engine Showcase</a>
    </h3>
    <p class="Works__item_title_ja">Cloud Rendered Metaverse</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Unreal Engine</a></li>
      <li class="Works__item_categoryList_item"><a>Pixel Streaming</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/spatial_audio.html" class="Works__item_title_link">Spatial Audio Environment</a>
    </h3>
    <p class="Works__item_title_ja">3D Sound & Spatial Web</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Web Audio API</a></li>
      <li class="Works__item_categoryList_item"><a>Spatial Acoustics</a></li>
    </ul>
  </div>
</div>'''

content = re.sub(r'<div class="Works__list">.*?</div> </div> <div class="Works__more">', works_list_new + ' </div> <div class="Works__more">', content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: index.html updated cleanly!")
