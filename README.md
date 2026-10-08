# Event Management API

A simple RESTful API built with Flask that supports full CRUD operations on a list of events. Data is stored in memory (a Python list of `Event` objects), so it resets every time the server restarts.

## Setup

```
git clone https://github.com/ndungupatriciawanjiru-hub0/course-8-module-5-flask-full-crud-api-lab.git
cd course-8-module-5-flask-full-crud-api-lab
pipenv install
pipenv shell
python app.py
```

Or install Flask directly with `pip install flask`. The server runs at `http://localhost:5000`.

## Routes

| Method | Route          | Description                  | Success status |
|--------|----------------|------------------------------|----------------|
| GET    | `/`            | JSON welcome message         | 200 OK         |
| GET    | `/events`      | List all events              | 200 OK         |
| POST   | `/events`      | Create a new event           | 201 Created    |
| PATCH  | `/events/<id>` | Update the title of an event | 200 OK         |
| DELETE | `/events/<id>` | Remove an event              | 204 No Content |

## Examples

### GET /

```
curl http://localhost:5000/
```

Response:

```
{ "message": "Welcome to the Event Management API" }
```

### GET /events

```
curl http://localhost:5000/events
```

Response (200 OK):

```
[
  { "id": 1, "title": "Tech Meetup" },
  { "id": 2, "title": "Python Workshop" }
]
```

### POST /events

```
curl -i -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Hackathon"}'
```

Response (201 Created):

```
{ "id": 3, "title": "Hackathon" }
```

### PATCH /events/1

```
curl -i -X PATCH http://localhost:5000/events/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Hackathon 2025"}'
```

Response (200 OK):

```
{ "id": 1, "title": "Hackathon 2025" }
```

### DELETE /events/2

```
curl -i -X DELETE http://localhost:5000/events/2
```

Response: 204 No Content (empty body).

## Error responses

| Situation                                   | Status          | Response body                        |
|---------------------------------------------|-----------------|--------------------------------------|
| POST or PATCH with missing/empty `title`    | 400 Bad Request | `{ "error": "Title is required" }`   |
| PATCH or DELETE with an ID that doesn't exist | 404 Not Found | `{ "error": "Event not found" }`     |

## Design notes

- Routes use nouns (`/events`) and the HTTP method describes the action.
- `request.get_json(silent=True)` reads the request body, so a missing or invalid body returns a clean 400 instead of crashing.
- A helper function, `find_event()`, looks up events by ID so the PATCH and DELETE routes don't repeat the same code.
- A second helper, `next_id()`, picks the next ID so a new event never reuses the ID of a deleted one.
- All responses use `jsonify()`.

## Running the tests

```
pytest
```