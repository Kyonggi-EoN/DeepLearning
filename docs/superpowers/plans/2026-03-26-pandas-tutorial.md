# Pandas Tutorial Notebook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `data_analytics/01_pandas.ipynb`에 포켓몬 데이터를 활용한 한국어 판다스 입문 튜토리얼을 완성한다.

**Architecture:** 기존 소개 마크다운 셀(id: `6dfa1327`) 아래에 섹션별 셀을 순서대로 삽입. 포켓몬 데이터로 흐름을 이끌고 마지막 연습 문제는 Students Social Media Addiction 데이터 사용.

**Tech Stack:** Python, pandas, matplotlib, kaggle CLI, Jupyter (NotebookEdit tool)

---

## 파일 구조

| 파일 | 역할 |
|------|------|
| `data_analytics/01_pandas.ipynb` | 수정 — 튜토리얼 셀 추가 |
| `data_analytics/data/Pokemon.csv` | 생성 — kaggle 다운로드 결과 |
| `data_analytics/data/Students Social Media Addiction.csv` | 기존 유지 — 연습 문제용 |

---

### Task 1: 소개 섹션 업데이트

기존 마크다운 셀을 더 풍부한 소개로 교체하고 섹션 헤더 셀을 추가한다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb` (cell id: `6dfa1327`)

- [ ] **Step 1: 기존 소개 셀을 교체**

NotebookEdit 호출 (edit_type: `replace`, cell_id: `6dfa1327`):

```markdown
# 🐼 판다스 배우기

**판다스(pandas)**란 데이터 분석을 진행하는 프로그래머들이 가장 많이 사용하는 파이썬 라이브러리입니다.

## 이 노트북에서 배울 것들

| 번호 | 주제 |
|------|------|
| 1 | 데이터 준비 — Kaggle에서 포켓몬 데이터 받기 |
| 2 | 데이터 로드 — CSV를 DataFrame으로 읽기 |
| 3 | 기본 탐색 — shape, info, describe |
| 4 | 컬럼 선택 — Series vs DataFrame |
| 5 | 필터링 — 조건에 맞는 행 골라내기 |
| 6 | 기본 연산 — 정렬, 집계, 빈도수 |
| 7 | 시각화 — 그래프 한 장 그리기 |
| 8 | 연습 문제 — 직접 해보기 |

📺 참고 재생 목록: https://youtube.com/playlist?list=PLNPt2ycoheHrQHSg7MqTELiWUmieIxH-5&si=U3BvLLY-ZdSY7S6K
```

- [ ] **Step 2: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: update pandas notebook intro section"
```

---

### Task 2: 데이터 준비 섹션 추가

Kaggle CLI로 포켓몬 데이터를 다운로드하는 방법을 설명하는 셀을 추가한다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 셀 삽입** (기존 소개 셀 아래에 insert)

NotebookEdit 호출 (edit_type: `insert`, insert_after: `6dfa1327`, cell_type: `markdown`):

```markdown
---
## 1. 데이터 준비 — Kaggle에서 포켓몬 데이터 받기

이 튜토리얼에서는 **포켓몬 스탯 데이터**를 사용합니다.
데이터는 Kaggle에서 무료로 받을 수 있습니다.

### Kaggle API 키 설정 (최초 1회)
1. https://www.kaggle.com/settings 에서 **"Create New Token"** 클릭
2. 다운로드된 `kaggle.json`을 `~/.kaggle/kaggle.json` 위치에 저장
3. 아래 셀을 실행하면 자동으로 다운로드됩니다
```

- [ ] **Step 2: 다운로드 코드 셀 삽입**

NotebookEdit 호출 (edit_type: `insert`, 방금 삽입한 셀 아래, cell_type: `code`):

```python
import os

# data 폴더가 없으면 만들기
os.makedirs("data", exist_ok=True)

# 포켓몬 데이터 다운로드 (kaggle CLI 필요)
# pip install kaggle  로 설치할 수 있습니다
!kaggle datasets download -d rounakbanik/pokemon --path data/ --unzip

print("다운로드 완료!")
print("파일 목록:", os.listdir("data"))
```

