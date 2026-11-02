import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const STORAGE_KEY = 'sidebar-collapsed'
const MOBILE_QUERY = '(max-width: 1023px)'

// Module-level state so the shell, the sidebar and the top bar share one source of truth
const collapsed = ref(false)
const mobileOpen = ref(false)
const isMobile = ref(false)

// Storage can throw (private windows, blocked cookies), so the sidebar must work without it
const readStored = () => {
  try {
    return localStorage.getItem(STORAGE_KEY) === 'true'
  } catch {
    return false
  }
}

const writeStored = (value) => {
  try {
    localStorage.setItem(STORAGE_KEY, String(value))
  } catch {
    // Persistence is a convenience, not a requirement
  }
}

// Created at module scope (not inside a component) so it outlives whichever component first
// used the composable
watch(collapsed, writeStored)

let initialized = false

export function useSidebar() {
  let mediaQuery = null
  let onMediaChange = null

  onMounted(() => {
    if (!initialized) {
      collapsed.value = readStored()
      initialized = true
    }

    mediaQuery = window.matchMedia(MOBILE_QUERY)
    isMobile.value = mediaQuery.matches
    onMediaChange = (event) => {
      isMobile.value = event.matches
      // Leaving mobile width should never strand an open drawer
      if (!event.matches) mobileOpen.value = false
    }
    mediaQuery.addEventListener('change', onMediaChange)
  })

  onBeforeUnmount(() => {
    if (mediaQuery && onMediaChange) mediaQuery.removeEventListener('change', onMediaChange)
  })

  const toggleCollapsed = () => {
    collapsed.value = !collapsed.value
  }
  const openMobile = () => {
    mobileOpen.value = true
  }
  const closeMobile = () => {
    mobileOpen.value = false
  }

  return { collapsed, mobileOpen, isMobile, toggleCollapsed, openMobile, closeMobile }
}
