export default function Footer({ name, email, github, extra }) {
  return (
    <footer className="app-footer">
      <div className="footer-inner">
        {name && <span className="footer-name">{name}</span>}
        <div className="footer-links">
          {email && (
            <a href={`mailto:${email}`} className="footer-link">
              {email}
            </a>
          )}
          {github && (
            <a
              href={`https://github.com/${github}`}
              className="footer-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              github.com/{github}
            </a>
          )}
          {extra && <span className="footer-link">{extra}</span>}
        </div>
      </div>
    </footer>
  )
}
