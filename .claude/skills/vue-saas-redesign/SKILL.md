---
name: vue-saas-redesign
description: Redesign a Vue 3 application's UI into a modern, polished SaaS-style interface with a collapsible vertical sidebar on the left in place of the top navigation bar, a consistent spacing scale, and shared design tokens. Use this skill whenever the user wants to modernize, restyle, refresh, or "make professional" a Vue 3 app, move navigation from a top nav/header to a left sidebar, add a dashboard-style app shell, fix inconsistent spacing or styling across views, or asks for a SaaS, admin-panel or dashboard look, even if they never say "sidebar" or "redesign" explicitly.
---

# Vue 3 SaaS redesign

Turn a Vue 3 app with a top navigation bar into a modern SaaS-style interface: a vertical sidebar on the left, a calm neutral visual language, and one consistent spacing and type scale. The goal is a result that looks designed rather than assembled, while behavior stays exactly as it was.

The change is deliberately scoped: **app shell + design tokens + shared component styles**, then a light consistency pass over each view. Restyling every view from scratch produces huge diffs that are hard to review and easy to break; most of the polish comes from the shell and the tokens anyway. Do a full page-by-page redesign only if the user explicitly asks for it.

## Ground rules

These exist because a redesign touches many files and the user has to trust that nothing functional moved.

- **Preserve behavior.** Routes, props, events, API calls, i18n keys, computed logic and state are untouched. You are changing markup structure and CSS, not features. If you must change a template to restructure layout, keep every `v-if`, `v-for`, `:key`, `@event` and binding.
- **Read project instructions first.** Check `CLAUDE.md` (root and client folder) and any other project conventions, and follow them. If the project says certain files must be handled by a specific subagent or skill, do that. If it forbids files or settings from being committed (private registries, lockfiles), leave them alone.
- **Add no dependencies.** Use inline SVG icons and plain CSS. A new UI library or icon package is a bigger decision than a restyle, and it can also break pinned registries or lockfiles.
- **Match the project's component style.** If the repo uses Options API with `setup()`, write the new components the same way. The templates in `assets/` use `<script setup>` for brevity; convert them when the project does not use it.
- **Keep translations working.** Nav labels, titles and any new visible string go through the project's i18n mechanism if it has one, in every locale. Do not hard-code English next to a translated app.
- **Keep it reviewable.** Prefer editing a small number of shared places (tokens, shell, global classes) over scattering edits across every view.

## Workflow

### 1. Audit what exists

Spend a few minutes reading before writing, because the right plan depends on how the app is built.

- Find the shell: usually `App.vue`, with a `<header>`/nav and a `<router-view />`. Note everything living in the header (logo, nav links, language switcher, profile menu, notification buttons) and any global bar between header and content (filters, breadcrumbs). Each of these needs a new home.
- Find the router (`main.js` / `router/index.js`) to get the list of top-level destinations and their order.
- Find where global styles live (an unscoped `<style>` in `App.vue`, `style.css`, `assets/*.css`) and what shared classes views rely on (`.card`, `.page-header`, `.badge`, `.table-container`, buttons, form controls). Views use these; changing them in one place restyles the whole app.
- Count hard-coded values. Grep for colors (`#[0-9a-f]{3,6}`), font sizes and paddings/margins in `px`/`rem`. Many different values for the same role is the inconsistency you are about to remove.
- Check for a design-system note in the project (palette, "no emojis", status colors). Keep it; it is the brand.

Write a short plan before editing: which files change, where each header item moves, and what the token set will be.

### 2. Establish design tokens

Create one source of truth for spacing, type, color, radius and shadow as CSS custom properties, so every later edit is "use the token" instead of "pick a number". Start from `assets/tokens.css` and adapt it:

- **Keep the app's existing palette and brand color** wherever it has one. Map its hex values onto token roles (`--color-text`, `--color-accent`, status colors) rather than introducing a new look. If the app has no palette, use the neutral slate defaults with a single accent.
- Spacing uses a 4px base scale (`--space-1` … `--space-12`). Section gaps, card padding and grid gaps all pick from it. Reading `references/design-system.md` explains the scale, type sizes and the specific rules for cards, tables and forms.
- Define tokens on `:root` in the project's existing global stylesheet (or a new `tokens.css` imported once in `main.js`).

### 3. Build the sidebar shell

Replace the top bar with a left sidebar plus a slim top bar inside the content area. Read `references/sidebar-shell.md` for the full layout and accessibility details, and start from the templates `assets/AppSidebar.vue` and `assets/useSidebar.js`.

The target structure:

