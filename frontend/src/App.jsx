import { useState, useEffect, useRef } from 'react'
import html2canvas from 'html2canvas'
import Board from './components/Board'
import WordInput from './components/WordInput'
import Footer from './components/Footer'
import './App.css'

const API = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export default function App() {
  const [lettersBoard, setLettersBoard] = useState(null)
  const [pointsBoard, setPointsBoard] = useState(null)
  const [totalPoints, setTotalPoints] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [ready, setReady] = useState(false)
  const [downloading, setDownloading] = useState(false)

  const boardRef = useRef(null)

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

  async function handleDownload() {
    if (!boardRef.current) return
    setDownloading(true)

    try {
      const canvas = await html2canvas(boardRef.current, {
        backgroundColor: '#6b4c2a',
        scale: 2,
        useCORS: true,
        logging: false,
      })

      const link = document.createElement('a')
      link.download = `palabramigos-${Date.now()}.png`
      link.href = canvas.toDataURL('image/png')
      link.click()
    } catch {
      setError('No se pudo generar la imagen. Inténtalo de nuevo.')
    } finally {
      setDownloading(false)
    }
  }

  const boardReady = totalPoints !== null

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <h1 className="app-title">
            <span className="title-tile">P</span>
            <span className="title-tile">A</span>
            <span className="title-tile">L</span>
            <span className="title-tile">A</span>
            <span className="title-tile">B</span>
            <span className="title-tile">R</span>
            <span className="title-tile">A</span>
            <span className="title-tile">M</span>
            <span className="title-tile">I</span>
            <span className="title-tile">G</span>
            <span className="title-tile">O</span>
            <span className="title-tile">S</span>
          </h1>
          <p className="app-subtitle">Encuentra la colocación óptima</p>
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
              <div ref={boardRef}>
                <Board lettersBoard={lettersBoard} pointsBoard={pointsBoard} />
              </div>
            ) : (
              <div className="board-placeholder">
                {error ? '—' : 'Conectando…'}
              </div>
            )}
          </section>

          <aside className="layout__panel">
            <WordInput onSubmit={handleSubmit} loading={loading} />

            {boardReady && (
              <div className="score-card">
                <span className="score-label">Puntuación</span>
                <span className="score-value">{totalPoints}</span>
                <span className="score-unit">pts</span>
              </div>
            )}

            {boardReady && (
              <div className="download-card">
                <div className="download-card__text">
                  <span className="download-title">Guardar tablero</span>
                  <span className="download-subtitle">
                    Descarga el resultado como imagen PNG
                  </span>
                </div>
                <button
                  className="btn btn--download"
                  onClick={handleDownload}
                  disabled={downloading}
                >
                  {downloading ? <span className="spinner" /> : <>↓ Descargar</>}
                </button>
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

      {/* Rellena con tus datos */}
      <Footer
        name="David Sanz"
        email="davidsanz@gmail.com"
        github="commandavid"
      />
    </div>
  )
}
