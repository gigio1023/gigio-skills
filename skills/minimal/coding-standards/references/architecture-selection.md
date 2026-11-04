# Architecture Selection

Read this when starting a project, adding a top-level directory or package, introducing an interface or a module that wraps other code, wiring an integration, implementing from a design document, building an agent loop, or when asked which architecture a project should use. Two decisions are separate. How deep the directory structure goes follows the domain and its responsibility boundaries from the start. Which abstractions exist (ports, a service layer, a unit of work, a message bus, a container) follows named triggers. An agent that generates a hexagonal skeleton with six interfaces for a hundred-line tool and an agent that puts a payment system in one file are making the same mistake from opposite ends: the first invents seams that nothing varies across, the second refuses boundaries the domain already has.

The Python spelling of everything below (file names, `Protocol` ports, Pydantic domain models, composition roots, and import-linter contracts) is in [Python architecture](python/architecture.md).

## Contents

- Structure follows boundaries
- Choose the shape
- Layouts
- Abstractions follow triggers
- Ports, adapters, and the composition root
- Implementing from a design document
- Agent loops
- Models in the domain
- Enforcing dependency direction
- Stop rules
- Pattern catalog and the authors' own limits
- Evidence
- Sources

## Structure follows boundaries

- **Domain first, then responsibility.** Top-level directories name domains or capabilities (billing, ingestion, scheduling). Inside a domain, split by responsibility: the model and its rules, use cases, ports, adapters, and the entry adapter. Go as deep as real boundaries warrant. A boundary is real when the code on each side has its own vocabulary, its own reason to change, or its own I/O.
- **Small files.** A file holds one responsibility a reader can state in a sentence. Size prompts a split and responsibility picks the cut; the numbers are in [functions and modules](functions-and-modules.md).
- **One file stays one file.** A one-off script, notebook-adjacent analysis, or a tool that is genuinely one responsibility stays one file. It becomes a directory split by responsibility when it gains a second entry point, a second importer, a second responsibility, or about 500 lines.
- **Depth is not scaffolding.** A directory or file exists because it has content. No placeholder packages, empty modules, or per-feature file template before something goes in them.
- **Per feature.** A CRUD feature stays framework-native in its own directory, with no ports, beside a feature with rules and ports. Depth follows the domain; abstraction follows triggers.
- **No restructuring as a side effect.** An existing repository keeps its shape unless the request is to change it.

## Choose the shape

| Project kind | Shape | Dependency direction | Add abstraction when | Over-engineered when |
| --- | --- | --- | --- | --- |
| One-off script, notebook-adjacent code | One file: records, pure rules, I/O helpers, an entry function | None inside the file; a notebook imports the module, never the reverse | It gains a second entry point, importer, or responsibility, or about 500 lines: it becomes a directory | Classes with one method, abstract base types, a package, a configuration framework |
| CLI tool | Entry module for argument parsing, exit codes, and output; one directory per capability, split inside by responsibility (pure planning apart from I/O); `backends/` when a capability has several implementations | The entry module imports capabilities; capabilities never import it | A second backend appears: a port plus a registry | Service classes wrapping functions, repositories for files, a DI container |
| Library or SDK | Public surface over private modules grouped by domain; public models and errors | Public modules import private ones; no composition root inside the library | Optional integrations as extras plus an adapter module; sync and async variants | Application layers or a container imposed on callers |
| HTTP service with little domain logic | By feature from the start: each feature directory holds its routes, schemas, persistence models, and query functions, framework-native | Routes to services or query functions to persistence models; no package cycles | A feature gains rules worth checking without the database; an integration gets a second implementation | A repository over the ORM session, pass-through service classes, mappers between identical shapes |
| Application with real domain rules and several integrations | Feature directories: pure model, use cases, ports for real seams, adapters, entry adapter; one composition root | Composition root to adapters to features; the model imports no I/O and no use case | Several features must stay independent (modular monolith); one event fans out to several handlers (message bus) | A port per class, a repository per entity, a unit of work over one repository, CQRS without a read problem |
| Data or ML pipeline, experiment code | Functional core split by stage (data, features, model, training, evaluation) plus entry scripts as the shell; one configuration model | Entry scripts import the core; the core imports no storage, tracking, or CLI | Several storage backends; several entry points sharing stages | Repositories for datasets, a service layer around a training loop |
| Long-running queue worker | Loop shell, handler functions, pure decision logic, ports for the model client, queue, and store | Composition root to adapters to loop and handlers to core | Many message types with several handlers each; per-message scoped resources | A message bus with one event type, a plugin registry with one plugin |
| LLM agent loop | Task contract, loop adapter, one port per tool, budget and termination as plain code, trajectory record, judge port; see Agent loops | Composition root to loop, tool, and judge adapters to the contract; the contract imports nothing | A second loop adapter (scripted policy or another model), a recorded tool environment for evaluation | A port per prompt, a framework built for one tool, budget enforced in prompt text |
| Large application, several teams | Modular monolith: top-level directories by business area, each with one public surface | Areas import each other only through their public module; no package cycles | Independent deployment or scaling becomes a measured need | Separate deployables or an in-process broker between areas |

