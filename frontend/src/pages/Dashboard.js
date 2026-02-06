import React, { useState } from "react";
import FileUpload from "../components/FileUpload";

function Dashboard() {
  const [data, setData] = useState(null);

  return (
    <div style={{ padding: 40 }}>
      <h2>Dashboard</h2>

      <FileUpload setData={setData} />

      {data && (
        <div style={{ marginTop: 20 }}>
          <h3>Financial Insight</h3>
          <p>{data.summary}</p>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
