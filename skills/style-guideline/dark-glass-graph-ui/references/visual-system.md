# Dark Glass Visual System

## Contents

1. Character
2. Neutral foundation
3. Accent strategy
4. Material hierarchy
5. Frosted glass
6. Glow
7. Hover, focus, and selection
8. Typography and geometry
9. Motion
10. Accessibility and performance

## Character

The interface is a focused technical workspace, not a cyberpunk poster. It should feel:

- quiet before interaction;
- precise and information-dense;
- dark without becoming blue or muddy;
- tactile through material contrast;
- luminous only where state or action deserves attention.

Visual tension comes from a nearly black environment, opaque graphite objects, fine neutral lines, restrained gray glass, and one high-energy accent.

## Neutral Foundation

Use neutral values as the invariant part of the system:

| Role | Default | Purpose |
|---|---:|---|
| Canvas | `#050605` | Main graph and page background |
| Deep band | `#080908` | Header and deepest structural areas |
| Surface | `#101210` | Rails, inspectors, panels |
| Object | `#171a17` | Primary nodes and controls |
| Hover object | `#202420` | Neutral hover backing |
| Divider | `#292d29` | Borders and separators |
| Strong divider | `#3c433c` | Inputs, modals, emphasized boundaries |
| Primary text | `#f4f7f3` | Headings and important values |
| Secondary text | `#9fa69f` | Supporting copy |
| Faint text | `#697169` | Paths, timestamps, metadata |

Avoid a visible canvas gradient. Subtle tonal differences should come from structural surfaces, not decorative blobs or blue haze.

## Accent Strategy

Choose one accent for each product or workspace. The bundled CSS defaults to phosphor green, but the system also works with cyan, electric blue, lime, or controlled magenta.

Define:

```css
:root {
  --dgg-accent: #58ff3d;
  --dgg-accent-rgb: 88 255 61;
  --dgg-accent-ink: #061106;
}
```

Change all three tokens together. `--dgg-accent-ink` is the foreground used on a heavily tinted selected object.

Use the accent for:

- keyboard focus;
- selected objects;
- active or live state;
- selected relationships;
- primary confirmation;
- small status details.

Do not use it for every border, heading, icon, and button simultaneously. Target:

- 70-80% near-black;
- 15-25% graphite and gray;
- under 5% accent, amber, and red combined.

Use amber for caution or manual provenance. Use red for failure, destructive state, or a confirmed root cause. Do not recolor errors with the product accent.

## Material Hierarchy

Assign materials by semantic role:

| Material | Role | Properties |
|---|---|---|
| Opaque graphite | Primary objects | Highest readability; hides edges |
| Raised graphite | Controls and inspectors | Quiet structural separation |
| Gray frosted glass | Context and evidence | Secondary, translucent, blurred |
| Accent-tinted graphite | Selected primary object | Strongest local focus |
| Amber or red graphite | Warning and error | Semantic exception |

Do not make every surface glass. Glass is valuable because it differs from stable primary objects.

## Frosted Glass

### The two-layer recipe

Use a backing layer and a material layer:

```css
.context-glass {
  position: relative;
  isolation: isolate;
}

.context-glass::before {
  position: absolute;
  z-index: 0;
  inset: 0;
  border-radius: inherit;
  background: rgb(43 48 43 / 86%);
  backdrop-filter: blur(28px) saturate(70%);
  content: "";
}

.context-glass__surface {
  position: relative;
  z-index: 1;
  border: 1px solid rgb(238 243 238 / 24%);
  background:
    linear-gradient(
      145deg,
      rgb(238 243 238 / 15%),
      rgb(150 158 150 / 7%) 46%,
      rgb(44 49 44 / 17%)
    ),
    rgb(69 75 69 / 72%);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 15%),
    0 10px 28px rgb(0 0 0 / 34%);
  backdrop-filter: blur(18px) saturate(115%);
}
```

The backing layer removes sharp visual noise. The surface layer creates the glass highlight and depth.

### What does not work

- `opacity: 0.5` on the whole card fades its text and controls.
- A nearly transparent background with no blur is merely transparent plastic.
- Blur without a sufficiently opaque gray substrate still exposes lines and labels.
- A fully opaque surface prevents backdrop blur from being visible.
- `filter: blur()` on the glass card blurs its own content; it is not a replacement for `backdrop-filter`.

