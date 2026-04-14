---
tags:
  - education-kit
---
# Python — Knowledge Base
> [!info] Comprehensive Python interview questions covering data structures, language mechanics, concurrency, type hints, asyncio, packaging, testing, design patterns, security, and modern Python 3.10-3.12 features.

## Quick Scan — Ctrl+F This

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Q1. How does a Python `dict` work internally?\|dict internals]] | hash table, open addressing, order 3.7+ | [[#Q2. What makes an object hashable?\|hashable]] | needs \_\_hash\_\_ + \_\_eq\_\_, mutable=not hashable |
| [[#Q3. `list` vs `tuple` — when do you pick which?\|list vs tuple]] | list=mutable, tuple=immutable+hashable | [[#Q4. When would you use a `set` and what are its key operations?\|set]] | O(1) membership, union/intersection/difference |
| [[#Q5. What is a `defaultdict` and when is it useful?\|defaultdict]] | auto-creates missing keys with factory | [[#Q7b. What is `collections.Counter` and when is it useful?\|Counter]] | dict for counting, most_common(n) |
| [[#Q7c. What is `namedtuple` vs `dataclass`?\|namedtuple vs dataclass]] | namedtuple=immutable, dataclass=flexible | [[#Q8. What is the GIL and why does it matter?\|GIL]] | one thread executes Python, I/O releases |
| [[#Q9. Explain decorators in plain terms.\|decorators]] | function wrapping function, @syntax | [[#Q10. What is a generator and why use one?\|generators]] | yield=lazy, memory efficient |
| [[#Q11. What is a context manager and how do you write one?\|context managers]] | with statement, \_\_enter\_\_/\_\_exit\_\_ | [[#Q12. Explain `*args` and `**kwargs`.\|*args/**kwargs]] | *args=positional tuple, **kwargs=keyword dict |
| [[#Q14b. What are `__slots__` and why would you use them?\|\_\_slots\_\_]] | fixed attrs, saves 40% memory | [[#Q14c. Explain `property` decorator — getter, setter, deleter.\|property]] | computed attributes, validation on set |
| [[#Q14d. What is `__init__` vs `__new__`?\|\_\_init\_\_ vs \_\_new\_\_]] | new=creates, init=initializes | [[#Q15. `threading` vs `multiprocessing` vs `asyncio` — when to use each?\|threading vs multiprocessing]] | threading=I/O, multiprocessing=CPU |
| [[#Q17. What happens if you share a regular `list` between threads?\|asyncio]] | single thread, cooperative, await I/O | [[#Q18b. What is `multiprocessing.Pool` and when do you use it?\|Pool]] | worker pool, pool.map() for CPU tasks |
| [[#Q19. What is the mutable default argument trap?\|mutable default arg]] | def f(x=[]): shared! use None | [[#Q20. Shallow copy vs deep copy — what is the difference?\|shallow vs deep copy]] | shallow=new container same refs |
| [[#Q21. What is the LEGB scope rule?\|LEGB scoping]] | Local→Enclosing→Global→Builtin | [[#Q22. Why does `is` vs `==` matter?\|is vs ==]] | is=same object, ==same value |
| [[#Q24. How do you read a large file efficiently in Python?\|large file]] | iterate lines, don't load all | [[#Q26. Virtual environments — why and how?\|venv]] | isolated packages per project |
| [[#Q28. How would you call a subprocess from Python?\|subprocess]] | run shell commands, capture output | [[#Common Interview Code Snippets\|late binding / list modify]] | closure captures var not value |
| [[#Q41. What is a metaclass and when would you use one?\|metaclasses]] | class of a class, auto-register, enforce | [[#Q42. How do descriptors work in Python?\|descriptors]] | \_\_get\_\_/\_\_set\_\_, property/ORM fields |
| [[#Q43. ABC vs Protocol — when to use which?\|ABC vs Protocol]] | ABC=nominal+runtime, Protocol=structural | [[#Q46. What is `TypeVar` and how does it differ from `Any`?\|TypeVar]] | preserves type relationships, constrained |
| [[#Q48. What is `@overload` and when is it needed?\|@overload]] | multiple signatures, type checker only | [[#Q49. What is `ParamSpec` and when do you need it?\|ParamSpec]] | captures full param signature, decorators |
| [[#Q52. How does the asyncio event loop work internally?\|event loop]] | single thread, I/O poll, cooperative | [[#Q54. `asyncio.gather()` vs `TaskGroup` — which to prefer?\|TaskGroup vs gather]] | TaskGroup cancels siblings on failure |
| [[#Q55. When and how do you use `asyncio.Semaphore`?\|Semaphore]] | limit concurrent fan-out, rate limit | [[#Q58. What is `pyproject.toml` and why did it replace `setup.py`?\|pyproject.toml]] | PEP 621, declarative metadata |
| [[#Q59. Poetry vs pip-tools vs uv — when to use each?\|Poetry/uv]] | uv=fast default, Poetry=all-in-one | [[#Q63. How do pytest fixtures work and what are their scopes?\|fixtures]] | DI for tests, scope=function/session |
| [[#Q69. How do you profile a Python script?\|profiling]] | cProfile first, then line_profiler | [[#Q74. How does the Strategy pattern look in Python?\|Strategy pattern]] | pass callable, no formal interface needed |
| [[#Q79. Explain structural pattern matching (`match/case`).\|match/case]] | structural patterns, not just switch | [[#Q85. `secrets` vs `random` — when does it matter?\|secrets vs random]] | secrets=crypto safe, random=predictable |
| [[#Q91. `argparse` vs `click` vs `typer` — when to use each?\|CLI tools]] | typer=modern, click=complex, argparse=stdlib | [[#Q84. What is `@override` (3.12) and why use it?\|@override]] | catches typos in method overrides |

---

## 1 — Data Structures

### Q1. How does a Python `dict` work internally?
It uses a hash table. Keys are hashed to find a slot; collisions are resolved via open addressing (probing). Since Python 3.7, dicts preserve insertion order as a language guarantee.

### Q2. What makes an object hashable?
It must implement `__hash__()` and `__eq__()`. Mutable objects (lists, dicts, sets) are not hashable by default because their hash could change after being used as a key.

### Q3. `list` vs `tuple` — when do you pick which?
Tuples are immutable, hashable (if contents are hashable), and slightly faster. Use tuples for fixed collections (coordinates, DB rows). Use lists when you need to add/remove items.

### Q4. When would you use a `set` and what are its key operations?
When you need fast membership testing (`O(1)`) or deduplication. Key operations: `union (|)`, `intersection (&)`, `difference (-)`, `symmetric_difference (^)`. Elements must be hashable.

### Q5. What is a `defaultdict` and when is it useful?
A dict subclass from `collections` that calls a factory function for missing keys instead of raising `KeyError`. Useful for grouping (`defaultdict(list)`) or counting (`defaultdict(int)`) without checking key existence.

### Q6. What is the difference between `dict.get(key)` and `dict[key]`?
`dict[key]` raises `KeyError` if the key is missing. `dict.get(key, default)` returns `None` (or a specified default) instead. Use `.get()` when absence is expected, bracket access when it is a bug.

### Q7. How does `collections.OrderedDict` differ from a regular `dict` in Python 3.7+?
Regular dicts preserve insertion order, but `OrderedDict` additionally supports `move_to_end()`, equality comparisons that consider order, and `popitem(last=True/False)`. Use it when order manipulation matters.

### Q7b. What is `collections.Counter` and when is it useful?
`Counter` is a dict subclass for counting hashable objects. `Counter("abracadabra")` → `{'a': 5, 'b': 2, ...}`. `most_common(n)` returns the n most frequent. Useful for frequency analysis, word counting, and histogram building without manual loops.

### Q7c. What is `namedtuple` vs `dataclass`?
`namedtuple` is immutable, lightweight, tuple-based — good for simple data containers. `dataclass` (Python 3.7+) is more flexible — mutable by default, supports default values, methods, `__post_init__`. Use `namedtuple` for simple records you won't modify. Use `dataclass` when you need defaults, type hints, or methods.

---

## 2 — Language Mechanics

### Q8. What is the GIL and why does it matter?
The Global Interpreter Lock ensures only one thread executes Python bytecode at a time. It makes CPython thread-safe but limits CPU-bound parallelism. For CPU work, use `multiprocessing`; the GIL is released during I/O, so threading is fine for I/O-bound tasks.

### Q9. Explain decorators in plain terms.
A decorator is a function that takes another function, wraps it with additional behavior, and returns the wrapper. Syntactic sugar: `@decorator` above a function definition is equivalent to `func = decorator(func)`. Always use `@functools.wraps` to preserve the original function's metadata.

### Q10. What is a generator and why use one?
A function that uses `yield` instead of `return`. It produces values lazily one at a time, keeping its state between calls. Memory-efficient for large datasets — processing a 10GB log file line by line instead of loading it all into memory.

### Q11. What is a context manager and how do you write one?
An object implementing `__enter__` and `__exit__` for setup/teardown (e.g., file handles, DB connections, locks). Easiest way: `@contextlib.contextmanager` with a `try/yield/finally` block. Guarantees cleanup even on exceptions.

### Q12. Explain `*args` and `**kwargs`.
`*args` collects positional arguments into a tuple, `**kwargs` collects keyword arguments into a dict. Used to write flexible functions or wrap/proxy other functions (common in decorators and CLI tools).

### Q13. What are `__str__` vs `__repr__`?
`__repr__` is for developers (unambiguous, ideally valid Python to recreate the object). `__str__` is for end users (readable). If only one is defined, implement `__repr__` — `print()` falls back to it.

### Q14. What does `if __name__ == '__main__':` do?
It guards code that should only run when the file is executed directly, not when imported as a module. Essential for scripts that are also importable libraries, and for keeping test/demo code out of imports.

### Q14b. What are `__slots__` and why would you use them?
`__slots__` restricts instance attributes to a fixed set, eliminating the per-instance `__dict__`. Saves memory (~40% for objects with few attributes) and speeds up attribute access. Use for classes with many instances (millions of data points). Don't use for classes that need dynamic attributes or inheritance flexibility.

### Q14c. Explain `property` decorator — getter, setter, deleter.
`@property` turns a method into a read-only attribute. Add `@x.setter` for write access. Useful for computed attributes, validation on set, and lazy initialization. Example: `@property def full_name(self): return f"{self.first} {self.last}"` — accessed as `obj.full_name`, not `obj.full_name()`.

### Q14d. What is `__init__` vs `__new__`?
`__new__` creates the instance (allocates memory), `__init__` initializes it (sets attributes). You rarely override `__new__` — only for immutable types (like extending `int` or `str`) or implementing singletons. For normal classes, `__init__` is all you need.

---

## 3 — Concurrency

### Q15. `threading` vs `multiprocessing` vs `asyncio` — when to use each?
`threading`: I/O-bound tasks (API calls, file reads) — threads release the GIL on I/O. `multiprocessing`: CPU-bound tasks (data crunching) — separate processes, each with its own GIL. `asyncio`: high-concurrency I/O (thousands of connections) — single thread, event loop, non-blocking.

### Q16. What is `concurrent.futures` and why prefer it?
A high-level abstraction over threading and multiprocessing. `ThreadPoolExecutor` and `ProcessPoolExecutor` share the same API, so you can switch between them with one line. Use `executor.map()` or `executor.submit()` + `as_completed()`.

### Q17. What happens if you share a regular `list` between threads?
Individual operations like `append()` are thread-safe in CPython due to the GIL, but compound operations (check-then-act) are not. Use `queue.Queue`, `threading.Lock`, or `collections.deque` for safe inter-thread communication.

### Q18. How does `asyncio` differ from threading in practice?
`asyncio` uses cooperative multitasking — coroutines explicitly `await` to yield control. No thread-switching overhead, no race conditions from preemption. But one blocking call (e.g., `time.sleep()` instead of `await asyncio.sleep()`) stalls the entire event loop.

### Q18b. What is `multiprocessing.Pool` and when do you use it?
`Pool` manages a pool of worker processes. `pool.map(func, items)` distributes items across processes and collects results. Use for CPU-bound tasks that can be parallelized — image processing, data transformation, batch computation. Each process has its own GIL, so true parallelism. Overhead: process creation is expensive, data must be serializable (pickle) to pass between processes.

### Q18c. Explain `queue.Queue` vs `asyncio.Queue`.
`queue.Queue` is thread-safe, blocks on get/put. Used in threading. `asyncio.Queue` is for coroutines, uses `await` for get/put. Used in async code. Don't mix them — using `queue.Queue` in async code blocks the event loop.

---

## 4 — Common Gotchas

### Q19. What is the mutable default argument trap?
Default arguments are evaluated once at function definition, not per call. `def f(items=[])` shares the same list across all calls. Fix: use `None` as default and create inside the function: `if items is None: items = []`.

### Q20. Shallow copy vs deep copy — what is the difference?
Shallow copy (`copy.copy()`, `list[:]`, `dict.copy()`) creates a new container but references the same nested objects. Deep copy (`copy.deepcopy()`) recursively copies everything. Matters when you have nested mutable structures.

### Q21. What is the LEGB scope rule?
Python resolves names in order: Local, Enclosing (closure), Global, Built-in. If you assign to a variable inside a function, Python treats it as local for the entire function — which is why you get `UnboundLocalError` if you read it before assignment.

### Q22. Why does `is` vs `==` matter?
`is` checks identity (same object in memory), `==` checks equality (same value). `is` should only be used for singletons (`None`, `True`, `False`). CPython caches small integers (-5 to 256), so `a is b` may work for small ints but fail for large ones.

### Q23. What happens with `except Exception as e` vs bare `except:`?
Bare `except:` catches everything including `SystemExit` and `KeyboardInterrupt`, which you almost never want. `except Exception` catches normal errors but lets system-level exceptions propagate. Always be specific about what you catch.

---

## 5 — Practical / DevOps

### Q24. How do you read a large file efficiently in Python?
Iterate line by line: `for line in open(file)` or use a context manager. Never `file.read()` for large files — it loads everything into memory. For binary data, read in chunks: `while chunk := f.read(8192)`.

### Q25. How do you handle errors in a production script?
Use specific exception types, not bare `except`. Log with the `logging` module (not `print`). Use `try/except/finally` for cleanup. For CLI tools, catch at the top level, log the traceback, and return a non-zero exit code.

### Q26. Virtual environments — why and how?
Isolate project dependencies from the system Python. `python -m venv .venv` creates one. Activate it to get an isolated `pip`. In CI/CD, always use venvs or containers. Modern alternative: `uv` for faster installs and lockfiles.

### Q27. `pip freeze` vs `requirements.txt` vs `pyproject.toml`?
`pip freeze` dumps all installed packages (including transitive deps) — useful for reproducible locks. `requirements.txt` is the classic format. Modern projects use `pyproject.toml` (PEP 621) as the single source of truth, often with `pip-tools` or `uv` for locking.

### Q28. How would you call a subprocess from Python?
Use `subprocess.run()` (Python 3.5+). Pass args as a list, not a string, to avoid shell injection. Use `capture_output=True` for stdout/stderr, `check=True` to raise on non-zero exit, and `timeout` to prevent hangs. Never use `os.system()`.

### Q29. How do you make a Python script into a proper CLI tool?
Use `argparse` (stdlib) or `click`/`typer` (third-party). Define arguments, flags, subcommands, and help text. Add `if __name__ == '__main__'` guard. For distribution, define an entry point in `pyproject.toml` so `pip install` creates a command.

### Q29b. How do you handle configuration in Python scripts?
For simple scripts: environment variables via `os.environ` + `.env` files via `python-dotenv`. For complex tools: `click` library for CLI args + YAML config files via `ruamel.yaml`. Never hardcode config — always externalize.

### Q29c. How do you structure a Python project for maintainability?
```
src/
  mypackage/
    __init__.py
    core.py
    cli.py
tests/
  test_core.py
pyproject.toml
```
Use `pyproject.toml` (PEP 621) instead of `setup.py`. Type hints everywhere. `pytest` for testing. `black` for formatting, `ruff` for linting, `mypy` for type checking.

---

## 6 — One-Liners and Comprehensions

### Q30. List comprehension vs `map()`/`filter()` — which to prefer?
List comprehensions are more Pythonic and readable for simple transformations. `map()`/`filter()` with lambdas are harder to read. Use generator expressions `(x for x in ...)` when you do not need the full list in memory.

### Q31. Write a one-liner to flatten a list of lists.
`flat = [item for sublist in nested for item in sublist]`. For arbitrary depth, use `itertools.chain.from_iterable()` or recursion. Note: deeply nested structures are rare in practice — if you have them, rethink the data model.

### Q32. How do you merge two dicts in one line?
Python 3.9+: `merged = d1 | d2` (right side wins on conflicts). Python 3.5+: `merged = {**d1, **d2}`. Both create a new dict. Use `d1 |= d2` (3.9+) for in-place update.

### Q33. What is the walrus operator `:=`?
Assignment expression (Python 3.8+). Assigns and returns a value in one expression. Common use: `while chunk := f.read(8192)` or `if (m := re.match(pattern, text))`. Avoid overusing it — readability matters.

### Q34. How do you sort a list of dicts by a key?
`sorted(items, key=lambda x: x['name'])` or use `operator.itemgetter('name')` for better performance. Both return a new list. Use `reverse=True` for descending. `list.sort()` sorts in place.

---

## 7 — Type Hints and Modern Python (3.10+)

### Q35. Why use type hints in a dynamically typed language?
They catch bugs early via `mypy`/`pyright`, serve as documentation, enable better IDE autocomplete, and make refactoring safer. They are not enforced at runtime by default — they are for tooling and readability.

### Q36. What changed with types in Python 3.10+?
`match/case` (structural pattern matching) in 3.10. Union types as `X | Y` instead of `Union[X, Y]`. Built-in generics: `list[int]` instead of `List[int]`. `TypeAlias` for explicit type aliases. `ParamSpec` and `TypeVarTuple` for advanced decorator typing.

### Q37. What is `typing.Protocol` and when do you use it?
Structural subtyping (duck typing with type checking). Define an interface as a `Protocol` class with method signatures. Any class matching those signatures satisfies the protocol — no inheritance needed. Perfect for dependency injection and plugin systems.

### Q38. How do you type hint a decorator?
Use `ParamSpec` (3.10+) and `TypeVar` to preserve the wrapped function's signature. Without this, the decorator erases the type information of the original function. This is the primary reason `@functools.wraps` alone is not enough for type checkers.

### Q39. What is `dataclasses.dataclass` and when to use it over a plain class?
`@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from annotated fields. Use for data containers (config objects, API responses, DTOs). Use `frozen=True` for immutable instances. For validation, use Pydantic instead.

### Q40. What is `TypedDict` and where is it useful?
Defines type hints for dicts with specific string keys and value types. Useful for typing JSON payloads, API responses, or config dicts where you cannot use a dataclass. Enforced by type checkers, not at runtime.

---

## Rapid-Fire Bonus

| Question | Answer |
|----------|--------|
| `any()` vs `all()`? | `any()` — True if at least one True. `all()` — True if all True. Both short-circuit. |
| What does `enumerate()` do? | Returns index-value pairs: `for i, val in enumerate(items)`. Takes optional `start` param. |
| `zip()` behavior on unequal lengths? | Stops at shortest. Use `itertools.zip_longest()` to pad. Python 3.10+: `zip(strict=True)` raises. |
| How to make a class iterable? | Implement `__iter__()` returning an iterator with `__next__()`. Or just `yield` in `__iter__`. |
| `@staticmethod` vs `@classmethod`? | `@staticmethod` has no access to class/instance. `@classmethod` gets `cls` as first arg — used for factory methods. |

---

## Common Interview Code Snippets

### "What's wrong with this code?"

Mutable default argument:
```python
# BAD — default list shared across all calls
def add_item(item, items=[]):
    items.append(item)
    return items
# add_item(1) → [1], add_item(2) → [1, 2] ← surprise!

# FIX
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

Late binding closure:
```python
# BAD — all functions return 4 (last value of i)
functions = [lambda: i for i in range(5)]
[f() for f in functions]  # [4, 4, 4, 4, 4]

# FIX — capture i as default argument
functions = [lambda i=i: i for i in range(5)]
[f() for f in functions]  # [0, 1, 2, 3, 4]
```

Checking type wrong:
```python
# BAD — doesn't handle inheritance
if type(x) == dict: ...

# FIX — isinstance handles subclasses
if isinstance(x, dict): ...
```

File not closed:
```python
# BAD — file handle leaked if exception occurs
f = open("data.txt")
data = f.read()
f.close()  # never reached if read() throws

# FIX — context manager
with open("data.txt") as f:
    data = f.read()
```

Modifying list while iterating:
```python
# BAD — skips elements, unpredictable behavior
for item in items:
    if should_remove(item):
        items.remove(item)

# FIX — iterate over a copy or use list comprehension
items = [item for item in items if not should_remove(item)]
```

---

## 8 — Advanced Python: Metaclasses, Descriptors, ABC, Protocols

### Q41. What is a metaclass and when would you use one?
A metaclass is the "class of a class" — it controls how classes themselves are created. The default metaclass is `type`. You define a custom metaclass by inheriting from `type` and overriding `__new__` or `__init_subclass__`. Use cases: auto-registering plugin classes, enforcing class-level constraints (e.g., all methods must have docstrings), injecting methods or attributes. Frameworks like Django ORM and SQLAlchemy use metaclasses internally. Rule of thumb: metaclasses are a last resort — prefer decorators, class decorators, or `__init_subclass__` first.

### Q42. How do descriptors work in Python?
A descriptor is any object that defines `__get__`, `__set__`, or `__delete__`. When an attribute lookup finds a descriptor on the class, Python calls the descriptor's method instead of returning the object directly. Data descriptors (with `__set__` or `__delete__`) take priority over instance `__dict__`. Non-data descriptors (only `__get__`) do not. `property`, `classmethod`, `staticmethod`, and Django model fields are all descriptors. Use descriptors for reusable attribute validation logic — e.g., a `PositiveInteger` descriptor you can attach to multiple classes.

### Q43. ABC vs Protocol — when to use which?
`abc.ABC` uses nominal subtyping — you explicitly inherit and implement abstract methods. The type checker and runtime both enforce it (`TypeError` on instantiation if abstract methods are missing). `typing.Protocol` uses structural subtyping — any class matching the method signatures satisfies it, no inheritance needed. Use ABC when you control the hierarchy and want runtime enforcement. Use Protocol for duck typing with static analysis — e.g., anything with a `.read()` method satisfies `Readable`. Protocol is better for dependency injection and third-party code you cannot modify.

### Q44. What is `__init_subclass__` and why is it often preferred over metaclasses?
Introduced in Python 3.6, `__init_subclass__` is called whenever a class is subclassed. It lets the parent class hook into subclass creation without a metaclass. Common use: auto-registering subclasses in a registry dict. It is simpler, more readable, and avoids metaclass conflicts (a class can only have one metaclass, but `__init_subclass__` composes freely).

### Q45. Explain `__set_name__` in descriptors.
Added in Python 3.6, `__set_name__(self, owner, name)` is called when the descriptor is assigned to a class attribute. It receives the attribute name, so the descriptor can store it without the user passing the name manually. Before 3.6, you had to use a metaclass or pass the name as a string.

---

## 9 — Advanced Typing: TypeVar, Generic, Protocol, Overload

### Q46. What is `TypeVar` and how does it differ from `Any`?
`TypeVar` defines a type variable for generic functions/classes. `T = TypeVar('T')` means "some specific type, determined at call time." Unlike `Any` (which opts out of type checking), `TypeVar` preserves relationships: if `def first(items: list[T]) -> T`, the return type matches the input element type. You can constrain: `T = TypeVar('T', int, str)` restricts to those types. You can also bound: `T = TypeVar('T', bound=Comparable)`.

### Q47. How do you create a generic class?
Inherit from `Generic[T]` (or use the 3.12 syntax: `class Stack[T]:`). This makes `T` a valid type within the class body. Example: `class Stack(Generic[T])` with `push(self, item: T)` and `pop(self) -> T`. Users write `Stack[int]` for type checking. Without `Generic`, there is no way to parameterize the class.

### Q48. What is `@overload` and when is it needed?
`@overload` from `typing` lets you declare multiple type signatures for a single function. The overloaded signatures are for the type checker only — the actual implementation is a single function (without `@overload`) that handles all cases. Use it when the return type depends on the input type in ways a `TypeVar` cannot express. Example: `json.loads()` returning `dict` for a dict string, `list` for a list string.

### Q49. What is `ParamSpec` and when do you need it?
`ParamSpec` (3.10+) captures the entire parameter signature of a callable. Essential for typing decorators that pass through `*args, **kwargs` to the wrapped function without losing type information. Without `ParamSpec`, decorated functions lose their parameter types in the type checker.

### Q50. Covariance and contravariance in Python typing?
Covariant (`TypeVar('T', covariant=True)`) means `Box[Dog]` is a subtype of `Box[Animal]` — safe for read-only containers. Contravariant (`TypeVar('T', contravariant=True)`) means `Processor[Animal]` is a subtype of `Processor[Dog]` — safe for write-only/consumer contexts. Invariant (default) means no subtyping relationship. `Sequence` is covariant, `list` is invariant (because it is mutable).

### Q51. Python 3.12 type parameter syntax?
Python 3.12 introduces native syntax: `def first[T](items: list[T]) -> T:` and `class Stack[T]:` — no need to import `TypeVar` or `Generic`. Cleaner, less boilerplate. Also adds `type` statement for type aliases: `type Vector = list[float]`.

---

## 10 — asyncio Deep Dive

### Q52. How does the asyncio event loop work internally?
The event loop runs in a single thread, maintaining a queue of ready callbacks and a set of I/O watchers (via `selectors`/`epoll`/`kqueue`). On each iteration: run ready callbacks, poll for I/O events (with timeout from nearest scheduled callback), then add newly ready callbacks. `await` is a yield point — the coroutine suspends and the event loop runs other tasks. This is cooperative multitasking: one blocking call (e.g., `time.sleep()` instead of `await asyncio.sleep()`) stalls everything.

### Q53. `asyncio.create_task()` vs `await` directly?
`await coro()` runs the coroutine inline — the caller waits for it. `asyncio.create_task(coro())` schedules it to run concurrently and returns a `Task` object. Use `create_task` when you want concurrency. The task starts running at the next `await` point. Always store task references — if a task is garbage collected, it is cancelled silently.

### Q54. `asyncio.gather()` vs `TaskGroup` — which to prefer?
`gather(*coros)` runs all concurrently and returns results as a list. But if one fails, others keep running (unless `return_exceptions=True`). `TaskGroup` (3.11+) is preferred: it cancels sibling tasks on first failure, prevents orphan tasks, and uses structured concurrency with `async with`. Use `TaskGroup` for new code; `gather` is legacy.

### Q55. When and how do you use `asyncio.Semaphore`?
Use Semaphore to limit concurrency when fanning out to external services — spawning 10,000 tasks hitting the same API exhausts connections and triggers rate limits. `sem = asyncio.Semaphore(20)` then `async with sem: await fetch(url)`. Match the limit to your connection pool size or API rate limit. `BoundedSemaphore` raises if released more times than acquired.

### Q56. How do you run blocking code in asyncio?
Use `loop.run_in_executor(None, blocking_func, arg)` to push CPU-bound or blocking I/O to a thread pool (default) or process pool. This prevents blocking the event loop. In 3.9+, use `asyncio.to_thread(blocking_func, arg)` as a shortcut. Never call blocking functions directly in async code.

### Q57. What are exception groups and `except*`?
Python 3.11 added `ExceptionGroup` — a container for multiple exceptions raised simultaneously. `TaskGroup` raises `ExceptionGroup` when multiple tasks fail. Handle with `except* ValueError as eg:` syntax, which catches matching exceptions from the group while re-raising the rest. This enables proper error handling in concurrent scenarios where multiple things fail at once.

---

## 11 — Packaging and Distribution

### Q58. What is `pyproject.toml` and why did it replace `setup.py`?
`pyproject.toml` (PEP 517/518/621) is the modern standard for Python project metadata. `[build-system]` declares the build backend (setuptools, hatchling, poetry-core, uv_build). `[project]` holds name, version, dependencies, entry points. It replaces `setup.py` (imperative, arbitrary code execution) with a declarative, standardized format. All modern tools support it.

### Q59. Poetry vs pip-tools vs uv — when to use each?
`pip-tools`: minimal, generates `requirements.txt` lockfiles from `requirements.in`. Good for existing projects. `Poetry`: all-in-one (init, add, lock, build, publish) with `poetry.lock`. Good for libraries. Poetry 2.0+ supports standard `[project]` table. `uv`: fastest option (Rust-based), drop-in pip replacement with lockfile support, virtual env management. 2025 pragmatic default for new projects. All solve the same core problem: deterministic dependency resolution.

### Q60. What is a wheel and why does it matter?
A wheel (`.whl`) is a pre-built binary distribution format (PEP 427). Unlike sdist (source), wheels skip the build step during install — no compilation needed. This means faster installs, no build toolchain required on the target machine, and reproducible deployments. `pip wheel .` builds one. For C extensions, you might need platform-specific wheels (manylinux, macosx).

### Q61. How do entry points work in `pyproject.toml`?
```toml
[project.scripts]
mytool = "mypackage.cli:main"
```
When the package is `pip install`ed, pip creates a wrapper script `mytool` in the bin/Scripts directory that calls `mypackage.cli.main()`. This is how CLI tools become system commands. For plugins, use `[project.entry-points."group_name"]`.

### Q62. What is the `src` layout and why use it?
Placing code under `src/mypackage/` instead of `mypackage/` prevents accidentally importing the local package during development (instead of the installed version). It forces you to install the package to test it, catching packaging bugs early. Recommended by PyPA and most modern build tools.

---

## 12 — Testing: pytest Advanced

### Q63. How do pytest fixtures work and what are their scopes?
Fixtures are dependency injection for tests. Declare with `@pytest.fixture`, use by naming the fixture as a test parameter. Scopes: `function` (default, per-test), `class`, `module`, `package`, `session`. Higher scopes share the fixture across tests — e.g., `scope="session"` creates a DB connection once for all tests. Use `yield` for setup/teardown. `autouse=True` applies a fixture to all tests without explicitly requesting it.

### Q64. What is `conftest.py` and how does fixture sharing work?
`conftest.py` is auto-discovered by pytest — no import needed. Place fixtures in `conftest.py` for automatic sharing across all tests in that directory and subdirectories. You can have multiple `conftest.py` files at different levels. Use for shared fixtures (DB connections, API clients, temp directories), custom markers, and pytest plugins.

### Q65. How does `@pytest.mark.parametrize` work?
Runs the same test with different inputs. `@pytest.mark.parametrize("x,expected", [(1,2),(3,4)])` generates two test cases. Supports multiple parametrize decorators for cartesian product. Indirect parametrization passes values through a fixture via `request.param`. Use `pytest.param(..., id="name")` for readable test IDs.

### Q66. Mocking in pytest: `monkeypatch` vs `unittest.mock`?
`monkeypatch` is pytest-native: `monkeypatch.setattr`, `monkeypatch.setenv`, `monkeypatch.delattr`. Auto-reverted after each test. `unittest.mock.patch` is more powerful: `MagicMock`, `PropertyMock`, `spec=True` for safe mocking, `assert_called_once_with()`. Use `monkeypatch` for simple env/attr overrides, `mock.patch` for complex mocking with assertions. Always mock at the import location, not the definition location.

### Q67. What is `pytest.raises` and how to use it properly?
Context manager for asserting exceptions: `with pytest.raises(ValueError, match="invalid")`. The `match` parameter checks the exception message against a regex. For checking exception attributes, use `excinfo = pytest.raises(...); excinfo.value.code == 42`. Always test the specific exception type and message — not just "it raised something."

### Q68. How do you test async code with pytest?
Use `pytest-asyncio` plugin. Mark tests with `@pytest.mark.asyncio`. Async fixtures also work. For testing event loop behavior, use `asyncio.TaskGroup` or mock the event loop. `anyio` backend support allows testing with both asyncio and trio.

---

## 13 — Performance: Profiling and Optimization

### Q69. How do you profile a Python script?
Start with `cProfile`: `python -m cProfile -s cumtime script.py` — shows call count, total time, cumulative time per function. Identify hotspots. Then drill down with `line_profiler`: `@profile` decorator + `kernprof -l -v script.py` — shows time per line within a function. For memory: `memory_profiler` or `tracemalloc` (stdlib). Strategy: profile first, optimize second — never guess.

### Q70. What are common Python performance optimizations?
Algorithm first (O(n^2) to O(n log n) beats any micro-optimization). Then: use built-in data structures (dict/set for O(1) lookups), avoid unnecessary copies, use generators for large datasets, prefer list comprehensions over loops, use `functools.lru_cache` for expensive repeated computations, avoid global variable lookups in tight loops. For CPU-bound: `multiprocessing`, C extensions (`cython`), or `numpy` for numeric work.

### Q71. What is `functools.lru_cache` and when to use it?
Memoization decorator that caches function results based on arguments. `@lru_cache(maxsize=128)` caches up to 128 unique argument combinations. Arguments must be hashable. Use for expensive pure functions called repeatedly with same args (fibonacci, API lookups with same params). `cache_info()` shows hit/miss stats. Python 3.9+: `@cache` is `lru_cache(maxsize=None)`.

### Q72. `__slots__` for performance — how much does it help?
Eliminates per-instance `__dict__`, saving ~40% memory per instance. Also speeds up attribute access. Critical when creating millions of objects (data processing, graph nodes). Trade-off: no dynamic attributes, some inheritance complications. Combine with `dataclass(slots=True)` in 3.10+.

### Q73. When should you reach for Cython or C extensions?
When profiling shows a pure-Python function is the bottleneck and algorithmic optimization is exhausted. `Cython` adds C-like type declarations to Python code for 10-100x speedups in numeric/loop-heavy code. `cffi` or `ctypes` for calling existing C libraries. For numeric work, `numpy` vectorization is usually enough. Do not prematurely optimize — most Python code is I/O-bound, not CPU-bound.

---

## 14 — Design Patterns in Python

### Q74. How does the Strategy pattern look in Python?
In Python, you do not need a formal Strategy interface — just pass a callable. Functions are first-class objects, so `def process(data, strategy: Callable)` works. For more structure, use a `Protocol` with a single method. Real use: pluggable serializers (JSON/YAML/TOML), configurable retry policies, interchangeable auth backends. Maps to Open/Closed principle.

### Q75. Factory pattern in Python?
A function or classmethod that returns instances of different classes based on input. `def create_notifier(type: str) -> Notifier:` returns `EmailNotifier` or `SlackNotifier`. Python idiom: use a dict mapping names to classes: `factories = {"email": EmailNotifier, "slack": SlackNotifier}; return factories[type]()`. Avoids long if/elif chains.

### Q76. Observer pattern in Python?
Subject maintains a list of callbacks (observers). When state changes, it calls each. Python approach: use a list of callables or `signal`/`blinker` library. Modern alternative: `asyncio` events or message queues for decoupled systems. Use for plugin hooks, event-driven architectures, UI updates.

### Q77. Singleton in Python — is it even needed?
Python modules are natural singletons — module-level variables are shared across imports. If you must enforce single instance: use a module, or `__new__` override, or a class variable check. The Borg pattern (shared `__dict__`) is a Python-specific alternative. But usually, a module-level instance is simpler and more Pythonic.

### Q78. Decorator pattern vs Python decorators?
The GoF Decorator pattern wraps an object to add behavior. Python `@decorator` syntax wraps a function. They are related but not identical. GoF Decorator: `class LoggingService(ServiceWrapper):` that adds logging around a service. Python decorator: `@retry(max=3)` that wraps a function with retry logic. In Python, both function decorators and class composition are used.

---

## 15 — Python 3.10-3.12 Features

### Q79. Explain structural pattern matching (`match/case`).
Python 3.10 added `match/case` — not a switch statement, but structural pattern matching. Matches against patterns including literals, sequences, mappings, class instances, and combinations. Supports guards (`case x if x > 0`), capture variables, wildcards (`_`), and OR patterns (`case 200 | 201`). Best for parsing command objects, AST nodes, protocol messages, or complex data structures. Avoid using it as a simple if/elif replacement.

### Q80. What are exception groups and `except*` (3.11)?
`ExceptionGroup("msg", [exc1, exc2])` bundles multiple exceptions. `except* TypeError as eg:` catches only `TypeError` instances from the group, re-raising the rest. Designed for concurrent code where multiple tasks fail simultaneously (`TaskGroup`). You can nest exception groups. `exceptiongroup` backport available for 3.9+.

### Q81. What is `tomllib` (3.11)?
Built-in TOML parser — read-only. `import tomllib; with open("config.toml", "rb") as f: data = tomllib.load(f)`. Must open in binary mode. For writing TOML, use third-party `tomli-w`. Added because `pyproject.toml` became the standard — Python itself needs to parse TOML.

### Q82. Python 3.11 performance improvements?
Faster CPython project: 10-60% faster than 3.10 (average 1.25x on benchmarks). Specializing adaptive interpreter: bytecodes specialize based on observed types. Zero-cost exception handling: `try` blocks have no overhead when no exception is raised. Better error messages with precise line-in-expression indicators.

### Q83. Python 3.12 key features?
Type parameter syntax (`def f[T](x: T) -> T:`), `type` statement for aliases, per-interpreter GIL (experimental), improved f-string parsing (nested quotes allowed), `@override` decorator from `typing`, improved error messages (did-you-mean suggestions for `import` errors), `pathlib` improvements.

### Q84. What is `@override` (3.12) and why use it?
`from typing import override`. Place on methods that override a parent class method. The type checker raises an error if the parent does not have that method — catches typos and refactoring mistakes. Similar to Java's `@Override`. Not enforced at runtime by default.

---

## 16 — Security in Python

### Q85. `secrets` vs `random` — when does it matter?
`random` uses a Mersenne Twister PRNG — predictable, not for security. `secrets` uses `os.urandom()` — cryptographically secure. Use `secrets` for tokens, passwords, session IDs, API keys. `secrets.token_hex(32)`, `secrets.token_urlsafe(32)`, `secrets.compare_digest()` for timing-safe comparison.

### Q86. How do you hash passwords in Python?
Never use `hashlib` alone (no salt, fast = brute-forceable). Use `bcrypt`, `argon2-cffi`, or `hashlib.scrypt()`. These are deliberately slow (key stretching) and auto-salt. For simple cases: `from hashlib import scrypt; hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1)`. In Django: `PBKDF2` by default. Always store the hash, never the password.

### Q87. How do you prevent command injection in Python?
Pass command arguments as a list, not a string: `subprocess.run(["ls", "-la", user_input])` — each element is a separate argument, no shell interpretation. Never use `shell=True` with user input. Never use `os.system()`. Validate and sanitize all user input before passing to any external command.

### Q88. What is `hmac.compare_digest()` and why use it?
Timing-safe comparison for digests/tokens. Regular `==` comparison short-circuits on first mismatch, leaking information about correct characters via timing differences. `hmac.compare_digest(a, b)` takes constant time regardless of where strings differ. Always use for comparing authentication tokens, HMAC digests, or password hashes.

### Q89. How do you handle secrets in Python applications?
Never hardcode secrets. Use environment variables (`os.environ["API_KEY"]`) with `.env` files (via `python-dotenv`) for development. In production: use a secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault). For CI/CD: use pipeline secret variables. Validate secrets exist at startup — fail fast if missing rather than failing mid-operation.

### Q90. Input validation best practices?
Validate type, length, format, and range at the boundary (API endpoints, CLI input, file parsing). Use `pydantic` for structured validation with type coercion and custom validators. For web: sanitize HTML, escape SQL (use parameterized queries), validate URLs/emails with purpose-built libraries. Never trust user input — validate even if the frontend "already validated."

---

## 17 — CLI Tools: argparse, click, typer

### Q91. `argparse` vs `click` vs `typer` — when to use each?
`argparse`: stdlib, zero dependencies, verbose but always available. Good for simple scripts in constrained environments. `click`: decorator-based, composable commands, rich features (prompts, colors, progress bars), widely adopted. Good for complex CLIs with subcommands. `typer`: built on click, uses type hints for argument definitions — minimal boilerplate. Good for modern Python with type hints. For DevOps tooling, `click` or `typer` are preferred for maintainability.

### Q92. How do you build a CLI with subcommands?
`argparse`: `subparsers = parser.add_subparsers()`. `click`: `@click.group()` + `@cli.command()`. `typer`: `app = typer.Typer(); @app.command()`. All three support nested subcommands (e.g., `mytool deploy staging`, `mytool config set key value`). click/typer compose better — each subcommand can live in its own module.

### Q93. How do you distribute a CLI tool?
Define entry points in `pyproject.toml`: `[project.scripts] mytool = "mypackage.cli:main"`. After `pip install`, the command is available system-wide. For standalone distribution: `pipx` installs CLI tools in isolated environments. For broader distribution: `shiv` or `pex` create single-file executables. Docker is another option for complex dependencies.

### Q94. How do you handle CLI configuration and defaults?
Precedence (highest to lowest): CLI flags > environment variables > config file > hardcoded defaults. `click` supports this via `auto_envvar_prefix` and `default_map`. `typer` uses `typer.Option(envvar="MY_VAR")`. For config files: `tomllib` to parse `~/.mytool/config.toml`. Always document the precedence in `--help`.

### Q95. Testing CLI tools?
`click` provides `CliRunner` for isolated testing: `result = runner.invoke(cli, ["--flag", "arg"]); assert result.exit_code == 0`. `typer` has `typer.testing.CliRunner`. For `argparse`: call the main function directly with sys.argv mocking. Always test both success and error paths, help output, and edge cases (missing args, invalid input).

---

## Sorulursa

> [!faq]- "Python vs C# — when do you choose which?"
> C# for application code — microservices, APIs, business logic. Type safety, performance, rich ecosystem for backend. Python for automation, scripting, and tooling — fast to write, easy to read, great for gluing systems together. Different tools, different jobs.

> [!faq]- "How do you handle errors in Python scripts?"
> Specific exceptions, not bare `except:`. Log the error with context (what operation, what input). For automation scripts: fail fast and loud — if a deployment step fails, stop and alert, don't continue with a broken state. Use `try/except/finally` for cleanup (close connections, release resources). Retry logic with exponential backoff for transient failures (network, API rate limits).

> [!faq]- "How do you test Python code?"
> `pytest` for everything. Fixtures for test setup (database connections, temp files). `unittest.mock.patch` for mocking external calls. Structure: `tests/` directory mirroring `src/`, one test file per module. `flake8` + `mypy` + `pytest` enforced in CI pipeline.
