# Design system reference

Specs for the shared classes and the rules behind the tokens in `assets/tokens.css`. Read this for steps 2, 4 and 5 of the workflow.

## Contents
- Spacing rules
- Typography
- Color usage
- Page header, cards and stat cards
- Tables
- Badges, buttons and form controls
- States: loading, empty, error
- Responsive behavior
- Audit commands

## Spacing rules

All spacing comes from the 4px scale (`--space-*`). Never type a raw `13px` or `1.3rem`.

| Situation | Token |
| --- | --- |
| Gap between icon and label, tight inline groups | `--space-2` |
| Padding inside small controls, between label and its input | `--space-2` to `--space-3` |
| Card padding | `--space-5` (compact) or `--space-6` (default) |
| Gap between cards in a grid | `--space-4` to `--space-6` (pick one per page and keep it) |
| Gap between page sections | `--space-6` to `--space-8` |
| Page padding | `--space-6` desktop, `--space-4` mobile |

Proximity carries meaning: a card title belongs to its content, so the gap below it is smaller than the gap between two cards. If everything has the same gap, nothing looks grouped.

## Typography

| Role | Size | Weight |
| --- | --- | --- |
| Page title | `--text-2xl` | 700, letter-spacing -0.02em |
| Section / card title | `--text-lg` | 600 |
| Body | `--text-base` | 400 |
| Table cell, nav item, secondary text | `--text-sm` | 400 to 500 |
| Caption, badge, table header | `--text-xs` | 500 to 600; table headers uppercase with slight tracking |

Use `font-variant-numeric: tabular-nums` on stat values and numeric table columns so digits align. Right-align numeric columns.

## Color usage

- Page background `--color-bg`, raised surfaces `--color-surface`. Separate them with a 1px `--color-border`, not with heavy shadows.
- Text: `--color-text` for primary, `--color-text-secondary` and `--color-text-muted` for supporting text. Muted text must still be readable (aim for at least 4.5:1 on its background).
- `--color-accent` is for the active nav item, primary buttons, links and focus. Do not use it as decoration.
- Status colors (success, warning, danger, info) appear as a soft background plus a stronger text/border color. They are used only to carry meaning.
- If the app already defines a palette, map it onto these roles instead of replacing it.

## Page header, cards and stat cards

- **Page header**: title (`--text-2xl`), optional one-line description in muted text, optional actions aligned right on wide screens. Margin-bottom `--space-6`.
- **Card**: surface background, 1px border, `--radius-lg`, `--shadow-sm`, padding `--space-6`. The card header has the title on the left and optional actions on the right, with a bottom margin of `--space-4`. Do not nest cards inside cards.
- **Stat card**: label (muted, `--text-sm`), value (large, 600 to 700, tabular numbers), optional delta or hint (small). Variants (`success`, `warning`, `danger`, `info`) change only a restrained accent: a left border or the value color, not a flood of background color.
- Stat/summary grids use `repeat(auto-fit, minmax(14rem, 1fr))` with a single gap token.

## Tables

- Wrap in a container with `overflow-x: auto`, a border and `--radius-lg`, so wide tables scroll inside the card.
- Header row: `--color-surface-muted` background, uppercase `--text-xs` labels, `position: sticky; top: 0` when the table is tall.
- Cells: `--space-3` vertical, `--space-4` horizontal padding; 1px bottom border in `--color-border`; no vertical borders.
- Row hover: `--color-surface-muted`. Clickable rows get `cursor: pointer`.
- Keep column widths stable (`table-layout: fixed` for predictable layouts) and truncate long text with an ellipsis plus a `title` rather than wrapping into tall rows.

## Badges, buttons and form controls

- **Badge**: `--text-xs`, 500 weight, pill or `--radius-sm`, padding `--space-1` `--space-2`, soft background with strong text in the status color.
- **Buttons**: one height scale (36px default, 32px small), `--radius-md`, 500 weight. Primary: accent background, white text. Secondary: surface background, border, text color. Danger only for destructive actions. A clear disabled style (reduced opacity, `not-allowed` cursor). Visible `:focus-visible` ring.
- **Inputs, selects, textareas**: 36px height, 1px `--color-border-strong`, `--radius-md`, `--space-3` horizontal padding, accent border plus `--focus-ring` on focus. Labels above fields in `--text-sm` 500 weight. Inline validation text in `--color-danger`.
- **Range sliders**: style track and thumb with tokens (thin track in `--color-border-strong`, accent thumb); do not leave the browser default if the rest of the form is styled.

## States: loading, empty, error

Every data-driven region needs all three, styled consistently:

- **Loading**: centered muted text or a subtle skeleton; it should not shift layout when content arrives.
- **Empty**: a short sentence in muted text inside the card or table body, optionally with a next action.
- **Error**: danger-soft background, danger text, concise message; keep the original message text, only restyle it.

## Responsive behavior

- >= 1024px: sidebar visible (expanded or collapsed rail). 768 to 1023px: drawer. < 768px: single-column content, reduced padding, tables scroll horizontally inside their container.
- Grids collapse via `auto-fit/minmax`, not fixed column counts. Avoid fixed pixel widths on cards and filters.
- Touch targets are at least 36px tall (40px for nav items).

## Audit commands

Use these during the audit and again before finishing to find leftovers (adapt paths):

```bash
# hard-coded colors still outside the token file
grep -rnE "#[0-9a-fA-F]{3,8}\b" client/src --include=*.vue --include=*.css | grep -v tokens.css | wc -l

# off-scale pixel/rem values in padding, margin and gap
grep -rnE "(padding|margin|gap)[a-z-]*:\s*[0-9.]+(px|rem)" client/src --include=*.vue --include=*.css | head -50

# leftover top-nav styles or markup that should have been removed
grep -rnE "top-nav|nav-container|nav-tabs" client/src
```

Zero hard-coded colors is not the goal inside views that render charts or data-driven colors; the goal is that shared UI (shell, cards, tables, forms, badges) draws from tokens.
