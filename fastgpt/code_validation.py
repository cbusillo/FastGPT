import re
import tempfile
import ast
from pylint.lint import Run
from black import format_str, FileMode
from pathlib import Path


class CodeValidator:
    @staticmethod
    def extract_code_blocks(text: str) -> list[str] | None:
        pattern = r"```(python|py)?\n?([\s\S]*?)```"
        code_blocks = re.findall(pattern, text)
        return ["\n".join(block[1].strip().split("\n")) for block in code_blocks]

    @staticmethod
    def is_valid_python(code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    @staticmethod
    def format_code(code: str) -> str:
        return format_str(code, mode=FileMode())

    @staticmethod
    def run_static_analysis(code: str) -> tuple[int, int, list[str]]:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".py", mode="w"
        ) as temp_file:
            temp_file.write(code)
            temp_file_path = Path(temp_file.name)

        pylint_output = Run([str(temp_file_path)], exit=False)

        error_count = pylint_output.linter.stats.error
        warning_count = pylint_output.linter.stats.warning
        messages = [str(msg) for msg in pylint_output.linter.reporter.messages]
        temp_file_path.unlink()
        return error_count, warning_count, messages
