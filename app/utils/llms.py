import os
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_openai import ChatOpenAI
from typing import Dict, List 

from app.config import settings  
from app.schemas.bible_schema import UserInput

response_schemas = [
    ResponseSchema(name="translation", description="The Bible translation (e.g., KJV, ASV, WEB)"),
    ResponseSchema(name="translation_id", description="The id of translation (e.g., 685d1470fe4d5c3b-01, c89622d31b60c444-02)"),
    ResponseSchema(name="book", description="The book of the Bible (e.g., John, James)"),
    ResponseSchema(name="book_id", description="The id of the book (e.g., GEN, JDG, 1JN )"),
    ResponseSchema(name="chapter", description="The chapter number (e.g., 3, 2)"),
    ResponseSchema(name="verse", description="The verse number (e.g., 16, 10)"),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()


prompt_template = PromptTemplate(
    template="""
    You are tasked with extracting and adjusting Bible references based on the following user input. The input contains a translation, book, chapter, and verse. 
    
    Use the list of available Bible versions below to select the most appropriate one. 
    Match by abbreviation, name, or language mentioned by the user, and return its exact ID.

    Available Bible Versions(here translation and translation_id provided):
    {bible_versions}
    Also provide the book name and book_id :
    {bible_book_ids}

    Current Reference:
    - Translation: {translation}
    - Translation_id: {translation_id}
    - Book: {book}
    - Book ID: {book_id}
    - Chapter: {chapter}
    - Verse: {verse}

    User Query: {user_query}

    Instructions:
    1. If the user mentions the next verse (e.g., "next verse", "next"), increase the current verse by 1. If the current verse is the last in the chapter, increase the chapter number instead, and if the book ends, go to the next book.
    2. If the user mentions the previous verse (e.g., "previous verse", "prev"), decrease the current verse by 1. If the current verse is the first in the chapter, decrease the chapter number instead, and if the chapter is the first in the book, go to the previous book.
    3. If the user provides a specific verse reference (e.g., "John 3:17", "John chapter 3 and verse 17"), adjust the reference to match that exact verse.
    4. If the user provides the verse text only (e.g., "For God so loved the world"), extract the book, chapter, and verse from the text.
    5. If the user does not provide a translation, use the default translation "KJV" with ID "bba9f40183526463-01".
    6. If the user does not provide a book, chapter, or verse, use the current reference as a fallback.

    **Critical Adjustments**:
    - Ensure the verse number and chapter are valid. If the verse is out of range for the chapter:
        - If the verse exceeds the number of verses in the chapter, move to the next chapter and set the verse to 1.
        - If the verse is less than 1, move to the previous chapter and set the verse to the last verse of that chapter.
        - If the chapter number exceeds the total chapters in the book, adjust to the last chapter.
    - Always ensure the provided chapter and verse exist within the selected book.
    
    {format_instructions}
    """,
    input_variables=["translation", "book", "chapter", "verse", "user_query", "bible_versions"],
    partial_variables={"format_instructions": format_instructions}
)


llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY
)

def extract_bible_reference(user_input: UserInput, bible_versions:List[Dict], bible_book_ids: Dict):
    """
    Extracts the Bible reference from the user input using a language model.
    
    Args:
        user_input (str): The input string containing the Bible reference.
        
    Returns:
        dict: A dictionary containing the extracted translation, book, chapter, and verse.
    """
    prompt = prompt_template.format(
        translation=user_input.translation,
        translation_id = user_input.translation_id,
        book=user_input.book,
        book_id = user_input.book_id,
        chapter=user_input.chapter,
        verse=user_input.verse,
        user_query=user_input.text,
        bible_versions = bible_versions,
        bible_book_ids = bible_book_ids
    )
    response = llm.invoke(prompt)
    json_output = output_parser.parse(response.content)
    
    return json_output
