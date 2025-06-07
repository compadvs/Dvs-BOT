#!/bin/bash
set -e
mkdir -p libs
cd libs

declare -a repos=(
  "mcpt"
  "market-structure"
  "IntramarketDifference"
  "TradeDependenceRunsTest"
  "TrendlineBreakoutMetaLabel"
  "TimeSeriesReversibility"
  "TimeSeriesVisibilityGraphs"
  "VSAIndicator"
  "RSI-PCA"
  "TechnicalAnalysisAutomation"
  "VolatilityHawkes"
  "PermutationEntropy"
  "TVLIndicator"
  "TrendLineAutomation"
)

for repo in "${repos[@]}"; do
  if [ ! -d "$repo" ]; then
    git clone --depth 1 "https://github.com/neurotrader888/$repo" "$repo"
  else
    echo "$repo already cloned"
  fi
 done

