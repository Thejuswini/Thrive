import React, { useState } from "react";
import axios from "axios";

function MentorSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/search_mentor", { query });
      setResults(res.data.mentors);
    } catch (err) {
      alert("Error searching mentors: " + (err.response?.data?.error || "Unknown error"));
    }
  };

  return (
    <div>
      <h2>Search Mentors</h2>
      <form onSubmit={handleSearch} style={{ display: "grid", gap: "10px", maxWidth: "400px" }}>
        <input type="text" placeholder="Enter expertise or topic" value={query} onChange={(e) => setQuery(e.target.value)} required />
        <button type="submit">Search</button>
      </form>
      <h3>Results:</h3>
      <ul>
        {results.length > 0 ? (
          results.map((mentor, index) => (
            <li key={index}>
              <strong>{mentor.name}</strong> - {mentor.expertise}
              <br />
              📧 {mentor.email} | 📞 {mentor.phone}
              <br />
              🔗 <a href={mentor.calendly} target="_blank" rel="noopener noreferrer">Book Call</a>
              <br />
              📝 {mentor.bio}
            </li>
          ))
        ) : <li>No results found.</li>}
      </ul>
    </div>
  );
}

export default MentorSearch;