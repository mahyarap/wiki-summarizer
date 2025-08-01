# Wikipedia Summarizer

This is a simple AI-powered Wikipedia summarizer built with FastAPI, LangChain, and OpenAI. You give it a topic, it goes and reads Wikipedia for you, then gives you a short and sweet summary.

## What it does

* You send a topic like `"Black holes"`
* The agent looks it up on Wikipedia
* Then it gives you a summary like a helpful buddy who's into science

## How to run it

You'll need **Docker** and an **OpenAI API key** to run the app.

```bash
# Build the Docker image
docker build -t wiki-summarizer .

# Run the app with your OpenAI API key
docker run -e OPENAI_API_KEY=your-key-here -p 8000:8000 wiki-summarizer
```

Now you can check the API endpoints:
[http://localhost:8000/docs](http://localhost:8000/docs) — to try it out in your browser!


## Environment variables

| Variable         | Required | Description         |
| ---------------- | -------- | ------------------- |
| `OPENAI_API_KEY` | yes      | your OpenAI API key |

## Docker

The `Dockerfile` is optimized using **multi-stage builds** and other tricks (like `.dockerignore` and `uv`) to keep the final image as **small** as possible.

## Running tests

We have a mix of fast unit tests and some heavier functional ones.

```bash
# Run unit tests only
pytest tests

# Run functional tests (disabled by default)
pytest -m "functional"
```

## Usage

Once the app is running (either locally or in Docker), you can test the summarizer with a simple `curl` command:

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"topic": "Artificial Intelligence"}'
```

Expected response:

```json
{
  "summary": "Artificial intelligence (AI) is the capability of computational systems to perform tasks ..."
}
```

## Quality & Dev Practices

* **Code quality**: Everything is typed, checked with pyright and linted using ruff.
*  **Tests**: There's both unit and functional tests using `pytest`. It tests both the agent and the FastAPI app.
*  **API quality**: The FastAPI routes follow basic REST ideas and requests/responses are validated with Pydantic

## Security Notes

The app's Docker container is built with security in mind.

* It uses an **optimized multi-stage build** to keep the image size as small as possible.
* It runs as a **non-root user** (`appuser`) by default.
* All **Linux capabilities can be dropped** using `--cap-drop=ALL` when running the container.

To run the container with enhanced security, use:

```bash
docker run --cap-drop=ALL -p 8000:8000 -e OPENAI_API_KEY=your-key wiki-agent:latest
```