```
┌──────────┬────────────────────────────────────────────┐
│ Logo     │  Top bar: page context · filters · actions   │
│          ├────────────────────────────────────────────┤
│ Nav      │                                              │
│  item    │  <router-view />   (max-width, padded)       │
│  item    │                                              │
│  item    │                                              │
│ ──────── │                                              │
│ Footer   │                                              │
└──────────┴────────────────────────────────────────────┘
```

- **Sidebar**: fixed to the left, full height, brand at the top, primary navigation in the middle, secondary items (language, profile, settings) at the bottom. Nav items are generated from the same router links the old nav used, with the same labels and active-state logic.
- **Collapsible**: a toggle shrinks it to an icon rail and back; the preference is remembered. Collapsed items need a `title`/tooltip because the label is hidden.
- **Mobile**: below the tablet breakpoint the sidebar becomes an off-canvas drawer opened from a menu button in the top bar, with a backdrop, closing on navigation, backdrop click and Escape.
- **Top bar**: holds what used to sit in the header's right side or in a global bar (filters, search, language, profile). Do not leave things stranded. If a global filter bar existed, it moves into the content area under the top bar and keeps working unchanged.
- **Templates are starting points**: the files in `assets/` open with a comment explaining how to adapt them. Delete that comment once you have adapted the file, so instructions meant for you do not ship in the user's codebase.
- **Icons**: inline SVG, one per nav item, in a consistent stroke style. Pick icons by meaning (overview → grid, inventory → box, orders → clipboard/list, finance → wallet/chart, demand → trend line, reports → document). `references/sidebar-shell.md` includes ready-made path data.

### 4. Restyle the shared classes

Update the global classes that views already use so the whole app inherits the new look without per-view edits: page header, cards, stat cards, tables, badges, buttons, form controls, empty/loading/error states. Replace hard-coded values with tokens as you touch them. Details and specs are in `references/design-system.md`.

If views have no shared button or input class, add a small set (`.btn`, `.btn-primary`, `.btn-secondary`, `.input`) in the global styles so new and existing screens can adopt one look.

### 5. Consistency pass over views

Open each view and fix only what breaks the system: ad-hoc margins that fight the page rhythm, off-scale font sizes, one-off colors, hand-rolled card styling that duplicates `.card`, fixed widths that overflow next to a sidebar. Swap values for tokens and shared classes. Leave structure, logic and data handling alone.

Check that wide tables and charts still fit now that the content area is narrower by the sidebar width: give wide tables a horizontally scrollable container instead of letting the page scroll sideways.

### 6. Verify

- Build the app (`npm run build` or the project's equivalent) and fix any errors or warnings you introduced.
- Run the dev server and look at it at desktop (~1440px), tablet (~768px) and phone (~375px) widths. If a browser tool is available, take screenshots; otherwise at least confirm the build and describe what could not be checked. Look for: nav active state on every route, the collapsed rail, the mobile drawer opening/closing, nothing overlapped by the fixed sidebar, no horizontal page scroll, readable contrast.
- Run existing tests if the project has them. Visual changes should not break logic tests; if one does, you changed behavior.
- Search the diff for anything that should not ship: lockfiles, registry config, build output.

### 7. Report

Tell the user what changed in plain terms: the new shell, the tokens added, which shared classes were restyled, which views got a pass and what was deliberately left alone, and anything you could not verify. Mention follow-ups (for example, views with heavy custom styling that deserve their own pass) instead of silently expanding scope.

## Design principles to apply with judgment

These matter more than any specific hex value. When a rule here conflicts with the app's established brand, the brand wins.

- **Restraint.** One accent color, neutral surfaces, color reserved for meaning (status, selection, primary action). A polished SaaS UI looks calm because most things are gray.
- **Rhythm.** Every gap comes from the spacing scale, and related things sit closer together than unrelated things. Inconsistent spacing is the single biggest reason an interface looks unprofessional.
- **Hierarchy.** Page title, section titles, body and captions have clearly different size and weight; do not rely on color alone. Numbers in tables and stat cards use tabular figures so columns align.
- **Subtle depth.** 1px borders and very soft shadows; avoid heavy shadows, gradients and decorative effects.
- **Clear states.** Hover, focus-visible, active, disabled, loading and empty states all exist and look intentional. Focus rings are visible for keyboard users.
- **Density that fits the data.** This is a work tool: comfortable but not airy row heights, and content that uses the width it has.

## What not to do

- Do not change copy, rename routes, reorder navigation or drop an item because it does not fit. If something truly does not fit, ask.
- Do not introduce a CSS framework, component library, icon package or font download without being asked.
- Do not leave the old top nav styles dead in the stylesheet; remove what you replaced so the next person is not confused by two systems.
- Do not use emojis as icons or decoration, and respect any "no emojis" rule in the project.
