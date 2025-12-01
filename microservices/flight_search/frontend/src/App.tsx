import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import "./index.css";

import { SearchBar } from "./SearchBar";
import { Results } from "./Results";
import { useState } from "react";

export function App() {
  const [results, setResults] = useState(null);

  function onSearch(values: {
    origin_code: string
    destination_code: string
    departure_date: string
    return_date: string
  }) {
    const params = new URLSearchParams({
      departure_date: values.departure_date,
      return_date: values.return_date,
    });
    fetch(`/search/${values.origin_code}/${values.destination_code}?${params}`)
      .then(response => response.json())
      .then(data => {
        setResults(data);
      });
  }

  return (
    <>
      <h1 className="text-3xl font-bold tracking-tight text-center">Flight Search Service</h1>
      <SearchBar onSearch={onSearch} />
      <Results results={results} />
    </>
  )
}

export default App;
