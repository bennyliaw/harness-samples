# 002 — Cart and pricing

A small shop back end in three modules:

- `src/catalog.py` — the product catalogue and SKU normalisation
- `src/pricing.py` — volume discount tiers
- `src/cart.py`    — the cart that ties the two together

`pytest` is red. Some of the failures show up in a module that is itself
correct: a cart test can fail because of how the catalogue normalises a SKU,
and a total can be wrong because of where a pricing tier begins. Follow each
failure to the module that actually owns the behaviour rather than patching it
where it surfaces.

**Your task:** make the test suite pass by changing files under `src/`.

The docstrings state the intended contracts — SKU canonical form, whether
adding a SKU twice accumulates, and whether the discount tiers include their
threshold. The tests are the specification.

See `AGENTS.md` at the repo root for the rules. In short: fix `src/`, never
`tests/`, standard library only.
