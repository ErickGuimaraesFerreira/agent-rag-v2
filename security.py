import re
from agno.guardrails.prompt_injection import PromptInjectionGuardrail
from agno.guardrails.base import BaseGuardrail
from typing import List, Union, Optional
from agno.run.agent import RunInput
from agno.run.team import TeamRunInput
from agno.exceptions import InputCheckError, CheckTrigger
from config import settings

######### Guardrails ##########
########## Proteção contra Prompt Injection ##########


def check(self, run_input: Union[RunInput, TeamRunInput]) -> None:

    if any(
        keyword in run_input.input_content_string().lower()
        for keyword in self.injection_patterns
    ):
        raise InputCheckError(
            "Detectada possível tentativa de jailbreak ou injeção de prompt.",
            check_trigger=CheckTrigger.PROMPT_INJECTION,
        )


# Instância pronta para uso como hook
protection_guardrail = PromptInjectionGuardrail(settings.injection_patterns)
