import React, { useState } from 'react'

export default function Reports() {
  const [prompt, setPrompt] = useState('')
  const [aiText, setAiText] = useState('')
  const [charts, setCharts] = useState([])
  const [loading, setLoading] = useState(false)

  const sendAI = async () => {
    if (!prompt.trim()) return
    setLoading(true)
    setAiText('')
    setCharts([])
    try {
      const res = await fetch('http://localhost:8000/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      })
      const j = await res.json()
      setAiText(j.text || '')
      setCharts(j.charts || [])
    } catch (e) {
      setAiText('✗ Ошибка: ' + String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>AI-отчёты</h2>
      <div style={{ marginBottom: 20 }}>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          rows={4}
          style={{ width: '100%', padding: 10, fontFamily: 'monospace' }}
          placeholder='Опишите отчёт, который хотите получить. Пример: "Сделай отчет по расходам за 2025-12 по категориям, построй круговую диаграмму"'
          disabled={loading}
        />
        <div style={{ marginTop: 10 }}>
          <button
            onClick={sendAI}
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: loading ? '#ccc' : '#4c78a8',
              color: '#fff',
              border: 'none',
              borderRadius: 4,
              cursor: loading ? 'default' : 'pointer'
            }}
          >
            {loading ? 'Генерируем...' : 'Отправить запрос ИИ'}
          </button>
        </div>
      </div>

      {aiText && (
        <div style={{ marginBottom: 20, padding: 15, border: '1px solid #ddd', borderRadius: 4, backgroundColor: '#f9f9f9' }}>
          <h3>Ответ ИИ</h3>
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word', fontFamily: 'monospace' }}>
            {aiText}
          </pre>
        </div>
      )}

      {charts.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h3>Сгенерированные графики</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 20 }}>
            {charts.map((c, i) => (
              <div key={i} style={{ padding: 15, border: '1px solid #ddd', borderRadius: 4 }}>
                <h4>{c.title || `График ${i + 1}`}</h4>
                <img
                  src={c.url}
                  alt={c.title || 'chart'}
                  style={{ maxWidth: '100%', border: '1px solid #eee', borderRadius: 4 }}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