- [ ] **Step 3: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add kaggle data download section to pandas notebook"
```

---

### Task 3: 데이터 로드 섹션 추가

`pd.read_csv()`로 DataFrame을 만드는 개념을 설명한다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 삽입**

NotebookEdit (insert after 다운로드 코드 셀, markdown):

```markdown
---
## 2. 데이터 로드 — CSV 파일을 DataFrame으로 읽기

판다스에서 가장 먼저 배울 것은 **데이터를 불러오는 것**입니다.
엑셀의 표처럼 생긴 구조를 판다스에서는 **DataFrame**이라고 부릅니다.

```python
import pandas as pd

df = pd.read_csv("파일경로.csv")
```

`pd`는 판다스의 별명(alias)입니다. 관례적으로 `pd`를 사용합니다.
```

- [ ] **Step 2: 로드 코드 셀 삽입**

NotebookEdit (insert, code):

```python
import pandas as pd

# 포켓몬 데이터 읽기
df = pd.read_csv("data/pokemon.csv")

# 처음 5행 보기
df.head()
```

- [ ] **Step 3: head/tail 설명 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
### head() vs tail()

| 함수 | 설명 |
|------|------|
| `df.head()` | 앞에서 5행 |
| `df.head(10)` | 앞에서 10행 |
| `df.tail()` | 뒤에서 5행 |
```

- [ ] **Step 4: tail 코드 셀 삽입**

NotebookEdit (insert, code):

```python
# 마지막 5행 보기
df.tail()
```

- [ ] **Step 5: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add data loading section to pandas notebook"
```

---

### Task 4: 기본 탐색 섹션 추가

`shape`, `info()`, `describe()`로 데이터를 파악하는 방법을 다룬다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
---
## 3. 기본 탐색 — 데이터의 생김새 파악하기

데이터를 받으면 먼저 **어떻게 생겼는지** 확인해야 합니다.
판다스에서 자주 쓰는 탐색 도구들을 배워봅시다.
```

- [ ] **Step 2: shape 코드 셀 삽입**

NotebookEdit (insert, code):

```python
# 데이터의 크기: (행 수, 열 수)
print("데이터 크기:", df.shape)
print(f"총 {df.shape[0]}개의 포켓몬, {df.shape[1]}개의 정보 항목")
```

- [ ] **Step 3: columns 코드 셀 삽입**

NotebookEdit (insert, code):

```python
# 컬럼(열) 이름 목록 보기
print("컬럼 목록:")
print(df.columns.tolist())
```

- [ ] **Step 4: info() 설명 마크다운 + 코드 삽입**

NotebookEdit (insert, markdown):

```markdown
### info() — 각 컬럼의 타입과 결측값 확인

`info()`를 실행하면 각 컬럼이 어떤 타입인지(숫자인지, 문자인지)와
**결측값(빈 값)이 있는지** 한눈에 볼 수 있습니다.
```

NotebookEdit (insert, code):

```python
df.info()
```

- [ ] **Step 5: describe() 설명 마크다운 + 코드 삽입**

NotebookEdit (insert, markdown):

```markdown
### describe() — 숫자 컬럼의 통계 요약

평균(mean), 최솟값(min), 최댓값(max) 등을 한 번에 볼 수 있습니다.
```

NotebookEdit (insert, code):

```python
df.describe()
```

- [ ] **Step 6: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add basic exploration section to pandas notebook"
```

---

### Task 5: 컬럼 선택 섹션 추가

`df['col']`(Series)과 `df[['a','b']]`(DataFrame)의 차이를 설명한다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
---
## 4. 컬럼 선택 — 원하는 열 골라내기

DataFrame에서 특정 열(컬럼)만 꺼낼 수 있습니다.
꺼내는 방식에 따라 결과 타입이 달라집니다.

| 방식 | 결과 | 예시 |
|------|------|------|
| `df['Name']` | **Series** (1개 열) | 포켓몬 이름 목록 |
| `df[['Name', 'HP']]` | **DataFrame** (여러 열) | 이름과 HP만 있는 표 |
```

