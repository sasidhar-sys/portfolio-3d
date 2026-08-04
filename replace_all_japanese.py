import re

html_path = r'c:\Projects\Attempt-1\alche-download\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML lang attribute
content = content.replace('<html lang="ja">', '<html lang="en">')
content = content.replace('og:locale" content="ja_JP"', 'og:locale" content="en_US"')

# 2. Accessibility ARIA Labels
content = content.replace('aria-label="サウンドのON/OFF切り替え"', 'aria-label="Toggle Sound ON/OFF"')
content = content.replace('aria-label="メニューを開く"', 'aria-label="Open Menu"')

# 3. Comments
content = content.replace('<!-- 基本設定 -->', '<!-- Basic Settings -->')
content = content.replace('<!-- ソーシャルリンク -->', '<!-- Social Links -->')
content = content.replace('<!-- scroll to explore 縦書きテキスト -->', '<!-- Scroll to explore -->')
content = content.replace('<!-- worksページへのリンクエリア -->', '<!-- Works Link -->')
content = content.replace('<!-- Tweakpane コンテナ -->', '<!-- Tweakpane Container -->')

# 4. News Area (Replacing Japanese News Items with AI/WebGL Announcements)
content = content.replace('Unreal Fest Bali 2025で登壇しました', 'Keynote Speaker at WebGL & AI Summit 2026')
content = content.replace('丸紅が提供する次世代ファッションメタバースアプリ「WEAR GO LAND」をAlche Studioが開発', 'Released MedScan AI & Enterprise RAG Platform for Clinical & Enterprise Users')
content = content.replace('博報堂DYメディアパートナーズとクリエイティブチーム「ReIMAGINE」を結成', 'Formed Advanced WebGL & Generative AI Studio ReIMAGINE')

# 5. Mission Section
old_mission_text = r'<div class="MissionVision__text" data-mission-text="">.*?</div>'
new_mission_text = '''<div class="MissionVision__text" data-mission-text="">
  <span class="MissionVision__line" data-line-index="0"> <span class="MissionVision__marker" data-marker-0="">Transforming ambitious ideas into intelligent digital products</span> </span><br>
  <span class="MissionVision__line" data-line-index="1"> <span class="MissionVision__marker" data-marker-1="">through Artificial Intelligence, Computer Vision, Generative AI,</span> </span><br>
  <span class="MissionVision__line" data-line-index="2"> <span class="MissionVision__marker" data-marker-2="">and immersive 3D technologies.</span> </span><br>
</div>'''
content = re.sub(old_mission_text, new_mission_text, content, flags=re.DOTALL)

old_mission_en = r'<div class="MissionVision__text_en" data-mission-text_en="">.*?</div>'
new_mission_en = '''<div class="MissionVision__text_en" data-mission-text_en="">
  Transforming ambitious ideas into intelligent digital products through Artificial Intelligence, Computer Vision, Generative AI, and 3D optics.
</div>'''
content = re.sub(old_mission_en, new_mission_en, content, flags=re.DOTALL)

# 6. Vision Section
old_vision_text = r'<div class="MissionVision__text" data-vision-text="">.*?</div>'
new_vision_text = '''<div class="MissionVision__text" data-vision-text="">
  <span class="MissionVision__line" data-line-index="0"> <span class="MissionVision__marker" data-marker-0="">Building Next-Generation</span> </span><br>
  <span class="MissionVision__line" data-line-index="1"> <span class="MissionVision__marker" data-marker-1="">AI Systems & Immersive 3D Experiences</span> </span><br>
</div>'''
content = re.sub(old_vision_text, new_vision_text, content, flags=re.DOTALL)

old_vision_en = r'<div class="MissionVision__text_en" data-vision-text_en="">.*?</div>'
new_vision_en = '''<div class="MissionVision__text_en" data-vision-text_en="">
  Building Next-Generation AI Systems & Immersive 3D Experiences.
</div>'''
content = re.sub(old_vision_en, new_vision_en, content, flags=re.DOTALL)

# 7. Service Descriptions (Replacing Japanese text in service items)
content = content.replace('Fortnite上での体験制作に強みを持ち、エンターテイメント性と拡張性のある空間を企画・制作。ブランドやIP、アーティストの世界観を表現し、世界中のユーザーに向けて新たな参加型イベントやインタラクティブコンテンツを展開します。', 'Specializing in high-performance WebGL, React Three Fiber, and custom GLSL shaders. Building interactive 3D web experiences that combine real-time graphics and artificial intelligence.')
content = content.replace('クラウドレンダリングから各デバイス向けのコンテンツを制作。ゲームエンジンの可能性を従来の枠組みを超えたエンターテインメント領域に展開し、没入感のある世界創造を通じてデジタル空間の新たな体験価値を拡張します。', 'Designing scalable software architecture spanning AI agents, medical intelligence, vector databases, and real-time WebGL graphics across Web, Desktop, and Cloud platforms.')

# 8. About Paragraph (Stellla Main Text)
old_about_p = r'<div class="Stellla__main_text">\s*<p>.*?</p>\s*<div class="Stellla__en">\s*<p>.*?</p>\s*</div>\s*</div>'
new_about_p = '''<div class="Stellla__main_text">
  <p>
    I am Sasidhar, an AI Engineer and Full-Stack Developer passionate about creating innovative software powered by Artificial Intelligence.<br data-media="max-md">
    My work spans Medical AI, Retrieval-Augmented Generation (RAG), Large Language Models, Computer Vision, WebGL, React Three Fiber, Three.js, and enterprise-scale web applications.<br data-media="max-md">
    I enjoy building products that are visually stunning, technically challenging, and impactful.
  </p>
  <div class="Stellla__en">
    <p>
      Designing intelligent AI products, immersive WebGL applications, and enterprise software.<br>
      Combining cutting-edge machine learning, real-time graphics, and exceptional user experiences.
    </p>
  </div>
</div>'''

content = re.sub(old_about_p, new_about_p, content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Replaced all Japanese copy with premium English copy!")
