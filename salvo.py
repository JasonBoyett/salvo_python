import subprocess
import json
from dataclasses import dataclass, field
from parser import *


@dataclass
class SalvoOptions:
    path: str = ""
    time: int = 0
    users: int = 1
    rate: float = 0.0
    timeout: int = 0
    success_codes: tuple[int, ...] = field(default_factory=lambda: (200,))


class Salvo:

    def __init__(self, opts: SalvoOptions):
        self.opts: SalvoOptions = opts

        # check to make sure slavo is callable
        expected_response = "no options provided"
        result = subprocess.run(
            "salvo",
            shell=True,
            text=True,
            capture_output=True,
        )

        if expected_response not in result.stdout:
            raise SystemError("unable to locate salvo binary")

    def run(self):
        opts_json = json.dumps(
            {
                "path": self.opts.path,
                "time": self.opts.time,
                "users": self.opts.users,
                "timeout": self.opts.timeout,
                "successCodes": self.opts.success_codes,
                "rate": self.opts.rate,
            }
        )

        call_string = f"salvo -json -opts={opts_json}"

        result = subprocess.run(
            call_string,
            shell=True,
            text=True,
            capture_output=True,
        )
