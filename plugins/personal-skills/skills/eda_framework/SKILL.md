---
name: eda_framework
description: Use this skill whenever the user wants exploratory data analysis (EDA) done on a tabular dataset/notebook in their usual style — trigger on "EDA 진행해", "탐색적 데이터 분석", "우리 늘하던 eda 프레임워크로", or when starting analysis on a new csv before modeling (분류/회귀/군집화 실습 등). Applies the user's standard 11-step EDA sequence: 임포트 -> 한글폰트 -> 데이터입력 -> 구조파악 -> 결측치 -> 분포확인 -> 이상치(boxplot) -> 변수간관계(kde) -> 상관관계(heatmap) -> 컬럼정리/X,y분리 -> 스케일링/인코딩.
---

# EDA 기본 프레임워크

노트북(.ipynb)에서 새 데이터셋을 받았을 때 항상 따르는 11단계 EDA 순서. 각 단계는 코드 셀 + (필요시) 발견한 내용을 요약하는 markdown 셀로 구성한다. 회귀/분류/군집화 등 문제 유형과 무관하게 이 뼈대를 따르고, 데이터 특성에 맞게 세부 컬럼/로직만 채운다.

## 1. 패키지 임포트
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
```

## 2. 한글 폰트 설정, 마이너스 기호 깨짐 방지
```python
import matplotlib.font_manager as fm
font_path = 'C:\\Windows\\Fonts\\H2GTRM.TTF'
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False
```

## 3. 데이터 입력받기
```python
df = pd.read_csv('파일명.csv')
df.shape
df.head()
```

## 4. 데이터 구조 파악, 독립/종속 변수 체크
```python
df.info()
df.describe()
```
- 컬럼별 dtype, non-null count 확인 → 결측 의심 컬럼 표시
- 타겟(종속변수) 컬럼이 무엇인지, 회귀인지 분류인지 확정
- 식별자성 컬럼(id, index성 컬럼)은 이후 제거 후보로 메모

## 5. 결측치 체크 및 처리
```python
df.isnull().sum()
```
- 결측이 여러 컬럼에서 같은 개수로 나오면 행단위 결측 의심 → 아래로 확인
```python
cols = [...]  # 결측 의심 컬럼들
df[cols].isnull().sum(axis=1).value_counts()
```
- 처리 방법은 컬럼 성격에 따라 결정하고 **왜 그렇게 처리했는지 markdown으로 남긴다**:
  - 타겟 결측 → 그 행은 `dropna` (지도학습은 라벨 없으면 못 씀)
  - 소수 결측 & 주변값과 유사 → 중앙값/평균/최빈값으로 `fillna`
  - 다수 컬럼 동시 결측(행단위) → 해당 행 삭제 검토

## 6. 데이터 분포 확인
```python
df.duplicated().sum()  # 중복행 확인

# 범주형: 값 종류/개수
df['범주형컬럼'].value_counts()

# 타겟 분포 (분류 문제 - 불균형 여부 확인)
df['target'].value_counts()
sns.countplot(data=df, x='target')
plt.show()

# 연속형 분포
df['수치형컬럼'].hist(bins=30)
plt.show()
```
- 타겟이 불균형하면 이후 `train_test_split`에 `stratify` 필요, 모델 `class_weight` 고려 메모

## 7. 이상치 처리 (boxplot)
```python
plt.figure(figsize=(16,16))
for i, col in enumerate(numeric_cols):
    plt.subplot(4,4,i+1)
    sns.boxplot(data=df, x='target', y=col)  # 분류면 타겟별로 비교
plt.tight_layout()
plt.show()
```
- 이상치를 무조건 삭제하지 말 것 — 타겟과 강하게 연관되면(`pd.crosstab`으로 확인) 신호일 수 있으니 남긴다
- 측정 오류로 보이는 경우만 삭제/대체

## 8. 주요 변수 간 관계 확인 (pairplot, kde)
```python
sns.pairplot(data=df[numeric_cols + ['target']], hue='target', diag_kind='kde',
             plot_kws={'alpha': 0.4, 's': 10})
plt.show()
```

## 9. 상관관계 체크 (heatmap)
```python
plt.figure(figsize=(12,10))
sns.heatmap(df[numeric_cols + ['target']].corr(), vmin=-1, vmax=1,
            square=True, annot=True, fmt='.2f', cmap='coolwarm')
plt.show()
```

## 10. 의미없는 컬럼 제거, 독립/종속 변수 분리
```python
df = df.drop(columns=['id같은 무의미 컬럼'])
X = df.drop(columns=['target'])
y = df['target']
```

## 11. 스케일링, 인코딩
```python
# 범주형 인코딩
# - 순서 의미 있으면 OrdinalEncoder(categories=[[...]])
# - 순서 없으면 OneHotEncoder 또는 pd.get_dummies
oEncoder = OrdinalEncoder(categories=[['순서1','순서2',...]])
X['범주형컬럼'] = oEncoder.fit_transform(X[['범주형컬럼']])

# 학습/검증 분리 (타겟 불균형이면 stratify)
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=820, stratify=y
)

# 스케일링 - 트리 기반 모델(DecisionTree/RandomForest 등)은 불필요, 거리/경사기반 모델은 필요
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)
```

## 진행 원칙
- 각 단계 결과를 보고 놀랍거나 의사결정이 필요한 지점은 markdown 셀로 짧게 근거를 남긴다 (나중에 "왜 이렇게 전처리했는지" 설명 요구에 대비).
- `random_state`는 노트북에서 이미 쓰던 값(날짜 기반, 예: 820, 821)을 이어서 사용한다.
- 이 프레임워크는 EDA~전처리 단계까지이며, 모델링(11 이후)은 별도 요청 시 진행한다.
