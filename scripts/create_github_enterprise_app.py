import time
import webbrowser

from textwrap import fill
from urllib.parse import urlencode

class Colors:
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    GREEN = '\033[92m'
    UNDERLINE = '\033[4m'


def ask(prompt):
    prompt = f"{Colors.GREEN}?{Colors.ENDC} {Colors.BOLD}{prompt}{Colors.ENDC}"
    return input(prompt)


def confirm(prompt, default=None):
    yes = {"y", "ye", "yes"}
    no = {"n", "no"}

    if default:
        if default == "yes":
            yes.add("")
        else:
            no.add("")

    answer = ask(prompt).lower()
    while answer not in (yes | no):
        print("Did not recongize the input. Please try again.")
        answer = ask(prompt)

    return answer in yes


def add_if_missing_https(url):
    if not url.startswith("https"):
        return f"https://{url}"
    return url


def input_url(prompt):
    return add_if_missing_https(ask(prompt).rstrip("/"))


def print_long(text):
    print("")
    for line in text.splitlines():
        print(fill(line, width=80, replace_whitespace=False))
    print("")


GITHUB_URL = input_url("Enter the URL of the self-hosted GitHub instance: ")

print_long(
    f"If your organization is at {GITHUB_URL}/my-organization, enter"
    " 'my-organization' here."
)
ORGANIZATION_NAME = ask("Enter the organization slug on GitHub: ")
DEEPSOURCE_INSTANCE_URI = input_url(
    "Enter the URL of the DeepSource instance"
    " (e.g., deepsource.example.com): "
)

print_long(
    "You shall be asked to enter Webhook Secrets. Use a random string with"
    " high entropy, e.g., by taking the output of:"
)
print("    ruby -rsecurerandom -e 'puts SecureRandom.hex(20)'")
print_long(
    "Kindly keep them safe with you, as you shall be asked to enter the same"
    " in the GitHub web interface."
)


NEW_APP_URL = f"{GITHUB_URL}/organizations/{ORGANIZATION_NAME}/settings/apps/new"
MAIN_APP_DESCRIPTION = (
    "DeepSource helps you find and fix issues during code reviews.\n"
    "\n"
    "Seamless integration with GitHub lets you start analyzing code in a"
    " couple of minutes. Follow our documentation and guides to get started"
    " â€”  https://deepsource.io/docs/"
)

MAIN_APP_PARAMS = urlencode({
    "name": f"DeepSource {ORGANIZATION_NAME}",
    "description": MAIN_APP_DESCRIPTION,
    "url": DEEPSOURCE_INSTANCE_URI,
    "callback_url": f"{DEEPSOURCE_INSTANCE_URI}/accounts/github/login/callback/",
    "request_oauth_on_install": "false",
    "setup_url": f"{DEEPSOURCE_INSTANCE_URI}/installation/ghe/",
    "setup_on_update": "false",
    "webhook_url": f"{DEEPSOURCE_INSTANCE_URI}/services/webhooks/github-enterprise/",
    "events[]": ["member", "public", "push", "repository", "organization", "pull_request"],
    # Permissions
    "administration": "read",
    "checks": "write",
    "contents": "write",
    "deployments": "read",
    "metadata": "write",
    "pull_requests": "write",
    "repository_hooks": "read",
    "single_file": "write",
    "single_file_name": ".deepsource.toml",
    "members": "read",
    "organization_hooks": "read",
    "public": True,
}, True)


print_long(
    f"{Colors.CYAN}In 5 seconds, you shall be redirected to the GitHub App "
    f"Registration page.{Colors.ENDC}\n"
)

print(f"{Colors.UNDERLINE}GitHub App{Colors.ENDC}")
print("""
 1. Scroll to the 'Webhook' section and check 'Active'.
 2. Scroll the the 'User Permissions' section and select 'Read-only'.
    for 'Email addresses' and 'Git SSH Keys'.
 3. Click 'Create GitHub App'.
""")


if __name__ == "__main__":
    time.sleep(5)

    default_app_url = f"{NEW_APP_URL}?{MAIN_APP_PARAMS}"
    print(f"URL to create app: {default_app_url}")
    # Print an empty newline

    webbrowser.open(default_app_url)