Choose per feature, not per project. State the chosen shape in the change summary when creating a project or a top-level directory, with the trigger that would add the next abstraction.

## Layouts

File names below omit the language's extension; the Python spelling is in [Python architecture](python/architecture.md). Files exist when they have content: in the production applications inspected, a use-case module appears in most feature packages and flow or task modules only where a feature has flows or tasks; no feature carries an empty template.

CLI tool:

```text
tool/
  cli             # argument parsing, exit codes, output formatting
  config/
    model         # configuration record and its validation
    load          # reading files and environment
  sync/           # one directory per capability, importable without argument parsing
    plan          # pure: decide what to copy
    transfer      # I/O: perform the copy
  backends/       # only when a capability has several implementations: a port plus a registry
```

Application with domain rules and several integrations:

```text
app/
  main                    # composition root: settings, adapters, services
  config                  # settings record
  billing/
    model/
      invoice             # entity and its state rules; no I/O imports
      money               # value objects
    service               # use cases: load, apply rules, call ports, save
    ports                 # interfaces the use cases need, only for real seams
    api                   # entry adapter for this feature, when it has one
  adapters/
    sql_invoice_store     # implements billing.ports.InvoiceStore
    stripe_gateway        # implements billing.ports.PaymentGateway
```

Pipeline or experiment code:

```text
pipeline/
  config  data/ (I/O)  features/ (pure)  model/ (no I/O)  train  evaluate
configs/train_small    notebooks/   # import from the package, never the reverse
```

Agent loop:

```text
agent/
  contract          # Task, Budget, StopReason, Outcome: the interface
  loop/
    episode         # the adapter: run(task) -> Outcome
    budget          # pure: continue or stop, with the reason
  tools/
    ports           # one port per tool
    search/         # production adapter and recorded adapter
  judge/
    port
    adapters/
  trajectory        # the record type the loop emits
  main              # composition root
```

Queue worker:

```text
worker/  main  config  loop (receive, dispatch, acknowledge, retry)  handlers  policy (pure decisions)  ports  adapters/
```

Ports arrive earlier in workers and agent loops than in a CRUD service, because reproducible checks and evaluation need a recorded or fake model client, queue, and tool environment; faking a port the code owns replaces mocking a vendor SDK.

## Abstractions follow triggers

| Abstraction | Trigger to add it | First move |
| --- | --- | --- |
| Functional core | Any rule worth reading or checking apart from I/O | Pull the rule that decides out of the code that reads and writes |
| An explicit port for one integration | A second implementation (vendor, environment, null variant, or a recorded or fake adapter a real-run check or evaluation uses), a seam named in an accepted design document, or a check that would otherwise mock a third-party library | An interface in the consuming feature's ports module, an adapter module, wiring in the composition root |
| Enforced dependency direction | A rule that people or agents have broken, or several features that must stay independent | A dependency-rule checker with forbidden, layered, acyclic, or independence contracts |
| Service layer | A second entry point (HTTP plus worker, CLI plus API) that would otherwise duplicate orchestration | Use-case functions that load, decide, act, and save |
| Unit of work, message bus, container | The triggers the pattern catalog lists | One pattern at a time, where the pain is |

