# Altschool Second semester project
# Project Title: Blog API with FastApI

This is a FastAPI-based blog API project. It provides endpoints for creating users, articles, and more.

### Running the Server
1. To start the server, run the following command: uvicorn main:app --reload. This will enable auto-reloading for development.
2. Open your browser and go to `http://localhost:8000` to access the root endpoint.
3. To test the endpoints interactively, visit `http://localhost:8000/docs` to use the Swagger UI FastAPI documentation.


### Creating Users and Articles

To test the endpoints, follow these steps:

1. **Create a User:**
- Use the `create user` endpoint in the user route.
- Take note of the **author ID** after creating the user, as this will be used whenever that user wants to create an article.
- Each user has a unique ID that links to their articles.

2. **Creating an Article:**
- Use the appropriate endpoint, ensuring you provide the author ID to link the author to the article.

3. **Authentication:**
- Some routes require authentication. After creating an account, make sure to log in to access these protected endpoints.
