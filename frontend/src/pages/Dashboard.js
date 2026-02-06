import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Charts from "../components/Charts";
import FileUpload from "../components/FileUpload";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [insight, setInsight] = useState(null);

  if (!localStorage.getItem("token")) {
    window.location.href = "/login";
  }

  return (
    <div style={{ display: "flex" }}>
      <Sidebar />

      <div style={{ padding: 40, flex: 1 }}>
        <h1>Financial Dashboard</h1>

        <FileUpload setData={setData} setInsight={setInsight} />

        {data && <Charts data={data} />}

        {insight && (
          <div style={{ marginTop: 20 }}>
            <h3>Insight</h3>
            <p>{insight}</p>
          </div>
        )}
      </div>
    </div>
  );
}