- [ ] **Step 2: Series 선택 코드 셀 삽입**

NotebookEdit (insert, code):

```python
# 1개 컬럼 선택 → Series 반환
names = df['Name']
print(type(names))  # <class 'pandas.core.series.Series'>
names.head()
```

- [ ] **Step 3: DataFrame 선택 코드 셀 삽입**

NotebookEdit (insert, code):

```python
# 여러 컬럼 선택 → DataFrame 반환
subset = df[['Name', 'Type 1', 'HP', 'Attack', 'Defense']]
print(type(subset))  # <class 'pandas.core.frame.DataFrame'>
subset.head()
```

- [ ] **Step 4: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add column selection section to pandas notebook"
```

---

### Task 6: 필터링 섹션 추가

조건문으로 행을 걸러내는 방법을 설명한다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
---
## 5. 필터링 — 조건에 맞는 행 골라내기

"HP가 100 이상인 포켓몬만 보고 싶다"처럼
특정 조건을 만족하는 행만 골라낼 수 있습니다.

```python
df[조건]
```
```

- [ ] **Step 2: 단일 조건 필터링 코드 셀 삽입**

NotebookEdit (insert, code):

```python
# HP가 100 이상인 포켓몬
high_hp = df[df['HP'] >= 100]
print(f"HP 100 이상 포켓몬 수: {len(high_hp)}")
high_hp[['Name', 'Type 1', 'HP']].head(10)
```

- [ ] **Step 3: 문자열 조건 필터링 마크다운 + 코드 삽입**

NotebookEdit (insert, markdown):

```markdown
### 문자열 조건으로 필터링

특정 타입의 포켓몬만 골라낼 수도 있습니다.
```

NotebookEdit (insert, code):

```python
# 불 타입(Fire) 포켓몬만
fire_pokemon = df[df['Type 1'] == 'Fire']
print(f"불 타입 포켓몬 수: {len(fire_pokemon)}")
fire_pokemon[['Name', 'Type 1', 'HP', 'Attack']].head(10)
```

- [ ] **Step 4: 다중 조건 필터링 마크다운 + 코드 삽입**

NotebookEdit (insert, markdown):

```markdown
### 다중 조건 — AND(&) 와 OR(|)

여러 조건을 동시에 적용할 때는 `&`(그리고)와 `|`(또는)를 사용합니다.
각 조건은 **반드시 괄호로 묶어야** 합니다.
```

NotebookEdit (insert, code):

```python
# 불 타입이면서 공격력(Attack)이 100 이상인 포켓몬
strong_fire = df[(df['Type 1'] == 'Fire') & (df['Attack'] >= 100)]
print(f"강력한 불 타입 포켓몬 수: {len(strong_fire)}")
strong_fire[['Name', 'Type 1', 'HP', 'Attack']].head()
```

- [ ] **Step 5: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add filtering section to pandas notebook"
```

---

### Task 7: 기본 연산 섹션 추가

`value_counts()`, `sort_values()`, 집계 함수를 다룬다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
---
## 6. 기본 연산 — 정렬, 집계, 빈도수

데이터를 정렬하거나 요약하는 방법을 배워봅시다.
```

- [ ] **Step 2: value_counts 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### value_counts() — 각 값의 등장 횟수

어떤 타입의 포켓몬이 가장 많은지 세어봅시다.
```

NotebookEdit (insert, code):

```python
# 포켓몬 타입별 수
type_counts = df['Type 1'].value_counts()
print("타입별 포켓몬 수 (상위 10개):")
type_counts.head(10)
```

- [ ] **Step 3: sort_values 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### sort_values() — 정렬하기

가장 빠른 포켓몬은 누구일까요?
```

NotebookEdit (insert, code):

