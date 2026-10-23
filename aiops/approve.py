"""Enregistre la decision humaine sur la remediation proposee. N'execute AUCUNE action.

Usage : python -m aiops.approve --decision approved|rejected --by "Prenom Nom" [--report report.json]
"""
import argparse
import json
import time


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--decision", choices=["approved", "rejected"], required=True)
    ap.add_argument("--by", required=True)
    ap.add_argument("--report", default="report.json")
    args = ap.parse_args()
    with open(args.report, encoding="utf-8") as fh:
        report = json.load(fh)
    report["safeguards"]["remediation_status"] = args.decision.upper()
    report["approval"] = {"decision": args.decision, "by": args.by,
                          "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                          "remediation": report["analysis"]["proposed_remediation"],
                          "executed_by_this_tool": False}
    with open(args.report, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    md = args.report.replace("report.json", "incident-report.md")
    try:
        with open(md, "a", encoding="utf-8") as fh:
            fh.write(f"\n## Decision humaine\n- Decision : **{args.decision}** par {args.by} le {report['approval']['at']}\n"
                     f"- Remediation concernee : {report['approval']['remediation']}\n"
                     "- Cet outil n'execute aucune action : l'operation reste a realiser par un humain.\n")
    except OSError:
        pass
    print(f"Decision enregistree : {args.decision} par {args.by} (aucune action executee par cet outil)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())