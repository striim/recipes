import sys
from pgvector.asyncpg import register_vector
import asyncio
import asyncpg
from langchain.embeddings import OpenAIEmbeddings

openai_api_key = "****"
connection_url = "postgres://*****:*****@*****.postgres.database.azure.com:5432/postgres?ssl=disable"
database_password = "****"  # @param {type:"string"}
host_name = "*******"  # @param {type:"string"}
database_name = "******"  # @param {type:"string"}
database_user = "******"  # @param {type:"string"}
min_price = 10
max_price = 100

matches = []


##################################
# Accepts user query for searching a product
##################################

embeddings_service = OpenAIEmbeddings(openai_api_key=f"{openai_api_key}",model="text-embedding-ada-002")

async def main(user_query):
        # Create connection to Azure PG database.
        conn = await asyncpg.connect(user=f"{database_user}", password=f"{database_password}",
                                 database=f"{database_name}", host=f"{host_name}", ssl="disable")

        await register_vector(conn)
        similarity_threshold = 0.7
        num_matches = 5

        ##################################
        # Converts the Query to embeddings using OpenAI
        ##################################
        qe = embeddings_service.embed_query(user_query)

        ##################################
        # Performs similarity search using pg vector extension functionality
        ##################################

        results = await conn.fetch(
            """
                            WITH vector_matches AS (
                              SELECT product_id, 1 - (embedding <=> $1) AS similarity
                              FROM aidemo.products
                              WHERE 1 - (embedding <=> $1) > $2
                              ORDER BY similarity DESC
                              LIMIT $3
                            )
                            SELECT product_name, list_price, description FROM aidemo.products
                            WHERE product_id IN (SELECT product_id FROM vector_matches)
                            AND list_price >= $4 AND list_price <= $5
                            """,
            qe,
            similarity_threshold,
            num_matches,
            min_price,
            max_price,
        )

        if len(results) == 0:
            raise Exception("Did not find any results. Adjust the query parameters.")

        for r in results:
            # Collect the description for all the matched similar toy products.
            matches.append(
                f"""The name of the toy is {r["product_name"]}.
                          The price of the toy is ${round(r["list_price"], 2)}.
                          Its description is below:
                          {r["description"]}."""
            )
        await conn.close()


from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from IPython.display import display, Markdown

def llmpart(user_query, matchingProducts):
    llm = OpenAI(openai_api_key=f"{openai_api_key}", temperature=0, model_name = 'gpt-3.5-turbo-instruct')
    ##################################
    # Returns a response generated using LLM service with the top matching product details
    ##################################
    map_prompt_template = """
              You will be given a detailed description of a toy product.
              This description is enclosed in triple backticks (```).
              Using this description only, extract the name of the toy,
              the price of the toy and its features.

              ```{text}```
              SUMMARY:
              """
    map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])
    combine_prompt_template = """
                You will be given a detailed description different toy products
                enclosed in triple backticks (```) and a question enclosed in
                double backticks(``).
                Select one toy that is most relevant to answer the question.
                Using that selected toy description, answer the following
                question in as much detail as possible.
                You should only use the information in the description.
                Your answer should include the name of the toy, the price of the toy
                and its features. Your answer should be less than 200 words.
                Your answer should be in Markdown in a numbered list format.


                Description:
                ```{text}```


                Question:
                ``{user_query}``


                Answer:
                """
    combine_prompt = PromptTemplate(
        template=combine_prompt_template, input_variables=["text", "user_query"]
    )
    docs = [Document(page_content=t) for t in matchingProducts]

    chain = load_summarize_chain(
        llm, chain_type="map_reduce", map_prompt=map_prompt, combine_prompt=combine_prompt
    )

    answer = chain.run(
        {
            "input_documents": docs,
            "user_query": user_query,
        }
    )
    return(answer);

import gradio as gr

def greet(user_query):
    mainCoro = asyncio.run(main(user_query));
    answer = llmpart(user_query, matches[-5:])
    return(str(answer))
head = """
    <link rel="icon" href="https://www.striim.com/wp-content/uploads/2023/05/Striim-Logo-Icon.svg">
"""
css = """
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

gradio-app {
    background: #050529 !important;
    background-image: url(https://media.striim.com/wp-content/uploads/2024/04/08020349/Group.png) !important;
    background-position: top center !important;
    background-position-x: right !important;
    background-position-y: top !important;
    background-repeat: no-repeat !important;
}
.gradio-container-4-25-0 .prose h1, .gradio-container-4-25-0 .prose p {
    color: white !important;
}

#component-2:before {
    content: url('https://www.striim.com/wp-content/uploads/2020/09/Logo-White.png'); 
    display: flex;
    align-items: center;
    justify-content: space-around;
    margin: 25px 0px;
}

#component-11 {
    width: 78px;
    display: flex;
    align-items: center;
    flex-direction: row;
    flex-wrap: nowrap;
}

.secondary.svelte-cmf5ev {
    font-size: 14px !important;
    font-weight: 800 !important;
    fill: #07072a !important;
    background-color: #07072a !important;
    border-style: solid !important;
    border-width: 01px 01px 01px 01px !important;
    border-radius: 30px 30px 30px 30px !important;
    padding: 9px 12px !important;
}

 #component-11 .primary.svelte-cmf5ev {
    font-size: 14px !important;
    font-weight: 800 !important;
    color: #07072a !important;
    border-style: solid !important;
    border-width: 01px 01px 01px 01px !important;
    border-radius: 30px 30px 30px 30px !important;
    padding: 9px 12px !important;
}

#component-11 .primary.svelte-cmf5ev {
    border: #00A8F0;
    background: #00A8F0;
    color: #050529;
}

.panel.svelte-vt1mxs {
    background: #050529 !important;
}

footer {
    display: none !important;
}
"""
title='Striim AI Realtime RAG demo'
description='Please enter a search query in natural language and hit submit. Top matching product with similar description will be displayed'

demo = gr.Interface(
greet,
gr.Textbox(label="Search for a product"),
[gr.Textbox(label="Result :")],
allow_flagging="never",
head=head,
title=title,
css=css,
description=description
)

demo.launch(show_api=False, debug=True, share=True)
