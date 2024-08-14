from prompt import generatePrompt, generateGitLogPrompt
from git import Git
from loguru import logger
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TALKS_DIR = os.path.join(ROOT_DIR, "talks")
os.makedirs(TALKS_DIR, exist_ok=True)


def getCustomPrompt(dir="."):
    files = os.listdir(dir)
    for fn in [".ai-commit-prompt", ".ai-prompt", "commit-prompt", "repo-desc"]:
        for file in files:
            if fn.lower() in file.lower():
                with open(os.path.join(dir, file), 'r') as f:
                    content = f.read()
                return f"The following content is from the user’s description file '{file}':\n {content}"
    return None


def getTalk(git_dir="."):
    git = Git(git_dir)
    staged = git.get_staged_diff()
    if not staged:
        raise RuntimeError("No staged changes found. Stage your changes manually")

    logger.info(git.get_detected_message(staged['files']))

    values: "list[str]" = []

    system = generatePrompt("zh-CN", 50, "conventional")
    values.append(f"<system>\n{system}\n</system>")

    custom = getCustomPrompt(git.work_dir)
    if custom:
        values.append(f"<repo>\n{custom}\n</repo>")

    commit_log = generateGitLogPrompt(git.get_recent_commits(10))
    if commit_log:
        values.append(f"<repo>\n{commit_log}\n</repo>")

    values.append(("-" * 30) + "Be sure to think carefully!" + ("-" * 30))

    user = staged['diff']
    values.append(f"<user>\n{user}\n</user>")

    return "\n".join(values)


if __name__ == "__main__":
    work_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    talk = getTalk(work_dir)
    output_file = os.path.join(TALKS_DIR, "talk.txt")

    with open(output_file, 'w+') as f:
        f.write(talk)
    logger.success("talk write to: {}", output_file)
