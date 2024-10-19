import ollama
import sys

def prompt(query):
    return f"""
    A user is trying to find local businesses that satisfy the query in quotes
    below.

    "{query}"

    To help with this, extract the following information from the query in
    quotes above:
    1. Name of the business being searched for
    2. Product or list of products being searched for
    3. Type of business being searched for
    4. City that the user is searching in.
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
                                    "type": "string",
                                    "description": "Type of business being searched",
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
    print(response["message"]["tool_calls"][0]["function"]["arguments"])
    print(f"Elapsed: {total_duration} seconds")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} \"type your search query\")")
        sys.exit(1)

    parse(" ".join(sys.argv[1:]))
