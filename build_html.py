import re

with open('temputf8.jsx', 'r', encoding='utf-8') as f:
    jsx = f.read()

# Replace PRODS
jsx = jsx.replace('const PRODS=[', 'const INIT_PRODS=[')

# Update SellerDash definition
jsx = jsx.replace('function SellerDash({ user, onLogout, theme, toggleTheme }) {', 'function SellerDash({ user, onLogout, theme, toggleTheme, onUpdateUser }) {')

# Add SellerDash states
seller_state = """
  const [prods, setProds] = useState(INIT_PRODS);
  const [showAddProd, setShowAddProd] = useState(false);
  const [newProd, setNewProd] = useState({ id:"", name:"", price:"", discount:"", cat:"General", stock:10 });
  const [profileForm, setProfileForm] = useState({ shopName: user?.shopName||"My Shop", email: user?.email||"seller@example.com", phone: user?.phone||"+91 9876543210" });
  
  useEffect(() => {
    setProfileForm({ shopName: user?.shopName||"My Shop", email: user?.email||"seller@example.com", phone: user?.phone||"+91 9876543210" });
  }, [user]);
"""
jsx = jsx.replace('const [tab, setTab] = useState("overview");', 'const [tab, setTab] = useState("overview");\n' + seller_state)
jsx = jsx.replace('PRODS.length', 'prods.length')
jsx = jsx.replace('PRODS.map', 'prods.map')

btn_target = '<button style={{ background:T.grad, color:"#fff", border:"none", borderRadius:11, padding:"10px 18px",'
new_btn = '<button onClick={() => setShowAddProd(true)} style={{ background:T.grad, color:"#fff", border:"none", borderRadius:11, padding:"10px 18px",'
jsx = jsx.replace(btn_target, new_btn)

add_prod_form = """
          {showAddProd && (
            <div style={{ marginBottom: 20, padding: 18, background: T.card, borderRadius: 12, border: `1px solid ${T.border}` }}>
              <h3 style={{color: T.text, marginBottom: 12}}>Add New Product</h3>
              <div style={{display:'flex', gap: 10, flexWrap:'wrap', marginBottom: 14}}>
                <input placeholder="Product ID" value={newProd.id} onChange={e=>setNewProd({...newProd, id:e.target.value})} style={{padding:'9px 12px', borderRadius:8, border:`1px solid ${T.border}`, background:T.surface, color:T.text, outline:'none'}} />
                <input placeholder="Name" value={newProd.name} onChange={e=>setNewProd({...newProd, name:e.target.value})} style={{padding:'9px 12px', borderRadius:8, border:`1px solid ${T.border}`, background:T.surface, color:T.text, outline:'none'}} />
                <input placeholder="Price" type="number" value={newProd.price} onChange={e=>setNewProd({...newProd, price:e.target.value})} style={{padding:'9px 12px', borderRadius:8, border:`1px solid ${T.border}`, background:T.surface, color:T.text, outline:'none'}} />
                <input placeholder="Discount (%)" type="number" value={newProd.discount} onChange={e=>setNewProd({...newProd, discount:e.target.value})} style={{padding:'9px 12px', borderRadius:8, border:`1px solid ${T.border}`, background:T.surface, color:T.text, outline:'none'}} />
              </div>
              <div style={{display:'flex', gap: 10}}>
                <button onClick={() => {
                  if(!newProd.name || !newProd.price || !newProd.id) return alert("Fill required fields");
                  setProds([...prods, { ...newProd, sales:0, rt:0, on:true }]);
                  setShowAddProd(false);
                  setNewProd({ id:"", name:"", price:"", discount:"", cat:"General", stock:10 });
                }} style={{padding: '9px 18px', background: T.green, color: '#fff', borderRadius: 8, border: 'none', cursor: 'pointer', fontWeight: 'bold'}}>Save Product</button>
                <button onClick={() => setShowAddProd(false)} style={{padding: '9px 18px', background: `${T.red}20`, color: T.red, borderRadius: 8, border: `1px solid ${T.red}`, cursor: 'pointer', fontWeight: 'bold'}}>Cancel</button>
              </div>
            </div>
          )}
"""
jsx = jsx.replace('<div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(210px,1fr))", gap:14 }}>', add_prod_form + '\n<div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(210px,1fr))", gap:14 }}>')

jsx = re.sub(r'<button style=\{\{ flex:1, background:`\$\{T\.red\}10`,.*?<Icon name="trash".*?</button>',
r'''<button onClick={() => setProds(prods.filter(x => x.id !== p.id))} style={{ flex:1, background:`${T.red}10`, color:T.red, border:`1px solid ${T.red}20`, borderRadius:8, padding:"7px", fontSize:11, fontWeight:600, cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center", gap:5, fontFamily:"inherit" }}>
<Icon name="trash" size={12} color={T.red} strokeWidth={2}/>Remove
</button>''', jsx, flags=re.DOTALL)

