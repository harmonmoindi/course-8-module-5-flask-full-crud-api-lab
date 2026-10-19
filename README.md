# Flask Full CRUD API – Events

A small RESTful API built with Flask that manages a list of events. Data is
stored **in memory** using `Event` class objects, so it resets every time the
server restarts. It demonstrates `POST`, `PATCH`, and `DELETE` handling with
`request.get_json()`, `jsonify()`, and proper HTTP status codes.

## Setup

```bash
git clone <repo-url>
cd course-8-module-5-flask-full-crud-api-lab
pipenv install
pipenv shell
```

Or with pip:

```bash
pip install flask pytest
```

## Run the server

```bash
python app.py
```

The API runs at `http://localhost:5000`.

## Run the tests

```bash
pytest
```

## Data model

```json
{ "id": 1, "title": "Tech Meetup" }
```

The app starts with two events:

| id | title           |
|----|-----------------|
| 1  | Tech Meetup     |
| 2  | Python Workshop |

## Endpoints

| Method | Route          | Description                 | Success   |
|--------|----------------|-----------------------------|-----------|
| POST   | `/events`      | Create a new event          | `201`     |
| PATCH  | `/events/<id>` | Update an event's title     | `200`     |
| DELETE | `/events/<id>` | Delete an event             | `204`     |

### POST /events

Creates a new event. The `id` is generated automatically.

**Request**

```bash
curl -X POST http://localhost:5000/events \
  -H "Content-Type: application/json" \
  -d '{"title": "Hackathon"}'
```

**Response – 201 Created**

```json
{ "id": 3, "title": "Hackathon" }
```

**Response – 400 Bad Request** (missing or empty `title`)

```json
{ "error": "A non-empty 'title' field is required" }
```

### PATCH /events/\<id\>

Updates the title of an existing event.

**Request**

```bash
curl -X PATCH http://localhost:5000/events/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Hackathon 2025"}'
```

**Response – 200 OK**

```json
{ "id": 1, "title": "Hackathon 2025" }
```

**Response – 404 Not Found**

```json
{ "error": "Event with id 99 not found" }
```

**Response – 400 Bad Request** (missing or empty `title`)

```json
{ "error": "A non-empty 'title' field is required" }
```

### DELETE /events/\<id\>

Removes an event.

**Request**

```bash
curl -X DELETE http://localhost:5000/events/2
```

**Response – 204 No Content** (empty body)

**Response – 404 Not Found**

```json
{ "error": "Event with id 99 not found" }
```

## Status codes

| Code | Meaning                                   |
|------|-------------------------------------------|
| 200  | OK – event updated                        |
| 201  | Created – event added                     |
| 204  | No Content – event deleted                |
| 400  | Bad Request – missing/invalid `title`     |
| 404  | Not Found – no event with that id         |

## Design notes

- Routes use the noun `/events` (RESTful naming).
- Helper functions (`find_event`, `next_event_id`, `get_valid_title`) keep the
  route functions short and avoid repeated code.
- New ids use `max(id) + 1` so ids are never reused after a delete.
- The list is modified in place (`append`, `remove`) so it behaves like a
  shared database for the whole app.
- Because data is in memory, it is lost when the server stops. A persistent
  database comes in the next module.