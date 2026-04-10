# Outta (아우타)

> **$2/month, 743 lines, 3 LLMs — brain-inspired AI framework**

모든 답변이 측두엽(맥락 분석) → 전두엽(응답 생성) → 소뇌(검증+증폭)를 거칩니다.
LLM 래퍼가 아닙니다. 뇌 과학 기반 신호 증폭 아키텍처입니다.

설계·구축: 함영재 (Ham Youngjae) | Since 2026-04-02

---

## 왜 Outta인가

| 기존 AI 프레임워크 | Outta |
|-------------------|-------|
| 프롬프트 체이닝 | 뇌 영역별 신호 처리 |
| 분류에 LLM 호출 | 효소 라우터 — API 0회, ~30ms |
| 할루시네이션 후처리 | 3중 방어 (코드→구조→LLM) |
| 단일 관점 응답 | 맥락 분석 → 증폭 → 검증 |

## 성능

| 항목 | 수치 |
|------|------|
| 분류 속도 | **~30ms** (효소 라우터, API 0, local embeddings ~400MB RAM) |
| FAST 경로 | **~1초** (LLM 1회) |
| BRAIN 경로 | **~5초** (LLM 3회) |
| 분류 정확도 | **93%** (독립 테스트 100개, 95% CI 88-98%) |
| 월 비용 | **~$2 API cost** (Groq free tier + DeepSeek, on Oracle Free Tier) |
| 할루시네이션 방어 | 3-layer (pattern → structural → LLM cross-check) |
| 코드 | **~750줄** core (excluding benchmarks/examples) |

## 아키텍처

```
입력
 ↓
기저핵 (캐시 히트?) ──→ 즉시 반환
 ↓ miss
해마 (관련 기억 주입)
 ↓
효소 라우터 (코사인 유사도, ~30ms, API 0)
 ↓ 확신도 < 20%이면 뇌간 LLM 폴백
FACTUAL 게이트 ──→ 고유명사/사실 질문 → SEARCH
 ↓
ACC (경로 결정)
 ├── FAST → 전두엽 단독 (LLM 1회) → 출력
 ├── SEARCH → 검색 필요 플래그 → 출력
 └── BRAIN ↓
      측두엽 (맥락/감정/숨은 의도)
       ↓
      전두엽 (맥락 기반 응답 생성)
       ↓
      소뇌 (검증 + 증폭)
       ↓   점수 < 8 → 수정+보강
       ↓   빠진 관점 → 증폭
      크리틱 (패턴 차단 + 구조적 환각)
       ↓
      뇌섬엽 (LLM 교차 검증, 점수 < 9일 때만)
       ↓
      요소 회로 (저장 전 독소 정제)
       ↓
출력 → 해마 저장 → 기저핵 캐시
```

## 할루시네이션 3중 방어

```
응답 생성
 ↓
[1차] 크리틱 — 코드 기반 패턴 매칭
  → 가짜 수치, 아부, 축 왜곡, 합성 오류, 가짜 다양성
 ↓
[2차] 뇌섬엽 — LLM 교차 검증
  → 크리틱이 못 잡는 미묘한 날조 감지
 ↓
[3차] 요소 회로 — 저장 전 정제
  → 메모리에 오염된 데이터가 쌓이는 것 자체를 차단
```

## 빠른 시작

```bash
git clone https://github.com/ham-youngjae/outta.git
cd outta
pip install sentence-transformers  # optional, 없으면 키워드 폴백
```

```python
from pipeline import OuttaPipeline

pipeline = OuttaPipeline(
    llm_fast=my_fast_llm,     # 경량: 효소 폴백 시 분류 (Groq Llama-70B)
    llm_think=my_think_llm,   # 사고: 측두엽 + 전두엽 (DeepSeek, Qwen-235B)
    llm_verify=my_verify_llm, # 검증: 소뇌 증폭 + 뇌섬엽 감시 (다른 모델 추천)
)

result = pipeline.process("직장을 그만둬야 할지 모르겠어")
print(result["answer"])
# 경로: BRAIN | 점수: 9
```

