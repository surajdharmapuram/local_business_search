import json
import ollama
import sys

def prompt(query):
    return f"""
    A user is trying to find local businesses that satisfy the query in quotes
    below.

    "{query}"

    To help with this, extract the following information from the query in
    quotes above:
    1. Name of a specific business being searched for, if any
    2. Product or list of products being searched for, if any
    3. Types of businesses being searched for, if any. This is the type of store
       or business where the user might find the product(s) that they're
       looking for.
    4. City that the user is searching in, if any
    5. Any other context or descriptive information that would be useful in
       enriching the search query.

    If there isn't enough information in the search query for a field, leave it
    empty.
    """

def parse(query):
    print(f"Query: {query}")
    response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert content analyzer, specializing in analyzing search queries and extracting structure from it",
                },
                {
                    "role": "user",
                    "content": f"{prompt(query)}",
                },
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "search businesses",
                        "description": "Search for businesses that satisfy the given search query",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "business_name": {
                                    "type": "string",
                                    "description": "Name of the business being searched",
                                },
                                "products": {
                                    "type": "array",
                                    "description": "List of products being searched",
                                },
                                "business_type": {
                                    "type": "array",
                                    "description": "Types of businesses being searched. This is the type of store or business that the user might find the products they're searching for.",
                                },
                                "city": {
                                    "type": "string",
                                    "description": "The city the user is searching in",
                                },
                                "context": {
                                    "type": "string",
                                    "description": "Any additional context of descriptive information that is useful to enrich the search but isn't captured by the other fields",
                                },
                            },
                            "required": ["products", "business_type"],
                        },
                    },
                },
            ])
    total_duration = response["total_duration"] / 10**9
    output = response["message"]["tool_calls"][0]["function"]["arguments"]
    print(json.dumps(output, indent=2))
    print(f"Elapsed: {total_duration} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} \"type your search query\")")
        sys.exit(1)

    parse(" ".join(sys.argv[1:]))
