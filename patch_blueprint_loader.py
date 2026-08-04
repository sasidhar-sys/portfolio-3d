import os

js_path = r"c:\Projects\Attempt-1\alche-download\js\index.astro_astro_type_script_index_0_lang.Cu0uHvXK.js"

with open(js_path, "r", encoding="utf-8") as f:
    code = f.read()

# STEP 4: Patch _startLogoAnimation()
old_step4 = "gsapWithCSS.set(this._logoContainer,{opacity:1}),this._logoController.reset()"
new_step4 = 'gsapWithCSS.set(this._logoContainer,{opacity:1}),this._logoContainer.innerHTML="",this._blueprintLoader=new window.BlueprintLoader(this._logoContainer),this._blueprintLoader.load().then(()=>{this._blueprintLoader.play()})'

if old_step4 in code:
    code = code.replace(old_step4, new_step4)
    print("STEP 4: Patched _startLogoAnimation successfully!")
else:
    print("STEP 4: Target string not found or already patched.")

# STEP 5: Prevent old Lottie update in _updateLogoAnimation()
old_step5 = "this._logoController.setProgress(.144+u*.3775)"
new_step5 = "if(!this._blueprintLoader){this._logoController.setProgress(.144+u*.3775)}"

if old_step5 in code:
    code = code.replace(old_step5, new_step5)
    print("STEP 5: Patched _updateLogoAnimation successfully!")
else:
    print("STEP 5: Target string not found or already patched.")

# STEP 6: Cleanup in _resetAnimations()
old_step6 = "this._logoController&&this._logoContainer&&(this._logoController.reset(),gsapWithCSS.set(this._logoContainer,{opacity:0}))"
new_step6 = "this._logoController&&this._logoContainer&&(this._logoController.reset(),gsapWithCSS.set(this._logoContainer,{opacity:0})),this._blueprintLoader&&(this._blueprintLoader.destroy(),this._blueprintLoader=null)"

if old_step6 in code:
    code = code.replace(old_step6, new_step6)
    print("STEP 6: Patched _resetAnimations successfully!")
else:
    print("STEP 6: Target string not found or already patched.")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(code)

print("SUCCESS: Bundle updated with BlueprintLoader integration!")
