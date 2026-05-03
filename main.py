from dotenv import load_dotenv
from agent.graph import build_graph

load_dotenv()

def main():
    graph = build_graph()

    print("Code Review Agent")
    print("─" * 40)
    print("Paste a file path or code snippet.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input(">>> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Bye.")
            break

        try:
            result = graph.invoke({"user_message": user_input})
            print("\n" + result["output"] + "\n")
        except FileNotFoundError as e:
            print(f"\n❌ File not found: {e}\n")
        except ValueError as e:
            print(f"\n⚠️  Invalid input: {e}\n")
        except Exception as e:
            print(f"\n💥 Unexpected error: {e}\n")

if __name__ == "__main__":
    main()