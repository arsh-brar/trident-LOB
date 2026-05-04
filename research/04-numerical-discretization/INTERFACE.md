# Numerical Discretization Interface

## Purpose

This is a Phase 0 research interface, not production code. It defines the minimum contracts a later numerical component should satisfy while remaining swappable inside the TRIDENT architecture. Recommendation: keep the discretization interface separate from data adapters, feature builders, model fitting, backtesting, paper trading, and risk management. Sources: repository architecture preference, file:///Users/arshbrar/Development/GitHub/trident_LOB/AGENTS.md; Python architecture decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Coordinate Contract

`PriceGrid` should describe the tick grid:

```text
symbol
venue
tick_size
reference_price
tick_min
tick_max
delta_p_ticks = 1
cell_count
coordinate_mode = fixed_ticks | mid_centered_ticks
```

Recommendation: default to fixed tick indices for Phase 1 fixtures and allow a later `mid_centered_ticks` mode only if conservative remapping is validated. Sources: SEC tick-size guide, https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/tick-sizes; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253.

`TimeGrid` should describe event and solver time:

```text
start_time
end_time
event_timestamps
clock_window_seconds
solver_substep_seconds
time_mode = clock | event | hybrid
```

Recommendation: keep event time and solver substep time separate because order-book events are irregular while explicit numerical updates are stability limited. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; CFL condition, https://doi.org/10.1147/rd.112.0215.

## State Contract

`LiquidityState` should hold side-specific arrays:

```text
q_plus[cell_count]
q_minus[cell_count]
u_plus[cell_count]
u_minus[cell_count]
```

`TurbulenceState` should hold:

```text
k[cell_count]
epsilon[cell_count]
nu_t[cell_count]
```

`LatentState` should hold optional Phase 2 arrays:

```text
ell_plus[cell_count]
ell_minus[cell_count]
phi[cell_count]
interface_tick
```

Recommendation: store states as arrays over tick cells with explicit side labels, because TRIDENT has side-specific liquidity and quote-velocity equations. Source: TRIDENT model specification, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md.

## Event Contract

`BookEvent` should represent observed or synthetic book changes:

```text
timestamp
event_type = add | cancel | delete | execute_visible | execute_hidden | halt | resume
side = plus | minus | unknown
price_tick
size_shares
order_id_optional
source
```

Recommendation: preserve event type, side, price, size, and timestamp because full source-sink validation needs add, cancel, delete, execution, and halt semantics. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; data decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/06-data-requirements-and-vendors/DECISION.md.

## Solver Config Contract

`SolverConfig` should include:

```text
delta_p_ticks
c_adv
c_diff
c_react
diffusion_mode = explicit | semi_implicit | implicit
reaction_mode = capped_explicit | exact_linear | implicit_positive
advection_mode = upwind_first_order | limited_finite_volume
boundary_mode = no_flux_diffusion_with_audited_outflow
random_seed_optional
```

Recommendation: expose stability constants and positivity modes as configuration, not hidden solver assumptions. Sources: CFL condition, https://doi.org/10.1147/rd.112.0215; positivity-preserving reaction-diffusion splitting, https://doi.org/10.1016/j.jcp.2021.110253; Patankar source treatment, https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow/Patankar/p/book/9780891165224.

## Step Interface

A future solver should expose conceptual operations:

```text
initialize_state(price_grid, initial_book_snapshot)
apply_event(state, book_event)
advance_between_events(state, t_start, t_end, forcing)
compute_stable_timestep(state, config)
locate_price_interface(latent_state)
validate_state(state, diagnostics_config)
```

Recommendation: keep event application separate from PDE advancement so empirical book accounting can be audited independently of model diffusion and quote transport. Sources: LOBSTER data structure, https://data.lobsterdata.com/info/DataStructure.php; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253.

## Output Contract

`StepResult` should include:

```text
state_next
accepted_delta_t
substep_count
mass_before
mass_after
source_mass
sink_mass_requested
sink_mass_realized
boundary_flux
positivity_violations
stability_margins
warnings
```

Recommendation: every accepted step should report mass accounting, capped sink differences, positivity status, and timestep margins. Sources: TRIDENT verification checks, file:///Users/arshbrar/Development/GitHub/trident_LOB/docs/TRIDENT_LOB_MODEL.md; LeVeque finite-volume methods, https://doi.org/10.1017/CBO9780511791253.

## Phase 1 Interface Subset

Phase 1 should use only:

```text
PriceGrid
TimeGrid
BookEvent fixtures
LiquidityState from top-book or synthetic depth
SolverConfig for diagnostics
StepResult diagnostics
```

Recommendation: do not expose a full PDE solver interface as a production dependency in Phase 1; use the subset for fixtures, feature validation, and invariant checks. Sources: market microstructure decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/00-market-microstructure-literature/DECISION.md; Python architecture decision, file:///Users/arshbrar/Development/GitHub/trident_LOB/research/12-python-architecture-and-stack/DECISION.md.

## Phase 2 Interface Additions

Phase 2 should add:

```text
L2 or L3 event replay adapter
finite_volume_flux_operator
positive_reaction_operator
diffusion_operator
stochastic_interface_operator
grid_remap_operator_optional
```

Recommendation: add the stochastic interface operator only after deterministic accounting and positivity gates pass. Sources: Kloeden and Platen SDE methods, https://doi.org/10.1007/978-3-662-12616-5; Cont and Mueller SPDE LOB model, https://doi.org/10.1137/19M1254489.

## Open Questions

1. Should hidden executions be represented as `execute_hidden` events that affect diagnostics but not visible `q_s`?
2. Should `mid_centered_ticks` be allowed before a conservative remap validation suite exists?
3. Should stochastic forcing be part of `forcing`, `state`, or a separate random stream contract?
4. Should the interface support adaptive nonuniform grids, or should that be deferred until fixed one-tick cells are validated?

