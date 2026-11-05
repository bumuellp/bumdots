Additionally, apply these JavaScript/TypeScript-specific checks:

SECURITY

- Prototype pollution, unsafe **proto**/Object merges, and untrusted JSON.parse use.
- eval/new Function/setTimeout-with-string, and dynamic require/import of user input.
- XSS via innerHTML/dangerouslySetInnerHTML/insertAdjacentHTML; missing sanitization.
- ReDoS-prone regexes; unbounded user-controlled regex.
- Insecure npm deps and scripts; postinstall risks; unpinned versions.

TYPES & CORRECTNESS

- any/unknown escapes, unsafe as-casts, non-null assertions (!) hiding bugs.
- Missing strict mode (strict, noUncheckedIndexedAccess); == vs ===; NaN handling.
- Floating promises / unhandled rejections; missing await; forgotten error handling.
- Mutating shared state; incorrect this binding; closures capturing stale values.

ASYNC & PERFORMANCE

- Sequential awaits that should be Promise.all; blocking the event loop with sync I/O
  or heavy CPU; memory leaks from listeners/timers not cleaned up.
- Large synchronous loops; unnecessary array copies; N+1 across awaits.

QUALITY

- Barrel-file circular deps; inconsistent module boundaries; leaking internal types.
- Proper discriminated unions and exhaustiveness; avoid enum foot-guns.

Report in the base prompt's format, citing exact file:line.
