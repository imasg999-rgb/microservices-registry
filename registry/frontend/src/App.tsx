import "./index.css";
import { useState, useEffect } from "react";
import { getAllServices } from "./api/registry";
import { SearchBar } from "./components/SearchBar";
import { Results } from "./components/Results";

export function App() {
  const [services, setServices] = useState(null);

  useEffect(() => {
    const allServices = getAllServices()
      .then(data => console.log(data))
      .catch();
  }, []);

  const onSearch = async (query: string) => {
    const allServices = await getAllServices();
    if (query.length == 0) {
      setServices(allServices);
    } else {
      const queryLen = query.length;
      for (let i = 0; i < allServices.length; ++i) {
        // TODO: Return matches of services that has the query as a prefix
      }
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-8 text-center relative z-10">
      <SearchBar onSearch={onSearch} />
      <Results services={services} />
    </div>
  );
}

export default App;
