# FTL Myanmar Group 5 — MindCare

This repository implements two conversational endpoints for mental health support:

- `Mic_Chat`: Retrieval-Augmented Generation (RAG) over a curated mental health corpus
- `Medical_Chat`: A fine-tuned `mT5` model for medical-style chat responses

Both endpoints are provided via a FastAPI service and can be run locally or in Docker.

## Safety, Intended Users, and Ethical Considerations

### Intended End-Users
This system is designed for:
- General users seeking emotional support or wellness-related guidance.
- People who want basic, supportive conversation about stress, mood, daily challenges, or coping ideas.

**Important:**  
This system is **not a medical tool** and **not a replacement for a licensed mental-health professional**. It does not diagnose conditions or provide medical-level treatment advice.

---

### Boundaries of Guidance
To ensure safe and ethical usage, both chat endpoints follow strict boundaries:
- Provide **general mental-wellness support**, such as coping suggestions, grounding techniques, or emotional validation.
- Avoid medical diagnosis, medication recommendations, or clinical instructions.
- Redirect users who appear to be in crisis to **professional help** rather than continuing the conversation.

---

### Risk & Crisis Detection
Although the system does not perform clinical risk assessment, it includes **basic safety heuristics**:
- Detects sensitive or high-risk phrases (e.g., extreme distress).
- Responds with supportive, non-clinical language.
- Advises the user to seek **professional mental-health support**, trusted family members, or local emergency services.

The model is intentionally prevented from giving instructions or descriptions related to self-harm or other unsafe behavior.

---

### Pre-Assessment Module (Optional Feature)
We plan to include a small, optional pre-screening form in the user flow to:
- Understand the user’s current emotional state
- Ask whether they are receiving professional support
- Determine if they may need immediate referral to licensed professionals

Possible questions:
- “How are you feeling right now?”
- “Are you currently under care of a mental-health professional?”
- “Do you feel safe at the moment?”

High-risk answers are redirected to safe resources instead of generating normal chat responses.

---

### System Limitations
- Not intended for clinical use  
- May provide general suggestions only  
- Cannot detect or diagnose mental-health conditions  
- Crisis detection is basic and non-medical  

Users who require medical or emergency support should always contact licensed professionals.



## Repository Layout

- `src/Deployment/api_endpoint/main.py`: FastAPI app exposing `/Mic_Chat` and `/Medical_Chat`
- `src/RAG_pipeline/`: RAG components (`Embedder`, `VectorStore`, prompt, generation)
- `src/Seq2Seq/medical_chat.py`: Train `mT5` chat wrapper
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

---

### Evaluation Strategy
Traditional accuracy metrics do not apply to mental-health conversational systems.  
Instead, we use **safety-oriented evaluation**:

1. **Response Safety Criteria**
   - Avoid harmful content  
   - Provide emotionally supportive but non-medical guidance  
   - Respect user privacy and avoid hallucinated facts  

2. **Human-in-the-Loop Review**
   - Manual review of sample conversations  
   - Labeling responses as: *safe*, *needs improvement*, *unsafe*  

3. **Harmful-Content Detection**
   - Checking for sensitive keywords  
   - Ensuring RAG sources and model outputs remain within safe boundaries  

This evaluation focuses on **helpfulness, appropriateness, and safety**, not model accuracy.

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

