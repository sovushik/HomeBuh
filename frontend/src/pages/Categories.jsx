import React, { useState, useEffect } from 'react'

export default function Categories() {
  const [categories, setCategories] = useState([])
  const [newCategory, setNewCategory] = useState('')
  const [parentId, setParentId] = useState('')

  useEffect(() => {
    fetchCategories()
  }, [])

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
    if (!newCategory) return
    try {
      const payload = { name: newCategory, parent_id: parentId ? parseInt(parentId) : null }
      const r = await fetch('http://localhost:8000/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (r.ok) {
        setNewCategory('')
        setParentId('')
        fetchCategories()
      }
    } catch (e) {
      alert('Ошибка: ' + String(e))
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Категории</h2>
      <div style={{ marginBottom: 20 }}>
        <input
          placeholder="Название категории"
          value={newCategory}
          onChange={e => setNewCategory(e.target.value)}
          style={{ marginRight: 10 }}
        />
        <select
          value={parentId}
          onChange={e => setParentId(e.target.value)}
          style={{ marginRight: 10 }}
        >
          <option value=''>Без родителя</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <button onClick={handleCreate}>Добавить</button>
      </div>
      <ul>
        {categories.map(c => (
          <li key={c.id}>
            {c.name} {c.parent_id ? `(подкат. #${c.parent_id})` : '(основная)'}
          </li>
        ))}
      </ul>
    </div>
  )
}
