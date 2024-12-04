def fetch_user(user_id: int):
    # Simulating a database call
    users_db = {1: "John Doe", 2: "Jane Doe", 3: "Alice"}
    return users_db.get(user_id, "User not found")
