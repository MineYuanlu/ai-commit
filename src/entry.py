from prompt import generatePrompt
from git import Git
from loguru import logger
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TALKS_DIR = os.path.join(ROOT_DIR, "talks")
os.makedirs(TALKS_DIR, exist_ok=True)


def getTalk(git_dir="."):
    git = Git(git_dir)
    staged = git.get_staged_diff()
    if not staged:
        raise RuntimeError("No staged changes found. Stage your changes manually")

    logger.info(git.get_detected_message(staged['files']))

    system = generatePrompt("zh-CN", 50, "conventional")
    user = staged['diff']

    return "\n".join([
        f"<system>{system}</system>",
        ("-" * 30) + "Be sure to think carefully!" + ("-" * 30),
        f"<user>{user}</user>"
    ])


if __name__ == "__main__":
    work_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    talk = getTalk(work_dir)
    output_file = os.path.join(TALKS_DIR, "talk.txt")

    with open(output_file, 'w+') as f:
        f.write(talk)
    logger.success("talk write to: {}", output_file)
