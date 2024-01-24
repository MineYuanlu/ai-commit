import subprocess
import os
import sys
from loguru import logger
from typing import TypedDict


def _exclude_from_diff(path: str):
    return f":(exclude){path}"


_files_to_exclude = [_exclude_from_diff(path) for path in [
    'package-lock.json',
    'pnpm-lock.yaml',
    '*.lock',
]]


class StagedDiff(TypedDict):
    files: "list[str]"
    diff: "str"


class Git:
    def __init__(self, work_dir=".", git_dir: str = None) -> None:
        self.work_dir = os.path.abspath(work_dir)
        self.git_dir = os.path.join(self.work_dir, '.git') if git_dir is None else git_dir
        logger.info("[Git] Work Dir: {}, Git Dir: {}", self.work_dir, self.git_dir)

    def run_git_command(self, command: "list[str]"):
        assert command[0] == 'git'
        command = ['git', f"--git-dir={self.git_dir}", f"--work-tree={self.work_dir}"] + list(command)[1:]
        logger.debug("[Git] Run Command: {}", " ".join(str(c) for c in command))
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError('Git command failed: ' + str(e))

    def assert_git_repo(self):
        command = ['git', 'rev-parse', '--show-toplevel']
        try:
            return self.run_git_command(command)
        except RuntimeError as e:
            raise Exception('The current directory must be a Git repository!') from e

    def get_staged_diff(self, exclude_files: "list[str]" = None) -> "StagedDiff|None":
        diff_cached = ['git', 'diff', '--cached', '--diff-algorithm=minimal']
        command_files = diff_cached + ['--name-only'] + _files_to_exclude
        if exclude_files:
            command_files.extend(_exclude_from_diff(path) for path in exclude_files)

        files = self.run_git_command(command_files)
        if not files:
            return None

        command_diff = diff_cached + _files_to_exclude
        if exclude_files:
            command_diff.extend(_exclude_from_diff(path) for path in exclude_files)

        diff = self.run_git_command(command_diff)

        return {
            'files': files.split('\n'),
            'diff': diff,
        }

    def get_detected_message(self, files: list):
        file_count = len(files)
        return f"Detected {file_count} staged file{'s' if file_count > 1 else ''}"