The first extraction is always the functional core: the rule that decides, pulled out of the code that reads and writes. Cosmic Python's first refactor is exactly this, a pure `determine_actions()` separated from the filesystem calls. The service layer's legitimate origin is a second entry point that would otherwise duplicate orchestration; the book's own advice is to introduce it "after you spot orchestration logic creeping into your controllers". Each move relocates code and, where public imports exist, re-exports it; the move order is in [functions and modules](functions-and-modules.md).

Before adding a module, wrapper, or layer, run the deletion test on it: imagine deleting it and putting what it does back into its callers. If the complexity disappears with it, because the module only renamed, forwarded, or re-wrapped calls that the callers could make directly, it was a pass-through and should not be added. If the same parsing, error handling, retries, or invariants would reappear in several callers, the module hides real complexity behind a smaller interface and earns its place. A port passes when deleting it would put vendor calls, or a mock of the vendor library, back into the checks and the use cases; a forwarding service or a one-implementation interface that the triggers above do not name fails. The test also settles an existing module before collapsing or splitting it: one that fails is a candidate to inline, and one whose deletion would spread logic across callers stays even when it is small.

## Ports, adapters, and the composition root

A port is an interface declared in the consuming feature's ports module, holding only the methods that caller uses. Adapters implement it in their own modules. Where the language has structural typing, adapters satisfy the port without inheriting from it and the type checker confirms conformance where the adapter is wired; a controlled adapter for a check or an evaluation satisfies the same port. Use an inherited base type only when it carries behavior every implementation shares (then it is a base class, not only a port) or when a plugin system instantiates implementations it discovered at runtime.

Services receive collaborators through typed constructor parameters and never construct clients themselves. One composition root (`main`, an application factory, or a bootstrap function) names the concrete adapters and owns their lifetimes, opening and closing connections through the language's scoped-resource construct or the framework's lifespan; checks and evaluation call it with controlled adapters or build services directly. Web frameworks already provide per-request dependency resolution; use it at the HTTP edge only and pass the session into the service layer. A DI container or service locator is justified by scoped dependency chains across many handlers, not by the number of classes; none of the production applications inspected uses one.

## Implementing from a design document

When an accepted design document (from `design-doc`, when installed) names interfaces, seams, adapters, and a verification split, implementation follows it:

- **Seams table to ports.** Each named seam gets a port in the consuming feature and one adapter per listed implementation. A component the document writes as plain code gets no port.
- **Verification split to checks.** The split decides what each component gets: a real-run check for most deterministic parts; a contract test only for an essential contract, which the document lists under the split with its reason, written by an author who has not seen the implementation ([test author packet](test-author-packet.md)); and evaluation for learned or judged behavior. A contract the split does not list as essential gets no new test unless the user decides otherwise.
- **Operating boundary to enforcement code.** For an attack or red-team agent, the document's Operating boundary section names what code must enforce: authorized targets and scope, budgets, containment, the never-do list, and evidence handling. Each item becomes a deterministic check in the loop or its tool adapters (a target allowlist checked before every tool call, budget enforcement, containment of the execution environment, refusal of never-do actions, and the evidence record), not prompt text, and each gets a real-run check on fixed input. A boundary item the code cannot enforce goes back to the document's owner as a question.
- **Composition root to production.** The composition root wires the production adapter the document names, and the same root with controlled adapters serves checks.
- **Evaluation through the interface.** Evaluation calls the same interface with the production configuration of the adapter under test. A side path that scores raw model text or an intermediate value measures a different system.
- **Adapter configuration.** Prompts, decoding settings, model revisions, preprocessing, and thresholds that belong to one candidate are adapter configuration, recorded with the adapter revision so every result binds to an identifiable adapter.
- **Deviations.** When the code cannot follow the document, say so and record the deviation with its reason; do not redesign silently.

Do this only when such a document exists. Without one, do not invent speculative ports; the triggers above decide.

## Agent loops

