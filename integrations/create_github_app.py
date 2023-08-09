import time
import webbrowser
from textwrap import fill
from urllib.parse import urlencode


class Colors:
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    ENDC = "\033[0m"
    GREEN = "\033[92m"
    UNDERLINE = "\033[4m"


def ask(prompt):
    prompt = f"{Colors.GREEN}?{Colors.ENDC} {Colors.BOLD}{prompt}{Colors.ENDC}"
    return input(prompt)


def add_if_missing_https(url):
    if not url.startswith("https"):
        return f"https://{url}"
    return url


def input_url(prompt):
    str_input = ask(prompt).rstrip("/")
    return add_if_missing_https(str_input) if len(str_input) else ""


def print_long(text):
    print("")
    for line in text.splitlines():
        print(fill(line, width=80, replace_whitespace=False))
    print("")


GITHUB_URL = input_url(
    "Enter the URL of your GitHub instance (press Enter for https://github.com): "
)
if not GITHUB_URL:
    GITHUB_URL = "https://github.com"

print_long(
    f"If your organization is at {GITHUB_URL}/my-organization, enter"
    " 'my-organization' here."
)
ORGANIZATION_NAME = ask("Enter the organization slug on GitHub: ")
DEEPSOURCE_INSTANCE_URI = input_url(
    "Enter the URL of the DeepSource instance (e.g., https://deepsource.example.com): "
)

MAIN_APP_DESCRIPTION = (
    "DeepSource helps you find and fix issues during code reviews.\n"
    "\n"
    "Seamless integration with GitHub lets you start analyzing code in a"
    " couple of minutes. Follow our documentation and guides to get started"
    " — https://deepsource.io/docs/"
)

GH_ENTERPRISE = GITHUB_URL != "https://github.com"
if GH_ENTERPRISE:
    callback_slug = "github-enterprise"
    setup_slug = "ghe"
else:
    callback_slug = "github"
    setup_slug = "gh"


# See https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app-using-url-parameters
GH_APP_PARAMS = {
    "name": f"DeepSource {ORGANIZATION_NAME}",
    "description": MAIN_APP_DESCRIPTION,
    "url": DEEPSOURCE_INSTANCE_URI,
    "callback_url": f"{DEEPSOURCE_INSTANCE_URI}/accounts/{callback_slug}/login/callback/",
    "request_oauth_on_install": "false",
    "setup_url": f"{DEEPSOURCE_INSTANCE_URI}/installation/{setup_slug}/",
    "setup_on_update": "false",
    "webhook_url": f"{DEEPSOURCE_INSTANCE_URI}/services/webhooks/{callback_slug}/",
    "events[]": [
        "member",
        "public",
        "push",
        "repository",
        "organization",
        "pull_request",
    ],
    # Permissions
    "administration": "read",
    "checks": "write",
    "statuses": "write",
    "contents": "write",
    "deployments": "read",
    "metadata": "write",
    "pull_requests": "write",
    "repository_hooks": "read",
    "single_file": "write",
    "single_file_name": ".deepsource.toml",
    "members": "read",
    "organization_hooks": "read",
    "emails": "read",
    "public": True,
}

print_long(
    f"{Colors.CYAN}In 5 seconds, you shall be redirected to the GitHub App "
    f"Registration page.{Colors.ENDC}\n"
)

print(f"{Colors.UNDERLINE}GitHub App{Colors.ENDC}")
print(
    """
 1. Scroll to the 'Webhook' section and check 'Active'.
 2. Scroll the the 'User Permissions' section and select 'Read-only'
    for 'Email addresses' and 'Git SSH Keys'.
 3. Click 'Create GitHub App'.
"""
)


if __name__ == "__main__":
    time.sleep(5)

    new_app_url = f"{GITHUB_URL}/organizations/{ORGANIZATION_NAME}/settings/apps/new"
    url_params = urlencode(GH_APP_PARAMS, True)
    default_app_url = f"{new_app_url}?{url_params}"
    print(f"URL to create app: {default_app_url}")
    print()

    webbrowser.open(default_app_url)