### LLM 인터페이스

```python
def my_llm(messages: list[dict], max_tokens: int, temperature: float) -> str:
    """OpenAI-호환 messages → 응답 문자열."""
    ...
```

3개 모델 모두 이 인터페이스만 맞추면 됩니다. 같은 모델 3개로도 동작합니다.

### 모델 배치 가이드

| 역할 | 특성 | 추천 | 이유 |
|------|------|------|------|
| `fast` | 빠르고 저렴 | Groq Llama-70B | 분류 폴백만. 효소가 대부분 처리 |
| `think` | 사고력 | DeepSeek-V3, Qwen-235B | 응답 품질 = 전체 품질 |
| `verify` | 객관적 | Gemini Flash, GPT-4o-mini | think과 다른 모델 → 교차 검증 효과 |

## 뇌 영역

### 실시간 처리

| 영역 | 역할 | 파일 |
|------|------|------|
| **효소 라우터** | 코사인 유사도 즉시 분류 (API 0) | `enzyme.py` |
| **뇌간** | 효소 폴백 시 LLM 분류 | `brainstem.py` |
| **ACC** | 확신도 기반 경로 분기 | `acc.py` |
| **측두엽** | 맥락/감정/숨은 의도 분석 | `temporal.py` |
| **전두엽** | 맥락 기반 응답 생성 | `frontal.py` |
| **소뇌** | 검증 + 빠진 관점 증폭 | `cerebellum.py` |
| **크리틱** | 패턴 차단 + 구조적 환각 감지 | `critic.py` |
| **뇌섬엽** | LLM 교차 검증 | `insula.py` |
| **글리아** | 적응형 temperature 조절 | `glia.py` |

### 저장

| 영역 | 역할 | 파일 |
|------|------|------|
| **해마** | 기억 저장/검색 | `hippocampus.py` |
| **기저핵** | 패턴 캐시 | `basal_ganglia.py` |

## 설계 원칙

1. **증폭 > 토론** — 같은 모델로 상반된 역할극은 연극이다. 하나의 응답을 검증하고 보강하는 게 진짜 증폭.
2. **분류에 LLM 쓰지 마** — 효소 라우터. 코사인 유사도면 충분하다. API 0회.
3. **생성에서 막아** — _postprocess 100줄보다 프롬프트 한 줄이 낫다.
4. **오염된 기억은 저장하지 마** — 요소 회로. 메모리에 들어가면 끝이다.
5. **검증은 생성과 분리** — 만드는 놈과 검사하는 놈이 달라야 한다.

## v1 → v2 변경 이력

| v1 | v2 | 이유 |
|----|-----|------|
| 뇌간 LLM 분류 (매번 API 1회) | 효소 라우터 (API 0, ~30ms) | FAST 경로 5초→1초 |
| 편도체×2 이중 신호 (효율 vs 연민) | 삭제 → 소뇌 증폭으로 통합 | 같은 모델로 상반된 관점은 연극 |
| 전두엽 3신호 합성 (merge) | 맥락 기반 단일 응답 (select) | 합치면 부풀고 서정이 끼어듦 |
| 크리틱 regex 3개 | 구조적 환각 2종 + 축왜곡 + 확장 | 가짜 다양성, 합성 오류 차단 |
| 글리아 칭찬만 감지 | 대화 유형별 적응형 temperature | 주제에 따라 temperature 자동 조절 |
| BRAIN LLM 6회 | LLM 3회 (측두→전두→소뇌) | 비용 절반, 속도 2배 |
| 요소 회로 없음 | 저장 전 독소 정제 | 메모리 오염 원천 차단 |

## 버전 이력

```
Outta v1 — 14영역 병렬 + 편도체 이중신호
Outta v2 — 증폭형 아키텍처 + 효소 라우터 + 구조적 환각 방어
```

## 라이선스

Apache License 2.0

## 만든 사람

함영재 (Ham Youngjae)
Since 2026-04-02
