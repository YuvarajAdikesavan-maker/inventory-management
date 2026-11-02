<!--
  Sidebar template. Adapt to the project:
  - Build `items` from the app's existing routes and i18n labels (same order, same labels).
  - Convert to the project's SFC style if it does not use <script setup>.
  - Icons are inline SVG path data (24x24, stroke style); see references/sidebar-shell.md.
-->
<template>
  <aside
    class="sidebar"
    :class="{ collapsed: collapsed && !isMobile, 'mobile-open': mobileOpen }"
    :aria-label="navLabel"
  >
    <div class="sidebar-brand">
      <slot name="brand">
        <span class="brand-mark" aria-hidden="true">{{ brandInitial }}</span>
        <span v-show="!collapsed || isMobile" class="brand-text">{{ brandName }}</span>
      </slot>
    </div>

    <nav class="sidebar-nav">
      <router-link
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        class="nav-item"
        :class="{ active: isActive(item.to) }"
        :title="collapsed && !isMobile ? item.label : undefined"
        :aria-current="isActive(item.to) ? 'page' : undefined"
        @click="closeMobile"
      >
        <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path v-for="(d, i) in item.icon" :key="i" :d="d" />
        </svg>
        <span v-show="!collapsed || isMobile" class="nav-label">{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <!-- Secondary controls that used to live in the header: language switcher, profile menu -->
      <slot name="footer" :collapsed="collapsed && !isMobile" />
      <button
        v-if="!isMobile"
        type="button"
        class="collapse-toggle"
        :aria-label="collapsed ? expandLabel : collapseLabel"
        :title="collapsed ? expandLabel : collapseLabel"
        @click="toggleCollapsed"
      >
        <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path :d="collapsed ? 'M9 18l6-6-6-6' : 'M15 18l-6-6 6-6'" />
        </svg>
        <span v-show="!collapsed" class="nav-label">{{ collapseLabel }}</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useSidebar } from '../composables/useSidebar'

defineProps({
  // [{ to: '/orders', label: 'Orders', icon: ['M...', 'M...'] }]
  items: { type: Array, required: true },
  brandName: { type: String, default: '' },
  brandInitial: { type: String, default: '' },
  navLabel: { type: String, default: 'Main navigation' },
  collapseLabel: { type: String, default: 'Collapse sidebar' },
  expandLabel: { type: String, default: 'Expand sidebar' }
})

const route = useRoute()
const { collapsed, mobileOpen, isMobile, toggleCollapsed, closeMobile } = useSidebar()

// "/" must only match exactly, otherwise it is active on every page
const isActive = (to) => (to === '/' ? route.path === '/' : route.path === to || route.path.startsWith(`${to}/`))
</script>

<style scoped>
.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  z-index: var(--z-sidebar);
  transition: width var(--transition-fast), transform var(--transition-fast);
}

.sidebar.collapsed {
  width: var(--sidebar-width-collapsed);
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  height: var(--topbar-height);
  padding: 0 var(--space-4);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  flex-shrink: 0;
  border-radius: var(--radius-md);
  background: var(--color-accent);
  color: #fff;
  font-weight: 700;
  font-size: var(--text-sm);
}

.brand-text {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--color-text);
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-4) var(--space-3);
  overflow-y: auto;
}

.nav-item,
.collapse-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  height: 2.5rem;
  padding: 0 var(--space-3);
  border: 0;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-muted);
  font: inherit;
  font-size: var(--text-sm);
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.nav-item:hover,
.collapse-toggle:hover {
  background: var(--color-surface-muted);
  color: var(--color-text);
}

.nav-item:focus-visible,
.collapse-toggle:focus-visible {
  outline: none;
  box-shadow: var(--focus-ring);
}

.nav-item.active {
  background: var(--color-accent-soft);
  color: var(--color-accent);
}

.nav-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.nav-label {
  white-space: nowrap;
}

.sidebar.collapsed .nav-item,
.sidebar.collapsed .collapse-toggle {
  justify-content: center;
  padding: 0;
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-3);
  border-top: 1px solid var(--color-border);
}

/* Below the tablet breakpoint the sidebar is an off-canvas drawer */
@media (max-width: 1023px) {
  .sidebar {
    width: var(--sidebar-width);
    transform: translateX(-100%);
    box-shadow: var(--shadow-md);
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .sidebar,
  .nav-item {
    transition: none;
  }
}
</style>
