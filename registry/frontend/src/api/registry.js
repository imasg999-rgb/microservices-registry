const REGISTRY_URL = "http://35.183.109.248:7993/";

export async function getAllServices() {
  const url = new URL("/services", REGISTRY_URL);
  const response = await fetch(url);
  return response.json();
}
