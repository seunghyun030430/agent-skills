# CLAUDE.md

이 레포에서 작업할 때 따를 규칙. (개인용 Claude Code 플러그인 마켓플레이스 레포)

## 레포 성격

이 레포는 **마켓플레이스**이고, 플러그인은 `plugins/` 아래에 둔다.
**플러그인 하나 = 분류 하나**다. 스킬 호출명은 `/<플러그인>:<스킬>`이 되므로, 플러그인 이름이 곧 분류 이름이다.

| 분류(플러그인) | 스킬 | 호출 |
|---|---|---|
| `study` | `docs`, `toy` | `/study:docs`, `/study:toy` |

## 구조

```
.
├── .claude-plugin/
│   └── marketplace.json              # 마켓플레이스 카탈로그 (name: seunghyun-skills — 레포 이름 agent-skills는 Anthropic 예약 이름이라 마켓플레이스 이름으로 쓸 수 없음)
└── plugins/
    └── <category>/                   # 예: study
        ├── .claude-plugin/
        │   └── plugin.json           # name == <category>
        └── skills/
            └── <skill>/
                ├── SKILL.md          # frontmatter의 name == 디렉토리명
                └── ...               # 보조 문서(선택)
```

- `marketplace.json`의 플러그인 항목 `name`과 `plugin.json`의 `name`은 같아야 한다.
- `source`는 마켓플레이스 루트 기준 상대경로(`./plugins/<category>`)로 쓰고 `..`은 쓰지 않는다.

## 기존 분류에 스킬 추가

1. `plugins/<category>/skills/<new-skill>/SKILL.md` 작성 — frontmatter의 `name`은 `<new-skill>`과 일치시킨다. 본문·description의 호출명은 `/<category>:<new-skill>`로 쓴다.
2. `plugins/<category>/.claude-plugin/plugin.json`의 `version`을 올린다.
3. `README.md`의 수록 스킬 표에 추가한다.
4. `claude plugin validate .`로 검증 → 커밋·푸시.
5. `/plugin marketplace update`로 갱신하면 `/<category>:<new-skill>`로 호출 가능.

## 새 분류 추가

1. `plugins/<new-category>/.claude-plugin/plugin.json` 작성(`name`, `description`, `version: 1.0.0`).
2. `plugins/<new-category>/skills/<skill>/SKILL.md` 작성.
3. `.claude-plugin/marketplace.json`의 `plugins` 배열에 `{ "name": "<new-category>", "source": "./plugins/<new-category>", "description": "..." }` 추가.
4. `README.md`에 분류 섹션 추가, 이 문서의 분류 표 갱신.
5. `claude plugin validate .` → 커밋·푸시. 사용자는 `/plugin install <new-category>@seunghyun-skills`로 설치한다.

분류 이름은 짧은 소문자 명사로 짓는다(예: `study`, `review`, `ops`). 스킬이 한두 개뿐인 분류를 남발하지 말고, 성격이 겹치면 기존 분류에 넣는다.

## 버전 관리

스킬을 수정하면 해당 분류의 `plugins/<category>/.claude-plugin/plugin.json` `version`을 올린다.
`version`을 안 올리면 commit SHA로 추적돼 업데이트 파악이 번거롭다.

## 커밋 컨벤션 (Conventional Commits)

형식: `<type>: <설명>` — 설명은 한글로 쓴다.

| type | 용도 |
|---|---|
| `feat` | 스킬·분류 추가 |
| `fix` | 버그·오류 수정 |
| `docs` | 문서(README, CLAUDE.md, SKILL.md 설명 등) 수정 |
| `refactor` | 동작 변화 없는 구조 개선(이름 변경·이동 포함) |
| `chore` | 설정·메타데이터·잡일 (plugin.json version, .gitignore 등) |

예) `feat: study 분류에 toy 스킬 추가`
