import { useState, useEffect } from 'react'
import Board from './components/Board'
import WordInput from './components/WordInput'
import './App.css'

const API = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export default function App() {
  const [lettersBoard, setLettersBoard] = useState(null)
  const [pointsBoard, setPointsBoard] = useState(null)
  const [totalPoints, setTotalPoints] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [ready, setReady] = useState(false)

  // Cargar el tablero vacío al montar
  useEffect(() => {
    fetch(`${API}/empty-board`)
      .then(r => r.json())
      .then(data => {
        setLettersBoard(data.letters_board)
        setPointsBoard(data.points_board)
        setReady(true)
      })
      .catch(() => setError('No se puede conectar con el servidor. ¿Está arrancado el backend?'))
  }, [])

  async function handleSubmit(words) {
    setLoading(true)
    setError(null)
    setTotalPoints(null)

    try {
      const res = await fetch(`${API}/play`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ words }),
      })

      const data = await res.json()

      if (!res.ok) {
        setError(data.detail ?? 'Error desconocido en el servidor.')
        return
      }

      setLettersBoard(data.letters_board)
      setPointsBoard(data.points_board)
      setTotalPoints(data.total_points)
    } catch {
      setError('Error de red al contactar con el servidor.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <h1 className="app-title">
            <span className="title-tile">S</span>
            <span className="title-tile">C</span>
            <span className="title-tile">R</span>
            <span className="title-tile">A</span>
            <span className="title-tile">B</span>
            <span className="title-tile">B</span>
            <span className="title-tile">L</span>
            <span className="title-tile">E</span>
          </h1>
          <p className="app-subtitle">Solver — Encuentra la mejor jugada</p>
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            ⚠ {error}
          </div>
        )}

        <div className="layout">
          <section className="layout__board">
            {ready ? (
              <Board lettersBoard={lettersBoard} pointsBoard={pointsBoard} />
            ) : (
              <div className="board-placeholder">
                {error ? '—' : 'Conectando…'}
              </div>
            )}
          </section>

          <aside className="layout__panel">
            <WordInput onSubmit={handleSubmit} loading={loading} />

            {totalPoints !== null && (
              <div className="score-card">
                <span className="score-label">Puntuación</span>
                <span className="score-value">{totalPoints}</span>
                <span className="score-unit">pts</span>
              </div>
            )}

            <div className="legend">
              <h3 className="legend-title">Leyenda</h3>
              <div className="legend-grid">
                <span className="legend-swatch" style={{ background: '#b5403a' }} />
                <span>Triple Palabra</span>
                <span className="legend-swatch" style={{ background: '#d4845a' }} />
                <span>Doble Palabra</span>
                <span className="legend-swatch" style={{ background: '#3a72b5' }} />
                <span>Triple Letra</span>
                <span className="legend-swatch" style={{ background: '#6aabce' }} />
                <span>Doble Letra</span>
              </div>
            </div>
          </aside>
        </div>
      </main>
    </div>
  )
}
