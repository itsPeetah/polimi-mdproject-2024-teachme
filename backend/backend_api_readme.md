# Backend API

## Register new user
**Route:** `/register`  
**Methods:** `POST`  
**Description:** Registers a new user in the system.   
**Request parameters:**
- **email (required, string):** email address of the user.
- **username (required, string):** username of the user.
- **password (required, string):** password of the user.
- **role (required, string):** role of the user. Possible values: *teacher*, *student*.

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
- **email (required, string):** email address of the user.
- **password (required, string):** password of the user.

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
- **teacher_email (required, string):** email address of the teacher.
- **student_email (required, string):** email address of the student.

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
- **teacher_email (required, string):** email address of the teacher.
- **student_email (required, string):** email address of the student.

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
- **user_level (required, string):** Level of the user. Possible values: *beginner*, *intermediate*, *advanced*.
- **difficulty (required, string):** Difficulty of the conversation. Possible values: *easy*, *medium*, *challenging*.
- **topic (optional, string):** Topic of the conversation. Defaults to None.
- **teacher_email (required, string):** Email address of the teacher who created the conversation.
- **student_email (required, string):** Email address of the student whom the conversation was assigned to.
- **time_limit (optional, string or int):** Time limit of the conversation (in minutes). Defaults to 5 minutes.

**Expected data format (example):**
```json
POST /create-conversation

{
    "user_level": "intermediate",
    "difficulty": "challenging",
    "topic": "Last summer holidays",
    "teacher_email": "teacher@example.com",
    "student_email": "student@example.com",
    "time_limit": 10
}
```
**Response:** The function returns the simple message "Ok" upon successful creation of the conversation.


## Initialize conversation
**Route:** `/initialize-conversation`  
**Methods:** `POST`  
**Description:** Initializes an already existing conversation. This is necessary in order to load the corresponding chatbot from the conversation in the database.  
**Request parameters:**
- **conversation_id (required, string)**: The unique identifier of the conversation.

**Expected data format (example):**
```json
POST /initialize-conversation

{
    "conversation_id": "6645c6ebda20b82cd697390d"
}
```
**Response:** The function returns the code 200 and the message "Conversation initialized successfully" upon successful creation of the conversation. If an error occurs, it returns the code 400 with a message specifying the error.


## Send user message to chatbot
**Route:** `/user-chat-message`  
**Methods:** `POST`  
**Description:** Handles user messages sent to the specified chatbot, through a POST request.  
**Request parameters:**
- **conversation_id (required, string)**: The unique identifier of the conversation.
- **sender_id (required, string)**: The unique identifier of the user who sends the message.
- **message (required, string)**: The text message sent by the user.

**Expected data format (example):**
```json
POST /user-chat-message

{
    "conversation_id": "6645c6ebda20b82cd697390d",
    "sender_id": "43379a1b-f39d-489b-bb9c-8d8adbce6325",
    "message": "Hi, my name is Ciuchino!"
}
```
**Response:** A JSON object with the following properties:
- **conversation_id (string)**: The conversation ID (same as the request parameter).
- **response (string)**: The chatbot's response to the user message.


## Get user's conversations
**Route:** `/list-user-conversations/<user_email>`  
**Methods:** `GET`  
**Description:** Returns the ids of all the conversations that the user is involved in. If the user is a teacher, this method returns all the conversations that the user created. If the user is a student, this method returns all the conversations that were assigned to the user.  
**Query parameters:**
- **user_email (required, string):** email address of the user.

**Expected data format (example):**  `GET /list-user-conversations/student@example.com`

**Response:** A JSON file containing the ids of all the conversations that the user is involed in.  
**Error handling:** Returns error 400 if a problem occurred.


## Get conversation info
**Route:** `/get-conversation-info/<conversation_id>`  
**Methods:** `GET`  
**Description:** Returns information about the conversation with the specified id.  
**Query parameters:**
- **conversation_id (required, string):** id of the conversation.

**Expected data format (example):**  `GET /get-conversation-info/6645c6ebda20b82cd697390d`

**Response:** A JSON containing the information about the conversation with the specified id.  
**Error handling:** Returns error 400 if a problem occurred.


## Get user's friends
**Route:** `/get-friends/<user_email>`  
**Methods:** `GET`  
**Description:** Retrieves all the friends of the user. If the user is a teacher, this returns all the teacher's students. If the user is a student, this returns all the student's teachers.  
**Query parameters:**
- **user_email (required, string):** email address of the user.

**Expected data format (example):**  `GET /get-friends/student@example.com`

**Response:** The function returns a JSON containing the friends of the specified user.  
**Error handling:** Returns error 400 if the specified user was not found in the database.