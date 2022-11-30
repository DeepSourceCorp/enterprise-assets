from textwrap import dedent, fill


class Colors:
    BOLD = "\033[1m"
    RED = "\033[31m"
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


SLACK_APP_NAME = ask(
    'Enter a name for the Slack app (press Enter for "DeepSource Enterprise"): '
)
if not SLACK_APP_NAME:
    SLACK_APP_NAME = "DeepSource Enterprise"

DEEPSOURCE_INSTANCE_URI = input_url(
    "Enter the URL of the DeepSource instance (e.g., https://deepsource.example.com): "
)
if not DEEPSOURCE_INSTANCE_URI:
    print(f"{Colors.RED}Please provide the DeepSource instance URL!{Colors.ENDC}")
    exit(1)

SLACK_APP_MANIFEST = dedent(
    f"""
    display_information:
      name: {SLACK_APP_NAME}
      description: DeepSource Integrations App
      background_color: "#000000"
    features:
      bot_user:
        display_name: DeepSource Enterprise
        always_online: true
    oauth_config:
      redirect_urls:
        - {DEEPSOURCE_INSTANCE_URI}/callback/integrations/slack
      scopes:
        bot:
          - channels:read
          - chat:write
          - groups:read
          - chat:write.public
          - incoming-webhook
    settings:
      interactivity:
        is_enabled: true
        request_url: {DEEPSOURCE_INSTANCE_URI}/services/integrations/webhooks/slack/
      org_deploy_enabled: false
      socket_mode_enabled: false
      token_rotation_enabled: false
  """
).strip()

print(
    f"{Colors.CYAN}\nPlease copy the following manifest and use it to create the Slack app {Colors.ENDC}"
)
print("-" * 75)
print(SLACK_APP_MANIFEST)
print("-" * 75)
