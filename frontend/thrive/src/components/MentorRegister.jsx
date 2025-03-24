import React, { useState } from "react";
import axios from "axios";

function MentorRegister() {
  const [mentor, setMentor] = useState({
    name: "",
    email: "",
    phone: "",
    calendly: "",
    expertise: "",
    experience: "",
    age: "",
    bio: "",
  });

  const handleChange = (e) => {
    setMentor({ ...mentor, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/register_mentor", mentor, {
        headers: {
          "Content-Type": "application/json"
        },
        withCredentials: true,
      });
      alert(res.data.message);
      setMentor({ name: "", email: "", phone: "", calendly: "", expertise: "", experience: "", age: "", bio: "" });
    } catch (err) {
      alert("Error registering mentor: " + (err.response?.data?.error || "Unknown error"));
    }
  };

  return (
    <div>
      <h2>Register a Mentor</h2>
      <form onSubmit={handleRegister} style={{ display: "grid", gap: "10px", maxWidth: "400px" }}>
        <input type="text" name="name" placeholder="Name" value={mentor.name} onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" value={mentor.email} onChange={handleChange} required />
        <input type="text" name="phone" placeholder="Phone" value={mentor.phone} onChange={handleChange} required />
        <input type="text" name="calendly" placeholder="Calendly Link" value={mentor.calendly} onChange={handleChange} required />
        <input type="text" name="expertise" placeholder="Expertise" value={mentor.expertise} onChange={handleChange} required />
        <input type="number" name="experience" placeholder="Years of Experience" value={mentor.experience} onChange={handleChange} required />
        <input type="number" name="age" placeholder="Age" value={mentor.age} onChange={handleChange} required />
        <textarea name="bio" placeholder="Short Bio" value={mentor.bio} onChange={handleChange} required />
        <button type="submit">Register Mentor</button>
      </form>
    </div>
  );
}

export default MentorRegister;