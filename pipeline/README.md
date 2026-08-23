# Recipe API Server

## Running the Server

To start the server, run the following command from the pipeline directory:

```bash
python app.py
```

Alternatively, you can use uvicorn directly:

```bash
uvicorn app:app --reload
```

Once the server is running, it will be accessible at:
- API: http://localhost:8000
- Swagger Documentation: http://localhost:8000/docs

## Testing the Endpoints

You can test the endpoints using the provided test script:

```bash
python -m routers.test_routers
```

Note: Make sure to update the port in the test_routers.py file if you changed the default port (8000).

## Available Endpoints

### Recipe Endpoints
- `POST /recipes` - Create a new recipe
- `GET /recipes/{recipe_id}` - Get a recipe by ID
- `PUT /recipes/{recipe_id}` - Update a recipe
- `DELETE /recipes/{recipe_id}` - Delete a recipe
- `GET /recipes?user_id={user_id}` - Get all recipes for a user

### Settings Endpoints
- `POST /settings/{user_id}` - Create settings
- `GET /settings/{user_id}` - Get settings
- `PUT /settings/{user_id}` - Update settings
- `DELETE /settings/{user_id}` - Delete settings

### Conversation Endpoints
- `POST /conversations` - Create a new conversation
- `GET /conversations/{conversation_id}` - Get a conversation
- `PUT /conversations/{conversation_id}` - Update a conversation
- `DELETE /conversations/{conversation_id}` - Delete a conversation
- `GET /conversations` - Get all conversations
