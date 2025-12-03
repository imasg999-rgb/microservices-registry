import "./index.css";
import { useState, useEffect } from "react";
import { getAllServices } from "./api/registry";
import { SearchBar } from "./components/SearchBar";
import { Results } from "./components/Results";

export function App() {
  const [services, setServices] = useState<any[]>([]);

  useEffect(() => {
    getAllServices()
      .then(data => setServices(data))
      .catch(e => console.log(e));
  }, []);

  const onSearch = async (query: string) => {
    const allServices = await getAllServices();
    if (query.length == 0) {
      setServices(allServices);
    } else {
      const matchingServices = [];
      for (let i = 0; i < allServices.length; ++i) {
        const serviceName: string = allServices[i]?.name;
        if (!serviceName) continue;
        if (query.length > serviceName.length) continue;
        if (query === serviceName.substring(0, query.length)) {
          matchingServices.push(allServices[i]);
        }
      }
      console.log(matchingServices);
      setServices(matchingServices);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-8 text-center relative z-10">
      <h1 className="text-4xl font-bold">Service Discovery</h1>
      <SearchBar onSearch={onSearch} />
      <Results services={services} />
    </div>
  );
}

export default App;
