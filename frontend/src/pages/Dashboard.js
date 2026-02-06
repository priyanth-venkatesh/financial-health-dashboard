import React, { useState } from "react";
import UploadForm from "../components/UploadForm";

function Dashboard() {
  const [data, setData] = useState(null);

  return (
    <div style={{ padding: 40 }}>
      <h2>Dashboard</h2>

      <UploadForm setData={setData} />

      {data && (
        <div>
          <h3>Financial Insight</h3>
          <p>{data.summary}</p>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
