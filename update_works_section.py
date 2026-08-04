import re

html_path = r'c:\Projects\Attempt-1\alche-download\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_works_list = '''<div class="Works__list">
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/nova.html" class="Works__item_title_link">NOVA</a>
    </h3>
    <p class="Works__item_title_ja">AI Desktop Assistant for Intelligent Automation & Productivity</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>AI Agents</a></li>
      <li class="Works__item_categoryList_item"><a>LLM</a></li>
      <li class="Works__item_categoryList_item"><a>Python</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/medscan.html" class="Works__item_title_link">MedScan AI</a>
    </h3>
    <p class="Works__item_title_ja">AI-Assisted Medical Intelligence Platform for Explainable Clinical Decision Support and Early Disease Detection</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Medical AI</a></li>
      <li class="Works__item_categoryList_item"><a>Explainable AI</a></li>
      <li class="Works__item_categoryList_item"><a>Computer Vision</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/portfolio_3d.html" class="Works__item_title_link">3D Interactive Portfolio</a>
    </h3>
    <p class="Works__item_title_ja">Cinematic WebGL Portfolio with Real-Time 3D Rendering & Custom Shader Experiences</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>React Three Fiber</a></li>
      <li class="Works__item_categoryList_item"><a>Three.js</a></li>
      <li class="Works__item_categoryList_item"><a>GLSL</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/futureforge.html" class="Works__item_title_link">FutureForge AI</a>
    </h3>
    <p class="Works__item_title_ja">AI-Powered Creative Automation Platform for Intelligent Video Generation & Content Workflows</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Generative AI</a></li>
      <li class="Works__item_categoryList_item"><a>Next.js</a></li>
      <li class="Works__item_categoryList_item"><a>Python</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/rag_assistant.html" class="Works__item_title_link">Enterprise RAG Assistant</a>
    </h3>
    <p class="Works__item_title_ja">Retrieval-Augmented Knowledge Platform with Semantic Search, Vector Intelligence & Enterprise AI Chat</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>RAG</a></li>
      <li class="Works__item_categoryList_item"><a>LangChain</a></li>
      <li class="Works__item_categoryList_item"><a>Vector Database</a></li>
    </ul>
  </div>
  <div class="Works__item" data-works_item="">
    <div class="Works__item_info">
      <time class="Works__item_date">2026</time>
    </div>
    <h3 class="Works__item_title" data-works_title="">
      <a href="works/detail/intern_analytics.html" class="Works__item_title_link">Intern Analytics Platform</a>
    </h3>
    <p class="Works__item_title_ja">AI-Powered Internship Performance Analytics, Prediction & Workforce Intelligence Dashboard</p>
    <ul class="Works__item_categoryList">
      <li class="Works__item_categoryList_item"><a>Machine Learning</a></li>
      <li class="Works__item_categoryList_item"><a>FastAPI</a></li>
      <li class="Works__item_categoryList_item"><a>Next.js</a></li>
    </ul>
  </div>
</div>'''

content = re.sub(r'<div class="Works__list">.*?</div> </div> <div class="Works__more">', new_works_list + ' </div> <div class="Works__more">', content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Updated Works section with user projects!")
