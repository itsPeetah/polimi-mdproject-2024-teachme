# Backend API

## Register new user
**Route:** `/register`  
**Methods:** `POST`  
**Description:** Registers a new user in the system.   
**Request parameters:**
- **email (required):** email address of the user.
- **username (required):** username of the user.
- **password (required):** password of the user.
- **role (required):** role of the user. Possible values: *teacher*, *student*.

**Expected data format (example):**  
```json
POST /register

{
    "email": "teacher@example.com",
    "username": "teacher1234",
    "password": "password1234",
    "role": "teacher"
}
```
**Response:** Returns code 200 if the user was registered correctly.  
**Error handling:** Returns error 400 if a problem occurred while registering the new user.


## Login user
**Route:** `/login`  
**Methods:** `POST`  
**Description:** Logs user into the system.   
**Request parameters:**
- **email (required):** email address of the user.
- **password (required):** password of the user.

**Expected data format (example):**  
```json
POST /login

{
    "email": "teacher@example.com",
    "password": "password1234"
}
```
**Response:** Returns code 200 if the user was logged in correctly.  
**Error handling:** Returns error 400 if a problem occurred while logging the user into the system.


## Get current user information
**Route:** `/me`  
**Methods:** `GET`  
**Description:** Retrieves information about the user currently logged in. If no user is logged in this returns an error.

**Response:** Returns a JSON object containing:
- user_id: The identifier of the logged-in user.
- role: The role of the logged-in user.

**Error handling:** Returns error 400 if no user is logged in.


## Create friendship
**Route:** `/create-friendship`  
**Methods:** `POST`  
**Description:** Creates a *friendship* between a teacher and a student in the database.  
**Request parameters:**
- **teacher_email (required):** email address of the teacher.
- **student_email (required):** email address of the student.

**Expected data format (example):**  
```json
POST /create-friendship

{
    "teacher_email": "teacher@example.com",
    "student_email": "student@example.com"
}
```
**Response:** The function returns the simple message "Ok" upon successful creation of the friendship.


## Remove friendship
**Route:** `/remove-friendship`  
**Methods:** `POST`  
**Description:** Removes the *friendship* between a teacher and a student in the database.  
**Request parameters:**
- **teacher_email (required):** email address of the teacher.
- **student_email (required):** email address of the student.

**Expected data format (example):**
```json
POST /remove-friendship

{
    "teacher_email": "teacher@example.com",
    "student_email": "student@example.com"
}
```
**Response:** The function returns the simple message "Ok" upon successful removal of the friendship.


## Create conversation
**Route:** `/create-conversation`  
**Methods:** `POST`  
**Description:** Creates a new conversation in the database.  
**Request parameters:**
- **user_level (required):** Level of the user. Possible values: *beginner*, *intermediate*, *advanced*.
- **difficulty (required):** Difficulty of the conversation. Possible values: *easy*, *medium*, *challenging*.
- **topic (optional):** Topic of the conversation. Defaults to None.
- **teacher_email (required):** Email address of the teacher who created the conversation.
- **student_email (required):** Email address of the student whom the conversation was assigned to.
- **time_limit (optional):** Time limit of the conversation (in minutes). Defaults to 5 minutes.

**Expected data format (example):**
```json
POST /create-conversation

{
    "user_level": "intermediate",
    "difficulty": "challenging",
    "topic": "Last summer holidays",
    "teacher_email": "teacher@example.com",
    "student_email": "student@example.com",
    "time_limit": "10"
}
```
**Response:** The function returns the simple message "Ok" upon successful creation of the conversation.


## Get user's friends
**Route:** `/get-friends/<user_email>`  
**Methods:** `GET`  
**Description:** Retrieves all the friends of the user. If the user is a teacher, this returns all the teacher's students. If the user is a student, this returns all the student's teachers.  
**Query parameters:**
- **user_email (required):** email address of the user.

**Expected data format (example):**  `GET /get-friends/student@example.com`

**Response:** The function returns a **list** containing the friends of the specified user.  
**Error handling:** Returns error 400 if the specified user was not found in the database.