For an LLM episode loop, the task contract is the interface: the goal, the inputs, the allowed actions, the budget in turns, tokens, and wall time, the termination conditions, and the outcome type the loop returns. The loop itself (model, prompt, scaffold) is the adapter behind that contract, so a scripted policy for known flows and a model-driven loop can sit behind the same contract and be compared.

- **Tools behind their own ports.** Each tool the loop calls has a production adapter and a controlled one, recorded (replaying captured responses) or fake. The controlled adapters let real-run checks exercise tool code and budget enforcement on fixed input and let evaluation run episodes in a reproducible environment.
- **Budget and termination as plain decision code.** A pure function of the loop state (turns used, tokens used, elapsed time, the last action and its result) returns continue or stop with a reason from a closed set. Tool permission checks are code too. Prompt text can ask the model to stop; only code enforces it.
- **The trajectory record is the output.** The loop emits each model call and tool call with its arguments and results, the decisions taken, the termination reason, and the adapter revisions, together with the end state. Evaluation scores the end state, not the agent's claim of success; the trajectory is the supporting record for diagnosis and audit.
- **A judge behind its own port.** A model that grades candidate outcomes inside the system is a learned component with its own adapters (the production judge, a fixed-verdict fake) and its own validation through evaluation.
- **Side effects and restarts.** When an episode touches external state, the tool adapter owns idempotency or compensation, and the trajectory records what was done so a restarted episode does not repeat an effect.

A queue worker that processes messages keeps the queue-worker shape: loop shell (receive, dispatch, acknowledge, retry), handlers, pure decisions, ports for the queue, store, and model client.

## Models in the domain

Domain entities and value objects are validated record types: immutable for value objects, with methods for state changes and invariants. The rule that protects the domain is "the model module imports no I/O", not "no third-party imports": a validation library performs no I/O, so a domain built on it runs and is checked without a database or network. ORM classes are a framework-required representation: in a CRUD feature the ORM entity is the working object and services operate on it; in a domain-rule feature the persistence adapter translates rows to domain models. Reuse the domain model as the API schema while exposure and naming match; a separate schema model appears when the public contract differs. A library that must not impose its validation dependency on users, or a measured hot path, uses the language's plain record types; the language reference states the split.

## Enforcing dependency direction

Add dependency-rule contracts when the change establishes the architecture, that is, when the request creates the project or the top-level boundary; an ordinary change does not add a checker as a side effect. The first contract is the one that matters: the model module imports no I/O. Then the composition root imports adapters, adapters import features, and never the reverse; and feature directories do not form import cycles. Three of the four production applications inspected have package-level import cycles that an acyclic-siblings contract would have reported (Dispatch would need 108 edges removed, Polar 296, Warehouse 31); none enforces direction. Feature packaging without a contract drifts toward an all-to-all graph.

## Stop rules

The concrete failure: asked for a hundred-line tool that renames photos by capture date, an agent generates entity, value-object, repository-interface, use-case-interface plus implementation, infrastructure, presentation, and container modules across six packages. Reading one behavior then takes six files, renaming a field touches five, three interfaces have one implementation, and the checks mock the repository instead of checking renamed files. That tool is genuinely one responsibility and stays one file.

1. **Depth follows boundaries, abstractions follow triggers.** Split directories where the domain has boundaries; add a port, layer, or pattern only when a trigger from the table has actually occurred.
2. **No file without content.** No empty modules, placeholder packages, or a per-feature file template before something goes in them.
3. **No interface with one implementation**, except a port at an I/O or model boundary whose controlled adapter a check or evaluation in the same change uses, or a seam an accepted design document names. Never an interface for a use case, a service, or a model class.
4. **No repository over an ORM in a CRUD feature.** Call the session or query functions. A repository is for an aggregate whose rules are checked without the database, or for storage with two implementations.
5. **No forwarding service.** A use-case function loads, decides, causes a side effect, and saves, or it does not exist.
6. **No unit of work, message bus, domain events, or CQRS by default.** A unit of work when one use case must commit several repositories atomically and the ORM session is not enough; a bus when one event triggers several independent side effects; CQRS read models when reads are a measured problem.
7. **No DI container while the composition root fits on one screen.**
8. **Shape per feature.** A CRUD feature stays flat inside its own directory next to a feature with ports.
9. **Scaffolding never outweighs behavior.** No seedwork, base classes, or generic repositories before two features need the same code. Duplication is cheaper than the wrong abstraction.
10. **No restructuring as a side effect.** When a generated layout has more architecture files than files containing rules or integration code, collapse the abstractions, not the domain directories.

