# **추천 시스템**


## **추천 시스템의 유형**
- 콘텐츠 기반 필터링

- 협업 필터링

    - 최근접 이웃 협업 필터링

    - 잠재 요인 협업 필터링

- 최근엔 행렬 분해(Matrix Factorization) 기법을 이용, **잠재 요인 협업 필터링 기반** 추천 시스템이 유행

- 아마존은 아직 아이템 기반의 최근접 이웃 협업 필터링을 사용한다.

---

### **콘텐츠 기반 필터링**

- a가 A 아이템을 선호하는 경우, A 아이템과 비슷한 정보(콘텐츠)를 가진 B 아이템을 추천

    - ex. a가 영화 A를 선호할 경우, 영화 A의 장르, 출연 배우, 감독, 영화 키워드 등 콘텐츠가 유사한 영화 B를 추천

---


### **협업 필터링**

- 취향이 비슷한 친구들에게 영화를 추천받는 것처럼 추천하는 알고리즘.

- 사용자의 행동 양식(평점, 장바구니에 담았는지 여부 등)을 바탕으로 추천

- **사용자-아이템 평점 매트릭스**와 같은 사용자 행동 데이터를 기반으로, 사용자가 아직 평가하지 않은 아이템을 예측 평가하는 것

- 사용자가 이미 평가한 다른 아이템을 기반으로, 사용자가 평가하지 않은 아이템의 예측 평가를 도출한다.

- 최근접 이웃 방식, 잠재 요인 방식으로 나뉜다. 두 방식 모두 **사용자-아이템 평점 행렬 데이터**에 의지해 추천을 수행

- Row는 개별 이용자, Column은 개별 아이템으로 구성

---

#### **최근접 이웃 협업 필터링**

- Memory 협업 필터링이라고도 함, 사용자 기반/아이템 기반으로 나뉨

- **사용자 기반** : 당신과 비슷한 고객들이 이 상품도 구매했습니다!

    - 특정 사용자와 유사한 다른 사용자를 TOP-N으로 선정, 이 사용자가 좋아하는 아이템을 추천

    - 특정 사용자와 타 사용자 간의 유사도를 측정, 가장 유사도가 높은 TOP-N을 선정하여 그들의 선호 아이템을 추천하는 것.
    - 유저 a가 평가한 다른 많은 아이템들이 b에게도 비슷하게 평가되었다면, a와 b는 유사한 사용자다.
    - 그래서, a가 평가한 아이템들 중 높은 평점을 받았는데, b에게는 평가되지 않았다면
    - b에게 그 아이템을 추천해준다.

- **아이템 기반** : 이 상품을 선택한 다른 고객들은 이 상품도 구매했습니다!

    - 특정 아이템과 유사한 다른 아이템을 찾아 주는 것.

    - 특정 아이템과 유사한 다른 아이템은 어떻게 찾는가? --> 아이템 간의 속성 X (중요)
    - A 아이템을 평가한 많은 다른 사람들이, 그와 비슷하게 B 아이템을 평가했다면 A와 B는 유사한 아이템이라고 볼 수 있다(취향 관점에서)
    - 그래서, A아이템을 평가한 사람 중 B아이템을 써보지 않은 사람에게 B 아이템을 추천해준다.

- 최근접 이웃 협업 필터링은 대부분 아이템 기반의 알고리즘을 적용한다.

    - 비슷한 상품을 좋아한다 --> 사람 취향이 비슷하다고 판단하긴 어렵기 때문, 그리고

    - 아이템 수에 비해, 사람 수는 매우매우매우 많음. --> 평점을 매기는 사람은 적지만, 평점을 받는 아이템은 많다. 아이템의 유사도 파악이 더 쉽다는 것

- 코사인 유사도가 추천 시스템의 유사도 측정에 가장 많이 사용된다.

    - 추천 시스템 사용 데이터는, 피처 벡터화된 텍스트 데이터와 동일하게 다차원 희소 행렬이라는 특징이 있음 --> 코사인 유사도 이용


