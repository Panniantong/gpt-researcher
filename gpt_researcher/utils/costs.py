import tiktoken

# Per OpenAI Pricing Page: https://openai.com/api/pricing/
ENCODING_MODEL = "o200k_base"
INPUT_COST_PER_TOKEN = 0.000005
OUTPUT_COST_PER_TOKEN = 0.000015
IMAGE_INFERENCE_COST = 0.003825
EMBEDDING_COST = 0.02 / 1000000 # Assumes new ada-3-small


# Cost estimation is via OpenAI libraries and models. May vary for other models
def estimate_llm_cost(input_content: str, output_content: str) -> float:
    encoding = tiktoken.get_encoding(ENCODING_MODEL)
    input_tokens = encoding.encode(input_content)
    output_tokens = encoding.encode(output_content)
    input_costs = len(input_tokens) * INPUT_COST_PER_TOKEN
    output_costs = len(output_tokens) * OUTPUT_COST_PER_TOKEN
    return input_costs + output_costs


def estimate_embedding_cost(model, docs):
    # Handle None or empty docs
    if not docs:
        return 0.0
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to a default encoding if model is not recognized
        encoding = tiktoken.get_encoding(ENCODING_MODEL)
    
    total_tokens = 0
    for doc in docs:
        if doc is not None:
            try:
                total_tokens += len(encoding.encode(str(doc)))
            except Exception as e:
                # Log the error but continue processing other docs
                print(f"Warning: Error encoding document: {e}")
                continue
    
    return total_tokens * EMBEDDING_COST

