# Video Brief Writer — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9163`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/video-brief-writer.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `Creator / Video Strategy`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Topic/URL → video production brief
- Suite: `Media Creator Suite`

## Deep features applied

- audience research
- hook lab
- retention graph
- shot list
- B-roll ideas
- title/thumbnail tests
- SEO tags
- repurposing pack

## Customization controls

- `execution_mode` — Execution mode (select)
- `platform` — platform (select)
- `niche` — niche (text)
- `duration` — duration (text)
- `creator_style` — creator style (select)
- `language` — language (select)
- `cta_goal` — CTA goal (text)
- `competitor_references` — competitor references (text)
- `production_budget` — production budget (text)
- `output_format` — output format (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `topic` — Topic (text) required
- `url` — URL (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Creator Production Studio** pattern.

**UX workflow:** Brief → script/asset plan → timeline → publishing package

**Domain components:**
- Creative brief canvas
- Storyboard/timeline
- Transcript or caption editor
- Platform publish checklist
- Asset quality scorecards

**Quick actions:**
- Build storyboard
- Create caption package
- Check hook/thumbnail
- Prepare publishing checklist

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
