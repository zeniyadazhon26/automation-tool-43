import inspect
from typing import Any, Callable, Dict, List, Optional


class CleanContext:
    """Auto-purging execution context for workflow steps."""

    def __init__(self, **initial_data: Any):
        self._store: Dict[str, Any] = initial_data
        self._history: List[str] = []

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._history.append(key)

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def purge_ephemeral(self) -> int:
        ephemeral_keys = [k for k in self._store if k.startswith("_")]
        for k in ephemeral_keys:
            del self._store[k]
        return len(ephemeral_keys)


class AutomationStep:
    """Pipeline step supporting shift operator composition."""

    def __init__(self, fn: Callable[[CleanContext], Any], name: Optional[str] = None):
        self.fn = fn
        self.name = name or fn.__name__

    def __rshift__(self, next_step: "AutomationStep") -> "TaskPipeline":
        return TaskPipeline([self, next_step])


class TaskPipeline:
    """Reorganized execution pipeline with automatic memory cleanup."""

    def __init__(self, steps: List[AutomationStep]):
        self.steps = steps

    def __rshift__(self, next_step: AutomationStep) -> "TaskPipeline":
        self.steps.append(next_step)
        return self

    def execute(self, **initial_args: Any) -> CleanContext:
        ctx = CleanContext(**initial_args)
        for step in self.steps:
            ctx.set("_current_step", step.name)
            result = step.fn(ctx)
            if result is not None:
                ctx.set(f"out_{step.name}", result)
            ctx.purge_ephemeral()

        ctx.purge_ephemeral()
        return ctx


def step(name: Optional[str] = None):
    def decorator(fn: Callable[[CleanContext], Any]) -> AutomationStep:
        return AutomationStep(fn, name=name)

    return decorator
