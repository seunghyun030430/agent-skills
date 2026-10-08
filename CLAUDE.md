# CLAUDE.md

이 레포에서 작업할 때 따를 규칙. (개인용 Claude Code 플러그인 마켓플레이스 레포)

## 레포 성격

이 레포는 **마켓플레이스**이고, 플러그인은 `plugins/` 아래에 둔다.
현재 플러그인은 `common` 하나이며, 기능은 그 안에 **스킬**로 늘려간다.

## 구조

```
.
├── .claude-plugin/
│   └── marketplace.json              # 마켓플레이스 카탈로그 (name: agent-skills)
└── plugins/
    └── common/
        ├── .claude-plugin/
        │   └── plugin.json           # 플러그인 매니페스트 (name: common)
        └── skills/
            └── <skill>/
                ├── SKILL.md          # frontmatter의 name == 디렉토리명
                └── ...               # 보조 문서(선택)
```

- `marketplace.json`의 플러그인 항목 `name`과 `plugin.json`의 `name`은 같아야 한다.
- `source`는 마켓플레이스 루트 기준 상대경로(`./plugins/<plugin>`)로 쓰고 `..`은 쓰지 않는다.

## 새 스킬 추가하는 법

1. `plugins/common/skills/<new-skill>/SKILL.md` 작성 — frontmatter의 `name`은 `<new-skill>`과 일치시킨다.
2. `claude plugin validate .`로 검증.
3. 커밋·푸시.
4. `/plugin marketplace update`로 갱신하면 `/common:<new-skill>`로 호출 가능.

## 버전 관리

스킬을 수정하면 `plugins/common/.claude-plugin/plugin.json`의 `version`을 올린다.
`version`을 안 올리면 commit SHA로 추적돼 업데이트 파악이 번거롭다.

## 커밋 컨벤션 (Conventional Commits)

형식: `<type>: <설명>` — 설명은 한글로 쓴다.

| type | 용도 |
|---|---|
| `feat` | 스킬·기능 추가 |
| `fix` | 버그·오류 수정 |
| `docs` | 문서(README, CLAUDE.md, SKILL.md 설명 등) 수정 |
| `refactor` | 동작 변화 없는 구조 개선 |
| `chore` | 설정·메타데이터·잡일 (plugin.json version, .gitignore 등) |

예) `feat: study 스킬 추가`
