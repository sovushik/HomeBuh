import React, { useState, useEffect } from 'react'
import Categories from './pages/Categories'
import Budgets from './pages/Budgets'
import Accounts from './pages/Accounts'
import Transfers from './pages/Transfers'
import Reports from './pages/Reports'

export default function App() {
  const [status, setStatus] = useState('...')
  const [currentPage, setCurrentPage] = useState('dashboard')

  useEffect(() => {
    fetch('http://localhost:8000/api/health')
      .then(r => r.json())
      .then(j => setStatus(j.status))
      .catch(() => setStatus('offline'))
  }, [])

  const navStyle = {
    display: 'flex',
    gap: 10,
    borderBottom: '2px solid #ddd',
    marginBottom: 20,
    paddingBottom: 10
  }

  const navButtonStyle = (active) => ({
    padding: '8px 16px',
    border: 'none',
    backgroundColor: active ? '#4c78a8' : '#f0f0f0',
    color: active ? '#fff' : '#000',
    cursor: 'pointer',
    borderRadius: 4,
    fontWeight: active ? 'bold' : 'normal'
  })

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px' }}>
      <header style={{ marginBottom: 20 }}>
        <h1>HomeBuh — Домашняя бухгалтерия</h1>
        <p>API статус: <strong>{status === 'ok' ? '✓ ' : '✗ '}{status}</strong></p>
      </header>

      <nav style={navStyle}>
        <button style={navButtonStyle(currentPage === 'dashboard')} onClick={() => setCurrentPage('dashboard')}>
          Главная
        </button>
        <button style={navButtonStyle(currentPage === 'categories')} onClick={() => setCurrentPage('categories')}>
          Категории
        </button>
        <button style={navButtonStyle(currentPage === 'budgets')} onClick={() => setCurrentPage('budgets')}>
          Бюджеты
        </button>
        <button style={navButtonStyle(currentPage === 'accounts')} onClick={() => setCurrentPage('accounts')}>
          Счёта
        </button>
        <button style={navButtonStyle(currentPage === 'transfers')} onClick={() => setCurrentPage('transfers')}>
          Переводы
        </button>
        <button style={navButtonStyle(currentPage === 'reports')} onClick={() => setCurrentPage('reports')}>
          AI-отчёты
        </button>
      </nav>

      <main>
        {currentPage === 'dashboard' && (
          <div style={{ padding: 20 }}>
            <h2>Добро пожаловать в HomeBuh</h2>
            <p>Используйте меню выше для навигации по разделам приложения:</p>
            <ul>
              <li><strong>Категории</strong> — управление категориями и подкатегориями расходов/доходов</li>
              <li><strong>Бюджеты</strong> — создание и отслеживание бюджетов по месяцам и категориям</li>
              <li><strong>Счёта</strong> — управление счётами (карта, банк, вклад и т.д.)</li>
              <li><strong>Переводы</strong> — перекидывание денег между счётами</li>
              <li><strong>AI-отчёты</strong> — создание отчётов по запросу с помощью ИИ</li>
            </ul>
            <p style={{ marginTop: 20, color: '#666 ' }}>Версия: 0.1.0 | PWA-приложение</p>
          </div>
        )}
        {currentPage === 'categories' && <Categories />}
        {currentPage === 'budgets' && <Budgets />}
        {currentPage === 'accounts' && <Accounts />}
        {currentPage === 'transfers' && <Transfers />}
        {currentPage === 'reports' && <Reports />}
      </main>
    </div>
  )
}
