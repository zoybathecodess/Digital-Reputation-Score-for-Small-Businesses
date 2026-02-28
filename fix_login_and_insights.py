import re

with open('ScoreShield.html', 'r', encoding='utf-8') as f:
    text = f.read()

# --- 1. Fix the Seller Login Bug ---
# The bug happens because customer login manual entry is getting blocked by seller constraints if the user toggled
# things weirdly or if role wasn't evaluated properly.
# Actually, the user says "when i login through the login page for seller or customer by givin manual entry it is not taking the id for seller".
# The UI for sellerId and platform is wrapped in `{role==="seller" && (...) }`. 
# In `const submit = () => {`, we have:
# `if (role==="seller" && !form.sellerId) return setErr("Seller ID is required...");`
# Wait, if mode is "login", does the UI show `sellerId`? Yes, because `{role==="seller" && ...}` is NOT wrapped in `mode==="signup"`.
# But wait, looking at the code for Seller Login inputs:
#
#             {role==="seller" && (
#               <>
#                 <div style={{ position:"relative", marginBottom: 13 }}>
#                 ... <input name="sellerId" ... />
#                 <div style={{ position:"relative", marginBottom: 13 }}>
#                 ... <select name="platform" ...>
#
# But wait, earlier we did: text = text.replace(login_state_search, login_state_replace)
# where login state initialized `platform:"WhatsApp Business"`.
# Why is it failing for seller manual entry?
# "it is not taking the id for seller and not logging in"
# Ah, maybe the user means typing in the Seller ID input isn't updating the state?
# Let's check `const update = e => { setForm(f => ({...f, [e.target.name]:e.target.value})); setErr(""); };`
# The input has `name="sellerId"`. This is correct.
# Wait, if they type an ID that doesn't exist?
# "validSeller = SELLERS.find(s => s.id === form.sellerId && s.pl === form.platform);"
# If they type "S1211", it works. But if they type "s1211" (lowercase), it fails because IDs might be case-sensitive.
# Let's make the ID check case-insensitive.

login_check_search = 'const validSeller = SELLERS.find(s => s.id === form.sellerId && s.pl === form.platform);'
login_check_replace = 'const validSeller = SELLERS.find(s => s.id.toLowerCase() === form.sellerId.toLowerCase() && s.pl === form.platform);'
text = text.replace(login_check_search, login_check_replace)

login_on_login_search = 'sellerId: form.sellerId'
login_on_login_replace = 'sellerId: form.sellerId.toUpperCase()'
text = text.replace(login_on_login_search, login_on_login_replace)


# --- 2. Add "Seller Profile" View to Customer Dashboard ---
# First, add a state for viewing a specific seller in CustomerDash

cust_dash_state_search = 'const [showReviewFor, setShowReviewFor] = useState(null);'
cust_dash_state_replace = 'const [showReviewFor, setShowReviewFor] = useState(null);\n  const [viewingSeller, setViewingSeller] = useState(null);'
text = text.replace(cust_dash_state_search, cust_dash_state_replace)

# Modify the Available Products and Orders list so that Clicking the Seller name/id opens their profile
# Old: '<div style={{ fontSize:10, color:T.muted, marginBottom:8 }}>Seller: {p.sellerId} on {p.platform} (Trust: {SELLERS.find(s=>s.id === p.sellerId && s.pl === p.platform)?.sc || 50}/100)</div>'
# New: A clickable link

seller_link_replace = """<div style={{ fontSize:11, color:T.muted, marginBottom:8, display:"flex", alignItems:"center", gap:4 }}>
                  Seller: <span onClick={() => { setViewingSeller({ id: p.sellerId, pl: p.platform }); setTab('sellerProfile'); }} style={{ color:T.blue, fontWeight:700, cursor:"pointer", textDecoration:"underline" }}>{p.sellerId}</span> 
                  on {p.platform} 
                  <span style={{ padding:"2px 6px", borderRadius:4, background: trustColor(SELLERS.find(s=>s.id === p.sellerId && s.pl === p.platform)?.sc || 50)+"20", color:trustColor(SELLERS.find(s=>s.id === p.sellerId && s.pl === p.platform)?.sc || 50), fontWeight:800, fontSize:10 }}>
                    {SELLERS.find(s=>s.id === p.sellerId && s.pl === p.platform)?.sc || 50} SC
                  </span>
                </div>"""
