from vector_store import retrieve, retrieve_with_score

query = "when is Paper-801 (B): Defence and Strategic Studies-II"

print("Query:", query)

result = retrieve_with_score(query, k=1)

if not result:
    print("No relevant documents found.")
else:
    print("\nRetrieved Documents with Scores:")
    for i, (doc, score) in enumerate(result):
        print(f"Document {i+1} (Score: {score:.4f}):\n{doc}\n{'-'*50}")