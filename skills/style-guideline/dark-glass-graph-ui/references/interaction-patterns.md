# Graph Interaction Patterns

## Contents

1. State model
2. Selection
3. Adjacency
4. Edge architecture
5. Layering and occlusion
6. Context expansion
7. Viewport policy
8. Editing
9. Live activity
10. Interaction verification

## State Model

Keep a single authoritative graph state rather than independent visual toggles:

```ts
type GraphViewState = {
  selectedNodeId?: string;
  hoveredNodeId?: string;
  focusedNodeId?: string;
  selectedEdgeId?: string;
  mode: "view" | "edit";
};
```

Derive these values from graph data and `selectedNodeId`:

- directly related node IDs;
- emphasized edge IDs;
- unrelated node IDs;
- contextual artifact IDs;
- combined bounds for viewport correction.

Do not let individual edge components own whether they are highlighted. Relationship emphasis is a projection of selection.

Evaluate node presentation in this order:

1. error or destructive;
2. selected;
3. active or live;
4. related;
5. obscured;
6. unrelated or dimmed;
7. keyboard focus;
8. hover;
9. default.

A broad dimming rule must never override selected or related objects.

## Selection

Use one click as the complete interaction:

```ts
function selectNode(nodeId: string) {
  setGraphState(current => ({
    ...current,
    selectedEdgeId: undefined,
    selectedNodeId:
      current.selectedNodeId === nodeId ? undefined : nodeId,
  }));
}

function clearSelection() {
  setGraphState(current => ({
    ...current,
    selectedNodeId: undefined,
    selectedEdgeId: undefined,
  }));
}
```

Required behavior:

- click an unselected node to select it;
- click another node to switch immediately;
- click the selected node to deselect it;
- click empty canvas to clear selection;
- `Enter` or `Space` follows the same toggle behavior;
- `Escape` clears selection or closes the highest-priority overlay.

Stop propagation on node clicks so the canvas handler does not immediately clear the selection. Do not use both `click` and `doubleClick` for selection.

## Adjacency

Build one adjacency index when graph data changes:

```ts
type Adjacency = Map<string, {
  nodeIds: Set<string>;
  edgeIds: Set<string>;
}>;
```

For the selected node:

- selected node gets selected styling;
- entries in `nodeIds` remain normal and become `is-related`;
- entries in `edgeIds` become emphasized;
- all other primary nodes become `is-dimmed`;
- context objects associated with the selected node may expand.

For directed graphs, preserve direction in data but decide whether visual relatedness is one-way or bidirectional. Dependency inspection usually benefits from showing both immediate inbound and outbound neighbors while distinguishing direction with arrowheads.

## Edge Architecture

Render two paths per edge:

```tsx
<g className="dgg-edge">
  <path className="dgg-edge__hit" d={path} />
  <path className="dgg-edge__path" d={path} markerEnd="url(#arrow)" />
</g>
```

- visible path: 1-2px;
- hit path: transparent, 10-16px, `pointer-events: stroke`;
- marker: uses the same state color as the visible path;
- label: separate and above the path, but below nodes.

States:

| State | Stroke | Width | Effect |
|---|---|---:|---|
| Default | neutral gray | 1-1.25px | none |
| Hover | brighter neutral | 1.5px | subtle |
| Related to selection | accent | 2px | local drop shadow |
| Manual or provisional | neutral/amber | 1.25px | dashed |
| Warning | amber | 2px | restrained glow |
| Failure | red | 2-2.5px | restrained glow |

An edge click may open details or select an edge in edit mode. It must not clear the selected node before that action runs. In view mode, clicking a related edge must not make the accent line disappear.

## Layering And Occlusion

Recommended relative layers:

| Layer | z-index |
|---|---:|
| Edge hit paths and visible edges | 1-4 |
| Edge labels | 4 |
| Default nodes | 10 |
| Related nodes | 14 |
| Selected edge decoration | below 14 |
| Selected node | 20 |
| Context connectors | 22 |
| Context glass | 30 |
| Canvas tools | 40 |
| Modals | 1000 |

Exact values matter less than ordering.

### Primary-object opacity

Every default, hover, related, active, warning, error, and selected node needs an opaque final background layer. Never rely on border and glow alone.

Common leak source:

```css
/* Wrong: relationship remains visible through this node. */
.node:hover {
  background: rgb(var(--accent) / 8%);
}
```

Correct:

```css
.node:hover {
  background:
    linear-gradient(rgb(var(--accent) / 8%), rgb(var(--accent) / 8%)),
    #171a17;
}
```

### Connection geometry

Connect to a handle or boundary anchor. If using custom routing:

1. find the ray from source center to target center;
2. intersect it with each node rectangle or shape;
3. use those boundary points as path endpoints;
4. offset the arrowhead so it stops before the border.

Do not draw center-to-center and hope the node hides the final segment.

### Crossing behavior

- An edge crossing an unrelated opaque node may disappear beneath that node.
- A selected edge must remain under every related node.
- A connected edge must end at the handle and never overlay text or icons.
- Edge labels need a small opaque canvas-colored backing if they overlap other edges.

## Context Expansion

Context objects may represent documents, annotations, evidence, alerts, traces, ownership, or related records.

On selection:

- position context near the selected object without covering it;
- visually distinguish context glass from opaque primary objects;
- group multiple context types by side, row, or labeled stack;
- use stable card dimensions;
- use short scale-and-fade entry;
- render context connectors below cards and above base edges;
- do not render empty placeholder cards when no context exists.

If glass overlaps graph objects, run the overlap fallback described in `visual-system.md`.

Context objects should not automatically become draggable in view mode. Their click behavior must be explicit: open details, navigate, pin, or filter.

## Viewport Policy

Compute the combined screen-space bounds of:

- selected object;
- visible context cards;
- any required labels or toolbars.

Compare those bounds with the visible viewport plus a 24-40px margin:

1. If everything is visible, do nothing.
2. If content fits but crosses one edge, pan only the minimum required distance.
3. If content cannot fit, reduce zoom only enough to fit, then center the combined bounds.
4. Preserve the user's zoom whenever possible.

Never hard-center solely because selection changed. Sudden recentering destroys spatial memory.

## Editing

Treat editing as a separate session:

- clear view-only selection and hidden filters;
- snapshot the current graph;
- reveal connection handles;
- enable dragging;
- increase edge hit areas;
- expose add object, add relation, edit relation, delete, save, and cancel;
- protect unsaved changes.

Differentiate generated, imported, and manually edited data. Editing a generated relationship should create an explicit override or provenance record rather than silently replacing its origin.

During edge editing:

- stop event propagation;
- show the selected edge without altering node-related highlighting;
- expose source, target, type, direction, and description;
- validate self-links and duplicate links;
- keep save disabled until a valid change exists.

## Live Activity

Live state should update graph meaning without making the whole canvas pulse:

- highlight only currently active objects and edges;
- use a slow breathing halo on the current object;
- show ordered events in a compact timeline or inspector;
- preserve the user's current selection;
- avoid viewport movement for every new event;
- announce important state changes accessibly.

## Interaction Verification

Test:

1. hover every node state and confirm no line appears through the background;
2. select, deselect, and switch nodes with one click;
3. click empty canvas and verify selection clears;
4. click a related edge and verify relationship highlighting remains;
5. verify related nodes remain normal while unrelated nodes dim;
6. verify selected edges remain underneath related nodes;
7. open multiple context cards and verify actual blur or fallback obscuration;
8. select near all four canvas edges and verify minimal movement;
9. use keyboard selection and focus;
10. enter edit mode, drag, connect, edit, save, cancel, and discard;
11. repeat with reduced motion.
