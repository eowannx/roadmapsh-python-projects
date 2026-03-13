import sys
import json
import urllib.request
import urllib.error


def get_url(username):
    # Returns GitHub API endpoint URL for the given username
    return f"https://api.github.com/users/{username}/events"


def fetch_activity(url):
    # request object wraps url and User-Agent header - required by GitHub API to identify the client
    # urlopen sends the request and returns response object with status, headers and body
    # .read() extracts only the body as bytes (last 30 events) from the response object
    request = urllib.request.Request(url, headers={"User-Agent": "github-activity-cli"})
    response = urllib.request.urlopen(request)
    data = response.read()
    return data


def parse_activity(data):
    # .decode("utf-8") converts bytes to string so json.loads can parse it
    # json.loads (s = string) converts JSON string to Python list of dictionaries
    events = json.loads(data.decode("utf-8"))
    return events


def display_activity(events):
    # This function displays 30 last events using for loop
    if not events:
        print("No recent activity found")
        return

    for event in events:
        event_type = event["type"]
        repo = event["repo"]["name"]
        # event[“repo”] is also a dictionary
        # so [“name”] retrieves the repository name from the nested dictionary

        if event_type == "PushEvent":
            # payload is a nested dictionary inside every event with details specific to that event type
            # .get("commits", []) safely extracts commits list from payload - returns empty list if not found
            commits = len(event["payload"].get("commits", []))
            if commits > 0:
                print(f"- Pushed {commits} commit(s) to {repo}")

        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            print(f"- {action.capitalize()} an issue in {repo}") #.capitalize() capitalizes the first letter.

        elif event_type == "WatchEvent":
            print(f"- Starred {repo}")

        elif event_type == "ForkEvent":
            print(f"- Forked {repo}")

        elif event_type == "CreateEvent":
            print(f"- Created a repository {repo}")

        elif event_type == "PullRequestEvent":
            action = event["payload"]["action"]
            print(f"- {action.capitalize()} a pull request in {repo}")

        elif event_type == "DeleteEvent":
            print(f"- Deleted a branch or tag in {repo}")

        elif event_type == "IssueCommentEvent":
            print(f"- Commented on an issue in {repo}")

        elif event_type == "ReleaseEvent":
            print(f"- Published a release in {repo}")

        elif event_type == "PullRequestReviewEvent":
            print(f"- Reviewed a pull request in {repo}")

        else:
            print(f"- {event_type} in {repo}")


def main():
    args = sys.argv[1:] # takes everything except the script name

    if not args:
        print("Usage: python github_activity.py <username>")
        return

    username = args[0]
    url = get_url(username)

    try:
        data = fetch_activity(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found")
        else:
            print(f"Error: HTTP error {e.code}")
        return
    except urllib.error.URLError:
        print("Error: Could not connect to GitHub API. Check your internet connection")
        return

    events = parse_activity(data)
    display_activity(events)

# This block executes only if file executed directly
# (and not imported as a module in another file)
if __name__ == "__main__":
    main()