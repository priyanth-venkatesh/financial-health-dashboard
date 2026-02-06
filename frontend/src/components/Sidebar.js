export default function Sidebar() {
    return (
      <div
        style={{
          width: 220,
          background: "#020617",
          color: "white",
          minHeight: "100vh",
          padding: 20,
        }}
      >
        <h2>💰 FinanceAI</h2>
        <hr />
        <p>Dashboard</p>
        <p>Upload</p>
        <p
          style={{ cursor: "pointer", marginTop: 40 }}
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/login";
          }}
        >
          Logout
        </p>
      </div>
    );
  }
  