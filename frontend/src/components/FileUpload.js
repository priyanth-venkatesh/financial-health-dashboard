import { useState } from "react";
import API from "../services/api";

export default function FileUpload({ setData, setInsight }) {
  const [file, setFile] = useState(null);

  const upload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await API.post("/upload", formData);
    setData(res.data.chart_data);
    setInsight(res.data.summary);
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload & Analyze</button>
    </div>
  );
}
