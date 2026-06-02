## AI-Powered Wedding Photo Organizer

Production-ready portfolio project for professional photographers.  
The application analyzes wedding images with Gemini Vision, stores metadata in SQLite, detects duplicates/blurry images, organizes files by category, and supports natural language search from Gradio.

## Tech Stack
- Python 3.11
- Gradio
- Gemini Vision (`google-generativeai`)
- Pillow + OpenCV + ImageHash
- SQLite
- Pydantic + Pandas

## Folder Structure
```text
Wedding_Photo_Organizer/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── config/
│   ├── llm/
│   ├── image_processing/
│   ├── metadata/
│   ├── organizer/
│   ├── search/
│   ├── database/
│   ├── logging/
│   └── utils/
├── input_photos/
├── organized_photos/
├── metadata/
├── database/
├── logs/
├── assets/
└── tests/
```

## Installation Guide
1. Install Python 3.11
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy environment template:
   ```bash
   copy .env.example .env
   ```
5. Add your Gemini key to `.env`

## API Key Setup Guide
1. Get Gemini API key from Google AI Studio
2. Update `.env`:
   ```env
   GEMINI_API_KEY=your_real_key
   GEMINI_MODEL=gemini-1.5-flash
   ```

## Run the Application
```bash
python app.py
```
Default UI: `http://localhost:7860`

## Core Workflow
1. Upload photos into `input_photos/` via UI
2. Analyze images with Gemini and CV engines
3. Persist metadata into SQLite (`database/wedding_photos.db`)
4. Organize into category folders under `organized_photos/`
5. Search with natural language query
6. Review analytics, metadata, and logs

## Architecture Explanation
- **Configuration Layer**: `src/config/config.py` handles typed env config and paths.
- **LLM Layer**: `src/llm/gemini_client.py` + retries for resilient image analysis.
- **Image Processing Layer**: duplicate and blur detection services.
- **Metadata Layer**: Pydantic contracts unify app-wide data model.
- **Database Layer**: SQLite repository for metadata persistence and querying.
- **Orchestration Layer**: `src/pipeline.py` coordinates batch processing.
- **Presentation Layer**: Gradio tabs in `app.py`.

## Design Decisions and Trade-offs
- SQLite chosen for local-first simplicity and interview-friendly reproducibility.
- Thread pool used for throughput while keeping implementation maintainable.
- JSON metadata file retained as fallback backup while SQLite is primary store.
- Rule-based query matching is fast and deterministic, but less semantic than embeddings.

## Scalability Discussion
- Add job queue (Celery/RQ) for very large weddings (100k+ images).
- Partition metadata by event and shoot date for faster queries.
- Move binary assets to object storage (S3/GCS) while retaining SQL metadata.
- Replace lexical search with embedding search for richer natural language behavior.
- Add API worker pool and request-level rate limiting for Gemini quotas.

## Testing
Run:
```bash
pytest -q
```

Included:
- Duplicate detection tests
- Blur detection tests
- Organizer tests
- Search tests
- Metadata repository tests

## Interview Preparation
### Architecture Summary
Modular clean architecture separates AI inference, CV quality checks, metadata persistence, and UI orchestration, enabling independent evolution and testing.

### End-to-End Explanation
Upload -> batch scan -> Gemini extraction -> duplicate/blur scoring -> categorization -> SQLite persistence -> folder organization -> NL search + dashboard.

### Resume Project Description
Built a production-ready AI Wedding Photo Organizer (Python, Gradio, Gemini Vision, SQLite) that automated metadata extraction, quality screening, duplicate detection, folder organization, and natural language retrieval for high-volume photography workflows.

### Sample Interview Q&A
1. **Why SQLite first?**  
   Fast local deployment, zero external infra, ideal for portfolio reproducibility.
2. **How do you handle LLM instability?**  
   Strict JSON prompt contracts, retries with backoff, and safe fallback parsing.
3. **How would you scale this?**  
   Queue-based parallel workers, storage decoupling, embedding search, and cloud deployment.
4. **How is quality measured?**  
   Perceptual hash similarity for duplicates and Laplacian variance for blur quality.

## Future Enhancements
- Face clustering with non-dlib alternatives
- Batch scheduling and background job monitoring
- Cloud deployment with auth and user workspaces
- Exportable curation reports and slideshow generation

