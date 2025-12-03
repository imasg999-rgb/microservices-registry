import "./SearchBar.css";

export function SearchBar({ onSearch }) {
  const handleSubmit = (formData) => {
    const query = formData.get("serviceName");
    onSearch(query);
  };

  return (
    <div className="search-bar-container">
      <form className="search-bar" action={handleSubmit}>
        <div className="label-container">
          <label htmlFor="serviceName" className="search-bar__label">Service Name</label>
        </div>
        <div className="textfield-container">
          <input className="search-bar__textfield" name="serviceName" id="serviceName" autoComplete="off" />
          <button className="search-bar__submit">Search</button>
        </div>
      </form>
    </div>
  );
}