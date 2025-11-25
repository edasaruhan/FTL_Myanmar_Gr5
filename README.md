# FTL Myanmar Group 5 — MindCare

This repository implements two conversational endpoints for mental health support:

- `Mic_Chat`: Retrieval-Augmented Generation (RAG) over a curated mental health corpus
- `Medical_Chat`: A fine-tuned `mT5` model for medical-style chat responses

Both endpoints are provided via a FastAPI service and can be run locally or in Docker.

## Repository Layout

- `src/Deployment/api_endpoint/main.py`: FastAPI app exposing `/Mic_Chat` and `/Medical_Chat`
- `src/RAG_pipeline/`: RAG components (`Embedder`, `VectorStore`, prompt, generation)
- `src/Fine_tuned/medical_chat.py`: Fine-tuned `mT5` chat wrapper
- `src/Schema/text_request.py`: Pydantic request model (`{"user_input": str}`)
- `Dockerfile`: Container image for the API server

## Requirements

- Python `3.10`
- `pip`
- Environment variable `OPENAI` containing an OpenRouter API key
  - The RAG generator uses OpenAI-compatible APIs via OpenRouter and the `gpt-4o-mini` model.

## Setup (Local)

1. Create and activate a virtual environment (optional but recommended)
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Configure environment variables
   ```bash
   echo "OPENAI=sk-or-xxxxxxxx" > .env
   ```

## Run (Local)

Start the API on port `8080`:

```bash
uvicorn src.Deployment.api_endpoint.main:app --host 0.0.0.0 --port 8080 --reload
```

## Run (Docker)

Build and run the container:

```bash
docker build -t ftl-mmr-api .
docker run --rm -e OPENAI=sk-or-xxxxxxxx -p 8080:8080 ftl-mmr-api
```

The Docker image:

- Uses `python:3.10-slim`
- Copies `src/Schema`, `src/Fine_tuned`, `src/RAG_pipeline`, and the API entrypoint
- Installs `requirements.txt`
- Serves with `uvicorn` on `0.0.0.0:8080`

## API Endpoints

All endpoints accept JSON with the shape:

```json
{ "user_input": "your question or message" }
```

- `POST /Mic_Chat`
  - Answers using RAG over `mental_health.txt`
  - Example:
    ```bash
    curl -X POST http://localhost:8080/Mic_Chat \
      -H "Content-Type: application/json" \
      -d '{"user_input": "How can I manage stress?"}'
    ```

- `POST /Medical_Chat`
  - Answers using fine-tuned `mT5` model (`YeBhoneLin10/FTL-Capstone-v2`)
  - Example:
    ```bash
    curl -X POST http://localhost:8080/Medical_Chat \
      -H "Content-Type: application/json" \
      -d '{"user_input": "I have trouble sleeping—any advice?"}'
    ```

## How It Works

- RAG
  - Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
  - Vector store: FAISS (CPU) if available, falls back to sklearn `NearestNeighbors`
  - Generation: OpenRouter `gpt-4o-mini` via the OpenAI client

- Fine-tuned Chat
  - Wrapper around `simpletransformers.t5` with an `mT5` model
  - Loads from the HF model path `YeBhoneLin10/FTL-Capstone-v2`
  - Uses CUDA automatically if available

## How We Built

<div align="center">

![Our System](/src/docs/our_system.png)

**Figure 1: Overview of Our System**

</div>

## Notes

- First run may download model weights; ensure network access.
- The `OPENAI` key must be valid for OpenRouter; requests are made to `https://openrouter.ai/api/v1`.
- If FAISS is unavailable, similarity search uses sklearn and still works.
- CPU-only environments are supported; GPU is used automatically when present.



## License

This project is for the FTL Myanmar Group 5 capstone. Licensing terms may be defined by the program or institution; consult project maintainers for details.

