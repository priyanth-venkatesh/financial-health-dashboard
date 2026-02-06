import React from "react";
import API from "../services/api";

function UploadForm({ setData }) {
  const upload = async (e) => {
    const file = e.target.files[0];

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("/upload", formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      setData(res.data);
    } catch (err) {
      alert("Upload failed");
    }
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={upload} />
    </div>
  );
}

export default UploadForm;
