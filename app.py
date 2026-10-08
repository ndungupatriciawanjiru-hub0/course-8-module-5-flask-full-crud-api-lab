from flask import Flask, jsonify, request

app = Flask(__name__)


# Event class: represents a single event in our simulated database
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory data store (resets every time the server restarts)
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]


# Helper: look up an event by id so the logic isn't repeated in every route
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


# Helper: generate the next id (highest existing id + 1, or 1 if list is empty)
def next_id():
    return max((event.id for event in events), default=0) + 1


# GET / - JSON welcome message
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event Management API"}), 200


# GET /events - return all events as a JSON array
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# POST /events - create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # silent=True returns None instead of raising an error on bad/missing JSON
    data = request.get_json(silent=True)

    # Validate: body must exist and contain a non-empty title
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_event = Event(next_id(), data["title"])
    events.append(new_event)

    # 201 Created for a successful POST
    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    # 204 No Content: success, nothing to return
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)