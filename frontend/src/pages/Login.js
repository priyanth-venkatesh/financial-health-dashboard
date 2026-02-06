import React, { useState } from "react";
import API from "../services/api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const res = await API.post("/login", { email, password });

      // store token
      localStorage.setItem("token", res.data.token);

      // redirect
      window.location.href = "/dashboard";
    } catch (err) {
      console.error(err);
      alert("Invalid email or password");
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Financial Health Dashboard Login</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br /><br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /><br />

      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;
