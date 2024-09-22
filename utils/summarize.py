from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
import typing as t
from helpers.prompt import QUICK_SUMMARY_PROMPT
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter


def quick_summarize(url: str) -> t.Union[str, t.Any]:
    """Quickly summarize a webpage using the stuff summarization chain"""

    loader = WebBaseLoader(url)
    docs = loader.load()

    prompt = PromptTemplate.from_template(QUICK_SUMMARY_PROMPT)

    # Define LLM chain
    llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    result = stuff_chain.run(docs)
    return result


def refined_summarize(url: str) -> t.Union[str, t.Any]:
    """Refined a summary of a webpage by looping over the input documents and iteratively updating its answer using the refine summarization chain"""

    loader = WebBaseLoader(url)
    docs = loader.load()
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    split_docs = text_splitter.split_documents(docs)

    prompt = PromptTemplate.from_template(QUICK_SUMMARY_PROMPT)

    refine_template = (
        "Your job is to produce a final summary\n"
        "We have provided an existing summary up to a certain point: {existing_answer}\n"
        "We have the opportunity to refine the existing summary"
        "(only if needed) with some more context below.\n"
        "------------\n"
        "{text}\n"
        "------------\n"
        "Given the new context, refine the original summary more concise, precise, coherent, insightful and comprehensive"
        "If the context isn't useful, return the original summary."
    )
    refine_prompt = PromptTemplate.from_template(refine_template)

    # Define LLM chain
    llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")

    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key="output_text",
    )
    result = chain({"input_documents": split_docs}, return_only_outputs=True)

    return result["output_text"]





