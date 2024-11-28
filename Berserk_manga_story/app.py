from htmlTemplates import css, bot_template, user_template
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import streamlit as st
import chromadb


# process user input and generate an answer using LangChain
def handle_userinput(user_question, model, collection):
    template = '''
    Answer the question below.

    Here is the answer: {info} 

    Question: {question}

    Answer: 
    '''

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    # query the database to perform vector similarity search
    results = collection.query(
    query_texts=[user_question],
    n_results=4
    )

    # concatenates the top 4 results to create a single string 
    res = ''
    for r in results['documents'][0]:
        res += r

    # generates the answer to the query
    result = chain.invoke({'question': user_question, 'info': res})

    # write query and answer in the Streamlit app using the given CSS
    st.write(user_template.replace('{{MSG}}', user_question), unsafe_allow_html=True)
    st.write(bot_template.replace('{{MSG}}', result), unsafe_allow_html=True)


def main():
    # fetch the ChromaBD and the relevant collection
    client = chromadb.PersistentClient(path='stores')
    collection = client.get_collection(name='vector')

    st.set_page_config(page_title='Berserk', page_icon=':crescent_moon:')
    st.write(css, unsafe_allow_html=True)

    # model used to generate the answer - downloaded and running locally on the machine
    model = OllamaLLM(model='llama3')

    # website cover image and title
    st.image('https://upload.wikimedia.org/wikipedia/commons/f/f1/Berserk_anime_logo.png')
    st.header('Berserk - by Kentaro Miura')
    instr = 'Ask a question about Berserk story and characters:'

    with st.form('chat_input_form'):
        # Create two columns
        col1, col2 = st.columns([4,1]) 

        with col1:
            user_question = st.text_input(
                instr,
                value=instr,
                placeholder=instr,
                label_visibility='collapsed')

        with col2:
            submitted = st.form_submit_button('Chat')

    if user_question and submitted:
        handle_userinput(user_question, model, collection)


if __name__ == '__main__':
    main()
