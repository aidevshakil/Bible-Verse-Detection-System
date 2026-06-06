
# Bible Verse Detection System

This project is a Bible Verse Detection System built with Python. It provides an API and web interface to detect and retrieve Bible verses from user voice.

## Project Structure

```
app/
    api/                # API endpoints
    data/               # Data files (Bible books, versions)
    models/             # Database models
    schemas/            # Pydantic schemas (if used)
    utils/              # Utility functions
    config.py           # Configuration settings
    main.py             # Application entry point
templates/
    index.html          # Web interface template
research/               # Research scripts and data
requirements.txt        # Python dependencies
.env                    # Environment variables
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/marziasu/Bible-Verse-Detection-System.git
   cd Bible-Verse-Detection-System
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create `.env` and update as needed.

5. **Run the application:**
   ```sh
   python app/main.py
   ```

## Features

- Detects Bible verses from voice input.
- Provides API endpoints for integration.
- Web interface for user interaction.
- Supports multiple Bible versions.

## API Endpoints

### `POST /get-verse/`

Retrieves a Bible verse based on user input.

**Request Body:**  
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
  "content": "(JOHN-12:3) Then took Mary a pound of ointment of spikenard, very costly, and anointed the feet of Jesus, and wiped his feet with her hair: and the house was filled with the odour of the ointment. "
}
```

## File Descriptions

- [`app/main.py`](app/main.py): Main entry point for the application.
- [`app/config.py`](app/config.py): Configuration settings.
- [`app/models/`](app/models/): Database models, including [`app/models/bible.py`](app/models/bible.py) and [`app/models/database.py`](app/models/database.py).
- [`app/data/`](app/data/): Contains Bible books and versions data.
- [`templates/index.html`](templates/index.html): Web interface template.

