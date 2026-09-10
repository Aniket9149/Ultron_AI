# ULTRON Architecture Blueprint

ULTRON is organized as independent biological layers. Runtime communication crosses module boundaries through `SynapseBus` impulses rather than direct calls between sensory, reasoning, motor, and vocal modules.

```text
ultron/
|-- 00_Config/
|   |-- __init__.py
|   `-- settings.py                 # Environment-backed single source of truth
|-- 01_Sense/
|   |-- __init__.py
|   |-- eye_stream.py               # Shared optical frame capture
|   |-- native_grounding.py         # Windows UI Automation grounding
|   `-- visual_grounding.py         # Visual fallback grounding
|-- 02_Brain/
|   |-- __init__.py
|   |-- cursor_router.py             # Relative cursor intent resolution
|   `-- brain_engine.py              # LM Studio tactical JSON pipeline
|-- 02_Nerves/
|   |-- __init__.py
|   `-- synapse_bus.py               # Thread-safe event-driven Pub/Sub singleton
|-- 03_Automation_Engines/
|   |-- __init__.py
|   |-- screen_inspector.py          # Foreground and running-window inspection
|   `-- universal_operator.py        # Generic OS-indexed application launching
|-- 05_Motor/
|   |-- __init__.py
|   `-- hand_motor.py                # Human-like pointer and keyboard control
|-- 06_Vocal/
|   |-- __init__.py
|   |-- phonetic_mapper.py           # Roman Hinglish phonetic mapping
|   |-- neural_vocal_engine.py       # Edge-TTS synthesis and Pygame playback
|   `-- vocal_tract.py               # VOCAL_IMPULSE subscriber
|-- 06_Tests/
|   |-- test_settings.py
|   |-- test_synapse_bus.py
|   |-- test_eye_stream.py
|   |-- test_native_grounding.py
|   |-- test_visual_grounding.py
|   |-- test_cursor_router.py
|   |-- test_brain_engine.py
|   |-- test_screen_inspector.py
|   |-- test_universal_operator.py
|   |-- test_hand_motor.py
|   |-- test_phonetic_mapper.py
|   |-- test_neural_vocal_engine.py
|   |-- test_vocal_tract.py
|   `-- test_life_pulse.py
|-- life_pulse.py                    # Session vigilance and ambient listening
|-- main.py                          # Runtime composition root
|-- requirements.txt
`-- .env                             # Local-only configuration overrides
```

## Impulse vocabulary

Modules publish and subscribe to named impulses such as `SENSORY_HEARD`, `OPTICAL_PULSE`, `MOTOR_DIRECTIVE`, and `VOCAL_IMPULSE`. The bus dispatches handlers asynchronously so producers are not blocked by consumer work.

## Dependency direction

`01_Sense` and `life_pulse.py` produce impulses. `02_Brain` consumes sensory impulses and produces tactical directives. `05_Motor` and `06_Vocal` consume directives. No sensory module imports a motor or vocal implementation.
