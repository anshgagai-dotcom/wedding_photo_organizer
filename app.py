from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import gradio as gr

from src.bootstrap import bootstrap_application
from src.database.repository import MetadataRepository
from src.logging.logging_setup import get_logger
from src.metadata.store import MetadataStore
from src.pipeline import WeddingPhotoPipeline
from src.search.query_engine import SearchEngine


LOGGER = get_logger(__name__)
SETTINGS = bootstrap_application()
STORE = MetadataStore(SETTINGS.metadata_file)
REPOSITORY = MetadataRepository()
SEARCH_ENGINE = SearchEngine()
PIPELINE: WeddingPhotoPipeline | None = None


def _get_pipeline() -> WeddingPhotoPipeline:
    global PIPELINE
    if PIPELINE is None:
        PIPELINE = WeddingPhotoPipeline(settings=SETTINGS, metadata_store=STORE)
    return PIPELINE


def _save_uploaded_files(files: list[Any] | None) -> str:
    if not files:
        return "No files uploaded."

    saved = 0
    SETTINGS.input_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
        source = Path(file.name)
        destination = SETTINGS.input_dir / source.name
        destination.write_bytes(source.read_bytes())
        saved += 1
    return f"Saved {saved} files to {SETTINGS.input_dir}."


def _analyze_photos(progress: gr.Progress = gr.Progress(track_tqdm=True)) -> tuple[str, dict[str, int], str]:
    def _report(done: int, total: int) -> None:
        progress(done / total, desc=f"Analyzing photo {done}/{total}")

    try:
        pipeline = _get_pipeline()
    except ValueError as exc:
        return (f"Configuration error: {exc}", {}, "[]")

    result = pipeline.analyze_all(progress_cb=_report)
    return (
        f"Analyzed {result.total_analyzed} photos.",
        result.category_distribution,
        json.dumps([item.model_dump() for item in result.sample], indent=2),
    )


def _organize_photos() -> str:
    records = STORE.load()
    if not records:
        return "No analyzed metadata found. Run Analyze Photos first."
    count = _get_pipeline().organize_all()
    return f"Organized {count} photos into {SETTINGS.organized_dir}."


def _search_photos(query: str) -> list[list[str]]:
    if not query.strip():
        return []
    db_matches = REPOSITORY.search(query)
    if db_matches:
        matches = db_matches
    else:
        records = STORE.load()
        matches = SEARCH_ENGINE.search(records, query)
    return [
        [m.path, m.primary_category, m.event_type, ", ".join(m.tags), m.scene_description, f"{m.confidence_score:.2f}"]
        for m in matches
    ]


def _view_metadata() -> str:
    records = STORE.load()
    return json.dumps([record.model_dump() for record in records], indent=2)


def _view_analytics() -> tuple[str, dict[str, int]]:
    analytics = REPOSITORY.analytics()
    headline = (
        f"Total: {analytics.get('total_photos', 0)} | "
        f"Duplicates: {analytics.get('duplicates', 0)} | "
        f"Blurry: {analytics.get('blurry', 0)} | "
        f"Avg confidence: {analytics.get('avg_confidence', 0.0):.2f}"
    )
    top_categories = analytics.get("top_categories", {})
    return headline, top_categories


def _read_logs() -> str:
    log_path = SETTINGS.logs_dir / "app.log"
    if not log_path.exists():
        return "No logs generated yet."
    return log_path.read_text(encoding="utf-8")


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="AI Wedding Photo Organizer") as demo:
        gr.Markdown("# AI-Powered Wedding Photo Organizer")
        gr.Markdown("Production workflow for photographers using Gemini Vision + Python.")

        with gr.Tab("Upload Photos"):
            uploader = gr.File(file_count="multiple", file_types=["image"])
            upload_status = gr.Textbox(label="Upload Status")
            upload_btn = gr.Button("Save Photos")
            upload_btn.click(fn=_save_uploaded_files, inputs=[uploader], outputs=[upload_status])

        with gr.Tab("Analyze Photos"):
            analyze_btn = gr.Button("Analyze All Photos")
            analyze_summary = gr.Textbox(label="Summary")
            analyze_distribution = gr.Label(label="Category Distribution")
            analyze_sample = gr.Code(label="Sample Metadata", language="json")
            insights_btn = gr.Button("Refresh Insights")
            insights_headline = gr.Textbox(label="Insights Summary")
            insights_categories = gr.Label(label="Top Categories")
            analyze_btn.click(
                fn=_analyze_photos,
                inputs=[],
                outputs=[analyze_summary, analyze_distribution, analyze_sample],
            )
            insights_btn.click(fn=_view_analytics, inputs=[], outputs=[insights_headline, insights_categories])

        with gr.Tab("Organize Photos"):
            organize_btn = gr.Button("Organize into Folders")
            organize_result = gr.Textbox(label="Organization Result")
            organize_btn.click(fn=_organize_photos, inputs=[], outputs=[organize_result])

        with gr.Tab("Search Photos"):
            query = gr.Textbox(label="Search Query", placeholder="Show bride photos")
            search_btn = gr.Button("Search")
            search_results = gr.Dataframe(
                headers=["Path", "Category", "Event", "Tags", "Scene", "Confidence"],
                datatype=["str", "str", "str", "str", "str", "str"],
                label="Matching Photos",
            )
            search_btn.click(fn=_search_photos, inputs=[query], outputs=[search_results])

        with gr.Tab("View Metadata"):
            metadata_btn = gr.Button("Refresh Metadata")
            metadata_view = gr.Code(language="json", label="Metadata Records")
            metadata_btn.click(fn=_view_metadata, inputs=[], outputs=[metadata_view])

        with gr.Tab("System Logs"):
            logs_btn = gr.Button("Refresh Logs")
            logs_view = gr.Textbox(lines=25, label="Application Logs")
            logs_btn.click(fn=_read_logs, inputs=[], outputs=[logs_view])

    return demo


if __name__ == "__main__":
    LOGGER.info("Starting AI Wedding Photo Organizer")
    build_ui().launch(server_name=SETTINGS.host, server_port=SETTINGS.port, show_error=True)
