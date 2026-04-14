"""
Walled Garden — Main Pipeline
Runs the full end-to-end Age-Aware RAG system.

Usage:
    # Interactive chat (single query):
    python main.py --mode chat --age 12 --prompt "what is depression"

    # Run full evaluation + generate charts:
    python main.py --mode eval

    # Run evaluation with limit + charts:
    python main.py --mode eval --limit 10

    # Generate charts from existing results (demo data):
    python main.py --mode charts --demo

    # Generate charts from existing CSV:
    python main.py --mode charts --input evaluation/results.csv
"""

import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from simulator import simulate_response
from rag.database import find_relevant_topic, retrieve_chunk


def chat_mode(user_age: int, prompt: str, system: str = "Proposed"):
    """Run a single query through the Walled Garden pipeline without any API."""
    topic = find_relevant_topic(prompt)
    context = retrieve_chunk(topic, user_age) if topic else ""

    print(f"\n{'─' * 60}")
    print(f"  System:   {system}")
    print(f"  User age: {user_age}")
    print(f"  Prompt:   {prompt}")
    if topic:
        print(f"  RAG topic retrieved: {topic}")
        print(f"  Context preview: {context[:80]}...")
    else:
        print("  No RAG context matched — system will redirect.")
    print(f"{'─' * 60}\n")

    response = simulate_response(
        system=system,
        prompt=prompt,
        user_age=user_age,
        context=context,
    )

    print(f"Response:\n{response}\n")
    return response


def main():
    parser = argparse.ArgumentParser(description="Walled Garden Age-Aware RAG Pipeline")
    parser.add_argument("--mode", choices=["chat", "eval", "charts"], default="chat")
    parser.add_argument("--api-key", default=os.environ.get("ANTHROPIC_API_KEY", ""))
    parser.add_argument("--age", type=int, default=12, help="User age (chat mode)")
    parser.add_argument("--prompt", type=str, default="", help="Prompt text (chat mode)")
    parser.add_argument("--system", type=str, default="Proposed", help="System variant (chat mode)")
    parser.add_argument("--limit", type=int, default=None, help="Limit prompts in eval mode")
    parser.add_argument("--input", type=str, default=None, help="Results CSV for charts mode")
    parser.add_argument("--demo", action="store_true", help="Use synthetic data in charts mode")
    args = parser.parse_args()

    if args.mode == "chat":
        if not args.prompt:
            print("Error: --prompt is required for chat mode.")
            sys.exit(1)
        chat_mode(args.age, args.prompt, args.system)

    elif args.mode == "eval":
        from evaluation.evaluator import run_evaluation
        run_evaluation(limit=args.limit)

        # Auto-generate charts after eval
        from visualization.charts import run as run_charts
        run_charts(input_csv="evaluation/results.csv")

    elif args.mode == "charts":
        from visualization.charts import run as run_charts
        run_charts(input_csv=args.input, demo=args.demo)


if __name__ == "__main__":
    main()