
import json
commitTypeFormats = {
    '': '<commit message>',
        "conventional": '<type>(<optional scope>): <commit message>',
}


def specifyCommitFormat(type):
    return f"The output response must be in format:\n${commitTypeFormats[type]}"


commitTypes = {
    '': '',


    # References:
    # Commitlint:
    # https://github.com/conventional-changelog/commitlint/blob/18fbed7ea86ac0ec9d5449b4979b762ec4305a92/%40commitlint/config-conventional/index.js#L40-L100

    # Conventional Changelog:
    # https://github.com/conventional-changelog/conventional-changelog/blob/d0e5d5926c8addba74bc962553dd8bcfba90e228/packages/conventional-changelog-conventionalcommits/writer-opts.js#L182-L193
        "conventional": "Choose a type from the type-to-description JSON below that best describes the git diff:\n" + json.dumps({
                        'docs': 'Documentation only changes',
                        'style': 'Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)',
                        'refactor': 'A code change that neither fixes a bug nor adds a feature',
                        'perf': 'A code change that improves performance',
                        'test': 'Adding missing tests or correcting existing tests',
                        'build': 'Changes that affect the build system or external dependencies',
                        'ci': 'Changes to our CI configuration files and scripts',
                        'chore': 'Other changes that do not modify src or test files',
                        'revert': 'Reverts a previous commit',
                        'feat': 'A new feature',
                        'fix': 'A bug fix',
        }, indent=2),
}


def generatePrompt(
        locale: str,
        maxLength: int,
        type: str,
):
    return "\n".join(x for x in [
        'Generate a concise git commit message written in present tense for the following code diff with the given specifications below:',
        f"Message language: {locale}",
        f"Commit message must be a maximum of {maxLength} characters.",
        'Exclude anything unnecessary such as translation. Your entire response will be passed directly into git commit.',
        commitTypes[type],
        specifyCommitFormat(type),
    ] if x)


def generateGitLogPrompt(
    logs: "str|list[str]",
):
    msg = """The following are commit messages from a git repository. Focus on the commit messages that start with $, as these follow the correct conventional style, including a type and a brief description of the change. Other messages might not follow the standard format and simply provide a general idea of the change. Identify and prioritize the $-prefixed messages as examples of the correct style.\n"""
    if isinstance(logs, list):
        logs = "\n".join(logs)
    if not logs.strip():
        return None
    return msg + logs
