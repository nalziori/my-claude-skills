"""
Evaluation harness scaffolding (English version)

Purpose:
- Score the agent's predictions (e.g. output.csv) against a golden set
- Includes a sanity check that catches degenerate strategies early
  (e.g. always escalate, always reply)
- Reusable across problem domains — just swap the column names / scoring logic

Usage:
    python eval_harness_en.py --pred output/output.csv --gold eval/golden_sample.csv
"""

import argparse
import csv
import sys
from collections import Counter


def load_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sanity_check(preds: list[dict], label_col: str = "decision") -> None:
    """Warn if predictions are dominated by a single label (degenerate strategy)."""
    counts = Counter(row[label_col] for row in preds)
    total = len(preds)
    for label, count in counts.items():
        ratio = count / total
        if ratio > 0.9:
            print(
                f"[warning] Label '{label}' makes up {ratio:.0%} of predictions. "
                f"Check that the system isn't collapsing onto a single strategy.",
                file=sys.stderr,
            )


def score(
    preds: list[dict],
    golds: list[dict],
    id_col: str = "id",
    label_col: str = "decision",
) -> dict:
    """Match predictions to gold labels by id and compute accuracy + confusion counts."""
    gold_map = {row[id_col]: row[label_col] for row in golds}
    pred_map = {row[id_col]: row[label_col] for row in preds}

    missing = set(gold_map) - set(pred_map)
    if missing:
        print(f"[warning] {len(missing)} item(s) missing from predictions: {list(missing)[:5]}...")

    correct = 0
    confusion = Counter()
    for _id, gold_label in gold_map.items():
        pred_label = pred_map.get(_id)
        confusion[(gold_label, pred_label)] += 1
        if pred_label == gold_label:
            correct += 1

    accuracy = correct / len(gold_map) if gold_map else 0.0

    return {
        "accuracy": accuracy,
        "n_gold": len(gold_map),
        "n_missing": len(missing),
        "confusion": confusion,
    }


def eval_loop_reminder() -> None:
    """Nudge to close the eval loop (build -> run -> inspect failures -> fix -> rerun)."""
    print(
        "\n[reminder] Don't just look at accuracy — open the rows marked MISS and figure "
        "out why they're wrong. This loop (build-run-inspect-fix-rerun) matters more than "
        "benchmark size. Log it in the 'Eval Loop Log' section of CLAUDE.md.",
        file=sys.stderr,
    )


def main():
    parser = argparse.ArgumentParser(description="Score agent output against a golden set")
    parser.add_argument("--pred", required=True, help="Path to the agent's predictions CSV")
    parser.add_argument("--gold", required=True, help="Path to the golden (ground-truth) CSV")
    parser.add_argument("--id-col", default="id")
    parser.add_argument("--label-col", default="decision")
    args = parser.parse_args()

    preds = load_csv(args.pred)
    golds = load_csv(args.gold)

    sanity_check(preds, label_col=args.label_col)
    result = score(preds, golds, id_col=args.id_col, label_col=args.label_col)

    print(f"\nAccuracy: {result['accuracy']:.2%} (of {result['n_gold']} items)")
    print(f"Missing predictions: {result['n_missing']}")
    print("\nConfusion (gold, pred) -> count:")
    for (gold_label, pred_label), count in sorted(
        result["confusion"].items(), key=lambda x: -x[1]
    ):
        marker = "OK" if gold_label == pred_label else "MISS"
        print(f"  [{marker}] {gold_label} -> {pred_label}: {count}")

    eval_loop_reminder()


if __name__ == "__main__":
    main()
