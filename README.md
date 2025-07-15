# Go Tripping Flask Backend API Documentation

## Authentication

### Register
- **POST** `/api/register`
- **Payload:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "yourpassword"
}
```
- **Response (201):**
```json
{"message": "User created successfully"}
```

### Login
- **POST** `/api/login`
- **Payload:**
```json
{
  "email": "john@example.com",
  "password": "yourpassword"
}
```
- **Response (200):**
```json
{
  "access_token": "<JWT_TOKEN>",
  "message": "Login successful"
}
```

---

## Profile

### Get Profile
- **GET** `/api/profile` (JWT required)
- **Response (200):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  ...
}
```

### Update Profile
- **PUT** `/api/profile` (JWT required)
- **Payload:**
```json
{
  "name": "Jane Doe"
}
```
- **Response (200):**
```json
{
  "message": "Profile updated successfully",
  "user": { "id": 1, "name": "Jane Doe", ... }
}
```

### Get All Users
- **GET** `/api/users` (JWT required)
- **Query:** `?page=1&per_page=10`
- **Response (200):**
```json
{
  "users": [ {"id": 1, "name": "..."}, ... ],
  "total": 20,
  "pages": 2,
  "current_page": 1,
  "has_next": true,
  "has_prev": false
}
```

### Get User by ID
- **GET** `/api/users/<user_id>` (JWT required)
- **Response (200):**
```json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "avatarUrl": "https://...",
  "bio": "Traveler",
  "age": 28,
  "gender": "female",
  "sun_sign": "leo",
  "interests": ["hiking", "photography"],
  "location": {"lat": 12.34, "lng": 56.78},
  "createdAt": "2024-07-15T12:34:56.789Z",
  "updatedAt": "2024-07-15T12:34:56.789Z",
  "followers_count": 10,
  "following_count": 5
}
```

---

## Follow System

### Follow User
- **POST** `/api/users/<user_id>/follow` (JWT required)
- **Response (200):**
```json
{"message": "Successfully followed <name>"}
```

### Unfollow User
- **POST** `/api/users/<user_id>/unfollow` (JWT required)
- **Response (200):**
```json
{"message": "Successfully unfollowed <name>"}
```

### Get Followers
- **GET** `/api/users/<user_id>/followers` (JWT required)
- **Response (200):**
```json
{"followers": [ {"id": 2, "name": "..."}, ... ]}
```

### Get Following
- **GET** `/api/users/<user_id>/following` (JWT required)
- **Response (200):**
```json
{"following": [ {"id": 3, "name": "..."}, ... ]}
```

---

## Community

### Create Community
- **POST** `/api/communities` (JWT required)
- **Payload:**
```json
{
  "name": "Nature Lovers",
  "description": "A group for nature enthusiasts."
}
```
- **Response (201):**
```json
{"message": "Community created", "community": {"id": 1, "name": "Nature Lovers", ...}}
```

### Get All Communities
- **GET** `/api/communities` (JWT required)
- **Response (200):**
```json
[{"id": 1, "name": "Nature Lovers", ...}, ...]
```

### Get Community Details
- **GET** `/api/communities/<community_id>` (JWT required)
- **Response (200):**
```json
{
  "id": 1,
  "name": "Nature Lovers",
  "members_details": [ {"id": 1, "name": "..."}, ... ],
  "is_member": true,
  ...
}
```

### Join Community
- **POST** `/api/communities/<community_id>/join` (JWT required)
- **Response (200):**
```json
{"message": "Joined community"}
```

### Leave Community
- **POST** `/api/communities/<community_id>/leave` (JWT required)
- **Response (200):**
```json
{"message": "Left community"}
```

### Get Joined Communities
- **GET** `/api/communities/joined` (JWT required)
- **Response (200):**
```json
[{"id": 1, "name": "Nature Lovers", ...}, ...]
```

---

## Community Posts

### Create Community Post
- **POST** `/api/communities/<community_id>/posts` (JWT required)
- **Payload:**
```json
{
  "title": "Trip to the mountains",
  "content": "We are planning a trip...",
  "image_urls": ["http://.../img1.jpg"]
}
```
- **Response (201):**
```json
{
  "id": 1,
  "title": "Trip to the mountains",
  ...
}
```

### Get Community Posts
- **GET** `/api/communities/<community_id>/posts` (JWT required)
- **Response (200):**
```json
[{"id": 1, "title": "Trip to the mountains", ...}, ...]
```

### Get Post by ID
- **GET** `/api/posts/<post_id>` (JWT required)
- **Response (200):**
```json
{
  "id": 1,
  "title": "Trip to the mountains",
  "author": {"id": 1, "name": "..."},
  ...
}
```

### Update Post
- **PUT** `/api/posts/<post_id>` (JWT required, only author)
- **Payload:**
```json
{
  "title": "Updated title",
  "content": "Updated content",
  "image_urls": ["http://.../img2.jpg"]
}
```