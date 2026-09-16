"""
Retail Agent Orchestrator - Simulation Runner

Executes an autonomous multi-agent dialogue between:
- Store Operations Lead (Store #104)
- Inventory Merchandising Lead (Western Division)

Resolves an out-of-stock anomaly for SKU-4092 prior to a promotional weekend.
"""

import os
import sys

# Ensure UTF-8 output handling for cross-platform terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from config import get_llm_config
from agents import create_store_ops_agent, create_inventory_merch_agent


def print_banner(title: str) -> None:
    border = "=" * 78
    print(f"\n{border}")
    print(f" {title.center(76)}")
    print(f"{border}\n")


def run_escalation_simulation():
    print_banner("RETAIL MULTI-AGENT INVENTORY ESCALATION SIMULATION")

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    print(f"[CONFIG] LLM Backend   : Google Gemini OpenAI-Compatible Endpoint")
    print(f"[CONFIG] Active Model  : {model_name}")
    print(f"[CONFIG] API Key Status: {'Configured' if api_key else 'Missing (Set GEMINI_API_KEY)'}")
    print("-" * 78)

    if not api_key:
        print("\n[ERROR] GEMINI_API_KEY environment variable is not set.")
        print("   Please create a .env file with your key:")
        print("   GEMINI_API_KEY=\"AIzaSy...\"")
        print("   GEMINI_MODEL=\"gemini-2.5-flash\"\n")
        sys.exit(1)

    # Initialize LLM config
    llm_config = get_llm_config()

    # Create agents
    print("[INIT] Initializing agents...")
    store_ops = create_store_ops_agent(llm_config=llm_config)
    inventory_merch = create_inventory_merch_agent(llm_config=llm_config)
    print(f"   [READY] {store_ops.name} initialized.")
    print(f"   [READY] {inventory_merch.name} initialized.")
    print("-" * 78)

    # Initial incident escalation message
    initial_alert = (
        "URGENT ESCALATION - STORE #104 (DENVER DOWNTOWN)\n"
        "--------------------------------------------------\n"
        "SKU: SKU-4092 ('Premium Slim Stretch Denim - Vintage Wash', Size 32x32)\n"
        "On-Hand Inventory: 0 units (Floor + Backroom completely depleted)\n"
        "Anomaly Trigger: POS sell-through spike detected; register walkaways reported.\n"
        "Promotion Window: High-traffic weekend promotion starts in < 48 hours (Saturday 07:00 AM).\n"
        "Projected Demand: 50 units.\n\n"
        "Standard 72-hour ground LTL freight will miss our promotional launch. "
        "We need an immediate emergency stock rebalance or expedited pull. "
        "What are our options to get 50 units on-shelf before Saturday morning?"
    )

    print("\n[START] Initiating autonomous conversation between agents...\n")

    # Start chat
    chat_result = store_ops.initiate_chat(
        recipient=inventory_merch,
        message=initial_alert,
        max_turns=6,
        summary_method="last_msg",
    )

    print_banner("SIMULATION COMPLETED")
    print("Chat history turns recorded:", len(chat_result.chat_history))
    print("\nFinal Consensus Output:\n")
    print(chat_result.summary)


if __name__ == "__main__":
    run_escalation_simulation()
