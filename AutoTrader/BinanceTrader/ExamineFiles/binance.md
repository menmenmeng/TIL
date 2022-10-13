1. Backtrading data
interval:
m -> minutes; h -> hours; d -> days; w -> weeks; M -> months
- 1m
- 3m
- 5m
- 15m
- 30m
- 1h
- 2h
- 4h
- 6h
- 8h
- 12h
- 1d
- 3d
- 1w
- 1M
Update Speed: 250ms

최대 1h정도의 interval로 데이터를 가져와서 backtrading한다.

2. Strategy
  1. MA돌파시 매매
  2. 변동성 돌파
  3. 그냥 간단하게 노가다로, 몇% 이상 먹으면 시장가 매도
  4. 수수료를 꼭 생각해야 함. 수수료는 어떻게 날아가는지



3. 개선점
  1. MA돌파시 매매
  - short가 이미 있는데, 그 포지션이 적어서 아직 쓸 돈이 남아 있다. 즉. asset - long_btc - short_btc가 아직 남아 있다. 면 short를 더 추가한다. 가 아니라 long을 청산하고 short를 가져가야지
  - 