## Pattern catalog and the authors' own limits

| Pattern | Smallest expression | The authors' own precondition or warning |
| --- | --- | --- |
| Layered (presentation, domain, data) | Three modules or directories; lower ones never import higher ones | Fowler: "should only be applied at a relatively small granularity"; once a layer gets too big, "split your top level into domain oriented modules which are internally layered" |
| Ports and adapters (hexagonal) | Ports in the consuming feature, adapter modules, one composition root | Cockburn: "favor a small number, two, three or four ports"; the pattern "says nothing about the structure of the inside of the hexagon" |
| Clean and onion | Identical to ports and adapters; the rings are the model, the use cases, the adapters, and the composition root | Martin calls the circles "schematic"; Palermo: "not appropriate for small websites … appropriate for long-lived business applications" |
| DDD tactical patterns | Entity: a validated record with an id and rule methods. Value object: an immutable record. Aggregate: a root that owns its children, one changed per transaction. Domain service: a module-level function. Factory: a named constructor. Event: an immutable record on the aggregate's events list | Fowler: "particularly suited to complex domains"; Evans: "Make the core small"; Vernon: true invariants, small aggregates, reference by identity |
| Repository | A port with get and save, a SQL adapter, an in-memory fake | Cosmic Python: "If your app is just a simple CRUD … wrapper around a database, then you don't need a domain model or a repository"; "An ORM already buys you some decoupling" |
| Service layer | Use-case functions taking primitives and dependencies | "If your app is purely a web app, your controllers/view functions can be the single place to capture all the use cases"; risk of the anemic domain model |
| Unit of work | A scoped resource exposing repositories and commit | "You can go a long way just passing a session around" |
| Domain events and message bus | An events list on the aggregate; a mapping from event type to handlers | "there is no single place in the system where you can understand how a request will be fulfilled"; synchronous handlers slow endpoints |
| CQRS | Read views as raw query functions | "Can't I just use repositories? Of course you can!" |
| Vertical slice, feature directories | One directory per capability with its routes, schemas, models, and service functions | Bogard: the team must "recognize when to push complex logic into the domain", else "this pattern is likely not for you" |
| Functional core, imperative shell | Pure functions or model methods that take values and return decisions; a thin shell that reads, calls, and applies | Bernhardt: the shell has "few conditionals"; works at any size |
| Modular monolith | Top-level business directories with one public module each, enforced by independence or acyclic contracts | Grzybek: modules need "a well-defined interface/contract"; Fowler: find the boundaries by building the monolith first |

## Evidence

Inspected on 2026-09-29 from shallow clones; all are Python projects.

| Repository | Size | Shape | Ports | Wiring | Package cycles |
| --- | --- | --- | --- | --- | --- |
| cosmicpython/code `14c84797` | 20 files, 736 lines | By layer: domain, service_layer, adapters, entrypoints | ABCs for repository, unit of work, notifications | `bootstrap()` with signature-based injection | None |
| Netflix/dispatch `dd2837e8` (archived 2025) | 493 files, 62,323 lines | 68 feature packages plus `plugins/` | 26 plugin base classes | FastAPI `Depends`; database-configured plugin lookup | 108 edges to remove |
| fastapi/full-stack-fastapi-template `cb740b65` | 19 files, 1,153 lines | By kind: api, core, crud, models | None | FastAPI `Depends` | 1 edge |
| polarsource/polar `caa3e19b` | 1,065 files, 192,219 lines | About 57 feature packages, central `models/`, `kit/`, `integrations/` | Protocols only where providers vary | FastAPI `Depends`; module-level service singletons | 296 edges to remove |
| pypi/warehouse `19127afb` | 288 files, 60,982 lines | 51 feature units | 30 zope interfaces, mostly with a null or local variant | Pyramid service locator | 31 edges to remove |
| pre-commit/pre-commit `a9bba55a` | 67 files, 7,163 lines | Flat modules, `commands/`, `languages/` | One Protocol satisfied by 22 modules | A plain dict registry | None |
| karpathy/nanoGPT `3adf61e1` | 1,220 lines | Flat scripts: `model.py` is the pure core, `train.py` the shell | None | `exec` of config files, which its own docstring calls "Probably a terrible idea" | Not applicable |

