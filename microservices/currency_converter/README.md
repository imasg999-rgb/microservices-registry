# Currency Converter Microservice

The Currency Converter microservice provides exchange-rate conversion using an external currency provider API.

---

### Building Frontend
- `cd frontend`, and then run `npm run build`. It should create a build folder `./frontend/dist/`.
  - index.py will serve whatever is in that `dist` folder.

## API Endpoints

### `GET /convert?from=USD&to=EUR&amount=100`

**Query Parameters:**
- **from** — Source currency code (e.g. `USD`)
- **to** — Target currency code (e.g. `CAD`)
- **amount** — Amount to convert (numeric)

**Example Response:**
```json
{
  "from": "USD",
  "to": "EUR",
  "amount": 100,
  "converted_amount": 92.51,
  "rate": 0.9251
}
