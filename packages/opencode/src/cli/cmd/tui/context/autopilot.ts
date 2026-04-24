// Ultron autopilot — when enabled, all permission requests are auto-approved
let _enabled = false

export const Autopilot = {
  get enabled() {
    return _enabled
  },
  enable() {
    _enabled = true
  },
  disable() {
    _enabled = false
  },
  toggle() {
    _enabled = !_enabled
    return _enabled
  },
}
