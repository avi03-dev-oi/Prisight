import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="bg-slate-950 text-white min-h-screen">

      {/* Navbar */}
      <nav className="flex justify-between items-center px-8 py-4 border-b border-white/10">
        <h1 className="text-xl font-bold">Prisight</h1>
        <div className="space-x-6 text-sm">
          <Link to="/login" className="text-gray-300">Login</Link>
          <Link to="/register" className="bg-indigo-500 px-4 py-2 rounded-lg">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="px-8 py-20 max-w-6xl mx-auto">
        <h2 className="text-5xl font-bold mb-6">
          Retail Decisions, Powered by AI Forecasting
        </h2>
        <p className="text-gray-400 max-w-3xl">
          Prisight combines ETL pipelines, LSTM-based demand forecasting,
          and intelligent decision engines to optimize pricing, promotions,
          and inventory planning.
        </p>

        <div className="grid md:grid-cols-3 gap-6 mt-10">
          {[
            { title: "Forecast Accuracy", value: "92%" },
            { title: "Revenue Lift", value: "+8–15%" },
            { title: "Stockout Reduction", value: "30%" },
          ].map((item, i) => (
            <div
              key={i}
              className="bg-white/5 border border-white/10 rounded-xl p-6"
            >
              <p className="text-gray-400">{item.title}</p>
              <p className="text-3xl font-bold mt-2">{item.value}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Pipeline */}
      <section className="px-8 py-20 max-w-6xl mx-auto">
        <h3 className="text-3xl font-bold mb-10">From Data to Decisions</h3>
        <div className="grid md:grid-cols-4 gap-6">
          {[
            "Retail Data",
            "ETL & Feature Engineering",
            "LSTM Forecasting",
            "Decision Engines",
          ].map((step, i) => (
            <div
              key={i}
              className="bg-white/5 border border-white/10 rounded-xl p-6 text-center"
            >
              <p className="font-semibold">{step}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Engines */}
      <section className="px-8 py-20 max-w-6xl mx-auto grid md:grid-cols-3 gap-6">
        {[
          {
            title: "Pricing Optimization",
            desc: "Simulates multiple prices and selects the most profitable one.",
          },
          {
            title: "Promotion Strategy",
            desc: "Evaluates discounts, bundles, and flash sales.",
          },
          {
            title: "Inventory Advisor",
            desc: "Predicts stockouts and recommends reorder quantity.",
          },
        ].map((engine, i) => (
          <div
            key={i}
            className="bg-white/5 border border-white/10 rounded-xl p-6"
          >
            <h4 className="text-xl font-semibold mb-2">{engine.title}</h4>
            <p className="text-gray-400">{engine.desc}</p>
          </div>
        ))}
      </section>

      {/* CTA */}
      <section className="py-20 text-center border-t border-white/10">
        <h2 className="text-4xl font-bold mb-6">
          Stop Guessing. Start Forecasting.
        </h2>
        <Link
          to="/register"
          className="bg-indigo-500 px-8 py-4 rounded-lg font-semibold"
        >
          Launch Prisight
        </Link>
      </section>
    </div>
  );
}
