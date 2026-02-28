import re

with open('ScoreShield.html', 'r', encoding='utf-8') as f:
    text = f.read()

with open('sellers_data.json', 'r', encoding='utf-8') as f:
    json_data = f.read()

# 1. Replace logo.png with logo without bg.png
text = text.replace('const LOGO_SRC = "./logo.png";', 'const LOGO_SRC = "./logo without bg.png";')

# 2. Update SELLERS array entirely
# We extract everything between `const SELLERS = [` and `];` and replace it with `const SELLERS = [...json_data]` 
text = re.sub(r'const SELLERS = \[.*?\];', f'const SELLERS = {json_data};', text, flags=re.DOTALL)

# 3. Modify Seller Login fields
login_state_search = 'const [form, setForm] = useState({ name:"", email:"", pass:"", phone:"", shop:"" });'
login_state_replace = 'const [form, setForm] = useState({ name:"", email:"", pass:"", phone:"", shop:"", sellerId:"", platform:"WhatsApp Business" });'
text = text.replace(login_state_search, login_state_replace)

submit_search = 'if (mode==="signup" && role==="seller" && !form.shop) return setErr("Shop name is required.");'
submit_replace = """if (mode==="signup" && role==="seller" && !form.shop) return setErr("Shop name is required.");
    if (role==="seller" && !form.sellerId) return setErr("Seller ID is required to verify identity.");
    
    // Check if seller ID exists
    const validSeller = SELLERS.find(s => s.id === form.sellerId && s.pl === form.platform);
    if (role==="seller" && mode==="login" && !validSeller) return setErr("Seller ID doesn't exist on this platform. Check records.");
"""
text = text.replace(submit_search, submit_replace)

update_user_search = '{ name: form.name||"Demo User", email: form.email, shopName: form.shop||"My Shop", phone: form.phone }'
update_user_replace = '{ name: form.name||"Demo User", email: form.email, shopName: form.shop||"My Shop", phone: form.phone, sellerId: form.sellerId, platform: form.platform }'
text = text.replace(update_user_search, update_user_replace)

google_login_search = '{ name:"Demo User", email:"demo@gmail.com", shopName:"Demo Shop" }'
google_login_replace = '{ name:"Demo User", email:"demo@gmail.com", shopName:"Demo Shop", sellerId:"S10", platform:"WhatsApp Business" }'
text = text.replace(google_login_search, google_login_replace)

login_inputs_search = """{mode==="signup" && role==="seller" && (
              <div style={{ position:"relative" }}>
                <div style={{ position:"absolute", left:14, top:"50%", transform:"translateY(-50%)", pointerEvents:"none", zIndex:1 }}>
                  <Icon name="store" size={17} color={T.muted} strokeWidth={1.8}/>
                </div>
                <input name="shop" value={form.shop} onChange={update} placeholder="Shop / Business Name *" style={inputStyle}
                  onFocus={e=>{e.target.style.borderColor=T.blue;e.target.style.boxShadow=`0 0 0 3px ${T.blue}22`;}}
                  onBlur={e=>{e.target.style.borderColor=T.border;e.target.style.boxShadow="none";}}/>
              </div>
            )}"""
            
login_inputs_replace = """{mode==="signup" && role==="seller" && (
              <div style={{ position:"relative", marginBottom: 13 }}>
                <div style={{ position:"absolute", left:14, top:"50%", transform:"translateY(-50%)", pointerEvents:"none", zIndex:1 }}>
                  <Icon name="store" size={17} color={T.muted} strokeWidth={1.8}/>
                </div>
                <input name="shop" value={form.shop} onChange={update} placeholder="Shop / Business Name *" style={inputStyle}
                  onFocus={e=>{e.target.style.borderColor=T.blue;e.target.style.boxShadow=`0 0 0 3px ${T.blue}22`;}}
                  onBlur={e=>{e.target.style.borderColor=T.border;e.target.style.boxShadow="none";}}/>
              </div>
            )}
            
            {role==="seller" && (
              <>
                <div style={{ position:"relative", marginBottom: 13 }}>
                  <div style={{ position:"absolute", left:14, top:"50%", transform:"translateY(-50%)", pointerEvents:"none", zIndex:1 }}>
                    <Icon name="tag" size={17} color={T.muted} strokeWidth={1.8}/>
                  </div>
                  <input name="sellerId" value={form.sellerId} onChange={update} placeholder="Seller ID (e.g. S121) *" style={inputStyle}
                    onFocus={e=>{e.target.style.borderColor=T.blue;e.target.style.boxShadow=`0 0 0 3px ${T.blue}22`;}}
                    onBlur={e=>{e.target.style.borderColor=T.border;e.target.style.boxShadow="none";}}/>
                </div>
                <div style={{ position:"relative", marginBottom: 13 }}>
                  <div style={{ position:"absolute", left:14, top:"50%", transform:"translateY(-50%)", pointerEvents:"none", zIndex:1 }}>
                    <Icon name="grid" size={17} color={T.muted} strokeWidth={1.8}/>
                  </div>
                  <select name="platform" value={form.platform} onChange={update} style={inputStyle}
                    onFocus={e=>{e.target.style.borderColor=T.blue;e.target.style.boxShadow=`0 0 0 3px ${T.blue}22`;}}
                    onBlur={e=>{e.target.style.borderColor=T.border;e.target.style.boxShadow="none";}}>
                    {[...new Set(SELLERS.map(s=>s.pl))].map(p=><option key={p} value={p}>{p}</option>)}
                  </select>
                </div>
              </>
            )}"""
