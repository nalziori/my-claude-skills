"""
평가 하네스 스캐폴딩 (한국어 버전)

목적:
- 에이전트가 생성한 예측 결과(예: output.csv)를 golden set과 비교해 채점
- 극단적 전략(전부 escalate, 전부 reply 등)을 조기에 걸러내는 sanity check 포함
- 문제 도메인에 맞게 컬럼명/채점 로직만 바꿔서 재사용

사용법:
    python eval_harness_ko.py --pred output/output.csv --gold eval/golden_sample.csv
"""

import argparse
import csv
import sys
from collections import Counter


def load_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sanity_check(preds: list[dict], label_col: str = "decision") -> None:
    """극단적 전략(단일 라벨로 몰아 찍기) 여부를 미리 경고"""
    counts = Counter(row[label_col] for row in preds)
    total = len(preds)
    for label, count in counts.items():
        ratio = count / total
        if ratio > 0.9:
            print(
                f"[경고] '{label}' 라벨이 전체의 {ratio:.0%}를 차지합니다. "
                f"단일 전략으로 몰아 찍고 있지 않은지 확인하세요.",
                file=sys.stderr,
            )


def score(
    preds: list[dict],
    golds: list[dict],
    id_col: str = "id",
    label_col: str = "decision",
) -> dict:
    """id 기준으로 매칭해서 정확도 + 라벨별 confusion 계산"""
    gold_map = {row[id_col]: row[label_col] for row in golds}
    pred_map = {row[id_col]: row[label_col] for row in preds}

    missing = set(gold_map) - set(pred_map)
    if missing:
        print(f"[경고] {len(missing)}개 항목이 예측 결과에서 누락됨: {list(missing)[:5]}...")

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
    """평가 루프(build -> run -> 실패 사례 확인 -> 수정 -> 재실행)를 잊지 않도록 상기"""
    print(
        "\n[리마인더] 정확도만 보지 말고, MISS로 표시된 케이스들을 직접 열어서 "
        "왜 틀렸는지 확인하세요. 이 루프(만들고-돌리고-확인하고-고치고-다시 돌리기)가 "
        "벤치마크 크기보다 중요한 신호입니다. CLAUDE.md의 '평가 루프 로그' 섹션에 기록하세요.",
        file=sys.stderr,
    )


def main():
    parser = argparse.ArgumentParser(description="에이전트 출력 채점 스크립트")
    parser.add_argument("--pred", required=True, help="에이전트 예측 CSV 경로")
    parser.add_argument("--gold", required=True, help="정답(golden) CSV 경로")
    parser.add_argument("--id-col", default="id")
    parser.add_argument("--label-col", default="decision")
    args = parser.parse_args()

    preds = load_csv(args.pred)
    golds = load_csv(args.gold)

    sanity_check(preds, label_col=args.label_col)
    result = score(preds, golds, id_col=args.id_col, label_col=args.label_col)

    print(f"\n정확도: {result['accuracy']:.2%} ({result['n_gold']}건 중)")
    print(f"누락된 예측: {result['n_missing']}건")
    print("\n혼동 행렬 (gold, pred) -> count:")
    for (gold_label, pred_label), count in sorted(
        result["confusion"].items(), key=lambda x: -x[1]
    ):
        marker = "OK" if gold_label == pred_label else "MISS"
        print(f"  [{marker}] {gold_label} -> {pred_label}: {count}")

    eval_loop_reminder()


if __name__ == "__main__":
    main()
