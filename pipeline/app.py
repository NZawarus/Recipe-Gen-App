from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import recipe, settings, conversation, generate

# Create FastAPI application
app = FastAPI(title="Recipe API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(recipe.router, tags=["Recipes"])
app.include_router(settings.router, tags=["Settings"])
app.include_router(conversation.router, tags=["Conversations"])
app.include_router(generate.router, tags=["Generations"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Recipe API. Visit /docs for API documentation."}

# Run the application with uvicorn when this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True) 