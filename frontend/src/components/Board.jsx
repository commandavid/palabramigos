import { useMemo } from 'react'

const CELL_COLORS = {
  T: { bg: '#b5403a', label: 'TP', title: 'Triple Palabra' },
  D: { bg: '#d4845a', label: 'DP', title: 'Doble Palabra' },
  '3': { bg: '#3a72b5', label: 'TL', title: 'Triple Letra' },
  '2': { bg: '#6aabce', label: 'DL', title: 'Doble Letra' },
  '1': { bg: '#c8b89a', label: '',  title: '' },
  '..': { bg: '#c8b89a', label: '', title: '' },
}

const CENTER_ROW = 7
const CENTER_COL = 7

export default function Board({ lettersBoard, pointsBoard }) {
  const cells = useMemo(() => {
    if (!lettersBoard || !pointsBoard) return null
    return lettersBoard.map((row, r) =>
      row.map((letter, c) => {
        const bonus = pointsBoard[r][c]
        const isEmpty = letter === '..'
        const isCenter = r === CENTER_ROW && c === CENTER_COL
        const hasLetter = !isEmpty && letter !== '1'

        const style = CELL_COLORS[hasLetter ? '1' : bonus] ?? CELL_COLORS['..']

        return { r, c, letter: hasLetter ? letter : null, bonus, style, isCenter }
      })
    )
  }, [lettersBoard, pointsBoard])

  if (!cells) return null

  return (
  <div className="board-outer">
    <div className="board-scroll-hint">← desliza para ver el tablero →</div>
        <div className="board-wrapper">
          <div className="board-grid">
            {cells.flat().map(({ r, c, letter, bonus, style, isCenter }) => (
              <div
                key={`${r}-${c}`}
                className={`cell ${letter ? 'cell--filled' : ''} ${isCenter && !letter ? 'cell--center' : ''}`}
                style={{ '--cell-bg': style.bg }}
                title={style.title}
              >
                {letter ? (
                  <>
                    <span className="cell-letter">{letter.toUpperCase()}</span>
                    <span className="cell-points">{getLetterPoints(letter)}</span>
                  </>
                ) : isCenter ? (
                  <span className="cell-star">★</span>
                ) : style.label ? (
                  <span className="cell-label">{style.label}</span>
                ) : null}
              </div>
            ))}
        </div>
    </div>
  </div>
  )
}

// Mapa de puntos básico para mostrar en la ficha (puedes ajustarlo a tu aw.points)
const POINTS = {
  a:1, e:1, i:1, o:1, u:1, s:1, n:1, l:1, r:1, t:1,
  d:2, g:2, b:3, c:3, m:3, p:3,
  f:4, h:4, v:4, y:4,
  ch:5, ll:5, j:6, ñ:8, q:8, rr:8,
  x:8, z:10,
}

function getLetterPoints(letter) {
  if (!letter) return ''
  const l = letter.toLowerCase()
  return POINTS[l] ?? ''
}
