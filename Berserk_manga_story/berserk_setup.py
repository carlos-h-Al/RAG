from spacy.lang.en import English
from PyPDF2 import PdfReader
import chromadb
import re

# path to the PDF file
FILE = '../files/Guts.pdf'


# format the name of the file to cut off any excessive characters
def name_formatter(name: str) -> str:
    ''' ../files/Guts.pdf --> Guts '''
    new_name = name.split('/')
    new_name = new_name[-1].split('.')
    new_name = new_name[0]
    return new_name


# creates a series of sentences chunks from a list of sentences
def chunkinator(original_list: list[str], size: int, div_list=[]) -> list:
    divided_list = []
    new_list = []
    if len(original_list) > (size - 1):
        for i in range(size):
            new_list.append(original_list[i])
        # join 
        new_list = ' '.join(new_list)
        if div_list == []:
            divided_list.append(new_list)
        else:
            div_list.append(new_list)
    else:
        for item in original_list:
            new_list.append(item)
        # join
        new_list = ' '.join(new_list)
        if div_list == []:
            divided_list.append(new_list)
        else:
            div_list.append(new_list)
    
    original_list = original_list[size:]

    if len(new_list) <= size and len(original_list) == 0:
        return div_list
    else:
        if div_list == []:
            return chunkinator(original_list, size, div_list=divided_list)
        else:
            return chunkinator(original_list, size, div_list=div_list)


# cleans the text
def text_formatter(text: str) -> str:
    cleaned_text = text.replace('\n', ' ').strip()
    cleaned_text = cleaned_text.replace('[', '').strip()
    cleaned_text = cleaned_text.replace(']', '').strip()
    cleaned_text = cleaned_text.replace('•', '').strip()
    cleaned_text = cleaned_text.replace('   ', '').strip()
    cleaned_text = cleaned_text.replace('  ', ' ').strip()
    cleaned_text, n = re.subn('[0-9]', '', cleaned_text)
    return cleaned_text


# extract text from PDF document
def get_pdf_text(pdf: str) -> str:
    pages_and_text = []
    text_chunks = []
    metadata = []

    nlp = English()
    nlp.add_pipe('sentencizer')
    pdf_reader = PdfReader(pdf)

    for page, raw_text in enumerate(pdf_reader.pages):
        text = raw_text.extract_text()
        text = text_formatter(text)
        sentences = list(nlp(text).sents)
        sentences = [str(sentence) for sentence in sentences]
        pages_and_text.append({'document': name_formatter(pdf),
                                'page_number': page + 1,
                                'sentences' : sentences,
                                'text': text})
        
    for item in pages_and_text:
        chunks = chunkinator(item['sentences'], 4)
        for chunk in chunks:
            text_chunks.append(chunk)
            metadata.append({'document': item['document'],
                            'page_number': item['page_number']})
            
    return text_chunks, metadata


def main():
    corpus, metadata = get_pdf_text(FILE)

    # created distinct ids for the ChromaDB
    ids = []
    for num in range(len(corpus)):
        ids.append(str(num))

    # creates a persistent ChromaDB and adds the text chunks, embeddings, metadata, and ids
    client = chromadb.PersistentClient(path='stores')
    collection = client.create_collection(name='vector')
    collection.add(
        documents=corpus,
        metadatas=metadata,
        ids=ids
    )


if __name__ == '__main__':
    main()
