import { useEffect, useState } from "react";
import axios from "axios";

export default function ProductTable({ onClose, onSelectProduct }) {
  const [products, setProducts] = useState([]);

  const fetchProducts = () => {
    axios
      .get("http://localhost:8000/products/all")
      .then((res) => setProducts(res.data.detail || []))
      .catch(() => setProducts([]));
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const deleteProduct = async (id) => {
    if (!confirm("Delete this product?")) return;

    await axios.delete(`http://localhost:8000/products/delete/${id}`);
    fetchProducts();
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white w-4/5 rounded-lg p-6 relative">
        <button
          className="absolute top-3 right-3 text-red-500 text-xl"
          onClick={onClose}
        >
          ✕
        </button>

        <h2 className="text-xl font-semibold mb-4">Products</h2>

        <table className="w-full border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border p-2">ID</th>
              <th className="border p-2">Name</th>
              <th className="border p-2">Category</th>
              <th className="border p-2">Brand</th>
              <th className="border p-2">Cost</th>
              <th className="border p-2">Price</th>
              <th className="border p-2">Actions</th>
            </tr>
          </thead>

          <tbody>
            {products.length === 0 ? (
              <tr>
                <td colSpan="7" className="text-center p-4">
                  No products found
                </td>
              </tr>
            ) : (
              products.map((p) => (
                <tr
                  key={p.id}
                  className="hover:bg-blue-50 cursor-pointer"
                >
                  <td
                    className="border p-2"
                    onClick={() => onSelectProduct(p.id)}
                  >
                    {p.id}
                  </td>
                  <td
                    className="border p-2"
                    onClick={() => onSelectProduct(p.id)}
                  >
                    {p.name}
                  </td>
                  <td className="border p-2">{p.category}</td>
                  <td className="border p-2">{p.brand}</td>
                  <td className="border p-2">₹{p.cost_price}</td>
                  <td className="border p-2">₹{p.current_price}</td>
                  <td className="border p-2 text-center">
                    <button
                      onClick={() => deleteProduct(p.id)}
                      className="text-red-600 text-sm"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
