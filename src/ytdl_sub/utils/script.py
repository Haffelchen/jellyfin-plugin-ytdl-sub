import json
import re
from typing import Any
from typing import Dict

from ytdl_sub.script.script import _is_function


class ScriptUtils:
    @classmethod
    def add_sanitized_variables(cls, variables: Dict[str, str]) -> Dict[str, str]:
        """
        Helper to add sanitized variables to a Script
        """
        sanitized_variables = {
            f"{name}_sanitized": f"{{%sanitize({name})}}"
            for name in variables.keys()
            if not _is_function(name)
        }
        return dict(variables, **sanitized_variables)

    @classmethod
    def to_script(cls, value: Any) -> str:
        """
        Converts a python value to a script value
        """
        if value is None:
            out = ""
        elif isinstance(value, str):
            out = value
        elif isinstance(value, int):
            out = f"{{%int({value})}}"
        elif isinstance(value, float):
            out = f"{{%float({value})}}"
        elif isinstance(value, bool):
            out = f"{{%bool({value})}}"
        else:
            dumped_json = json.dumps(value, ensure_ascii=False, sort_keys=True)
            # Remove triple-single-quotes from JSON to avoid parsing issues
            dumped_json = re.sub("'{3,}", "'", dumped_json)

            out = f"{{%from_json('''{dumped_json}''')}}"

        return out

    @classmethod
    def bool_formatter_output(cls, output: str) -> bool:
        """
        Translate formatter output to a boolean
        """
        if not output or output.lower() == "false":
            return False
        try:
            return bool(json.loads(output))
        except Exception:  # pylint: disable=broad-except
            return True
