import React from "react";

export function IconButton({ icon, onClick }) {
  return (
    <button onClick={onClick} className="icon-btn">
      {icon}
    </button>
  );
}

export function SearchForm() {
  return (
    <form>
      <input type="text" placeholder="Search..." className="outline-none" />
      <button type="submit">Go</button>
    </form>
  );
}

export function Card({ title, onClick }) {
  return (
    <div onClick={onClick} style={{ transition: "all 0.3s ease" }}>
      <h3>{title}</h3>
      <p>Loading...</p>
      <p>He said "hello" to the team.</p>
      <img src="/photo.jpg" />
    </div>
  );
}
