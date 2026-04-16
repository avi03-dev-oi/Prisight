import { useState } from "react";
import axios from "axios";

export default function EditProductModal({ product, onClose, refresh }) {
  const [form, setForm] = useState({
    name: product.name,
    category: product.category,
    brand: product.brand,
    cost_price: product.cost_price,
    current_price: product.current_price
  });

  const updateProduct = async () => {
    await axios.put(
      `http://localhost:8000/products/update/${product.id}`,
      form
    );
    refresh();
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white w-96 rounded-lg p-6 relative">
        <button
          className="absolute top-3 right-3 text-red-500 text-xl"
          onClick={onClose}
        >
          ✕
        </button>

        <h2 className="text-lg font-semibold mb-4">Edit Product</h2>

        {Object.keys(form).map((key) => (
          <input
            key={key}
            placeholder={key.replace("_", " ")}
            value={form[key]}
            onChange={(e) =>
              setForm({ ...form, [key]: e.target.value })
            }
            className="w-full border p-2 mb-3 rounded"
          />
        ))}

        <button
          onClick={updateProduct}
          className="w-full bg-green-600 text-white py-2 rounded"
        >
          Update Product
        </button>
      </div>
    </div>
  );
}
