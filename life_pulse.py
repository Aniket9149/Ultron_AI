"""ULTRON life pulse: the autonomous multimodal composition root."""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import os
import sys
import time
from typing import Any

import speech_recognition as sr


ROOT_DIR = Path(__file__).resolve().parent
SESSION_SECONDS = float(os.getenv("ULTRON_SESSION_SECONDS", "45"))


def _load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@dataclass(slots=True)
class RuntimeComponents:
    synapse: Any
    vocals: Any
    spine: Any
    inspector: Any
    operator: Any
    brain: Any
    wake_core: Any
    planner: Any = None
    executor: Any = None


def load_runtime() -> RuntimeComponents:
    """Build all subsystems around one shared SynapseBus instance."""
    bus_module = _load_module("ultron_runtime_synapse_bus", ROOT_DIR / "02_Nerves" / "synapse_bus.py")
    synapse = bus_module.SynapseBus()

    vocal_module = _load_module("ultron_runtime_vocal_tract", ROOT_DIR / "06_Vocal" / "vocal_tract.py")
    vocals = vocal_module.VocalTract(bus=synapse)

    spine_module = _load_module("ultron_runtime_reflex_spine", ROOT_DIR / "04_Spine" / "reflex_planner.py")
    spine = spine_module.ReflexSpine(bus=synapse)

    grounding_module = _load_module("ultron_runtime_native_grounding", ROOT_DIR / "01_Sense" / "native_grounding.py")
    inspector_module = _load_module("ultron_runtime_surface_inspector", ROOT_DIR / "01_Sense" / "surface_inspector.py")
    operator_module = _load_module("ultron_runtime_universal_operator", ROOT_DIR / "03_Automation_Engines" / "universal_operator.py")
    operator = operator_module.UniversalOperator(ui_grounding=grounding_module.native_grounding, bus=synapse)

    brain_module = _load_module("ultron_runtime_brain_engine", ROOT_DIR / "02_Brain" / "brain_engine.py")
    planner_module = _load_module("ultron_runtime_task_planner", ROOT_DIR / "02_Brain" / "task_planner.py")
    execution_module = _load_module("ultron_runtime_execution_engine", ROOT_DIR / "03_Automation_Engines" / "execution_engine.py")
    wake_module = _load_module("ultron_runtime_wake_detector", ROOT_DIR / "01_Voice" / "wake_detector.py")
    executor = execution_module.ExecutionEngine(
        operator=operator,
        motor_controller=spine_module.motor,
        inspector=inspector_module.surface_inspector,
        bus=synapse,
    )
    return RuntimeComponents(
        synapse=synapse,
        vocals=vocals,
        spine=spine,
        inspector=inspector_module.surface_inspector,
        operator=operator,
        brain=brain_module.brain_engine,
        wake_core=wake_module.wake_detector,
        planner=planner_module.task_planner,
        executor=executor,
    )


def _publish(runtime: RuntimeComponents, topic: str, payload: dict[str, Any]) -> None:
    futures = runtime.synapse.publish(topic, payload)
    if topic == "VOCAL_IMPULSE":
        for future in futures:
            future.result()


def _refresh_microphone_after_vocal(runtime: RuntimeComponents, recognizer: Any, source: Any, generation: int) -> int:
    current_generation = getattr(runtime.vocals, "speech_generation", generation)
    if not isinstance(current_generation, int) or current_generation == generation:
        return generation
    recognizer.adjust_for_ambient_noise(source, duration=0.1)
    return current_generation


