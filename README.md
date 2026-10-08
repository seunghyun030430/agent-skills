# agent-skills

개인용 Claude Code 플러그인 마켓플레이스. 현재 플러그인 `common` 하나와 그 안의 스킬을 담는다.

## 설치

Claude Code 세션에서 아래를 순서대로 실행한다.

```
/plugin marketplace add <github-owner>/agent-skills
```

```
/plugin install common@agent-skills
```

설치 후 새 세션부터 스킬이 인식된다. 이미 추가한 마켓플레이스를 갱신하려면 `/plugin marketplace update`.

## 수록 스킬

| 스킬 | 호출 | 설명 |
|---|---|---|
| `study` | `/common:study` | 기술 주제를 조사해 번호 매긴 Markdown 학습 문서 레포로 정리 |

## 사용 예제

### `study`

기술 주제 하나를 정리한 학습 문서 레포를 현재 디렉토리에 만든다.

- **빈 디렉토리에서 실행한다.** 산출물을 현재 작업 디렉토리에 생성하므로 새 디렉토리에서 시작한다.
- 문서 단위로 한글 커밋한다.
- 비교표 중심 README와 작성 컨벤션 CLAUDE.md를 세팅한다.
- 필요하면 사용자 확인을 받아 코드 샘플까지 작성하고, 산출물을 검증·보완한다.
- `/common:study`로 명시적으로 호출해야 동작한다.

```
/common:study kafka
```
