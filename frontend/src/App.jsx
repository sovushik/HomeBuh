import React, {useEffect, useState} from 'react'

export default function App(){
  const [status, setStatus] = useState('...')
  const [prompt, setPrompt] = useState('')
  const [aiText, setAiText] = useState('')
  const [charts, setCharts] = useState([])
  const [categories, setCategories] = useState([])
  const [accounts, setAccounts] = useState([])
  const [budgets, setBudgets] = useState([])
  const [newCategory, setNewCategory] = useState('')
  const [budgetCategory, setBudgetCategory] = useState('')
  const [budgetAmount, setBudgetAmount] = useState('')
  const [transfer, setTransfer] = useState({from_account_id:'', to_account_id:'', amount:''})

  useEffect(()=>{
    fetch('http://localhost:8000/api/health').then(r=>r.json()).then(j=>setStatus(j.status)).catch(()=>setStatus('offline'))
    fetchCategories()
    fetchAccounts()
    fetchBudgets()
  },[])

  const fetchCategories = async ()=>{
    try{
      const r = await fetch('http://localhost:8000/api/categories')
      const j = await r.json()
      setCategories(j)
    }catch(e){ }
  }

  const fetchAccounts = async ()=>{
    try{
      const r = await fetch('http://localhost:8000/api/accounts')
      const j = await r.json()
      setAccounts(j)
    }catch(e){ }
  }

  const fetchBudgets = async ()=>{
    try{
      const r = await fetch('http://localhost:8000/api/budgets')
      const j = await r.json()
      setBudgets(j)
    }catch(e){ }
  }

  const createCategory = async ()=>{
    if(!newCategory) return
    try{
      const r = await fetch('http://localhost:8000/api/categories',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name:newCategory})})
      const j = await r.json()
      setNewCategory('')
      fetchCategories()
    }catch(e){ alert('error') }
  }

  const createBudget = async ()=>{
    if(!budgetCategory || !budgetAmount) return
    try{
      // we expect year_month format; use current month for demo
      const ym = new Date().toISOString().slice(0,7)
      const payload = {year_month: ym, category_id: parseInt(budgetCategory), amount: parseFloat(budgetAmount)}
      const r = await fetch('http://localhost:8000/api/budgets',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)})
      await r.json()
      setBudgetAmount('')
      fetchBudgets()
    }catch(e){ alert('error') }
  }

  const doTransfer = async ()=>{
    if(!transfer.from_account_id || !transfer.to_account_id || !transfer.amount) return alert('fill fields')
    try{
      const payload = {from_account_id: parseInt(transfer.from_account_id), to_account_id: parseInt(transfer.to_account_id), amount: parseFloat(transfer.amount)}
      const r = await fetch('http://localhost:8000/api/transfer',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)})
      const j = await r.json()
      if(j.status === 'ok'){
        alert('Transfer OK')
        fetchAccounts()
      }else{
        alert(JSON.stringify(j))
      }
    }catch(e){ alert('Transfer error: '+String(e)) }
  }

  const sendAI = async () => {
    setAiText('loading...')
    setCharts([])
    try{
      const res = await fetch('http://localhost:8000/api/ai/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({prompt})})
      const j = await res.json()
      setAiText(j.text || '')
      setCharts(j.charts || [])
    }catch(e){
      setAiText('Error: ' + String(e))
    }
  }

  return (
    <div style={{fontFamily:'Arial', padding:20}}>
      <h1>HomeBuh</h1>
      <p>API: <strong>{status}</strong></p>

      <section style={{marginTop:20}}>
        <h3>Создать отчёт с ИИ</h3>
        <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} rows={4} style={{width:'100%'}} placeholder='Опишите отчёт: например, "Сделай отчет по расходам за 2025-11 по категориям, диаграмма"' />
        <div style={{marginTop:8}}>
          <button onClick={sendAI}>Отправить запрос ИИ</button>
        </div>
        <div style={{marginTop:12}}>
          <strong>Ответ ИИ:</strong>
          <pre style={{whiteSpace:'pre-wrap'}}>{aiText}</pre>
        </div>
        <div style={{marginTop:12}}>
          {charts.map((c, i)=> (
            <div key={i} style={{marginBottom:12}}>
              <div><strong>{c.title || 'chart'}</strong></div>
              <img src={c.url} alt={c.title || 'chart'} style={{maxWidth:'100%', border:'1px solid #ddd'}} />
            </div>
          ))}
        </div>
      </section>

      <section style={{marginTop:20}}>
        <h3>Категории</h3>
        <div>
          <input placeholder="Новая категория" value={newCategory} onChange={e=>setNewCategory(e.target.value)} />
          <button onClick={createCategory}>Добавить</button>
        </div>
        <ul>
          {categories.map(c=> <li key={c.id}>{c.name} (id:{c.id})</li>)}
        </ul>
      </section>

      <section style={{marginTop:20}}>
        <h3>Бюджеты</h3>
        <div>
          <select value={budgetCategory} onChange={e=>setBudgetCategory(e.target.value)}>
            <option value=''>Выберите категорию</option>
            {categories.map(c=> <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          <input placeholder="Сумма" value={budgetAmount} onChange={e=>setBudgetAmount(e.target.value)} />
          <button onClick={createBudget}>Создать бюджет (текущий месяц)</button>
        </div>
        <ul>
          {budgets.map(b => <li key={b.id}>{b.year_month} - cat:{b.category_id} - {b.amount}</li>)}
        </ul>
      </section>

      <section style={{marginTop:20}}>
        <h3>Переводы между счетами</h3>
        <div>
          <select value={transfer.from_account_id} onChange={e=>setTransfer({...transfer, from_account_id:e.target.value})}>
            <option value=''>Счёт-отправитель</option>
            {accounts.map(a=> <option key={a.id} value={a.id}>{a.name} ({a.balance})</option>)}
          </select>
          <select value={transfer.to_account_id} onChange={e=>setTransfer({...transfer, to_account_id:e.target.value})}>
            <option value=''>Счёт-получатель</option>
            {accounts.map(a=> <option key={a.id} value={a.id}>{a.name} ({a.balance})</option>)}
          </select>
          <input placeholder="Сумма" value={transfer.amount} onChange={e=>setTransfer({...transfer, amount:e.target.value})} />
          <button onClick={doTransfer}>Перевести</button>
        </div>
      </section>

      <p style={{marginTop:30}}>Это минимальная PWA-заготовка. Продолжим развивать UI по задаче.</p>
    </div>
  )
}
