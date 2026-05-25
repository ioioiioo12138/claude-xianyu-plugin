"""一键初始化脚本 — 检查环境、安装 goofish-cli、配置认证。

用法：
    python setup.py           # 完整初始化
    python setup.py --check   # 仅诊断，不做修改
    python setup.py --login   # 仅登录
"""

import subprocess
import sys
import os
import json
from pathlib import Path

GOOFISH_CLI_DIR = Path.home() / ".goofish-cli"
COOKIES_PATH = GOOFISH_CLI_DIR / "cookies.json"
SKILLS_DIR = Path.home() / ".claude" / "skills"


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command with UTF-8 encoding."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(cmd, capture_output=True, text=True, env=env, **kwargs)


def green(text: str) -> str:
    return f"\033[92m{text}\033[0m"


def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m"


def check_python() -> bool:
    """Check Python version >= 3.11."""
    v = sys.version_info
    ok = v.major >= 3 and v.minor >= 11
    if ok:
        print(f"  ✅ Python {v.major}.{v.minor}.{v.micro}")
    else:
        print(red(f"  ❌ Python {v.major}.{v.minor}.{v.micro} — 需要 ≥ 3.11"))
    return ok


def check_goofish_cli() -> bool:
    """Check goofish-cli is installed."""
    r = run(["goofish", "version"])
    if r.returncode == 0:
        print(f"  ✅ goofish-cli {r.stdout.strip()}")
        return True
    else:
        print(yellow("  ⚠️  goofish-cli 未安装"))
        return False


def install_goofish_cli() -> bool:
    """Install goofish-cli via pip."""
    print("  📦 安装 goofish-cli ...")
    r = run([sys.executable, "-m", "pip", "install", "goofish-cli", "-q"])
    if r.returncode == 0:
        print(green("  ✅ goofish-cli 安装成功"))
        return True
    else:
        print(red(f"  ❌ 安装失败: {r.stderr}"))
        return False


def check_auth() -> bool:
    """Check goofish login status."""
    r = run(["goofish", "auth", "status"])
    if r.returncode == 0:
        try:
            data = json.loads(r.stdout)
            if data.get("valid"):
                print(green(f"  ✅ 已登录闲鱼 (用户: {data.get('tracknick', 'unknown')})"))
                return True
        except json.JSONDecodeError:
            pass
    print(yellow("  ⚠️  未登录闲鱼"))
    return False


def do_login() -> bool:
    """Guide user through goofish login."""
    print("\n📱 选择登录方式：")
    print("  1. 扫码登录（推荐）→ 电脑屏幕显示二维码，手机闲鱼扫码")
    print("  2. 浏览器自动检测 → 从浏览器提取已有 Cookie")
    print("  3. 手动导入 Cookie JSON 文件")
    choice = input("  选择 (1/2/3) [1]: ").strip() or "1"

    if choice == "1":
        print("\n  🔳 打开扫码窗口，请用手机闲鱼 App 扫码...")
        r = run(["goofish", "auth", "login", "--qr", "--qr-timeout", "180"])
    elif choice == "2":
        browser = input("  浏览器 (chrome/edge/brave) [edge]: ").strip() or "edge"
        r = run(["goofish", "auth", "login", "--browser", browser])
    elif choice == "3":
        path = input("  Cookie JSON 文件路径: ").strip()
        r = run(["goofish", "auth", "login", path])
    else:
        print(red("  无效选择"))
        return False

    if r.returncode == 0:
        print(green("  ✅ 登录成功"))
        return True
    else:
        print(red(f"  ❌ 登录失败: {r.stderr[-200:] if r.stderr else '未知错误'}"))
        return False


def check_skills() -> bool:
    """Check if goofish skills are installed."""
    expected = ["goofish-overview", "goofish-publish-item", "goofish-reply-buyer",
                 "goofish-risk-guard", "goofish-shop-diagnosis"]
    if not SKILLS_DIR.exists():
        print(yellow("  ⚠️  Skills 目录不存在"))
        return False

    installed = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
    missing = [s for s in expected if s not in installed]
    if missing:
        print(yellow(f"  ⚠️  缺少 Skills: {', '.join(missing)}"))
        return False
    print(green(f"  ✅ {len(expected)} 个 goofish Skills 已安装"))
    return True


def install_skills() -> bool:
    """Install goofish skills."""
    print("  📦 安装 goofish Skills ...")
    r = run(["goofish", "skills", "install"])
    if r.returncode == 0:
        print(green("  ✅ Skills 安装成功"))
        return True
    else:
        print(yellow(f"  ⚠️  Skills 安装可能失败: {r.stderr[-200:] if r.stderr else ''}"))
        print("  手动安装: goofish skills install")
        return False


def check_mcp_config() -> bool:
    """Check if MCP config references goofish."""
    mcp_path = Path.cwd() / ".claude" / "mcp.json"
    if not mcp_path.exists():
        print(yellow("  ⚠️  .claude/mcp.json 不存在"))
        return False
    try:
        data = json.loads(mcp_path.read_text(encoding='utf-8'))
        if "goofish" in data.get("mcpServers", {}):
            print(green("  ✅ MCP 已配置 goofish"))
            return True
    except (json.JSONDecodeError, OSError):
        pass
    print(yellow("  ⚠️  MCP 未配置 goofish"))
    return False


def print_summary(results: dict) -> None:
    """Print diagnostic summary."""
    print(f"\n{'='*50}")
    print("  诊断结果")
    print(f"{'='*50}")
    all_ok = True
    for name, ok in results.items():
        status = green("✅") if ok else red("❌")
        print(f"  {status}  {name}")
        if not ok:
            all_ok = False
    print(f"{'='*50}")
    if all_ok:
        print(green("  🎉 环境就绪，可以开始上架商品了！"))
    else:
        print(yellow("  ⚠️  以上 ❌ 项需要修复"))
    print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="闲鱼插件一键初始化")
    parser.add_argument("--check", action="store_true", help="仅诊断")
    parser.add_argument("--login", action="store_true", help="仅登录")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print("  闲鱼自动化插件 — 环境诊断")
    print(f"{'='*50}\n")

    results = {}

    # 1. Python
    print("[1/5] Python 环境")
    results["Python ≥ 3.11"] = check_python()

    # 2. goofish-cli
    print("\n[2/5] goofish-cli")
    ok = check_goofish_cli()
    if not ok and not args.check:
        ok = install_goofish_cli()
    results["goofish-cli"] = ok

    # 3. Auth
    print("\n[3/5] 闲鱼登录")
    ok = check_auth()
    if not ok and not args.check:
        if args.login:
            ok = do_login()
        else:
            print(yellow("  跳过登录（用 --login 单独登录）"))
    results["闲鱼登录"] = ok or not args.check  # 不强制

    # 4. Skills
    print("\n[4/5] goofish Skills")
    ok = check_skills()
    if not ok and not args.check:
        ok = install_skills()
    results["goofish Skills"] = ok

    # 5. MCP
    print("\n[5/5] MCP 配置")
    results["MCP 配置"] = check_mcp_config()

    print_summary(results)

    if not any(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