```python
# 스피드(Speed) 기준으로 내림차순 정렬
fastest = df[['Name', 'Type 1', 'Speed']].sort_values('Speed', ascending=False)
print("가장 빠른 포켓몬 Top 10:")
fastest.head(10)
```

- [ ] **Step 4: 집계 함수 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### 집계 함수 — mean, max, min

숫자 컬럼에 대해 평균, 최댓값, 최솟값을 구할 수 있습니다.
```

NotebookEdit (insert, code):

```python
# HP 통계
print(f"HP 평균: {df['HP'].mean():.1f}")
print(f"HP 최댓값: {df['HP'].max()} — {df.loc[df['HP'].idxmax(), 'Name']}")
print(f"HP 최솟값: {df['HP'].min()} — {df.loc[df['HP'].idxmin(), 'Name']}")
```

- [ ] **Step 5: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add basic operations section to pandas notebook"
```

---

### Task 8: 시각화 섹션 추가

`df.plot()`으로 간단한 그래프를 그린다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
---
## 7. 시각화 — 데이터를 그래프로 보기

판다스는 matplotlib을 내장하고 있어서 DataFrame에서 바로 그래프를 그릴 수 있습니다.
```

- [ ] **Step 2: 막대 그래프 코드 셀 삽입**

NotebookEdit (insert, code):

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', family='DejaVu Sans')  # 한글 폰트 문제 방지

# 타입별 포켓몬 수 막대 그래프
type_counts = df['Type 1'].value_counts().head(10)

type_counts.plot(kind='bar', figsize=(10, 5), color='skyblue', edgecolor='black')
plt.title('Top 10 Pokemon Types')
plt.xlabel('Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

- [ ] **Step 3: 히스토그램 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### 히스토그램 — HP 분포 보기

포켓몬들의 HP가 어떻게 분포되어 있는지 살펴봅시다.
```

NotebookEdit (insert, code):

```python
df['HP'].plot(kind='hist', bins=20, figsize=(8, 4), color='lightgreen', edgecolor='black')
plt.title('Pokemon HP Distribution')
plt.xlabel('HP')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
```

- [ ] **Step 4: 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add visualization section to pandas notebook"
```

---

### Task 9: 연습 문제 섹션 추가

Students Social Media Addiction 데이터를 사용한 연습 문제를 추가한다.

**Files:**
- Modify: `data_analytics/01_pandas.ipynb`

- [ ] **Step 1: 섹션 헤더 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
---
## 8. 연습 문제 — 직접 해보기

이번엔 **학생 소셜 미디어 중독 데이터**를 사용해 직접 판다스를 실습해봅시다.
경로: `data/Students Social Media Addiction.csv`

컬럼 정보:
| 컬럼 | 설명 |
|------|------|
| `Student_ID` | 학생 ID |
| `Age` | 나이 |
| `Gender` | 성별 (Male / Female) |
| `Academic_Level` | 학력 (High School / Undergraduate / Graduate) |
| `Avg_Daily_Usage_Hours` | 하루 평균 소셜미디어 사용 시간 |
| `Most_Used_Platform` | 가장 많이 쓰는 플랫폼 |
| `Sleep_Hours_Per_Night` | 하루 평균 수면 시간 |
| `Mental_Health_Score` | 정신 건강 점수 (1~10) |
| `Addicted_Score` | 중독 점수 (1~10) |
```

- [ ] **Step 2: 데이터 로드 연습 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### 문제 1: 데이터 로드 및 탐색

아래 코드를 완성해서 데이터를 불러오고 크기를 확인하세요.
```

NotebookEdit (insert, code):

```python
# 데이터 불러오기
students = pd.read_csv("data/Students Social Media Addiction.csv")

# TODO: students의 크기(shape)를 출력하세요
# TODO: 처음 5행을 출력하세요
# TODO: 각 컬럼의 타입을 확인하세요 (info())
```

- [ ] **Step 3: 필터링 연습 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### 문제 2: 필터링

조건에 맞는 학생들을 골라보세요.
```

