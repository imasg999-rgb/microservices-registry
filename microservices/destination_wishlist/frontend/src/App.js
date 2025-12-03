// src/App.js
import { useEffect, useState } from "react";
import "./App.css";

const STORAGE_KEY = "travel_wishlist";

function App() {
  const [destinations, setDestinations] = useState([]);
  const [newName, setNewName] = useState("");
  const [newCountry, setNewCountry] = useState("");
  const [selectedDestination, setSelectedDestination] = useState(null);
  const [description, setDescription] = useState("");
  const [loadingDescription, setLoadingDescription] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed)) setDestinations(parsed);
      } catch { }
    }
  }, []);

  const saveWishlist = (list) => {
    setDestinations(list);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  };

  const handleAdd = (e) => {
    e.preventDefault();
    setError("");

    const name = newName.trim();
    const country = newCountry.trim();

    if (!name) {
      setError("Destination name is required.");
      return;
    }

    const newDestination = {
      id: Date.now(),
      name,
      country: country || null,
      imageUrl: null,
    };

    const updated = [...destinations, newDestination];
    saveWishlist(updated);

    setNewName("");
    setNewCountry("");
  };

  const handleRemove = (id) => {
    const updated = destinations.filter((d) => d.id !== id);
    saveWishlist(updated);

    if (selectedDestination?.id === id) {
      setSelectedDestination(null);
      setDescription("");
    }
  };

  const handleSelect = (destination) => {
    setSelectedDestination(destination);
    setDescription("");
    setError("");

    //fetch both description + image when Details is clicked
    fetchDescription(destination);
  };

  const fetchDescription = async (destination) => {
    const { id, name, country } = destination;

    setLoadingDescription(true);
    setError("");

    try {
      const params = new URLSearchParams({ name });
      if (country) params.append("country", country);

      const res = await fetch(`/api/destination-description?${params.toString()}`);

      if (!res.ok) {
        let msg = "Failed to load description.";
        try {
          const body = await res.json();
          if (body.error) msg = body.error;
        } catch {
          // ignore JSON parse error
        }
        throw new Error(msg);
      }

      const data = await res.json();

      setDescription(data.description || "");

      if (data.image_url) {
        setSelectedDestination((prev) =>
          prev && prev.id === id ? { ...prev, imageUrl: data.image_url } : prev
        );

        const updatedList = destinations.map((d) =>
          d.id === id ? { ...d, imageUrl: data.image_url } : d
        );
        saveWishlist(updatedList);
      }
    } catch (err) {
      console.error(err);
      setError("Could not load description. Please try again.");
    } finally {
      setLoadingDescription(false);
    }
  };

  return (
    <div className="app">
      <h1 className="title">Travel Wishlist</h1>

      <form className="form" onSubmit={handleAdd}>
        <div className="field-row">
          <div className="field">
            <label>Destination name</label>
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="e.g. Paris"
            />
          </div>
          <div className="field">
            <label>Country (optional)</label>
            <input
              type="text"
              value={newCountry}
              onChange={(e) => setNewCountry(e.target.value)}
              placeholder="e.g. France"
            />
          </div>
        </div>
        <button className="btn-add">Add to wishlist</button>
      </form>

      {error && <div className="error-banner">{error}</div>}

      <div className="layout">
        <div className="panel">
          <h2>Wishlist</h2>
          {destinations.length === 0 ? (
            <p className="empty">No destinations yet. Add one above!</p>
          ) : (
            <ul className="destination-list">
              {destinations.map((d) => (
                <li
                  key={d.id}
                  className={
                    selectedDestination?.id === d.id
                      ? "destination-item selected"
                      : "destination-item"
                  }
                >
                  <div>
                    <div className="dest-name">{d.name}</div>
                    {d.country && (
                      <div className="dest-country">{d.country}</div>
                    )}
                  </div>

                  <div className="actions">
                    <button
                      className="btn-small"
                      onClick={() => handleSelect(d)}
                    >
                      Details
                    </button>
                    <button
                      className="btn-remove"
                      onClick={() => handleRemove(d.id)}
                    >
                      Remove
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="panel">
          <h2>Destination Details</h2>

          {!selectedDestination && (
            <p className="empty">Select a destination.</p>
          )}

          {selectedDestination && (
            <>
              <h3 className="detail-title">
                {selectedDestination.name}
                {selectedDestination.country
                  ? `, ${selectedDestination.country}`
                  : ""}
              </h3>

              {selectedDestination.imageUrl && (
                <img
                  src={selectedDestination.imageUrl}
                  alt={selectedDestination.name}
                  className="detail-image"
                />
              )}

              {loadingDescription && <p className="loading">Loading…</p>}
              {!loadingDescription && description && (
                <p className="description">{description}</p>
              )}

              {!loadingDescription && !description && !error && (
                <p className="empty">No description available.</p>
              )}

              <button
                className="btn-refresh"
                onClick={() => fetchDescription(selectedDestination)}
              >
                Refresh Description
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
