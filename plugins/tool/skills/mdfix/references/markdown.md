# 마크다운 문법 근거

mdfix가 포맷을 고칠 때 기대는 문법 사실. 출처는 CommonMark 0.31.2, GFM 0.29-gfm, GitHub 문서다. 렌더러가 GitHub이 아니면 해당 렌더러 문서를 우선한다.

- [줄바꿈](#줄바꿈)
- [블록 사이 빈 줄](#블록-사이-빈-줄)
- [이스케이프](#이스케이프)
- [취소선과 물결표](#취소선과-물결표)
- [표](#표)
- [내보내기 흔적](#내보내기-흔적)

## 줄바꿈

| 입력 | 결과 | 근거 |
| --- | --- | --- |
| 줄 끝 공백 2칸 이상 + 개행 | 하드 줄바꿈(`<br />`) | [CommonMark §6.7](https://spec.commonmark.org/0.31.2/#hard-line-breaks) |
| 줄 끝 `\` + 개행 | 하드 줄바꿈 | 같은 절 |
| 그냥 개행 | 소프트 줄바꿈. 브라우저에서 공백 하나로 보임 | [CommonMark §6.8](https://spec.commonmark.org/0.31.2/#soft-line-breaks) |

- 블록의 마지막 줄 끝에서는 두 방식 모두 무시된다
- mdfix는 문장 단위 줄바꿈에 공백 2칸을 쓴다. 원문이 이미 `\` 방식이면 그 방식을 유지한다
- 문장 경계가 아닌 곳에서 끊긴 소프트 줄바꿈(에디터 폭에 맞춰 끊긴 자국)은 한 줄로 합친 뒤 문장 단위로 다시 나눈다
- 공백 2칸은 눈에 안 보이고 일부 에디터가 저장 시 지운다
- GitHub의 이슈·PR·Discussion 본문은 개행을 그대로 줄바꿈으로 렌더링한다. `.md` 파일에는 해당하지 않는다 ([GitHub 문서](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax))

## 블록 사이 빈 줄

| 블록 | 빈 줄 없이 앞 문단을 끊을 수 있나 | 근거 |
| --- | --- | --- |
| ATX 헤딩(`#`) | 가능 | [CommonMark 예제 78](https://spec.commonmark.org/0.31.2/#atx-headings) |
| 불릿 목록 | 가능 | [CommonMark §5.2](https://spec.commonmark.org/0.31.2/#list-items) |
| 번호 목록 | 1로 시작할 때만 가능. `14. ...`는 앞 문단에 이어 붙음 | 같은 절 규칙 1 |
| 펜스 코드블록, 인용, 수평선 | 가능 | [CommonMark §4](https://spec.commonmark.org/0.31.2/#leaf-blocks) |
| 표 | GitHub 문서는 앞 빈 줄 필수로 명시 | [GitHub 표 문서](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables) |

- 표는 빈 줄이나 다른 블록이 나올 때까지 이어진다. 표 바로 다음 줄에 문단을 붙이면 그 줄이 표의 행으로 흡수된다 ([GFM 예제 202](https://github.github.com/gfm/#tables-extension-))
- 스펙상 필수가 아닌 곳에도 블록 앞뒤 빈 줄을 두는 이유는 렌더러 간 호환과 원문 가독성이다. 원조 Markdown.pl은 빈 줄을 요구했다

## 이스케이프

- 이스케이프 가능한 문자는 ASCII 구두점 전체 ([CommonMark §2.4](https://spec.commonmark.org/0.31.2/#backslash-escapes))
- 단어 안의 `_`는 강조가 되지 않는다. `FOO_BAR`, `user_id`에 `\_`는 불필요 ([CommonMark §6.2](https://spec.commonmark.org/0.31.2/#emphasis-and-strong-emphasis), "foo_bar_baz")
- 단어 안의 `*`는 강조가 된다(`foo*bar*baz`). `*`의 이스케이프는 지우기 전에 렌더링이 바뀌는지 확인한다
- 헤딩 `## 1\. 제목`의 `\.`는 불필요. `1.`이 목록이 되는 건 줄 맨 앞일 때뿐이고, 헤딩 안에서는 목록이 되지 않는다
- 코드 스팬·코드블록 안에서는 이스케이프가 동작하지 않으므로 손대지 않는다

## 취소선과 물결표

- GFM은 물결표 1개와 2개 모두 취소선으로 처리한다. 3개 이상은 취소선이 아니다 ([GFM §6.5](https://github.github.com/gfm/#strikethrough-extension-), 예제 491·493)
- 범위 표기 `1~3`이 같은 문단에 두 번 나오면 그 사이가 취소선이 된다. 이 경우 `\~`를 유지하거나 `1–3`, `1부터 3까지`로 바꾼다
- 같은 문단에 `~`가 하나뿐이면 `\~`를 지워도 렌더링이 같다

## 표

- 셀은 인라인만 담는다. 목록·코드블록 같은 블록은 넣을 수 없다 ([GFM §4.10](https://github.github.com/gfm/#tables-extension-))
- 셀 안의 `|`는 `\|`로 쓴다. 코드 스팬 안에서도 같다 (GFM 예제 200)
- 헤더 행과 구분 행의 셀 수가 다르면 표로 인식되지 않는다 (GFM 예제 203)
- 셀 안 줄바꿈 `<br>`은 공식 문서에 명시가 없다. 쓰지 않는 쪽을 기본으로 한다

## 내보내기 흔적

위키·에디터에서 내보낸 마크다운에 흔히 남는 것. 렌더링 결과는 같거나 내용이 없으므로 지운다.

| 흔적 | 예 | 처리 |
| --- | --- | --- |
| 단어 안 `_` 이스케이프 | `ORDER\_ITEM` | `ORDER_ITEM` |
| 헤딩 번호 이스케이프 | `## 2\. 설치` | `## 2. 설치` |
| 내용 없는 HTML | `<table><tr><td><br></td></tr></table>`, 단독 `<br>` | 삭제 |
| 임베드 자리표시자 | `[embed: ...]` | 유지. 원본 도구에서 다시 붙일 단서 |
