import re
import httpx
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.config import settings
from app.utils.llms import extract_bible_reference
from app.schemas.bible_schema import UserInput, ModelOutput
    
router = APIRouter(prefix="/bible")

try:
    with open("app/data/bible-versions.txt", "r", encoding="utf-8") as file:
        bible_versions = json.load(file)

    with open("app/data/bible-book.txt", "r", encoding="utf-8") as file:
        bible_book_ids = json.load(file)
except FileNotFoundError as e:
    raise HTTPException(status_code=500, detail=f"Configuration files not found: {str(e)}")

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "api-key": settings.BIBLE_API_KEY
}


@router.post("/get-verse/", response_model=ModelOutput)
async def get_verse(input_text: UserInput):
    try:
        res = extract_bible_reference(input_text, bible_versions, bible_book_ids)
        
        book = res.get('book', '')
        book_id = res.get('book_id', '')
        translation = res.get('translation', '')
        translation_id = res.get("translation_id", '')
        chapter_number = res.get('chapter', '')
        verse_number = res.get('verse', '')
        
        # Validate required fields
        if not all([book_id, translation_id, chapter_number, verse_number]):
            return ModelOutput(
                book=book,
                book_id=book_id,
                translation=translation,
                translation_id=translation_id,
                chapter=chapter_number,
                verse=verse_number,
                content="Invalid verse reference. Please check the book, chapter, and verse numbers.",
            )
        
        # Check if Bible API key is configured
        if not settings.BIBLE_API_KEY:
            return ModelOutput(
                book=book,
                book_id=book_id,
                translation=translation,
                translation_id=translation_id,
                chapter=chapter_number,
                verse=verse_number,
                content=f"Bible API key not configured. Detected reference: {book} {chapter_number}:{verse_number}",
            )
        
        url = f"https://api.scripture.api.bible/v1/bibles/{translation_id}/verses/{book_id}.{chapter_number}.{verse_number}"

        # Configure timeout and retry settings
        timeout = httpx.Timeout(10.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    try:
                        content = response.json()['data']['content']
                        content_text = re.sub(r'<.*?>', '', content) 
                        content_text = re.sub(r'^\s*\d+[\.\):]?\s*', '', content_text)
                        content_text = f"{res['book'].title()} {chapter_number}:{verse_number} ({translation}) \n\n{content_text}"
                        
                        return ModelOutput(
                            book=book,
                            book_id=book_id,
                            translation=translation,
                            translation_id=translation_id,
                            chapter=chapter_number,
                            verse=verse_number,
                            content=content_text,
                        )
                    except (KeyError, json.JSONDecodeError) as e:
                        print(f"Error parsing API response: {e}")
                        return ModelOutput(
                            book=book,
                            book_id=book_id,
                            translation=translation,
                            translation_id=translation_id,
                            chapter=chapter_number,
                            verse=verse_number,
                            content="Error parsing verse content from API response.",
                        )
                else:
                    # Handle different HTTP status codes
                    if response.status_code == 404:
                        error_msg = f"Verse not found: {book} {chapter_number}:{verse_number}"
                    elif response.status_code == 401:
                        error_msg = "API authentication failed. Please check your API key."
                    elif response.status_code == 429:
                        error_msg = "API rate limit exceeded. Please try again later."
                    else:
                        error_msg = f"API error (Status {response.status_code}): Unable to fetch verse."
                    
                    return ModelOutput(
                        book=book,
                        book_id=book_id,
                        translation=translation,
                        translation_id=translation_id,
                        chapter=chapter_number,
                        verse=verse_number,
                        content=error_msg,
                    )
                    
            except httpx.ConnectTimeout:
                return ModelOutput(
                    book=book,
                    book_id=book_id,
                    translation=translation,
                    translation_id=translation_id,
                    chapter=chapter_number,
                    verse=verse_number,
                    content="Connection timeout. The Bible API is currently unavailable. Please try again later.",
                )
            except httpx.RequestError as e:
                return ModelOutput(
                    book=book,
                    book_id=book_id,
                    translation=translation,
                    translation_id=translation_id,
                    chapter=chapter_number,
                    verse=verse_number,
                    content=f"Network error: Unable to connect to Bible API. Please check your internet connection.",
                )
            except Exception as e:
                print(f"Unexpected error in API call: {e}")
                return ModelOutput(
                    book=book,
                    book_id=book_id,
                    translation=translation,
                    translation_id=translation_id,
                    chapter=chapter_number,
                    verse=verse_number,
                    content="An unexpected error occurred while fetching the verse.",
                )
                
    except Exception as e:
        print(f"Error in get_verse endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