None of the four production applications has a persistence-ignorant domain model; services operate on ORM objects. Ports appear where implementations actually vary: Warehouse storage backends and null variants, Dispatch plugins, Polar migration sources and tax providers, pre-commit languages. Feature packaging bounds where a change lands, not how big a module grows: Polar's largest service modules reach 3,000 to 4,500 lines, which this skill's small-file rule would split.

Seven "DDD" or "clean architecture" template repositories on GitHub (330 to 1,045 stars) were also inspected. All are teaching examples or starter templates, three say so in their README, and they share the failure modes the stop rules target: every use case as an interface plus an implementation subclass plus a factory; 84 empty files in one, 30 and 29 in two others; a health check spread over 21 files; a base service forwarding every call through an untyped repository behind a container; a `seedwork/` three times the size of the richest domain module. The one worth imitating in miniature gives each of its five ports a second implementation and leaves its CRUD module as five flat files.

## Sources

Accessed 2026-09-29.

- Martin Fowler, [PresentationDomainDataLayering](https://martinfowler.com/bliki/PresentationDomainDataLayering.html) (2015), [AnemicDomainModel](https://martinfowler.com/bliki/AnemicDomainModel.html) (2003), [DomainDrivenDesign](https://martinfowler.com/bliki/DomainDrivenDesign.html) (2020), [MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html) (2015).
- Alistair Cockburn, [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture) (2005); Juan Manuel Garrido de Paz, [Hexagonal Architecture](https://jmgarridopaz.github.io/content/hexagonalarchitecture.html) (2018). The 2024 book by both was not read.
- Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) (2012); Jeffrey Palermo, [The Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) (2008).
- Eric Evans, [Domain-Driven Design Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) (2015); Vaughn Vernon, [Effective Aggregate Design](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf) (2011).
- Harry Percival and Bob Gregory, [Architecture Patterns with Python](https://www.cosmicpython.com/) and its [book source](https://github.com/cosmicpython/book) at `d4522c44` (2025-09-08): chapters 2, 3, 4, 6, 7, 8, 9, 13, and the epilogue.
- Jimmy Bogard, [Vertical Slice Architecture](https://www.jimmybogard.com/vertical-slice-architecture/) (2018); Gary Bernhardt, [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) (2012); Kamil Grzybek, [Modular Monolith: A Primer](https://www.kamilgrzybek.com/blog/posts/modular-monolith-primer) (2019); David Seddon, [How we organise our very large Python monolith](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/) (2023).
- Skeptics: Mark Seemann, [Interfaces are not abstractions](https://blog.ploeh.dk/2010/12/02/Interfacesarenotabstractions/) (2010); Sandi Metz, [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) (2016); Oren Eini, [Repository is the new Singleton](https://ayende.com/blog/3955/repository-is-the-new-singleton) (2009).
- The deletion test is adapted from the `codebase-design` skill in [mattpocock/skills at 4ae2317](https://github.com/mattpocock/skills/tree/4ae2317/skills/engineering/codebase-design) (MIT License, Copyright (c) 2026 Matt Pocock), accessed 2026-11-04 and rewritten here. It restates as a thought experiment the shallow-module and pass-through-method red flags in John Ousterhout's *A Philosophy of Software Design*.

The design-document mapping and the agent-loop shape implement the interface, seam, and verification-split vocabulary that `design-doc` defines and credits; it is not repeated here. The decision-table thresholds ("about 500 lines", "fits on one screen") and the rule that directory depth follows domain boundaries from the start are this pack's choices, not measured constants. Evans', Vernon's, and Martin's books and Bernhardt's screencast were represented by their reference texts and abstracts, not read in full.