# Handle Seller profile
jsx = re.sub(
    r'\{\[\s*\["Shop Name",user\?\.shopName\|\|"My Shop","tag"\],\s*\["Email",user\?\.email\|\|"seller@example\.com","mail"\],\s*\["Phone",user\?\.phone\|\|"\+91 9876543210","phone"\],\s*\["Platform","Meesho, Instagram","grid"\]\s*\].*?defaultValue=\{v\}',
    r'''{Object.entries({shopName: ["Shop Name", profileForm.shopName, "tag"], email: ["Email", profileForm.email, "mail"], phone: ["Phone", profileForm.phone, "phone"], platform: ["Platform", "Meesho, Instagram", "grid"]}).map(([key, [k,v,ic]])=>(
              <div key={k} style={{ marginBottom:16 }}>
                <label style={{ fontSize:11, color:T.muted, display:"flex", alignItems:"center", gap:5, marginBottom:6, fontWeight:600, textTransform:"uppercase", letterSpacing:0.8 }}>
                  <Icon name={ic} size={12} color={T.muted} strokeWidth={1.8}/>{k}
                </label>
                <input value={v} onChange={e=>setProfileForm({...profileForm, [key]: e.target.value})} disabled={key === 'platform'}''',
    jsx, flags=re.DOTALL
)

jsx = re.sub(
    r'<button style=\{\{ background:T\.grad, color:"#fff", border:"none", borderRadius:10, padding:"11px 24px".*?>Save Changes</button>',
    r'''<button onClick={() => { onUpdateUser(profileForm); alert("Profile Updated Successfully!"); }} style={{ background:T.grad, color:"#fff", border:"none", borderRadius:10, padding:"11px 24px", fontWeight:700, fontSize:14, cursor:"pointer", boxShadow:`0 4px 16px ${T.blue}35`, fontFamily:"inherit" }}>Save Changes</button>''',
    jsx, flags=re.DOTALL
)

# Handle Customer Dash
jsx = jsx.replace('function CustomerDash({ user, onLogout, theme, toggleTheme }) {', 'function CustomerDash({ user, onLogout, theme, toggleTheme, onUpdateUser }) {')

cust_state = """
  const [profileForm, setProfileForm] = useState({ name: user?.name||"Demo Customer", email: user?.email||"customer@example.com", phone: user?.phone||"+91 9876543210" });
  useEffect(() => {
    setProfileForm({ name: user?.name||"Demo Customer", email: user?.email||"customer@example.com", phone: user?.phone||"+91 9876543210" });
  }, [user]);
"""
jsx = jsx.replace('const [tab, setTab] = useState("home");', 'const [tab, setTab] = useState("home");\n' + cust_state)

jsx = re.sub(
    r'\{\[\s*\["Full Name",user\?\.name\|\|"Demo Customer","user"\],\s*\["Email",user\?\.email\|\|"customer@example\.com","mail"\],\s*\["Phone",user\?\.phone\|\|"\+91 9876543210","phone"\]\s*\].*?defaultValue=\{v\}',
    r'''{Object.entries({name: ["Full Name", profileForm.name, "user"], email: ["Email", profileForm.email, "mail"], phone: ["Phone", profileForm.phone, "phone"]}).map(([key, [k,v,ic]])=>(
              <div key={k} style={{ marginBottom:15 }}>
                <label style={{ fontSize:11, color:T.muted, display:"flex", alignItems:"center", gap:5, marginBottom:6, fontWeight:600, textTransform:"uppercase", letterSpacing:0.8 }}>
                  <Icon name={ic} size={12} color={T.muted} strokeWidth={1.8}/>{k}
                </label>
                <input value={v} onChange={e=>setProfileForm({...profileForm, [key]: e.target.value})}''',
    jsx, flags=re.DOTALL
)

jsx = re.sub(
    r'<button style=\{\{ background:T\.grad, color:"#fff", border:"none", borderRadius:10, padding:"11px 24px".*?</button>',
    r'''<button onClick={() => { onUpdateUser(profileForm); alert("Profile Updated!"); }} style={{ background:T.grad, color:"#fff", border:"none", borderRadius:10, padding:"11px 24px", fontWeight:700, fontSize:14, cursor:"pointer", boxShadow:`0 4px 16px ${T.blue}35`, fontFamily:"inherit", display:"flex", alignItems:"center", gap:8 }}>
              <Icon name="check" size={15} color="#fff" strokeWidth={2.5}/>Update Profile
            </button>''',
    jsx, flags=re.DOTALL
)

# Replace App setup
app_update = """
  const updateUser = (data) => setUser({ ...user, ...data });
"""
jsx = jsx.replace('const logout = () => { setUser(null); setRole(null); };', 'const logout = () => { setUser(null); setRole(null); };\n' + app_update)
jsx = jsx.replace('onLogout={logout}', 'onLogout={logout} onUpdateUser={updateUser}')
jsx = jsx.replace('export default function App()', 'function App()')

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScoreShield - AI Verification</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://unpkg.com/prop-types/prop-types.min.js"></script>
    <script src="https://unpkg.com/recharts/umd/Recharts.js"></script>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const {{ useState, useEffect, useRef }} = React;
        const {{ AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend }} = window.Recharts;
        const LOGO_SRC = "./logo.png";
        
{jsx}

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

with open('ScoreShield.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