### Transformed-canvas fallback

Graph libraries often place nodes inside transformed layers. Some browser and stacking-context combinations make `backdrop-filter` unable to sample sibling nodes correctly.

Use a deterministic fallback:

1. compute the screen-space rectangle of each open glass card;
2. compute screen-space rectangles for underlying primary objects;
3. mark only intersecting unrelated objects as `is-obscured`;
4. apply `filter: blur(6px) brightness(0.2) saturate(0.2)`;
5. remove the class immediately when overlap ends.

Do not blur the entire graph. Selected and directly related objects should remain readable unless the product explicitly prioritizes privacy over context.

## Glow

Glow communicates energy or focus. Build it in layers:

```css
box-shadow:
  0 0 0 2px rgb(var(--dgg-accent-rgb) / 10%),
  0 0 20px rgb(var(--dgg-accent-rgb) / 16%),
  0 8px 22px rgb(0 0 0 / 28%);
```

Each layer has a job:

- crisp ring: defines the boundary;
- medium aura: signals focus;
- black shadow: separates the object from the canvas.

Rules:

- default objects get little or no glow;
- hover gets a small local aura;
- selection gets a stronger aura;
- live state may breathe slowly;
- ordinary component glow should remain within roughly 20-30px;
- avoid multiple competing accent glows in one viewport;
- do not use giant blurred gradients to imitate glow.

## Hover, Focus, And Selection

### Default

- opaque graphite fill;
- neutral or lightly accent-tinted border;
- no strong halo;
- white title, gray metadata.

### Hover

- brighten the border;
- add a 6-8% accent tint over the same opaque base;
- add a restrained local glow;
- optionally use `translateY(-1px)` or `scale(1.005)`, never enough to disturb edge routing;
- transition in 140-180ms.

Hover must not equal selection. It previews affordance rather than changing graph meaning.

### Keyboard focus

Use a clear 2px accent outline with an offset. Do not rely on glow alone because it can disappear against nearby selected edges.

### Selected

- place a 45-55% accent tint over an opaque graphite base;
- use a stronger accent border and local aura;
- switch text and icons to `--dgg-accent-ink` when required for contrast;
- highlight connected relationships;
- keep dimensions identical to the default state.

Use direct layered backgrounds:

```css
background:
  linear-gradient(
    rgb(var(--dgg-accent-rgb) / 50%),
    rgb(var(--dgg-accent-rgb) / 50%)
  ),
  var(--dgg-object);
```

The opaque final layer prevents relationship lines from leaking through.

### Related and unrelated

Related objects keep their normal appearance. Unrelated objects may use:

```css
filter: brightness(0.34) saturate(0.32);
```

Do not reduce unrelated-object opacity to zero or change its geometry. The user still needs the graph's overall shape.

## Typography And Geometry

Use the product's existing neutral sans stack. Use monospace only for paths, timestamps, identifiers, status codes, and compact provenance labels.

Recommended sizes:

| Context | Size |
|---|---:|
| Workspace title | 14-17px |
| Panel title | 13-15px |
| Object title | 11-13px |
| Body and controls | 10-13px |
| Path, type, timestamp | 8-10px |

Use normal letter spacing. Keep common controls 28-36px high, panel padding 11-16px, and radii 5-8px. Give graph objects fixed or constrained dimensions so hover, badges, and long labels do not move the layout.

## Motion

| Interaction | Duration |
|---|---:|
| Hover and focus | 140-180ms |
| Selection | 170-220ms |
| Context entry | 200-240ms |
| Panel expansion | 180-240ms |
| Viewport correction | 220-280ms |
| Live breathing | 1.6-2.4s |

Use `cubic-bezier(0.2, 0.72, 0.2, 1)` for context entry. Keep continuous animation limited to genuine live state.

## Accessibility And Performance

- Verify text contrast in default, selected, dimmed, warning, and error states.
- Preserve visible keyboard focus.
- Pair color with shape, icon, text, or line style for critical states.
- Do not use blur on hundreds of objects. Apply fallback blur only to actual intersections.
- Prefer transform and opacity for entry motion; avoid animating large blur radii.
- Provide a `prefers-reduced-motion` override.
- Test with browser zoom and high-density displays; 1px borders must remain legible.
