#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT_DIR/config/farm_profile.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE"
  echo "Copy config/farm_profile.env.example to config/farm_profile.env and fill values."
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

replace() {
  local search="$1"
  local repl="$2"
  find "$ROOT_DIR" -type f \( -name "*.md" -o -name "*.csv" \) ! -path "*/.git/*" -print0 \
    | xargs -0 sed -i "s|$search|$repl|g"
}

replace "\\[Your Farm Name\\]" "$FARM_NAME"
replace "\\[Farm Name\\]" "$FARM_NAME"
replace "\\[Your Name\\]" "$OWNER_NAME"
replace "\\[Name\\]" "$OWNER_NAME"
replace "\\[Your Email\\]" "$OWNER_EMAIL"
replace "\\[Your Phone\\]" "$OWNER_PHONE"
replace "\\[Insert\\]" "TBD"

# Specific buyer one-pager placeholders
replace "Minimum order: \[Insert\]" "Minimum order: $BUYER_MIN_ORDER"
replace "Lead time: \[Insert\]" "Lead time: $BUYER_LEAD_TIME"
replace "Payment terms: \[Insert\]" "Payment terms: $BUYER_PAYMENT_TERMS"

echo "Done. Placeholders replaced across markdown/csv files."
