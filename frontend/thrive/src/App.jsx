import React from "react";
import MentorRegister from "./components/MentorRegister";
import MentorSearch from "./components/MentorSearch";

function App() {
  return (
    <div
      style={{
        padding: "20px",
        fontFamily: "Arial",
        backgroundColor: "white",
        color: "black",
        textAlign: "center",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <h1>Mentor Finder</h1>
      <MentorRegister />
      <MentorSearch />
    </div>
  );
}

export default App;