text = text.replace('<div style={{ fontSize:10, color:T.muted, marginBottom:8 }}>Seller: {p.sellerId} on {p.platform} (Trust: {SELLERS.find(s=>s.id === p.sellerId && s.pl === p.platform)?.sc || 50}/100)</div>', seller_link_replace)

# Modify Analytics/Search lists to allow clicking on Seller ID too.
# There is a Find Sellers tab (`tab==="search"`)
# In that tab, we map over `results` which are actual sellers from SELLERS array.
# Old: `<div style={{ fontWeight:700, fontSize:15, color:T.text }}>{r.id} <span style={{fontSize:12,color:T.sub,fontWeight:500}}>({r.pl})</span></div>`
# New: Clickable link

search_item_search = '<div style={{ fontWeight:700, fontSize:15, color:T.text }}>{r.id} <span style={{fontSize:12,color:T.sub,fontWeight:500}}>({r.pl})</span></div>'
search_item_replace = '<div onClick={() => { setViewingSeller({ id: r.id, pl: r.pl }); setTab("sellerProfile"); }} style={{ fontWeight:700, fontSize:15, color:T.blue, cursor:"pointer", textDecoration:"underline" }}>{r.id} <span style={{fontSize:12,color:T.sub,fontWeight:500,textDecoration:"none"}}>({r.pl})</span></div>'
text = text.replace(search_item_search, search_item_replace)

# Now inject the `sellerProfile` tab UI into CustomerDash
# We need to find the end of the `tab==="search"` block or similar to inject this.
# Let's inject it right before `{/* ANALYTICS */}`