text = text.replace(login_inputs_search, login_inputs_replace)

# Disable the gap 13px globally on inputs wrapper and use margins inside inputs to allow conditional gap
text = text.replace('<div className="fu3" style={{ display:"flex", flexDirection:"column", gap:13 }}>', '<div className="fu3" style={{ display:"flex", flexDirection:"column" }}>')

input_wrappers = ['<div style={{ position:"relative" }}>']
for w in input_wrappers:
    text = text.replace(w, '<div style={{ position:"relative", marginBottom: 13 }}>')

# 4. Integrate Seller ID into Seller Dashboard Context globally
text = text.replace('const [profileForm, setProfileForm] = useState({ shopName: user?.shopName||"My Shop", email: user?.email||"seller@example.com", phone: user?.phone||"+91 9876543210" });',
                    'const [profileForm, setProfileForm] = useState({ shopName: user?.shopName||"My Shop", email: user?.email||"seller@example.com", phone: user?.phone||"+91 9876543210", platform: user?.platform || "WhatsApp Business" });')

text = text.replace('const trust = 87;', 'const trust = user?.sellerId ? (SELLERS.find(s=>s.id === user.sellerId && s.pl === user.platform)?.sc || 50) : 87;')

text = text.replace('{Object.entries({shopName: ["Shop Name", profileForm.shopName, "tag"], email: ["Email", profileForm.email, "mail"], phone: ["Phone", profileForm.phone, "phone"], platform: ["Platform", "Meesho, Instagram", "grid"]})',
                    '{Object.entries({shopName: ["Shop Name", profileForm.shopName, "tag"], email: ["Email", profileForm.email, "mail"], phone: ["Phone", profileForm.phone, "phone"], platform: ["Platform", profileForm.platform, "grid"]})')


# 5. Fix Add Product in Seller Dashboard to use the actual logged-in Platform / Seller mapping

add_prod_buy = """const newOrder = { id: "ORD-" + Math.floor(Math.random()*10000), product: p.name, buyer: user?.name || "Demo Customer", amount: p.price, status: "Delivered", date: "Just Now", rt: null, prodId: p.id };"""
add_prod_buy_fixed = """const newOrder = { id: "ORD-" + Math.floor(Math.random()*10000), product: p.name, buyer: user?.name || "Demo Customer", amount: p.price, status: "Delivered", date: "Just Now", rt: null, prodId: p.id, sellerId: p.sellerId || "Unknown" };"""

text = text.replace(add_prod_buy, add_prod_buy_fixed)

alert_msg = 'alert("Successfully purchased " + p.name + "!");'
alert_msg_fixed = 'alert("Successfully purchased " + p.name + " from seller ID: " + p.sellerId + " on " + p.platform + "!");'
text = text.replace(alert_msg, alert_msg_fixed)

seller_add_prods = 'setGlobalProds([{ ...newProd, sales:0, rt:0, on:true }, ...globalProds]);'
seller_add_prods_fixed = 'setGlobalProds([{ ...newProd, sales:0, rt:0, on:true, sellerId: user.sellerId, platform: user.platform }, ...globalProds]);'
text = text.replace('setProds([...prods, { ...newProd, sales:0, rt:0, on:true }]);', seller_add_prods_fixed)

customer_prods_ui_old = '<div style={{ fontSize:10, color:T.muted, marginBottom:8 }}>Seller Rating: {SELLERS[Math.floor(Math.random()*SELLERS.length)].sc}/100</div>'
customer_prods_ui_new = '<div style={{ fontSize:10, color:T.muted, marginBottom:8 }}>Seller: {p.sellerId} on {p.platform} (Trust: {SELLERS.find(s=>s.id === p.sellerId && s.pl === p.platform)?.sc || 50}/100)</div>'
text = text.replace(customer_prods_ui_old, customer_prods_ui_new)


with open('ScoreShield.html', 'w', encoding='utf-8') as f:
    f.write(text)

