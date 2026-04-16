import { useState } from "react";
import axios from "axios";

export default function SalesUploadModal({ onClose }) {
  const [file, setFile] = useState(null);

  const upload = async () => {
    if (!file) return alert("Select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

    await axios.post(
      "http://localhost:8000/sales/upload_sales_csv",
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    alert("Sales uploaded successfully");
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded w-96 relative">
        <button onClick={onClose} className="absolute top-2 right-3 text-red-500">
          ✕
        </button>

        <h2 className="text-lg font-semibold mb-4">Upload Sales CSV</h2>

        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          className="mb-4"
        />

        <button
          onClick={upload}
          className="w-full bg-blue-600 text-white py-2 rounded"
        >
          Upload
        </button>
      </div>
    </div>
  );
}
