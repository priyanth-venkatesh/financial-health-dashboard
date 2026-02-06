import React from "react";
import API from "../services/api";

function FileUpload({ setData }) {
  const upload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("/upload", formData);
      setData(res.data);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  return (
    <div style={{ marginTop: 20 }}>
      <input type="file" accept=".csv" onChange={upload} />
    </div>
  );
}

export default FileUpload;
