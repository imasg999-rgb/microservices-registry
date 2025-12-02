### API Endpoints
- `/search/<AIRPORT_CODE1>/<AIRPORT_CODE2>
  - `departure_date` and `return_date` in `YYYY-MM-DD` format can be passed as query parameters
 
### Building Frontend
- `cd frontend`, and then run `bun run build`. It should create a build folder `./frontend/dist/`.
  - index.py will serve whatever is in that `dist` folder.