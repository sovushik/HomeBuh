import React, { useState, useEffect } from 'react'

export default function Budgets() {
  const [budgets, setBudgets] = useState([])
  const [categories, setCategories] = useState([])
  const [budgetCategory, setBudgetCategory] = useState('')
  const [budgetAmount, setBudgetAmount] = useState('')

  useEffect(() => {
    fetchBudgets()
    fetchCategories()
  }, [])

  const fetchBudgets = async () => {
    try {
      const r = await fetch('http://localhost:8000/api/budgets')
      const j = await r.json()
      setBudgets(j)
    } catch (e) {
      console.error('Failed to fetch budgets:', e)
    }
  }

  const fetchCategories = async () => {
    try {
      const r = await fetch('http://localhost:8000/api/categories')
      const j = await r.json()
      setCategories(j)
    } catch (e) {
      console.error('Failed to fetch categories:', e)
    }
  }

  const handleCreate = async () => {
    if (!budgetCategory || !budgetAmount) return
    try {
      const ym = new Date().toISOString().slice(0, 7)
      const payload = { year_month: ym, category_id: parseInt(budgetCategory), amount: parseFloat(budgetAmount) }
      const r = await fetch('http://localhost:8000/api/budgets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (r.ok) {
        setBudgetAmount('')
        setBudgetCategory('')
        fetchBudgets()
      }
    } catch (e) {
      alert('Ошибка: ' + String(e))
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Бюджеты</h2>
      <div style={{ marginBottom: 20 }}>
        <select
          value={budgetCategory}
          onChange={e => setBudgetCategory(e.target.value)}
          style={{ marginRight: 10 }}
        >
          <option value=''>Выберите категорию</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <input
          placeholder="Сумма"
          value={budgetAmount}
          onChange={e => setBudgetAmount(e.target.value)}
          type="number"
          style={{ marginRight: 10 }}
        />
        <button onClick={handleCreate}>Создать (текущий месяц)</button>
      </div>
      <ul>
        {budgets.map(b => (
          <li key={b.id}>
            {b.year_month} — Категория #{b.category_id} — {b.amount} {b.currency || 'USD'}
          </li>
        ))}
      </ul>
    </div>
  )
}
