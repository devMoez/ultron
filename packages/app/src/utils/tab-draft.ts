/**
 * Per-tab draft storage.
 * When the user switches tabs on the "new session" screen (no params.id),
 * we save the current input text and restore the target tab's draft.
 *
 * Uses a custom event so sidebar-shell can signal the prompt-input without
 * needing to thread context through the component tree.
 */

import type { TabType } from "@/context/session-type"

const KEY = "ultron:tab-drafts"

export function loadDraft(tab: TabType): string {
  try {
    const map = JSON.parse(localStorage.getItem(KEY) ?? "{}") as Record<string, string>
    return map[tab] ?? ""
  } catch {
    return ""
  }
}

export function saveDraft(tab: TabType, text: string) {
  try {
    const map = JSON.parse(localStorage.getItem(KEY) ?? "{}") as Record<string, string>
    map[tab] = text
    localStorage.setItem(KEY, JSON.stringify(map))
  } catch {}
}

export function clearDraft(tab: TabType) {
  saveDraft(tab, "")
}

/** Dispatch from sidebar when switching tabs. prompt-input listens. */
export function dispatchSwitchTab(fromTab: TabType, toTab: TabType) {
  window.dispatchEvent(new CustomEvent("ultron:switch-tab", { detail: { fromTab, toTab } }))
}

/** Listen in prompt-input. Return cleanup fn. */
export function onSwitchTab(
  handler: (fromTab: TabType, toTab: TabType) => void,
): () => void {
  const listener = (e: Event) => {
    const { fromTab, toTab } = (e as CustomEvent).detail as { fromTab: TabType; toTab: TabType }
    handler(fromTab, toTab)
  }
  window.addEventListener("ultron:switch-tab", listener)
  return () => window.removeEventListener("ultron:switch-tab", listener)
}
