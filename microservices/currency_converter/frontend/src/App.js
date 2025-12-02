import { useState } from "react";
import "./App.css";

const CURRENCIES = [
  { code: "USD", name: "US Dollar" },
  { code: "CAD", name: "Canadian Dollar" },
  { code: "EUR", name: "Euro" },
  { code: "GBP", name: "British Pound" },
  { code: "JPY", name: "Japanese Yen" },
  { code: "AUD", name: "Australian Dollar" },
  { code: "NZD", name: "New Zealand Dollar" },
  { code: "INR", name: "Indian Rupee" },
  { code: "CHF", name: "Swiss Franc" },
  { code: "CNY", name: "Chinese Yuan" },
  { code: "MXN", name: "Mexican Peso" },
];

function App() {
  const [fromCurrency, setFromCurrency] = useState("USD");
  const [toCurrency, setToCurrency] = useState("CAD");
  const [amount, setAmount] = useState("100");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSwap = () => {
    setFromCurrency(toCurrency);
    setToCurrency(fromCurrency);
    setResult(null);
    setError(null);
  };

  const handleConvert = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!amount || Number.isNaN(Number(amount))) {
      setError("Please enter a valid amount.");
      return;
    }

    setLoading(true);
    try {
      const params = new URLSearchParams({
        from: fromCurrency,
        to: toCurrency,
        amount: amount,
      });

      const res = await fetch(`/convert?${params.toString()}`);
      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Conversion failed");
      } else {
        setResult(data);
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-root">
      <div className="app-card">
        <header className="app-header">
          <h1>Currency Converter</h1>
          <p>Convert between currencies using live exchange rates.</p>
        </header>

        <form className="app-form" onSubmit={handleConvert}>
          <div className="form-row">
            <label className="form-label">Amount</label>
            <input
              className="form-input"
              type="number"
              min="0"
              step="0.01"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="Enter amount"
            />
          </div>

          <div className="form-row form-row--split">
            <div className="form-col">
              <label className="form-label">From</label>
              <select
                className="form-select"
                value={fromCurrency}
                onChange={(e) => setFromCurrency(e.target.value)}
              >
                {CURRENCIES.map((c) => (
                  <option key={c.code} value={c.code}>
                    {c.code} — {c.name}
                  </option>
                ))}
              </select>
            </div>

            {/* SIMPLE swap button */}
            <button
              type="button"
              className="swap-button"
              onClick={handleSwap}
            >
              ↔
            </button>

            <div className="form-col">
              <label className="form-label">To</label>
              <select
                className="form-select"
                value={toCurrency}
                onChange={(e) => setToCurrency(e.target.value)}
              >
                {CURRENCIES.map((c) => (
                  <option key={c.code} value={c.code}>
                    {c.code} — {c.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            type="submit"
            className="primary-button"
            disabled={loading}
          >
            {loading ? "Converting..." : "Convert"}
          </button>
        </form>

        {error && (
          <div className="alert alert--error">
            ⚠️ {error}
          </div>
        )}

        {result && (
          <div className="result-card">
            <div className="result-main">
              <span className="result-label">
                {result.amount} {result.from}
              </span>
              <span className="result-value">
                {result.converted_amount} {result.to}
              </span>
            </div>
            {result.rate && (
              <div className="result-meta">
                <span>Rate:</span>
                <span>
                  1 {result.from} = {result.rate} {result.to}
                </span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
