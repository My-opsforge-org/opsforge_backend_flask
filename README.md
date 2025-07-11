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
- **Response (200):**
```json
{
  "id": 1,
  "title": "Updated title",
  ...
}
```

### Delete Post
- **DELETE** `/api/posts/<post_id>` (JWT required, only author)
- **Response (200):**
```json
{"message": "Post deleted successfully"}
```

---

## Profile Posts

### Create Profile Post
- **POST** `/api/profile/posts` (JWT required)
- **Payload:**
```json
{
  "title": "My new post",
  "content": "Hello!",
  "image_urls": ["http://.../img.jpg"]
}
```
- **Response (201):**
```json
{
  "message": "Post created successfully",
  "post": {"id": 1, "title": "My new post", ...}
}
```

### Get User Profile Posts
- **GET** `/api/profile/<user_id>/posts` (JWT required)
- **Response (200):**
```json
{
  "posts": [ {"id": 1, "title": "My new post", ...}, ... ]
}
```

### Update Profile Post
- **PUT** `/api/profile/posts/<post_id>` (JWT required, only author)
- **Payload:**
```json
{
  "title": "Updated title",
  "content": "Updated content",
  "image_urls": ["http://.../img2.jpg"]
}
```
- **Response (200):**
```json
{
  "message": "Post updated successfully",
  "post": {"id": 1, "title": "Updated title", ...}
}
```

### Delete Profile Post
- **DELETE** `/api/profile/posts/<post_id>` (JWT required, only author)
- **Response (200):**
```json
{"message": "Post deleted successfully"}
```

---

## Comments

### Create Comment
- **POST** `/api/posts/<post_id>/comments` (JWT required)
- **Payload:**
```json
{
  "content": "Nice post!"
}
```
- **Response (201):**
```json
{
  "id": 1,
  "content": "Nice post!",
  ...
}
```

### Get Comments for Post
- **GET** `/api/posts/<post_id>/comments` (JWT required)
- **Response (200):**
```json
[
  {"id": 1, "content": "Nice post!", ...},
  ...
]
```

### Update Comment
- **PUT** `/api/comments/<comment_id>` (JWT required, only author)
- **Payload:**
```json
{
  "content": "Updated comment"
}
```
- **Response (200):**
```json
{
  "id": 1,
  "content": "Updated comment",
  ...
}
```

### Delete Comment
- **DELETE** `/api/comments/<comment_id>` (JWT required, only author)
- **Response (200):**
```json
{"message": "Comment deleted successfully"}
```

---

## Bookmarks

### Bookmark Post
- **POST** `/api/posts/<post_id>/bookmark` (JWT required)
- **Response (200):**
```json
{"message": "Post bookmarked successfully"}
```

### Remove Bookmark
- **DELETE** `/api/posts/<post_id>/bookmark` (JWT required)
- **Response (200):**
```json
{"message": "Bookmark removed successfully"}
```

### Get Bookmarked Posts
- **GET** `/api/bookmarks` (JWT required)
- **Response (200):**
```json
[
  {"id": 1, "title": "Trip to the mountains", ...},
  ...
]
```

---

## Reactions

### Like Post
- **POST** `/api/posts/<post_id>/like` (JWT required)
- **Response (200):**
```json
{"message": "Post liked successfully"}
```

### Dislike Post
- **POST** `/api/posts/<post_id>/dislike` (JWT required)
- **Response (200):**
```json
{"message": "Post disliked successfully"}
```

### Remove Reaction
- **DELETE** `/api/posts/<post_id>/reaction` (JWT required)
- **Response (200):**
```json
{"message": "Reaction removed successfully"}
```

---

## Feed

### Get Feed
- **GET** `/api/feed` (JWT required)
- **Query:** `?page=1&per_page=10`
- **Response (200):**
```json
{
  "posts": [ {"id": 1, "title": "...", ...}, ... ],
  "total": 10,
  "pages": 1,
  "current_page": 1,
  "has_next": false,
  "has_prev": false
}
```

---

## Explore

### Get Places
- **GET** `/api/explore/places` (JWT required)
- **Query:** `?lat=...&lng=...&radius=1500&type=tourist_attraction`
- **Response (200):**
```json
{
  "results": [ {"name": "Eiffel Tower", ...}, ... ],
  ...
}
```

### Geocode Address
- **GET** `/api/explore/geocode` (JWT required)
- **Query:** `?address=...`
- **Response (200):**
```json
{
  "address": "Paris, France",
  "latitude": 48.8566,
  "longitude": 2.3522
}
``` 