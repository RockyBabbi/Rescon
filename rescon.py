  
    import os  
    from openai import AzureOpenAI  
    
    endpoint = os.getenv("ENDPOINT_URL", "https://bc-openai.openai.azure.com/")  
    deployment = os.getenv("DEPLOYMENT_NAME", "gpt4vision")  
    search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://bc-ai-search-eastus.search.windows.net")  
    search_key = os.getenv("SEARCH_KEY", "put your Azure AI Search admin key here")  
    search_index = os.getenv("SEARCH_INDEX_NAME", "test-demo")  
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")  
    
    # Initialize Azure OpenAI client with key-based authentication
    client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version="2024-05-01-preview",  
    )  
      
    # Prepare the chat prompt  
    chat_prompt = [
    {
        "role": "system",
        "content": "Your goal is to generate questions from a user on a given product.\n\nYou are given a context, a persona and a product.\nThe context describes where the user is accessing the product.\nThe persona describes the user themselves.\nThe product is the item the user is interested in.\n\n# instructions\n- empathize with the user based on the given persona\n- imagine a situation grounded in the given context where the user would access the product\n- generate {{count}} question(s) this user would have on this product\n- return the {{count}} question(s) in JSONL format `{\"question\":\"[QUESTION]\"}`\n"
    },
    {
        "role": "user",
        "content": "- context: {{context}}\n- persona: {{persona}}\n- product: {{product}}\n"
    },
    {
        "role": "assistant",
        "content": ""
    }
]  
    
    # Include speech result if speech is enabled  
    speech_result = chat_prompt  
    
    # Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,  
        messages=speech_result,  
        past_messages=10,  
        max_tokens=800,  
        temperature=0.45,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False  
    )  
      
 ,
      extra_body={
        "data_sources": [{
          "type": "azure_search",
          "parameters": {
            "endpoint": f"{search_endpoint}",
            "index_name": "test-demo",
            "semantic_configuration": "default",
            "query_type": "vector_semantic_hybrid",
            "fields_mapping": {},
            "in_scope": True,
            "role_information": "Your goal is to generate questions from a user on a given product.\n\nYou are given a context, a persona and a product.\nThe context describes where the user is accessing the product.\nThe persona describes the user themselves.\nThe product is the item the user is interested in.\n\n# instructions\n- empathize with the user based on the given persona\n- imagine a situation grounded in the given context where the user would access the product\n- generate {{count}} question(s) this user would have on this product\n- return the {{count}} question(s) in JSONL format `{\"question\":\"[QUESTION]\"}`\n",
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
              "type": "api_key",
              "key": f"{search_key}"
            },
            "embedding_dependency": {
              "type": "deployment_name",
              "deployment_name": "text-embedding-ada-002"
            }
          }
        }]
      }   print(completion.to_json())  
    
