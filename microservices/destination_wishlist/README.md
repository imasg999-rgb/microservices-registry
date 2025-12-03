# Destination Wishlist Microservice

The Destination Wishlist microservice retrieves descriptions and images for destinations using the Wikipedia REST API.

---

## Building Frontend
- `cd frontend`, and then run `npm run build`. It should create a build folder `./frontend/dist/`.
  - index.py will serve whatever is in that `dist` folder.

## API Endpoints

### `GET /api/destination-description?name=Paris&country=France`

**Query Parameters:**
- **name** — Required. Destination name (e.g., `Paris`)
- **country** — Optional. Provides location context (e.g., `France`)

**Example Response:**
```json
{
  "name": "Paris",
  "country": "France",
  "description": "Paris is the capital city of France...",
  "image_url": "https://upload.wikimedia.org/.../thumbnail.jpg"
}
