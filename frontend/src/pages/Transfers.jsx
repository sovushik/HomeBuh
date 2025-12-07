import React, { useState, useEffect } from 'react'

export default function Transfers() {
  const [accounts, setAccounts] = useState([])
  const [transfer, setTransfer] = useState({ from_account_id: '', to_account_id: '', amount: '' })
  const [message, setMessage] = useState('')

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

  const handleTransfer = async () => {
    if (!transfer.from_account_id || !transfer.to_account_id || !transfer.amount) {
      setMessage('Заполните все поля')
      return
    }
    if (transfer.from_account_id === transfer.to_account_id) {
      setMessage('Счёта отправителя и получателя должны быть разными')
      return
    }
    try {
      const payload = {
        from_account_id: parseInt(transfer.from_account_id),
        to_account_id: parseInt(transfer.to_account_id),
        amount: parseFloat(transfer.amount),
        currency: 'USD'
      }
      const r = await fetch('http://localhost:8000/api/transfer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const j = await r.json()
      if (r.ok && j.status === 'ok') {
        setMessage('✓ Перевод выполнен успешно')
        setTransfer({ from_account_id: '', to_account_id: '', amount: '' })
        fetchAccounts()
      } else {
        setMessage('✗ Ошибка: ' + (j.detail || JSON.stringify(j)))
      }
    } catch (e) {
      setMessage('✗ Ошибка запроса: ' + String(e))
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Переводы между счётами</h2>
      <div style={{ marginBottom: 20, border: '1px solid #ddd', padding: 15, borderRadius: 4 }}>
        <div style={{ marginBottom: 10 }}>
          <label>Счёт-отправитель:</label>
          <select
            value={transfer.from_account_id}
            onChange={e => setTransfer({ ...transfer, from_account_id: e.target.value })}
            style={{ width: '100%', padding: 8, marginTop: 5 }}
          >
            <option value=''>Выберите счёт</option>
            {accounts.map(a => (
              <option key={a.id} value={a.id}>
                {a.name} (баланс: {a.balance.toFixed(2)})
              </option>
            ))}
          </select>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Счёт-получатель:</label>
          <select
            value={transfer.to_account_id}
            onChange={e => setTransfer({ ...transfer, to_account_id: e.target.value })}
            style={{ width: '100%', padding: 8, marginTop: 5 }}
          >
            <option value=''>Выберите счёт</option>
            {accounts.map(a => (
              <option key={a.id} value={a.id}>
                {a.name} (баланс: {a.balance.toFixed(2)})
              </option>
            ))}
          </select>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>Сумма:</label>
          <input
            type="number"
            placeholder="0.00"
            value={transfer.amount}
            onChange={e => setTransfer({ ...transfer, amount: e.target.value })}
            style={{ width: '100%', padding: 8, marginTop: 5 }}
          />
        </div>
        <button
          onClick={handleTransfer}
          style={{ width: '100%', padding: 10, backgroundColor: '#4c78a8', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}
        >
          Выполнить перевод
        </button>
      </div>
      {message && (
        <div style={{ padding: 10, backgroundColor: message.includes('✓') ? '#d4edda' : '#f8d7da', color: message.includes('✓') ? '#155724' : '#721c24', borderRadius: 4 }}>
          {message}
        </div>
      )}
    </div>
  )
}
