---
name: dark-glass-graph-ui
description: Create, restyle, or review graph-based web interfaces with a neutral near-black foundation, one configurable luminous accent, true frosted-glass context surfaces, and robust node-edge interaction. Use for topology maps, dependency graphs, trace viewers, monitoring consoles, workflow diagrams, agent activity views, knowledge graphs, node inspectors, or any interface that needs dark glass, local glow, hover and selection states, connected-edge emphasis, contextual overlays, or graph layering without visual leaks.
---

# Dark Glass Graph UI

Build dense, readable graph workspaces from four materials:

1. a neutral near-black canvas;
2. opaque graphite primary objects;
3. gray frosted-glass secondary context;
4. one scarce luminous accent for interaction and state.

The style must remain useful before it becomes decorative. Selection, relationships, occlusion, and text hierarchy are more important than glow.

## Read The Relevant Reference

- Read [references/visual-system.md](references/visual-system.md) before choosing the palette, accent, glass recipe, glow, typography, spacing, hover, or selected appearance.
- Read [references/interaction-patterns.md](references/interaction-patterns.md) for node state precedence, selection, adjacency, edge routing, context expansion, viewport movement, and editing.
- Read [references/implementation-patterns.md](references/implementation-patterns.md) when implementing components, graph-library adapters, overlap fallback, or theme variables.
- Read [references/pitfalls-and-validation.md](references/pitfalls-and-validation.md) before final visual QA. It records the failure modes this system is designed to prevent.
- Reuse [assets/dark-glass-graph-theme.css](assets/dark-glass-graph-theme.css) as a framework-neutral token and primitive baseline. Adapt class names to the existing architecture when needed.

## Workflow

1. Inspect the existing frontend, graph library, icon system, layering model, and interaction handlers.
2. Identify primary objects, secondary context objects, relationships, and status states. Do not assume they are code modules, documents, or annotations.
3. Choose one accent hue that fits the product. Define both its color and RGB channel token; keep warning and error colors separate.
4. Write the state matrix before styling: default, hover, keyboard focus, selected, related, unrelated, active, warning, error, obscured, editing, loading, empty, and disabled.
5. Implement selection and adjacency as state-derived behavior. A selected object determines related objects and emphasized edges.
6. Establish layers before adding transparency: edges, primary objects, related objects, context glass, toolbars, and modals.
7. Make every primary object fully opaque in every state. Add tint and glow on top of an opaque base so lines cannot leak through.
8. Implement frosted glass as a two-layer material with an overlap fallback. Transparency without actual obscuration is not acceptable.
9. Add local glow and motion only after interaction, occlusion, and contrast are correct.
10. Verify with dense data, crossing edges, long labels, selected context, transformed canvases, mobile widths, keyboard use, and reduced motion.

## Core Visual Contract

- Use a neutral near-black base, not navy, purple-black, or a page-wide gradient.
- Keep most surfaces graphite and opaque. Use the accent on less than roughly 5% of the screen.
- Use one product accent for focus, selection, active state, confirmation, and selected relationships.
- Use amber for caution or manual provenance and red for failures or destructive actions.
- Keep glow close to its source. Build it from a crisp ring, a medium aura, and a grounding shadow.
- Use 5-8px radii for tools and graph objects. Avoid excessive pills and inflated cards.
- Use compact typography and stable object dimensions. State changes must not cause layout shifts.
- Use Lucide or the existing icon library for commands, with accessible names for icon-only controls.

## Glass Contract

- Primary graph objects are opaque graphite, never glass.
- Secondary contextual objects may use gray frosted glass so object categories remain visually distinct.
- Glass needs all three: translucent gray backing, `backdrop-filter`, and a subtle border/highlight.
- Do not apply `opacity` to the whole card; it also fades text and controls.
- If transformed graph layers prevent reliable backdrop blur, detect actual overlap and blur/darken only the underlying unrelated objects.
- Glass must make sharp content behind it unreadable while keeping its own content crisp.

## Edge Contract

- Render visible edges below every object surface.
- Give each edge a separate wide transparent hit path; never make the visible stroke artificially thick just to improve clicking.
- Derive emphasized edges from the selected object's adjacency. Clicking an edge must not independently turn that relationship highlight off.
- Related objects remain at normal brightness and above emphasized edges. Only unrelated objects dim.
- Route connections to boundary handles or computed anchors, not object centers.
- A crossing edge may disappear beneath an opaque unrelated object. A connected edge must terminate at that object's boundary and never cross its content.

## Interaction Contract

- Hover uses a small border, surface, and local-glow change without reflow.
- Keyboard focus is at least as visible as hover.
- Selected objects use a 45-55% accent tint over an opaque base, strong border, local glow, and contrast-correct foreground.
- Clicking an unselected object selects it.
- Clicking another object switches selection in one click.
- Clicking the selected object or empty canvas deselects it.
- Related objects keep their normal treatment; unrelated objects dim without moving.
- Move the viewport only when selected or expanded content would otherwise leave the visible bounds.

## Motion

- Hover and focus: 140-180ms.
- Selection and context entry: 180-240ms.
- Viewport correction: 220-280ms, only when needed.
- Live breathing state: 1.6-2.4s.
- Prefer opacity, color, border, shadow, and tiny transforms. Never continuously animate the whole graph.
- Honor `prefers-reduced-motion`.

## Required Verification

Before finishing:

- Confirm single-click select, switch, and deselect behavior.
- Confirm hover and selected backgrounds remain opaque and hide every line beneath them.
- Confirm selected edges highlight automatically and cannot be toggled off accidentally.
- Confirm directly related objects stay readable while unrelated objects dim.
- Confirm glass actually blurs or fallback-obscures overlapping content.
- Confirm context expansion does not force a needless hard recenter.
- Confirm long labels, dense crossings, error states, modals, loading, empty, disabled, keyboard focus, and reduced motion.
- Inspect rendered screenshots at desktop and mobile sizes; run the repository's typecheck, tests, and production build when available.
