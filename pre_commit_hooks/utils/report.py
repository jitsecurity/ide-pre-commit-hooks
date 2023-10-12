def print_report(findings, type):
    print(f"\n🔍 Security Findings Report ({type}) 🔍\n")
    print("-" * 80)

    for finding in findings:
        print(f"\n📁 File: \033[1m{finding['filename']}\033[0m")
        print(f"📍 Line: \033[1m{finding['line_range']}\033[0m")
        print(f"🚨 Severity: \033[1m{finding['issue_severity']}\033[0m")
        print(f"💡 Issue: \033[1m{finding['issue_text']}\033[0m")

        print("-" * 80)

    print(f"\nEnd of {type} report.\n")
