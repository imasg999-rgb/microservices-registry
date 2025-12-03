// import dummy_response from "./example_response.json";

const REGISTRY_URL = "http://35.183.109.248:7993/";

export async function getAllServices() {
  // return dummy_response;
  const url = new URL("/services", REGISTRY_URL);
  const response = await fetch(url);
  return response.json();
}
