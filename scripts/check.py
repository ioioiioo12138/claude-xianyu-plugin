"""快速诊断 — 检查闲鱼插件所有依赖是否就绪。可被 Claude Code 调用。"""

import subprocess
import sys
import os
import json
from pathlib import Path


def run(cmd):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(cmd, capture_output=True, text=True, env=env)


def main():
    issues = []
    ok = []

    # Python
    v = sys.version_info
    if v.major >= 3 and v.minor >= 11:
        ok.append(f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        issues.append(f"Python {v.major}.{v.minor} 需要 ≥ 3.11")

    # goofish-cli
    r = run(["goofish", "version"])
    if r.returncode == 0:
        ok.append(f"goofish-cli {r.stdout.strip()}")
    else:
        issues.append("goofish-cli 未安装 (pip install goofish-cli)")

    # Auth
    r = run(["goofish", "auth", "status"])
    if r.returncode == 0:
        try:
            data = json.loads(r.stdout)
            if data.get("valid"):
                ok.append(f"闲鱼已登录 ({data.get('tracknick', '')})")
            else:
                issues.append("闲鱼登录已过期 (goofish auth login)")
        except json.JSONDecodeError:
            issues.append("无法解析登录状态")
    else:
        issues.append("闲鱼未登录 (goofish auth login --qr)")

    # MCP config
    mcp_path = Path.cwd() / ".claude" / "mcp.json"
    if mcp_path.exists():
        try:
            data = json.loads(mcp_path.read_text(encoding='utf-8'))
            if "goofish" in data.get("mcpServers", {}):
                ok.append("MCP goofish 已配置")
            else:
                issues.append("MCP 未配置 goofish")
        except (json.JSONDecodeError, OSError):
            issues.append("MCP 配置文件格式错误")
    else:
        issues.append(".claude/mcp.json 不存在")

    # Output
    print("=== 闲鱼插件诊断 ===\n")
    for item in ok:
        print(f"✅ {item}")
    if issues:
        print()
        for item in issues:
            print(f"❌ {item}")
    print()

    if not issues:
        print("🎉 环境就绪！可以开始上架商品。")
    else:
        print("💡 修复建议：python scripts/setup.py")

    return len(issues) == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
