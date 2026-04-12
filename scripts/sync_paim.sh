#!/bin/bash

# Bidirectional PAIM sync script - syncs whichever file is newer
# Usage: ./sync_paim.sh

XENON="/Users/keithstanigar/Documents/Projects/Xenon_3/NON-X_PAIM_Memory.md"
ANALYTICS="/Users/keithstanigar/Documents/Projects/non-x_analytics/docs/NON-X_PAIM_Memory.md"

# Check if both files exist
if [ ! -f "$XENON" ]; then
  echo "❌ Xenon_3 PAIM not found: $XENON"
  exit 1
fi

if [ ! -f "$ANALYTICS" ]; then
  echo "⚠️  non-x_analytics PAIM not found, creating from Xenon_3"
  cp "$XENON" "$ANALYTICS"
  echo "✅ PAIM synced: Xenon_3 → non-x_analytics"
  exit 0
fi

# Compare modification times
XENON_TIME=$(stat -f %m "$XENON" 2>/dev/null || stat -c %Y "$XENON" 2>/dev/null)
ANALYTICS_TIME=$(stat -f %m "$ANALYTICS" 2>/dev/null || stat -c %Y "$ANALYTICS" 2>/dev/null)

if [ "$XENON_TIME" -gt "$ANALYTICS_TIME" ]; then
  cp "$XENON" "$ANALYTICS"
  echo "✅ PAIM synced: Xenon_3 → non-x_analytics (Xenon_3 was newer)"
elif [ "$ANALYTICS_TIME" -gt "$XENON_TIME" ]; then
  cp "$ANALYTICS" "$XENON"
  echo "✅ PAIM synced: non-x_analytics → Xenon_3 (non-x_analytics was newer)"
else
  echo "ℹ️  PAIM files already in sync (same timestamp)"
fi