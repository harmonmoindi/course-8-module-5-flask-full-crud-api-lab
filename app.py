from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# ---------- Helper functions ----------

def find_event(event_id):
    """Return the Event with the given id, or None if it doesn't exist."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def next_event_id():
    """Generate the next id: one more than the highest existing id.

    Using max() instead of len(events) + 1 avoids duplicate ids after a
    delete (e.g. deleting id 1 from [1, 2] would make len + 1 == 2 again).
    """
    return max((event.id for event in events), default=0) + 1


def get_valid_title(data):
    """Extract and validate the 'title' from parsed JSON.

    Returns the cleaned title string, or None if it is missing/invalid.
    """
    if not isinstance(data, dict):
        return None
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return None
    return title.strip()


# ---------- Routes ----------

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # silent=True returns None instead of raising an error on bad/missing JSON
    data = request.get_json(silent=True)

    # Validate input: a non-empty "title" is required
    title = get_valid_title(data)
    if title is None:
        return jsonify({"error": "A non-empty 'title' field is required"}), 400

    # Build the new event, store it, and return it
    new_event = Event(next_event_id(), title)
    events.append(new_event)

    # 201 Created for a successful POST
    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Look the event up first so a missing event always returns 404
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    # Validate input before changing anything
    data = request.get_json(silent=True)
    title = get_valid_title(data)
    if title is None:
        return jsonify({"error": "A non-empty 'title' field is required"}), 400

    # Mutate the existing object in place
    event.title = title

    # 200 OK with the updated event
    return jsonify(event.to_dict()), 200


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    # Remove in place (don't reassign `events`, or other modules/tests
    # holding a reference to the list would no longer see the change)
    events.remove(event)

    # 204 No Content: success, nothing to return in the body
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)