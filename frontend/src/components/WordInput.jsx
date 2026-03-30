import { useState, useRef, useEffect } from 'react'

const MAX_WORDS = 8

export default function WordInput({ onSubmit, loading }) {
  const [words, setWords] = useState([])
  const [current, setCurrent] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    if (!loading) inputRef.current?.focus()
  }, [loading])

  function handleKeyDown(e) {
    if (e.key === 'Enter') addWord()
  }

  function addWord() {
    const trimmed = current.trim()
    if (!trimmed || words.length >= MAX_WORDS) return
    setWords(prev => [...prev, trimmed])
    setCurrent('')
  }

  function handleFocus(e) {
      setTimeout(() => {
        e.target.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 300)
  }

  function removeWord(index) {
    setWords(prev => prev.filter((_, i) => i !== index))
  }

  function handleSubmit() {
    if (words.length === 0) return
    onSubmit(words)
  }

  const isFull = words.length >= MAX_WORDS

  return (
    <div className="word-input-panel">
      <h2 className="panel-title">Palabras</h2>
      <p className="panel-subtitle">
        Introduce hasta {MAX_WORDS} palabras. Pulsa <kbd>Enter</kbd> para añadir.
      </p>

      <div className="word-chips">
        {words.map((w, i) => (
          <span key={i} className="chip">
            {w}
            <button
              className="chip-remove"
              onClick={() => removeWord(i)}
              disabled={loading}
              aria-label={`Eliminar ${w}`}
            >
              ×
            </button>
          </span>
        ))}
        {!isFull && (
          <span className="chip-counter">{words.length}/{MAX_WORDS}</span>
        )}
      </div>

      <div className="input-row">
        <input
          ref={inputRef}
          className="word-field"
          onFocus={handleFocus}
          type="text"
          value={current}
          onChange={e => setCurrent(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isFull ? 'Límite alcanzado' : 'Escribe una palabra…'}
          disabled={isFull || loading}
          maxLength={30}
        />
        <button
          className="btn btn--add"
          onClick={addWord}
          disabled={!current.trim() || isFull || loading}
        >
          +
        </button>
      </div>

      <button
        className="btn btn--play"
        onClick={handleSubmit}
        disabled={words.length === 0 || loading}
      >
        {loading ? (
          <span className="spinner" />
        ) : (
          'Calcular'
        )}
      </button>
    </div>
  )
}
