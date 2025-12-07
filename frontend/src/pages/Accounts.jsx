import React, { useState, useEffect } from 'react'

export default function Accounts() {
  const [accounts, setAccounts] = useState([])
  const [newName, setNewName] = useState('')
  const [newBalance, setNewBalance] = useState('')

  useEffect(() => {
    fetchAccounts()
  }, [])

  const fetchAccounts = async () => {
    try {
      const r = await fetch('http://localhost:8000/api/accounts')
      const j = await r.json()
      setAccounts(j)
    } catch (e) {
      console.error('Failed to fetch accounts:', e)
    }
  }

  const handleCreate = async () => {
    if (!newName || !newBalance) return
    try {
      const payload = { name: newName, balance: parseFloat(newBalance), currency: 'USD' }
      const r = await fetch('http://localhost:8000/api/accounts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (r.ok) {
        setNewName('')
        setNewBalance('')
        fetchAccounts()
      }
    } catch (e) {
      alert('Ошибка: ' + String(e))
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Счёта</h2>
      <div style={{ marginBottom: 20 }}>
        <input
          placeholder="Название счёта"
          value={newName}
          onChange={e => setNewName(e.target.value)}
          style={{ marginRight: 10 }}
        />
        <input
          placeholder="Начальный баланс"
          value={newBalance}
          onChange={e => setNewBalance(e.target.value)}
          type="number"
          style={{ marginRight: 10 }}
        />
        <button onClick={handleCreate}>Создать</button>
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #ddd' }}>
            <th style={{ padding: 8, textAlign: 'left' }}>ID</th>
            <th style={{ padding: 8, textAlign: 'left' }}>Название</th>
            <th style={{ padding: 8, textAlign: 'right' }}>Баланс</th>
            <th style={{ padding: 8, textAlign: 'left' }}>Валюта</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map(a => (
            <tr key={a.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: 8 }}>{a.id}</td>
              <td style={{ padding: 8 }}>{a.name}</td>
              <td style={{ padding: 8, textAlign: 'right' }}>{a.balance.toFixed(2)}</td>
              <td style={{ padding: 8 }}>{a.currency}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
