#!/bin/bash
# Renders the series-callback shot O once the cartoon and the scan render are done (one heavy job at a time).
while pgrep -f "tools/render_ep1[.]sh" >/dev/null || pgrep -f "tools/after_cartoon[.]sh" >/dev/null; do sleep 60; done
"$(dirname "$0")/render_ep1.sh" O
