from urllib.parse import urlparse, urlunparse
import ipaddress
import pyautogui
import pyperclip
import time

# ================= تنظیمات =================

CONFIG_FILE = "config.txt"
IP_FILE = "ip-in.txt"
OUTPUT_FILE = "outputconfigs.txt"

NEW_PORT = 40443

BATCH_SIZE = 500

# چند ثانیه فرصت برای فوکوس کردن پنجره V2RayN
FOCUS_DELAY = 5

# زمان انتظار برای اتمام تست هر دسته
PING_WAIT_SECONDS = 120

# ===========================================


def replace_ip_and_port(vless_link, new_ip, new_port):
    try:
        parsed = urlparse(vless_link)

        if parsed.scheme.lower() != "vless":
            return None

        username = parsed.username
        if not username:
            return None

        netloc = f"{username}@{new_ip}:{new_port}"

        return urlunparse((
            parsed.scheme,
            netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))

    except Exception:
        return None


def load_ips(ip_file):
    result = []

    with open(ip_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                if "/" in line:
                    network = ipaddress.ip_network(
                        line,
                        strict=False
                    )

                    for ip in network:
                        result.append(str(ip))
                else:
                    ipaddress.ip_address(line)
                    result.append(line)

            except ValueError:
                print(f"Invalid IP or range skipped: {line}")

    return result


def build_configs():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        configs = [line.strip() for line in f if line.strip()]

    ips = load_ips(IP_FILE)

    results = []
    counter = 1

    for config in configs:
        for ip in ips:

            new_config = replace_ip_and_port(
                config,
                ip,
                NEW_PORT
            )

            if not new_config:
                continue

            if "#" in new_config:
                new_config = new_config.split("#", 1)[0]

            new_config += f"#{counter}"

            results.append(new_config)
            counter += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"Loaded {len(ips)} IPs")
    print(f"Generated {len(results)} configs")
    print(f"Saved to: {OUTPUT_FILE}")

    return results


def chunks(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def import_and_ping_batches(configs):
    total_batches = (len(configs) + BATCH_SIZE - 1) // BATCH_SIZE

    print()
    print("=" * 50)
    print("V2RayN should be opened now.")
    print(f"You have {FOCUS_DELAY} seconds to focus the V2RayN window.")
    print("=" * 50)

    time.sleep(FOCUS_DELAY)

    for batch_num, batch in enumerate(
        chunks(configs, BATCH_SIZE),
        start=1
    ):

        print(
            f"\nProcessing batch "
            f"{batch_num}/{total_batches} "
            f"({len(batch)} configs)"
        )

        batch_text = "\n".join(batch)

        pyperclip.copy(batch_text)

        # Paste configs
        pyautogui.hotkey("ctrl", "v")

        time.sleep(5)

        # Select all
        pyautogui.hotkey("ctrl", "a")

        time.sleep(1)

        # Real Delay Test
        pyautogui.hotkey("ctrl", "r")

        print(
            f"Waiting {PING_WAIT_SECONDS} seconds "
            f"for latency test..."
        )

        time.sleep(PING_WAIT_SECONDS)

    print("\nAll batches processed.")


def main():
    configs = build_configs()
    import_and_ping_batches(configs)


if __name__ == "__main__":
    main()