---

#### **코사인 유사도**
- 유사도를 측정하는 방법으로 유클리드 거리를 재는 방법, 코사인 유사도 등이 있음.

    - 유클리드 거리 : 점과 점이 얼마나 가까운지를 평가

    - 코사인 유사도 : 벡터 관점에서 방향이 얼마나 비슷한지를 평가
- 텍스트 분석의 경우 문서의 길이, 추천 시스템의 경우 사용자 간 기준 차이가 유사도 차이를 만들어낼 경우가 존재함. --> 이러면 안돼 원래는
- 그래서, 텍스트 분석과 추천 시스템에서 유사도를 체크할 때는 코사인 유사도를 사용한다.(방향이 같은지만 본다.)

---

#### **잠재 요인 협업 필터링**

- 사용자-아이템 평점 행렬 데이터만으로, '잠재 요인'을 끄집어 내는 것.

- '잠재 요인' 이 뭔지는 명확히 정의 불가하다.

- 다차원 희소 행렬인 사용자-아이템 행렬 데이터를 저차원 밀집 행렬의 <사용자-잠재요인>행렬과 <잠재요인-아이템>행렬로 분해할 수 있다.

- 분해된 두 행렬의 내적을 통해 새로운 예측 사용자-아이템 평점 행렬 데이터를 만듦

- 위의 예측 행렬로 평점이 미부여된 아이템에 대한 예측 평점을 생성

- 사용자~영화 간 평점 행렬 R : P * Q.T로 분해 가능

    - 여기서 P는 사용자~영화장르 선호도 행렬, Q는 아이템~영화장르 분류 행렬
    
    - User1이 Item1에 높은 점수를 주었다
        - User1의 모든 장르 선호도와
        - Item1의 모든 장르 차지 비율
        - 이러한 잠재 요인(장르)를 따져서 잠재 요인 행렬 요소의 곱으로 나타낼 수 있음.

- 다차원의 매트릭스를 저차원 매트릭스로 분해하는 기법을 행렬 분해(Matrix Factorization)이라고 한다.


##### **행렬 분해의 이해**

- SVD(Singular Vector Decomposition), NMF(Non-Negative Matrix Factorization) 등이 있다.

- (M, N)의 행렬을 (M, K) * (K, N) 의 행렬로 분해될 수 있다.

- R행렬을 사용자-아이템 평점 행렬이라 하고, P, Q를 각각 사용자-잠재요인 행렬, 잠재요인-아이템 행렬이라고 하면 R = P * Q.T 라고 쓸 수 있다.

- 요소로 따지면, r_(u, i) = p_u * q^t_i.

- R을 P, Q로 분해한 후에는 사용자가 평가하지 않은 아이템에 대한 평점도 P * Q.T를 통해 유추할 수 있다.


- 행렬 분해를 어떻게? --> 일반적으로 SVD를 쓸 수 있지만, SVD는 Null값이 있으면 사용 불가하다!
- 우리는 Null값이 존재하는 행렬을 분해해야 하므로, 일반적 SVD 방식으로는 분해 불가능
    - SGD(확률적 경사하강법), ALS(Alternating Least Squares) 방식을 이용해 SVD를 수행한다.

---
 
##### **확률적 경사 하강법 행렬 분해**

- P, Q로 계산된 예측 R행렬 값이 실제 R행렬 값과 가장 최소의 오류를 가질 수 있도록 반복적인 비용 함수 최적화

- P, Q를 임의의 값을 가진 행렬로 설정한 뒤, R^ 행렬을 계산 --> 오류 값 계산

- 오류값을 최소화하도록 P, Q를 적절한 값으로 업데이트(회귀의 과정과 비슷)

- L2 규제를 고려한다. L1 : 일차, L2 : 이차
    - p_u, q_i의 각 요소들의 L2 norm이 너무 높지 않게, 즉 과적합을 피한다.

- p, q의 변화를 어떻게 계산하는지? 직접 찾아보기.