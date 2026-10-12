# Sourced by the brain's blocking hooks (intent-first.sh, preflight-hook.sh,
# home-staleness.sh). Each block is journaled through `tabula report`, the
# one writer of the journal format, as a hook-blocked entry whose note starts
# "gate <name>:" so `tabula doctor` counts it under that name. The block
# stands whatever happens here: a failed or absent tabula costs one stderr
# line and never the exit.
# Per wiki/tabula/adrs/brain-tooling-follow-ups.tabula.

journal_block() {
  local root="$1" ref="$2" gate="$3" saw="$4"
  if [ -n "$root" ] && command -v tabula >/dev/null 2>&1 \
    && timeout 5 tabula report --as session --kind hook-blocked --ref "${ref:-nosession}" \
      --note "gate ${gate}: ${saw}" --root "$root" >/dev/null 2>&1; then
    return 0
  fi
  printf 'gate %s: this block was not journaled (tabula report unavailable or failed).\n' "$gate" >&2
  return 0
}
