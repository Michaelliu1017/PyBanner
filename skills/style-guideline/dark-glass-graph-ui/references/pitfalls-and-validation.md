# Pitfalls And Validation

## Contents

1. Glass failures
2. Edge failures
3. Selection failures
4. Viewport failures
5. Color and glow failures
6. Validation matrix

## Glass Failures

### Glass is transparent but not frosted

**Symptom:** labels and edges behind a context card remain sharp and compete with its text.

**Cause:** the card only uses alpha, or the gray backing is too weak.

**Fix:** use the two-layer glass recipe, increase backing opacity, and verify `backdrop-filter` is active.

### Backdrop blur has no visible effect

**Symptom:** the CSS property exists but transformed graph siblings remain sharp.

**Cause:** browser compositing or stacking contexts prevent reliable backdrop sampling.

**Fix:** compute actual overlap in screen space and apply `is-obscured` to only the underlying unrelated objects.

### The glass card itself is blurry

**Symptom:** its own text and icons lose sharpness.

**Cause:** `filter: blur()` was applied to the card rather than `backdrop-filter` to its backdrop.

**Fix:** remove self-blur. Keep content on a crisp layer above the backing layer.

### All nearby objects blur

**Symptom:** selection destroys context rather than clarifying it.

**Cause:** blur is based on selection or proximity instead of actual rectangle intersection.

**Fix:** blur only intersecting objects. Protect the selected and related set.

## Edge Failures

### Lines appear inside a node

**Symptom:** a relationship is visible through a default, hover, selected, or dimmed node.

**Causes:**

- transparent node background;
- hover rule replaced an opaque background with an alpha-only fill;
- pseudo-element created an unexpected stacking context;
- selected edge z-index was raised above related nodes.

**Fixes:**

- give every node state an opaque final background layer;
- keep edges below node surfaces;
- keep related nodes above emphasized edges;
- test hover and selection separately because each may replace `background`.

### A connected line crosses node content

**Symptom:** the line reaches the center of its source or target.

**Cause:** center-to-center geometry or a missing handle.

**Fix:** route to boundary anchors and offset the arrow marker.

### Edges are hard to click

**Symptom:** the design uses an ugly thick stroke to make edge editing possible.

**Fix:** keep a thin visible path and add a separate 10-16px transparent hit path.

### Selected edge can be turned off

**Symptom:** clicking a highlighted relationship removes the green line while its node remains selected.

**Cause:** edge highlight is stored as independent mutable state.

**Fix:** derive highlighted edge IDs from selected-node adjacency. Edge details may be separate, but relationship emphasis is not.

### Related nodes become dark

**Cause:** a broad dimming selector overrides related styling.

**Fix:** derive disjoint state sets and use selectors such as:

```css
.node.is-dimmed:not(.is-related):not(.is-selected) { ... }
```

## Selection Failures

### Selection requires two clicks

**Causes:**

- pane click runs after node click and immediately clears selection;
- separate handlers own inspector selection and graph selection;
- click and double-click both change state;
- an overlay intercepts the first click.

**Fixes:**

- stop node-click propagation;
- keep one selected-node source of truth;
- make one click authoritative;
- inspect pointer events on context and edge layers.

### Clicking the selected node cannot deselect

**Cause:** the handler always assigns the clicked ID.

**Fix:** toggle against the current ID.

### Switching nodes flashes or retains old context

**Cause:** old context closes in one update and new context opens in another.

**Fix:** derive context directly from `selectedNodeId` and update selection atomically.

## Viewport Failures

### Every click recenters the graph

**Symptom:** users lose spatial memory and the interface feels forceful.

**Cause:** unconditional `fitView` or `setCenter` after selection.

**Fix:** compare combined selected-plus-context bounds against the current viewport. Pan only the missing distance; zoom only if bounds cannot fit.

### Context opens outside the viewport

**Fix:** position context first, measure its screen-space bounds, then perform one minimal correction.

### Graph jumps when a node changes state

**Cause:** border width, padding, font weight, badge size, or scale changes geometry.

**Fix:** reserve dimensions in the default state and animate paint properties. Keep scale below roughly 1.01 if used.

## Color And Glow Failures

### The page looks like one neon color

**Cause:** the accent is used on default borders, every icon, every button, and every heading.

**Fix:** return inactive elements to graphite. Reserve accent for current state and primary action.

### Glow becomes fog

**Cause:** large blur radii, high opacity, or page-sized gradients.

**Fix:** keep ordinary aura under 20-30px and add a dark grounding shadow.

### Hover looks selected

**Cause:** hover uses a strong fill or the same glow as selection.

**Fix:** hover uses 6-8% tint; selection uses 45-55% tint plus connected-edge emphasis.

### Selected text loses contrast

**Cause:** light text remains on a bright selected fill.

**Fix:** switch to `--dgg-accent-ink` and verify contrast for the chosen accent.

## Validation Matrix

| Scenario | What must remain true |
|---|---|
| Default dense graph | Hierarchy is readable; accent is scarce |
| Hover with edge behind node | Node remains opaque; no line leak |
| Keyboard focus | Focus is unmistakable without relying on glow |
| Select node | Accent fill, connected edges, and context agree |
| Select another node | Switches in one click with no stale context |
| Click selected node | Deselects in one click |
| Click highlighted edge | Relationship highlight remains derived from node |
| Related versus unrelated | Related stays normal; unrelated dims |
| Glass overlaps graph | Underlying content is blurred or fallback-obscured |
| Context already fits | Viewport does not move |
| Context leaves viewport | Minimal pan; zoom only when necessary |
| Warning and error | Amber/red remain distinct from accent |
| Edit mode | Hit targets are usable without thick visible lines |
| Reduced motion | No continuous breathing or forced animated pan |
| Mobile | Touch targets remain usable; text does not shrink |

Take screenshots for the states that depend on compositing: hover occlusion, selected edges, and glass overlap. These cannot be validated from source code alone.
