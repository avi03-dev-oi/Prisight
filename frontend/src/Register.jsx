import React from "react";
import { Link } from "react-router-dom";

export default function Register() {
  const [formData, setFormData] = React.useState({
    name: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: ""
  });
  const [error, setError] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError(""); // Clear error on input change
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check if passwords match
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    // Prepare data to send (matching backend field names)
    const registerData = {
      name: formData.name,
      email: formData.email,
      phone_number: formData.phone,  // Changed from 'phone' to 'phone_number'
      password: formData.password
    };

    setLoading(true);
    
    try {
      const response = await fetch("http://localhost:8000/users/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(registerData),
      });

      const data = await response.json();

      if (response.ok) {
        // Registration successful
        alert("Registration successful!");
        // Redirect to login page
        window.location.href = "/login";
      } else {
        // Handle error from backend
        setError(data.detail || "Registration failed. Please try again.");
      }
    } catch (err) {
      setError("Network error. Please check your connection.");
      console.error("Registration error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-slate-900 to-indigo-900">
      
      <div className="w-full max-w-md bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8 shadow-2xl text-white">
        
        <h2 className="text-3xl font-bold text-center mb-2">
          Create Account
        </h2>
        <p className="text-center text-sm text-gray-300 mb-6">
          Start making data-driven decisions
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Name */}
          <div>
            <label className="text-sm">Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="John Doe"
              required
              className="w-full mt-1 px-4 py-2 rounded-lg bg-white/20 border border-white/30 focus:outline-none focus:ring-2 focus:ring-indigo-400 placeholder-gray-300"
            />
          </div>

          {/* Email */}
          <div>
            <label className="text-sm">Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="admin@store.com"
              required
              className="w-full mt-1 px-4 py-2 rounded-lg bg-white/20 border border-white/30 focus:outline-none focus:ring-2 focus:ring-indigo-400 placeholder-gray-300"
            />
          </div>

          {/* Phone */}
          <div>
            <label className="text-sm">Phone</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+1234567890"
              required
              className="w-full mt-1 px-4 py-2 rounded-lg bg-white/20 border border-white/30 focus:outline-none focus:ring-2 focus:ring-indigo-400 placeholder-gray-300"
            />
          </div>

          {/* Password */}
          <div>
            <label className="text-sm">Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Create password"
              required
              minLength={6}
              className="w-full mt-1 px-4 py-2 rounded-lg bg-white/20 border border-white/30 focus:outline-none focus:ring-2 focus:ring-indigo-400 placeholder-gray-300"
            />
          </div>

          {/* Confirm Password */}
          <div>
            <label className="text-sm">Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm password"
              required
              minLength={6}
              className="w-full mt-1 px-4 py-2 rounded-lg bg-white/20 border border-white/30 focus:outline-none focus:ring-2 focus:ring-indigo-400 placeholder-gray-300"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-500 hover:bg-indigo-600 transition py-2 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>

        <p className="text-sm text-center mt-4 text-gray-300">
          Already have an account?{" "}
          <Link to="/login" className="text-indigo-400 font-medium">
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}