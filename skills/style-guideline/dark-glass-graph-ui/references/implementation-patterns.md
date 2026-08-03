# Implementation Patterns

## Contents

1. Theme setup
2. Shell
3. Primary object
4. Context glass
5. Edges
6. Overlap fallback
7. Graph-library integration
8. Responsive behavior
9. Visual verification

## Theme Setup

Import `assets/dark-glass-graph-theme.css` once, then override tokens at the application root:

```css
.product-theme {
  --dgg-accent: #53e7ff;
  --dgg-accent-rgb: 83 231 255;
  --dgg-accent-ink: #031114;
}
```

Map these tokens into an existing design system instead of adding a second global reset. Preserve established component APIs and icon libraries.

## Shell

Use structural regions, not floating page-section cards:

```tsx
<main className="dgg-shell">
  <header className="dgg-header">...</header>
  <div className="dgg-workspace">
    <aside className="dgg-sidebar">...</aside>
    <section className="dgg-main">
      <div className="dgg-canvas">...</div>
      <div className="dgg-timeline">...</div>
    </section>
    <aside className="dgg-inspector">...</aside>
  </div>
</main>
```

The canvas owns unused space. Rails scroll independently and remain visually quiet.

## Primary Object

Separate the graph wrapper from its opaque visual surface when the graph library needs handles outside the object:

```tsx
<div
  className={cx("dgg-node", {
    "is-selected": selected,
    "is-related": related,
    "is-active": active,
    "is-warning": warning,
    "is-error": error,
    "is-dimmed": dimmed,
    "is-obscured": obscured,
  })}
  onClick={event => {
    event.stopPropagation();
    onToggleSelect(id);
  }}
>
  <div className="dgg-node__surface">
    <span className="dgg-node__icon"><Icon /></span>
    <span className="dgg-node__copy">
      <strong>{name}</strong>
      <span>{category}</span>
    </span>
  </div>
  <SourceHandle />
  <TargetHandle />
</div>
```

Keep wrapper and surface dimensions stable. Put the opaque background on `dgg-node__surface`; keep handles outside that surface when required.

## Context Glass

Use distinct semantics and material:

```tsx
<div className="dgg-context" data-context-id={id}>
  <button className="dgg-context__surface" onClick={onOpen}>
    <span className="dgg-context__icon"><FileText /></span>
    <span className="dgg-context__copy">
      <small>{kind}</small>
      <strong>{title}</strong>
      <span>{summary}</span>
    </span>
  </button>
</div>
```

The wrapper supplies backing blur and the surface supplies the translucent material. Do not use a glass card for a primary graph object.

## Edges

Use a wide invisible hit path:

```tsx
function GraphEdge({ path, related, markerEnd, onClick }) {
  return (
    <g
      className={cx("dgg-edge", { "is-related": related })}
      onClick={event => {
        event.stopPropagation();
        onClick?.();
      }}
    >
      <path className="dgg-edge__hit" d={path} />
      <path
        className="dgg-edge__path"
        d={path}
        markerEnd={markerEnd}
      />
    </g>
  );
}
```

Define markers per state or use `context-stroke` where supported. The marker color must change with the edge.

For labels:

```css
.edge-label {
  padding: 2px 4px;
  background: var(--dgg-bg);
  color: var(--dgg-faint);
  pointer-events: none;
}
```

## Overlap Fallback

Run overlap checks after selection, pan, zoom, resize, or context-layout changes. Throttle continuous updates with `requestAnimationFrame`.

```ts
function intersect(a: DOMRect, b: DOMRect) {
  return !(
    a.right <= b.left ||
    a.left >= b.right ||
    a.bottom <= b.top ||
    a.top >= b.bottom
  );
}

function obscuredNodeIds(
  contextElements: HTMLElement[],
  nodeElements: HTMLElement[],
  protectedIds: Set<string>,
) {
  const contextRects = contextElements.map(element =>
    element.getBoundingClientRect(),
  );

  return new Set(
    nodeElements
      .filter(element => !protectedIds.has(element.dataset.nodeId ?? ""))
      .filter(element => {
        const nodeRect = element.getBoundingClientRect();
        return contextRects.some(contextRect =>
          intersect(contextRect, nodeRect),
        );
      })
      .map(element => element.dataset.nodeId)
      .filter((id): id is string => Boolean(id)),
  );
}
```

`protectedIds` normally contains the selected and directly related objects. Use screen-space rectangles because the browser has already applied graph pan and zoom transforms.

Do not run this against every object on every animation frame. Recompute only when geometry changes, and use spatial indexing for very large graphs.

## Graph-Library Integration

Use an established graph library when the product needs zoom, pan, handles, minimap, layout, or editing.

For React Flow or similar:

- keep stable node dimensions;
- place custom node surfaces above the SVG edge layer;
- set opaque backgrounds on every node state;
- use library handles or boundary anchors;
- keep edge interaction width larger than visible stroke width;
- prevent pane-click handlers from running after node or edge clicks;
- disable automatic `fitView` after initial load;
- calculate minimal viewport correction for context expansion;
- hide vendor attribution only when licensing permits.

Do not solve a z-index issue solely by assigning a huge z-index to SVG edges. That often fixes one selected line while making it cross related node content.

## Responsive Behavior

At medium widths:

- narrow side rails before shrinking text;
- allow the inspector to collapse;
- preserve graph controls and object dimensions.

At mobile widths:

- stack the graph and inspector or use an explicit tab/sheet model;
- give the graph a stable height;
- open context records in a bottom sheet if side placement no longer fits;
- preserve touch targets of at least 40px even if visible icons remain compact;
- avoid viewport-scaled typography.

## Visual Verification

Capture and inspect at least:

- default dense graph;
- node hover with crossing edges;
- selected node with related and unrelated nodes;
- selected node with multiple context cards;
- warning and error paths;
- graph edit mode;
- narrow desktop and mobile;
- reduced-motion mode.

Pixel inspection matters for blur and occlusion. A passing typecheck cannot prove that a relationship line is hidden behind a node or that glass obscures content.