seller_profile_tab = """
      {/* SELLER PROFILE VIEW */}
      {tab==="sellerProfile" && viewingSeller && (() => {
        const s = SELLERS.find(x => x.id === viewingSeller.id && x.pl === viewingSeller.pl) || {};
        const sProds = globalProds.filter(p => p.sellerId === viewingSeller.id && p.platform === viewingSeller.pl);
        const sOrders = globalOrders.filter(o => o.sellerId === viewingSeller.id && o.rt !== null); // Reviews left for this seller
        
        return (
          <div className="fu0">
            <button onClick={() => setTab("home")} style={{ background:"transparent", border:"none", color:T.blue, cursor:"pointer", marginBottom:16, fontWeight:600, display:"flex", alignItems:"center", gap:4 }}>
              <Icon name="arrowLeft" size={16} color={T.blue} /> Back
            </button>
            
            <div style={{ background: T.card, border: `1px solid ${T.border}`, borderRadius: 16, padding: 24, marginBottom: 24 }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"flex-start" }}>
                <div>
                  <h2 style={{ fontSize:28, fontWeight:900, color:T.text, margin:0 }}>{s.id}</h2>
                  <div style={{ fontSize:14, color:T.sub, marginTop:4 }}>Platform: <b>{s.pl}</b> | Category: <b>{s.ct || "Mixed"}</b></div>
                </div>
                <div style={{ textAlign:"right" }}>
                  <div style={{ fontSize:32, fontWeight:900, color: trustColor(s.sc || 0) }}>{s.sc || 0}</div>
                  <div style={{ fontSize:12, fontWeight:800, color: trustColor(s.sc || 0), background: trustColor(s.sc || 0)+"15", padding:"4px 8px", borderRadius:6 }}>{trustLabel(s.sc || 0)}</div>
                </div>
              </div>
              
              <div style={{ display:"flex", gap:16, marginTop:20, flexWrap:"wrap" }}>
                <div style={{ flex:1, minWidth:120, background:T.surface, padding:12, borderRadius:12, border:`1px solid ${T.border}` }}>
                  <div style={{ fontSize:11, color:T.muted }}>Total Reviews</div>
                  <div style={{ fontSize:18, fontWeight:800, color:T.text }}>{s.rv || 0}</div>
                </div>
                <div style={{ flex:1, minWidth:120, background:T.surface, padding:12, borderRadius:12, border:`1px solid ${T.border}` }}>
                  <div style={{ fontSize:11, color:T.muted }}>Authentic</div>
                  <div style={{ fontSize:18, fontWeight:800, color:T.green }}>{s.gn || 0}</div>
                </div>
                <div style={{ flex:1, minWidth:120, background:T.surface, padding:12, borderRadius:12, border:`1px solid ${T.border}` }}>
                  <div style={{ fontSize:11, color:T.muted }}>Fake/Flagged</div>
                  <div style={{ fontSize:18, fontWeight:800, color:T.red }}>{s.fk || 0}</div>
                </div>
                <div style={{ flex:1, minWidth:120, background:T.surface, padding:12, borderRadius:12, border:`1px solid ${T.border}` }}>
                  <div style={{ fontSize:11, color:T.muted }}>Avg Rating</div>
                  <div style={{ fontSize:18, fontWeight:800, color:T.amber }}>â˜… {s.rt || "0.0"}</div>
                </div>
              </div>
            </div>

            <h3 style={{ fontSize: 18, color: T.text, marginBottom: 12 }}>Available Products ({sProds.length})</h3>
            {sProds.length === 0 ? <p style={{ color:T.muted, fontSize:13 }}>This seller has not listed any products yet.</p> : (
              <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(210px,1fr))", gap:14, marginBottom: 32 }}>
                {sProds.map(p=>(
                  <div key={p.id} className="card" style={{ background:T.surface, border:`1px solid ${T.border}`, borderRadius:16, padding:18 }}>
                    <div style={{ fontSize:14, fontWeight:700, color:T.text, marginBottom:2 }}>{p.name}</div>
                    <div style={{ fontSize:11, color:T.muted, marginBottom:12 }}>{p.cat}</div>
                    <div style={{ fontSize:16, fontWeight:800, color:T.blue, marginBottom:12 }}>â‚¹{p.price}</div>
                    <button onClick={() => {
                       alert("Successfully purchased " + p.name + " from seller ID: " + p.sellerId + " on " + p.platform + "!");
                       const newOrder = { id: "ORD-" + Math.floor(Math.random()*10000), product: p.name, buyer: user?.name || "Demo Customer", amount: p.price, status: "Delivered", date: "Just Now", rt: null, prodId: p.id, sellerId: p.sellerId || "Unknown" };
                       setGlobalOrders([newOrder, ...globalOrders]);
                       setTab("orders");
                    }} style={{ width:"100%", background:T.gradG, color:"#fff", border:"none", borderRadius:8, padding:"8px", cursor:"pointer", fontWeight:600 }}>Buy Now</button>
                  </div>
                ))}
              </div>
            )}
            
            <h3 style={{ fontSize: 18, color: T.text, marginBottom: 12 }}>Customer Reviews</h3>
            {sOrders.length === 0 ? <p style={{ color:T.muted, fontSize:13, marginBottom:40 }}>No reviews left for this seller yet.</p> : (
              <div style={{ display:"flex", flexDirection:"column", gap:12, marginBottom:40 }}>
                {sOrders.map((o, i) => (
                  <div key={i} style={{ background:T.surface, border:`1px solid ${T.border}`, borderRadius:12, padding:16 }}>
                    <div style={{ display:"flex", justifyContent:"space-between", marginBottom:8 }}>
                      <div style={{ fontSize:13, fontWeight:700, color:T.text }}>{o.buyer} <span style={{ color:T.muted, fontWeight:400, fontSize:11 }}>bought {o.product}</span></div>
                      <div style={{ color:T.amber, fontWeight:800, fontSize:13 }}>â˜… {o.rt}</div>
                    </div>
                    <div style={{ fontSize:13, color:T.sub }}>"Great quality and fast delivery. Trust score is accurate."</div>
                  </div>
                ))}
              </div>
            )}
            
          </div>
        );
      })()}
"""

text = text.replace('{/* ANALYTICS */}', seller_profile_tab + '\n      {/* ANALYTICS */}')

with open('ScoreShield.html', 'w', encoding='utf-8') as f:
    f.write(text)
