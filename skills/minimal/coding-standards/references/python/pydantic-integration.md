# Python Pydantic Integration

Read this when the task changes Pydantic models, validation, or serialization. This pack's Pydantic-first representation policy takes precedence over optional alternatives in upstream examples. For library behavior (field constraints, validators, coercion, serialization), use the version-matched official Pydantic documentation, or the official `pydantic` skill from [pydantic/skills](https://github.com/pydantic/skills) when it is installed. Match advice to the project's installed Pydantic version; do not guess an unfamiliar API or silently upgrade the application.

## Local modeling and boundary policy

Default to Pydantic v2 `BaseModel` for application-owned structured data, including internal records and external validation or serialization. Reuse the same model across a boundary when the meaning and exposure rules are unchanged. Do not create parallel `TypedDict`, dataclass, dictionary, and Pydantic versions of one record. Alternative representations require a specific need such as an SDK input type, a framework's dataclass requirement, a genuine dynamic-key mapping, an existing compatibility promise, or a measured constraint. Keep the reason near the exceptional code. A v1 application needs a scoped migration before adopting incompatible APIs; do not silently change a supported dependency range.

Pydantic-first modeling does not mean every class inherits `BaseModel`: services and resource owners are behavior, not data records. Prefer simple models with explicitly annotated fields, and explain non-obvious field semantics, units, defaults, or invariants in the model docstring or appropriate field description. A name and type that already explain the field need no paraphrase. Keep custom validators and shared base models limited to real shared behavior; do not build a model framework for anticipated needs.

Domain entities and value objects in an application with real rules are also `BaseModel`s: frozen for value objects, which then compare and hash by value, and with methods for state changes and invariants. What protects the domain is that its model module imports no I/O, not that it avoids third-party imports; see [architecture selection](../architecture-selection.md) and its Python spelling in [Python architecture](architecture.md). Three consequences, verified on Pydantic 2.13 and SQLAlchemy 2.1 on 2026-09-29: SQLAlchemy's classical mapping onto a `BaseModel` fails at `session.add()`, so a persistence adapter translates rows with `model_validate` or stores the model's JSON rather than mapping the domain class; `validate_assignment=True` catches `invoice.state = "bogus"` but not `invoice.items.append(...)`, so invariants live in methods rather than in field types alone; and constructing a frozen `BaseModel` costs about twice a frozen dataclass (0.34 µs against 0.18 µs), which matters only in a hot loop over millions of objects and is then the measured-constraint exception above. The default applies to the work this pack usually does: applications, services, tools, pipelines, and agents that already depend on Pydantic, where one model per meaning removes a whole layer of parallel records. Two cases are different, and code in them says so beside the record: a library or SDK whose users must not inherit a Pydantic dependency, and a measured hot path where construction or validation cost dominates. There, records are dataclasses, `NamedTuple`, or plain classes, with `frozen=True` and `slots=True` where the value semantics are wanted. That is the case attrs' documentation argues from when it calls Pydantic "the right tool for Commands" and warns against re-validating trusted objects in the domain layer, and the case fastapi is in when it keeps `BaseModel` at its schema boundary and dataclasses inside: both are frameworks shipping into other people's dependency trees. Do not carry the framework case into ordinary application code, and do not carry the application default into a library.

Choose unknown-field handling deliberately:

| Boundary requirement | Appropriate policy |
| --- | --- |
| Owned input with a closed schema | Usually `extra="forbid"` |
| Independently versioned input whose unknown fields may safely be discarded | `extra="ignore"`, with that loss intentional |
| Data that must retain unknown fields for forwarding, round trips, or audit | `extra="allow"` or preservation of the original payload alongside the validated view |

Select strictness by source and field. Configuration text and JSON do not necessarily share coercion requirements. Check allowed and rejected values through a real run on fixed input; neither blanket strictness nor silent default coercion settles the intended behavior.

Keep enum members in runtime models unless a specific existing interface requires primitive values. Do not set `use_enum_values=True` on a shared base model just to produce JSON: it changes values during validation. Prefer an explicit JSON-compatible dump or JSON-text serialization at output, and check the actual output. A localized primitive-storage exception must also handle enum defaults consistently.

Do not treat `model_construct()` or `model_copy(update=...)` as validation of new untrusted values. Validate the input through the intended boundary. Keep authorization and I/O outside schema validation; valid fields do not imply an allowed action. Select output fields deliberately so internal or subclass-only data is not exposed accidentally.

Use `TypeAdapter` when a boundary needs validation of a container, union, or an already-required non-model type. It is a validation/serialization adapter, not a field annotation or a reason to choose `TypedDict` or dataclasses for new application records.

When changing these behaviors, check the affected field names and aliases, unknown-field retention, coercion, enum values and runtime types, rejected input, and output exposure through the real entry point on fixed input. A serialized or persisted format that callers or stored data depend on is an essential contract, which gets a contract test written from the contract. Check only what the change touches; do not duplicate existing coverage.

## Source scope

These official references were checked on 2026-09-29 against Pydantic 2.13 and supplement the external skill's coverage:

- [Configuration](https://pydantic.dev/docs/validation/latest/api/pydantic/config/): `extra`, `use_enum_values`, and validation of defaults.
- [Serialization](https://pydantic.dev/docs/validation/latest/concepts/serialization/): Python mode versus JSON mode, aliases, and subclass serialization.
- [Strict mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/): call, field, and model-level strictness, including input-source differences.
- [Models](https://pydantic.dev/docs/validation/latest/concepts/models/): model construction and validation behavior.
- [TypeAdapter](https://pydantic.dev/docs/validation/latest/concepts/type_adapter/): validation and serialization without defining a `BaseModel`.

The upstream skill is MIT-licensed and remains external. This package contains no vendored copy, updater, or installer. Install instructions belong to the pack's distribution documentation, and using this skill does not refresh global skill directories.
