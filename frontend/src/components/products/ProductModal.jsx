import { useState } from "react";
import { api } from "../../services/api";

export default function ProductModal({ onClose, refresh, product }) {
  const [form, setForm] = useState(product || {});

  async function submit() {
    if (product) {
      await api(`/products/update/${product.id}`, "PUT", form);
    } else {
      await api("/products/create", "POST", form);
    }
    refresh();
    onClose();
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center">
      <div className="bg-white p-6 rounded w-96">
        <h3 className="font-bold mb-4">
          {product ? "Update Product" : "Add Product"}
        </h3>

        {["code","name","category","brand","cost_price","selling_price"].map(f => (
          <input
            key={f}
            className="w-full mb-2 border p-2 rounded"
            placeholder={f}
            value={form[f] || ""}
            onChange={e => setForm({ ...form, [f]: e.target.value })}
          />
        ))}

        <div className="flex justify-end gap-3">
          <button onClick={onClose}>Cancel</button>
          <button onClick={submit} className="bg-blue-600 text-white px-4 py-1 rounded">
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
