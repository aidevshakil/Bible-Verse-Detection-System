
# Bible Verse Detection System

A Python-based system that detects and retrieves Bible verses from user voice input. Provides a REST API and web interface supporting multiple Bible translations.

**Author:** [aidevshakil](https://github.com/aidevshakil)  
**Repository:** [https://github.com/aidevshakil/Bible-Verse-Detection-System](https://github.com/aidevshakil/Bible-Verse-Detection-System)

---

## Project Structure

```
app/
    api/                # API endpoints
    data/               # Data files (Bible books, versions)
    schemas/            # Pydantic schemas
    utils/              # Utility functions (LLM integration)
    config.py           # Configuration settings
    main.py             # Application entry point
templates/
    index.html          # Web interface
requirements.txt        # Python dependencies
setup.py                # Package setup
.env                    # Environment variables (not committed)
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/aidevshakil/Bible-Verse-Detection-System.git
   cd Bible-Verse-Detection-System
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in the required values.

5. **Run the application:**
   ```sh
   python app/main.py
   ```

## Features

- Detects Bible verses from voice input using LLM integration.
- REST API endpoints for programmatic access.
- Web interface for interactive use.
- Supports multiple Bible translations/versions.
- Navigate to next/previous verses in context.

## API Endpoints

### `POST /get-verse/`

Retrieves a Bible verse based on user input text.

**Request — fetch a specific verse:**
```json
{
  "translation": "",
  "translation_id": "",
  "book": "",
  "book_id": "",
  "chapter": "",
  "verse": "",
  "text": "John chapter 12 verse 2"
}
```

**Response:**
```json
{
  "book": "John",
  "book_id": "JHN",
  "translation": "KJV",
  "translation_id": "de4e12af7f28f599-01",
  "chapter": "12",
  "verse": "2",
  "content": "(JOHN-12:2) There they made him a supper; and Martha served: but Lazarus was one of them that sat at the table with him."
}
```

**Request — navigate to next verse:**
```json
{
  "translation": "KJV",
  "translation_id": "de4e12af7f28f599-01",
  "book": "John",
  "book_id": "JHN",
  "chapter": "12",
  "verse": "2",
  "text": "next verse"
}
```

**Response:**
```json
{
  "book": "John",
  "book_id": "JHN",
  "translation": "KJV",
  "translation_id": "de4e12af7f28f599-01",
  "chapter": "12",
  "verse": "3",
  "content": "(JOHN-12:3) Then took Mary a pound of ointment of spikenard, very costly, and anointed the feet of Jesus, and wiped his feet with her hair: and the house was filled with the odour of the ointment."
}
```

## File Descriptions

- [app/main.py](app/main.py) — Application entry point.
- [app/config.py](app/config.py) — Configuration settings.
- [app/api/](app/api/) — Versioned API route definitions.
- [app/schemas/bible_schema.py](app/schemas/bible_schema.py) — Pydantic request/response schemas.
- [app/utils/llms.py](app/utils/llms.py) — LLM integration for verse detection.
- [app/data/](app/data/) — Bible book names and version data files.
- [templates/index.html](templates/index.html) — Web interface template.

## License

This project is open source. See the repository for details.
