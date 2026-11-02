# Sidebar shell reference

How to restructure the app shell (`App.vue` or the layout component) around a left sidebar. Read this before step 3 of the workflow. Templates: `assets/AppSidebar.vue`, `assets/useSidebar.js`, `assets/tokens.css`.

## Contents
- Shell structure
- Moving the old header's contents
- Collapse, mobile drawer and accessibility
- Content area and layout CSS
- Icon path data
- Common pitfalls

## Shell structure

```vue
<div class="app-shell" :class="{ 'sidebar-collapsed': collapsed && !isMobile }">
  <AppSidebar :items="navItems" :brand-name="..." :brand-initial="...">
    <template #footer="{ collapsed }">
      <!-- language switcher, profile menu -->
    </template>
  </AppSidebar>

  <div v-if="isMobile && mobileOpen" class="sidebar-backdrop" @click="closeMobile" />

  <div class="app-main">
    <header class="topbar">
      <button v-if="isMobile" class="icon-button" aria-label="Open navigation" @click="openMobile">...</button>
      <!-- page context / title, global actions -->
    </header>
    <!-- global filter bar, if the app had one -->
    <main class="main-content"><router-view /></main>
  </div>

  <!-- existing modals stay here, unchanged -->
</div>
```

Keep modals, teleports and global listeners where they were. Only the header and layout wrappers change.

`navItems` is a computed list built from the same routes and labels the old nav used, in the same order:

```js
const navItems = computed(() => [
  { to: '/', label: t('nav.overview'), icon: ICONS.grid },
  { to: '/inventory', label: t('nav.inventory'), icon: ICONS.box },
  // ...one entry per old nav link
])
```

If the old nav had a link with a hard-coded label (not translated), keep it as-is; adding translation is a separate change.

## Moving the old header's contents

Make a list of everything in the old header and decide a home for each before deleting it:

| Old header item | New home |
| --- | --- |
| Logo / company name / subtitle | Sidebar brand area (subtitle can be dropped when collapsed, or moved to the top bar) |
| Nav links | Sidebar nav |
| Language switcher | Sidebar footer, or top bar right side |
| Profile menu, notifications, tasks | Sidebar footer, or top bar right side. Keep its dropdown opening direction sensible: a menu in the footer opens upward, one in the top bar opens downward |
| Global filter bar under the header | Directly under the top bar, inside `.app-main`, unchanged in behavior |
| Search | Top bar |

Dropdowns and popovers positioned for a header (`top: 100%`, right aligned) often need their anchoring flipped when they move to the footer. Open each one after moving it.

## Collapse, mobile drawer and accessibility

- Desktop (>= 1024px): sidebar is `--sidebar-width`; a toggle collapses it to `--sidebar-width-collapsed` (icons only). Persist the choice in `localStorage` inside try/catch. `useSidebar.js` does this.
- Below 1024px: the sidebar is hidden off-canvas. A menu button in the top bar opens it; a backdrop covers the content. Close it on route change, backdrop click and Escape. The drawer always shows labels (never the icon rail).
- Collapsed items need a `title` (tooltip) and the link still needs an accessible name; keep the label in the DOM (hidden visually with `v-show`/`sr-only`) or use `aria-label`.
- Mark the current page with `aria-current="page"`.
- Use `<nav aria-label="...">` for the nav list, real `<a>`/`<router-link>` for destinations and real `<button type="button">` for actions.
- Every interactive element gets a visible `:focus-visible` style (the templates use `--focus-ring`).
- When the drawer is open on mobile, move focus into it, and return focus to the menu button when it closes. At minimum, close on Escape:

```js
const onKeydown = (e) => { if (e.key === 'Escape') closeMobile() }
onMounted(() => window.addEventListener('keydown', onKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))
```

- Respect `prefers-reduced-motion` (templates already disable the transitions).

## Content area and layout CSS

