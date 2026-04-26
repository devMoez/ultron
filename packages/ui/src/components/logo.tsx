import { ComponentProps } from "solid-js"

// ── Ultron "U" mark (compact, used in new-session view) ─────────────────────
export const Mark = (props: { class?: string }) => {
  return (
    <svg
      data-component="logo-mark"
      classList={{ [props.class ?? ""]: !!props.class }}
      viewBox="0 0 16 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* U shape: two vertical bars connected at bottom */}
      <rect x="0" y="0" width="4" height="16" fill="var(--icon-strong-base)" />
      <rect x="12" y="0" width="4" height="16" fill="var(--icon-strong-base)" />
      <rect x="0" y="14" width="16" height="4" fill="var(--icon-strong-base)" />
      <rect x="2" y="2" width="12" height="10" fill="var(--icon-weak-base)" />
    </svg>
  )
}

// ── Ultron splash (loading screen, 80×100 viewBox) ───────────────────────────
export const Splash = (props: Pick<ComponentProps<"svg">, "ref" | "class">) => {
  return (
    <svg
      ref={props.ref}
      data-component="logo-splash"
      classList={{ [props.class ?? ""]: !!props.class }}
      viewBox="0 0 80 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Large U shape */}
      <rect x="0" y="0" width="22" height="80" fill="var(--icon-strong-base)" />
      <rect x="58" y="0" width="22" height="80" fill="var(--icon-strong-base)" />
      <rect x="0" y="68" width="80" height="22" fill="var(--icon-strong-base)" />
      <rect x="10" y="10" width="60" height="52" fill="var(--icon-weak-base)" />
    </svg>
  )
}

// ── Ultron full logo (not used in main app, kept for compatibility) ───────────
export const Logo = (props: { class?: string }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 180 36"
      fill="none"
      classList={{ [props.class ?? ""]: !!props.class }}
    >
      {/* U */}
      <rect x="0" y="0" width="6" height="30" fill="var(--icon-strong-base)" />
      <rect x="18" y="0" width="6" height="30" fill="var(--icon-strong-base)" />
      <rect x="0" y="24" width="24" height="6" fill="var(--icon-strong-base)" />
      {/* L */}
      <rect x="30" y="0" width="6" height="36" fill="var(--icon-strong-base)" />
      <rect x="30" y="30" width="18" height="6" fill="var(--icon-strong-base)" />
      {/* T */}
      <rect x="54" y="0" width="18" height="6" fill="var(--icon-strong-base)" />
      <rect x="60" y="0" width="6" height="36" fill="var(--icon-strong-base)" />
      {/* R */}
      <rect x="78" y="0" width="6" height="36" fill="var(--icon-strong-base)" />
      <rect x="78" y="0" width="18" height="6" fill="var(--icon-strong-base)" />
      <rect x="78" y="15" width="18" height="6" fill="var(--icon-strong-base)" />
      <rect x="90" y="6" width="6" height="9" fill="var(--icon-strong-base)" />
      <rect x="90" y="21" width="6" height="15" fill="var(--icon-strong-base)" />
      {/* O */}
      <rect x="102" y="0" width="6" height="36" fill="var(--icon-strong-base)" />
      <rect x="120" y="0" width="6" height="36" fill="var(--icon-strong-base)" />
      <rect x="102" y="0" width="24" height="6" fill="var(--icon-strong-base)" />
      <rect x="102" y="30" width="24" height="6" fill="var(--icon-strong-base)" />
      {/* N */}
      <rect x="132" y="0" width="6" height="36" fill="var(--icon-strong-base)" />
      <rect x="150" y="0" width="6" height="36" fill="var(--icon-strong-base)" />
      <rect x="132" y="0" width="24" height="6" fill="var(--icon-strong-base)" />
    </svg>
  )
}
