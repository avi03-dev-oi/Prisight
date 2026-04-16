import { api } from "../../services/api";

export default function SalesUpload({ productId }) {
  async function upload(e) {
    const fd = new FormData();
    fd.append("file", e.target.files[0]);
    await api("/sales/upload_sales_csv", "POST", fd, true);
    alert("Uploaded");
  }

  return (
    <input type="file" accept=".csv" onChange={upload} />
  );
}
