import re

with open('ScoreShield.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update DARK colors for better visibility of muted/sub text
dark_colors_search = 'muted:"#4a5580", sub:"#7880a8"'
dark_colors_replace = 'muted:"#8e9ecf", sub:"#b1c1ec"'
text = text.replace(dark_colors_search, dark_colors_replace)

# 2. Fix the logo bg and size in the Shell component
logo_row_search = """        <div style={{ padding:open?"18px 16px":"16px 12px", borderBottom:`1px solid ${T.border}`,
          display:"flex", alignItems:"center", gap:10, minHeight:65 }}>
          <div style={{ flexShrink:0, width:36, height:36, borderRadius:10, overflow:"hidden",
            background:T.grad, display:"flex", alignItems:"center", justifyContent:"center",
            boxShadow:`0 4px 12px ${T.blue}40` }}>
            <img src={LOGO_SRC} alt="SS" style={{ width:28, height:28, objectFit:"contain" }}/>
          </div>
          {open && (
            <span style={{ fontSize:17, fontWeight:900, letterSpacing:-0.8, whiteSpace:"nowrap",
              background:T.grad, WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent" }}>
              ScoreShield
            </span>
          )}
        </div>"""

logo_row_replace = """        <div style={{ padding:open?"18px 16px":"16px 12px", borderBottom:`1px solid ${T.border}`,
          display:"flex", alignItems:"center", gap:10, minHeight:65 }}>
          <div style={{ flexShrink:0, display:"flex", alignItems:"center", justifyContent:"center" }}>
            <img src={LOGO_SRC} alt="SS" style={{ width:45, height:45, objectFit:"contain", filter: theme==="dark" ? "drop-shadow(0 2px 8px rgba(255,255,255,0.15))" : "drop-shadow(0 2px 8px rgba(0,0,0,0.1))" }}/>
          </div>
          {open && (
            <span style={{ fontSize:20, fontWeight:900, letterSpacing:-0.8, whiteSpace:"nowrap", color: T.text }}>
              ScoreShield
            </span>
          )}
        </div>"""
text = text.replace(logo_row_search, logo_row_replace)

# 3. Fix any hardcoded `#000` text that might clash on dark or light backgrounds
text = text.replace('color: "#000"', 'color: T.bg')
text = text.replace('color:"#000"', 'color:T.bg')

with open('ScoreShield.html', 'w', encoding='utf-8') as f:
    f.write(text)

