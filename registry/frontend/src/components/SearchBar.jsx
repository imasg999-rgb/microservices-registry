import "./SearchBar.css";

export function SearchBar({ onSearch }) {
  const handleSubmit = (event) => {
    event.preventDefault();
    const serviceQuery = event.target.elements?.serviceName?.value;
    if (serviceQuery) {
      onSearch(serviceQuery);
    }
  };

  return (
    <div className="search-bar-container">
      <form className="search-bar" action={handleSubmit}>
        <label for="service-name" className="search-bar__label">Service Name</label>
        <input className="search-bar__textfield" name="service-name" id="serviceName" />
        <button className="search-bar__submit">Search</button>
      </form>
    </div>
  );
}