```css
.app-shell { min-height: 100vh; background: var(--color-bg); }

.app-main {
  margin-left: var(--sidebar-width);
  min-width: 0;                       /* lets wide tables scroll instead of stretching the page */
  transition: margin-left var(--transition-fast);
}
.app-shell.sidebar-collapsed .app-main { margin-left: var(--sidebar-width-collapsed); }

.topbar {
  position: sticky; top: 0; z-index: var(--z-topbar);
  display: flex; align-items: center; gap: var(--space-4);
  height: var(--topbar-height); padding: 0 var(--space-6);
  background: var(--color-surface); border-bottom: 1px solid var(--color-border);
}

.main-content {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--space-6);
}

.sidebar-backdrop {
  position: fixed; inset: 0; z-index: var(--z-backdrop);
  background: rgba(15, 23, 42, 0.4);
}

@media (max-width: 1023px) {
  .app-main, .app-shell.sidebar-collapsed .app-main { margin-left: 0; }
  .topbar { padding: 0 var(--space-4); }
  .main-content { padding: var(--space-4); }
}
```

Two details that cause most layout bugs: `min-width: 0` on `.app-main` (flex/grid children refuse to shrink otherwise, so wide tables push the page sideways) and a sticky top bar whose `z-index` sits below the sidebar and above content.

If any view uses `position: sticky; top: <old header height>` for its own headers, update that offset to `var(--topbar-height)`.

## Icon path data

Stroke-style 24x24 icons (Lucide-like; draw with `fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"`). Each entry is an array of `d` values.

```js
export const ICONS = {
  grid: ['M3 3h7v7H3z', 'M14 3h7v7h-7z', 'M14 14h7v7h-7z', 'M3 14h7v7H3z'],
  box: ['M21 8l-9-5-9 5v8l9 5 9-5z', 'M3 8l9 5 9-5', 'M12 13v8'],
  clipboard: ['M9 3h6a1 1 0 011 1v1H8V4a1 1 0 011-1z', 'M8 5H6a2 2 0 00-2 2v13a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2h-2', 'M9 12h6', 'M9 16h6'],
  wallet: ['M3 7a2 2 0 012-2h14v4', 'M3 7v11a2 2 0 002 2h16V9H5a2 2 0 01-2-2z', 'M16 14h2'],
  trend: ['M3 17l6-6 4 4 8-8', 'M14 7h7v7'],
  refresh: ['M21 12a9 9 0 11-3-6.7', 'M21 4v5h-5'],
  document: ['M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z', 'M14 3v5h5', 'M9 13h6', 'M9 17h6'],
  menu: ['M4 6h16', 'M4 12h16', 'M4 18h16'],
  settings: ['M12 15a3 3 0 100-6 3 3 0 000 6z', 'M19.4 15a1.7 1.7 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.7 1.7 0 00-1.8-.3 1.7 1.7 0 00-1 1.5V21a2 2 0 11-4 0v-.1a1.7 1.7 0 00-1.1-1.5 1.7 1.7 0 00-1.8.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.7 1.7 0 00.3-1.8 1.7 1.7 0 00-1.5-1H3a2 2 0 110-4h.1a1.7 1.7 0 001.5-1.1 1.7 1.7 0 00-.3-1.8l-.1-.1a2 2 0 112.8-2.8l.1.1a1.7 1.7 0 001.8.3H9a1.7 1.7 0 001-1.5V3a2 2 0 114 0v.1a1.7 1.7 0 001 1.5 1.7 1.7 0 001.8-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.7 1.7 0 00-.3 1.8V9a1.7 1.7 0 001.5 1H21a2 2 0 110 4h-.1a1.7 1.7 0 00-1.5 1z'],
  users: ['M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2', 'M9 11a4 4 0 100-8 4 4 0 000 8z', 'M23 21v-2a4 4 0 00-3-3.9', 'M16 3.1a4 4 0 010 7.8']
}
```

Choose by meaning. If the app has a destination none of these fit (for example "Restocking"), `refresh` or `box` is fine; do not spend time inventing an icon.

## Common pitfalls

- Active state wrong for `/`: it must match exactly, or Overview is highlighted everywhere.
- Fixed sidebar covering content: forgetting `margin-left` on the main area, or not resetting it on mobile.
- Content wider than the viewport: missing `min-width: 0`, or tables without a scroll container.
- Modals appearing under the sidebar: raise modal `z-index` above `--z-sidebar`.
- A dropdown clipped by the sidebar's `overflow` when moved to the footer: render it outside the scrolling nav, or position it with `position: fixed`.
- Drawer left open after navigating: close on `@click` of nav items and on route change.
- Hydration or SSR code touching `window`/`localStorage` at module load: only touch them in `onMounted`.
