import { useState } from "react"

function App() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const search = async () => {
    // YOUR CODE HERE:
    // 1. set loading to true, clear error
    setLoading(true)
    setError("")
    // 2. fetch from http://127.0.0.1:5000/recommend?title=<query>
      try {
        const response = await fetch(`http://127.0.0.1:5000/recommend?title=${encodeURIComponent(query)}`)
        const data = await response.json()
        if (!response.ok) {
          setError(data.error || 'Something went wrong.')
          setResults([])
        } else {
                setResults(data)
          }
            
      } catch (err) {
        setError("Failed to fetch recommendations.")
      } finally {
        setLoading(false)
      }


  }

  return (
    <div style={{ maxWidth: "700px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>🎬 CineMatch</h1>

      {/* Search bar */}
      <div style={{ display: "flex", gap: "8px", marginBottom: "24px" }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === "Enter" && search()}
          placeholder="Enter a movie title..."
          style={{ flex: 1, padding: "10px", fontSize: "16px" }}
        />
        <button onClick={search} style={{ padding: "10px 20px", fontSize: "16px" }}>
          Search
        </button>
      </div>

      {/* States */}
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Results table */}
      {results.length > 0 && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #ccc", textAlign: "left" }}>
              <th style={{ padding: "8px" }}>Title</th>
              <th style={{ padding: "8px" }}>IMDb</th>
              <th style={{ padding: "8px" }}>RT Score</th>
            </tr>
          </thead>
          <tbody>
            {results.map((movie, idx) => (
              <tr key={idx} style={{ borderBottom: "1px solid #eee" }}>
                <td style={{ padding: "8px" }}>{movie.title}</td>
                <td style={{ padding: "8px" }}>{movie.imdb_rating}</td>
                <td style={{ padding: "8px" }}>{movie.rotten_tomatoes_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default App