NotebookEdit (insert, code):

```python
# TODO: Addicted_Score가 8 이상인 학생들을 출력하세요
# TODO: 위 학생들의 수는 몇 명인가요?

# TODO: Instagram을 가장 많이 쓰는 학생들만 골라내세요
```

- [ ] **Step 4: 연산 연습 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### 문제 3: 집계 및 분석
```

NotebookEdit (insert, code):

```python
# TODO: 플랫폼별 학생 수를 세어보세요 (value_counts)
# TODO: 하루 평균 소셜미디어 사용 시간이 가장 긴 학생은 누구인가요? (sort_values)
# TODO: Mental_Health_Score의 평균, 최댓값, 최솟값을 구하세요
```

- [ ] **Step 5: 시각화 연습 코드 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
### 문제 4: 시각화

플랫폼별 사용자 수를 막대 그래프로 그려보세요.
```

NotebookEdit (insert, code):

```python
# TODO: students 데이터에서 Most_Used_Platform 별 학생 수를 막대 그래프로 그리세요
# 힌트: value_counts().plot(kind='bar', ...)
```

- [ ] **Step 6: 정답 셀 삽입**

NotebookEdit (insert, markdown):

```markdown
---
<details>
<summary>💡 정답 보기 (먼저 스스로 해보세요!)</summary>

```python
# 문제 1
print(students.shape)
students.head()
students.info()

# 문제 2
addicted = students[students['Addicted_Score'] >= 8]
print(len(addicted))
instagram_users = students[students['Most_Used_Platform'] == 'Instagram']

# 문제 3
print(students['Most_Used_Platform'].value_counts())
print(students.sort_values('Avg_Daily_Usage_Hours', ascending=False).head(1))
print(students['Mental_Health_Score'].mean(), students['Mental_Health_Score'].max(), students['Mental_Health_Score'].min())

# 문제 4
students['Most_Used_Platform'].value_counts().plot(kind='bar', figsize=(10,5))
plt.title('Platform Usage')
plt.tight_layout()
plt.show()
```

</details>
```

- [ ] **Step 7: 마무리 마크다운 삽입**

NotebookEdit (insert, markdown):

```markdown
---
## 잘 하셨습니다! 🎉

이 노트북에서 배운 핵심 판다스 기능들:

| 함수 | 역할 |
|------|------|
| `pd.read_csv()` | CSV 파일을 DataFrame으로 읽기 |
| `df.head() / tail()` | 첫/마지막 N행 보기 |
| `df.shape` | 행/열 수 확인 |
| `df.info()` | 컬럼 타입 및 결측값 확인 |
| `df.describe()` | 숫자 컬럼 통계 요약 |
| `df['col']` | 1개 컬럼 선택 (Series) |
| `df[['a','b']]` | 여러 컬럼 선택 (DataFrame) |
| `df[df['col'] > 값]` | 조건 필터링 |
| `df['col'].value_counts()` | 값별 등장 횟수 |
| `df.sort_values('col')` | 정렬 |
| `df['col'].mean/max/min()` | 집계 |
| `df.plot()` | 간단한 시각화 |

다음 단계: `02_matplotlib.ipynb` 에서 더 다양한 시각화를 배워봅시다!
```

- [ ] **Step 8: 최종 커밋**

```bash
git add data_analytics/01_pandas.ipynb
git commit -m "docs: add exercises and closing section to pandas notebook"
```

---

## 검증 방법

1. VS Code에서 `data_analytics/01_pandas.ipynb` 열기
2. `01_pandas.ipynb` 디렉토리에서 Jupyter 커널 실행
3. `kaggle datasets download` 셀 실행 후 `data/pokemon.csv` 파일 생성 확인
4. "Run All" 실행 → 모든 셀 오류 없이 실행 확인
5. 시각화 섹션에서 막대 그래프, 히스토그램 2개 출력 확인
6. 연습 문제 정답 셀 실행 확인