def dispatch_action(packet: dict[str, Any], runtime: RuntimeComponents) -> None:
    """Dispatch one tactical packet through the appropriate subsystem boundary."""
    if not isinstance(packet, dict):
        return

    packet_type = packet.get("type")
    reply = packet.get("reply", packet.get("response", ""))
    if packet_type == "TALK":
        if reply:
            _publish(runtime, "VOCAL_IMPULSE", {"text": reply})
        return
    if packet_type not in ("TASK", None):
        return

    action = packet.get("action")
    target = packet.get("target", "")
    if reply and action != "MULTI_STEP_TASK":
        _publish(runtime, "VOCAL_IMPULSE", {"text": reply})

    if action == "MULTI_STEP_TASK":
        if runtime.planner is None or runtime.executor is None:
            _publish(runtime, "VOCAL_IMPULSE", {"text": "Workflow engine available nahi hai."})
            return
        plan = packet.get("plan") or runtime.planner.plan(str(target))
        _publish(runtime, "VOCAL_IMPULSE", {"text": reply or "Kaam shuru kar raha hoon."})
        result = runtime.executor.execute(plan)
        completion = "Kaam poora ho gaya hai." if result.get("success") else "Kaam poora nahi ho paya."
        _publish(runtime, "VOCAL_IMPULSE", {"text": completion})
    elif action == "OPEN_APP":
        result = runtime.operator.open_any_app(target)
        if isinstance(result, dict) and not result.get("success"):
            _publish(runtime, "VOCAL_IMPULSE", {"text": result.get("prompt", "App launch nahi ho paya.")})
    elif action in ("CLOSE_APP", "CLOSE_WINDOW"):
        if not runtime.operator.close_window(target):
            _publish(runtime, "VOCAL_IMPULSE", {"text": "Window band nahi ho payi."})
    elif action == "CLICK_UI":
        if not runtime.operator.click_element(target):
            _publish(runtime, "VOCAL_IMPULSE", {"text": f"Screen par '{target}' locate nahi ho paya."})
    elif action == "MOVE_CURSOR":
        _publish(
            runtime,
            "MOTOR_DIRECTIVE",
            {"action": "MOVE_CURSOR", "data": {"x": packet.get("x"), "y": packet.get("y")}},
        )
    elif action == "INSPECT_SCREEN":
        _publish(runtime, "VOCAL_IMPULSE", {"text": runtime.inspector.summarize_view()})
    elif action == "HOTKEY":
        _publish(runtime, "MOTOR_DIRECTIVE", {"action": "HOTKEY", "data": {"keys": packet.get("keys", [])}})
    elif action == "SCROLL":
        _publish(
            runtime,
            "MOTOR_DIRECTIVE",
            {
                "action": "SCROLL",
                "data": {
                    "direction": packet.get("direction", target or "down"),
                    "amount": packet.get("amount", 3),
                },
            },
        )


def pulse_boot(runtime: RuntimeComponents | None = None) -> None:
    """Run wake-word vigilance and the bounded command session loop."""
    runtime = runtime or load_runtime()
    _publish(runtime, "VOCAL_IMPULSE", {"text": "Ultron autonomous workstation agent online."})
    print("\n" + "=" * 55)
    print(">>> ULTRON MULTIMODAL AUTONOMOUS AGENT ACTIVE")
    print(">>> Decoupled Synapse Architecture | LM Studio Powered")
    print(">>> Say 'Ultron' to initiate command session.")
    print("=" * 55)

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 280
    recognizer.dynamic_energy_threshold = False

    try:
        while True:
            with sr.Microphone() as source:
                if not runtime.wake_core.listen_for_wake_word(source):
                    continue
                _publish(runtime, "VOCAL_IMPULSE", {"text": "Bolo Aniket."})
                session_start = time.monotonic()
                speech_generation = getattr(runtime.vocals, "speech_generation", 0)
                while time.monotonic() - session_start < SESSION_SECONDS:
                    try:
                        speech_generation = _refresh_microphone_after_vocal(
                            runtime, recognizer, source, speech_generation
                        )
                        audio = recognizer.listen(source, timeout=3.5, phrase_time_limit=6.0)
                        text = recognizer.recognize_google(audio, language="en-IN")
                        print(f'\n[USER COMMAND]: "{text}"')
                        session_start = time.monotonic()
                        if any(word in text.casefold() for word in ("shutdown", "sleep", "exit", "band ho ja")):
                            _publish(runtime, "VOCAL_IMPULSE", {"text": "Ultron offline ja raha hai."})
                            return
                        plan = runtime.brain.decide(text)
                        print(f"[TACTICAL PACKET]: {plan}")
                        dispatch_action(plan, runtime)
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except Exception as exc:
                        print(f"[STREAM ERROR]: {exc}")
                print("\n>>> Returning to standby vigilance ('Ultron')...")
    except KeyboardInterrupt:
        print("\n[AGENT TERMINATED BY USER]")


if __name__ == "__main__":
    pulse_boot()