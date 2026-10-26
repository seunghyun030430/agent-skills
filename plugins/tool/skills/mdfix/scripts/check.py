"""mdfix 검사. usage: python3 -I check.py <file.md> [...]
기계적으로 판정 가능한 항목만 본다. 문체·의미는 사람이(에이전트가) 직접 읽어서 판단한다."""
import re
import sys

MAX = 100  # 렌더링 기준 한 줄 최대 글자 수
LIST = re.compile(r'^\s*([*-]|\d+\.) ')
LABEL = re.compile(r'^\s*[*-] \*\*[^*]+\*\*\s*[:：]')
ATTR = re.compile(r'^\s*[*-] (?!\*\*)[^,]+?\s[—–:]\s?.*,')  # `이름 — 속성1, 속성2`
SLANG = r'죽였|킬했|짜른|짤랐|날렸|갈아엎|뒤엎|박았|꽂았|먹혔|안 먹|삽질|뻘짓|레알|ㅋㅋ|ㅎㅎ'
SLOP = r'에 대해|에 대한|을 통해|를 통해|되어지|되어졌|에 있어서|혁신적|강력[한하]|효율적[인으]|매끄러운|원활[한하]|손쉽게|매우 중요|핵심은|핵심입니다|주목할|중요한 것은|결론적으로|요약하자면|앞으로도|단순히 .*아니라'
HAEYO = re.compile(r'(어요|아요|해요|예요|이에요|돼요|둬요|줘요|봐요|네요)[.!?)]?(\s|$)')
PLAIN = re.compile(r'([가-힣]?)([가-힣])다(?:[.!?)]|$)')  # 문장 끝만: '마다 ' 같은 조사 제외


def is_plain(m):
    """'합니다·습니다'(니 앞 글자 받침 ㅂ)는 합니다체라 제외."""
    return not (m[2] == '니' and m[1] and (ord(m[1]) - 0xAC00) % 28 == 17)
# 비유 은어 후보. 전체 목록이 아니며 references/style-ko.md의 판단 기준이 우선
METAPHOR = r'박제|태우|태워|때리|때려|털어|털었|땜빵|뻗었|뻗어|날먹|말아먹'
EMOJI = re.compile('[\U0001F300-\U0001FAFF\u2600-\u27BF]')
# 한글 종결 뒤 . ? ! 다음에 글이 더 이어지면 한 줄에 문장이 둘 이상. 소수점·버전·약어는 한글 뒤가 아니라 제외됨
MULTI = re.compile(r'[가-힣][.?!]\s+\S')


def rendered(s):
    """렌더링될 글자만 남긴다: 링크 URL, 서식 기호, 목록·헤딩 기호, 줄 끝 하드 줄바꿈 제거."""
    s = s.rstrip()
    s = re.sub(r'\\$', '', s)
    s = re.sub(r'^\s*(#+\s|>\s?|[*-]\s|\d+\.\s)', '', s)
    s = re.sub(r'!?\[([^\]]*)\](\([^)]*\)|\[[^\]]*\])', r'\1', s)
    s = re.sub(r'<(https?://[^>]+)>', r'\1', s)
    s = re.sub(r'`([^`]*)`', r'\1', s)
    s = re.sub(r'(\*\*|__|~~)(.+?)\1', r'\2', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'\1', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\\([!-/:-@\[-`{-~])', r'\1', s)
    return s.strip()


def check(path):
    text = open(path, encoding='utf-8').read()
    lines = text.splitlines()
    kinds, in_code, prev = {}, False, ''  # 줄번호 → 종류 (코드블록 밖만)
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith(('```', '~~~')):
            in_code = not in_code
            kinds[i] = prev = 'fence'
            continue
        if in_code:
            continue
        if not s: k = ''
        elif s.startswith('|'): k = 'table'
        elif LIST.match(ln): k = 'list'
        elif s.startswith('#'): k = 'heading'
        elif ln[:1] in (' ', '\t') and prev in ('list', 'cont'): k = 'cont'  # 목록 항목의 이어지는 줄
        else: k = 'para'
        kinds[i] = k
        if k: prev = k
    body = [(i, lines[i - 1]) for i, k in kinds.items() if k != 'fence']
    out = {}

    def add(key, i, s=''):
        out.setdefault(key, []).append(f'L{i} {s.strip()[:60]}')

    for i, ln in body:
        k, s = kinds[i], ln.strip()
        if re.search(SLANG, ln): add('구어·속어', i, ln)
        if re.search(SLOP, ln): add('AI slop 후보', i, ln)
        if re.search(METAPHOR, ln): add('비유 은어 후보(교체 또는 용어 검토)', i, ln)
        if EMOJI.search(ln) and k != 'table': add('이모지(표 밖)', i, ln)
        if re.search(r'\\[_*.#\-]', ln) or re.match(r'^#+ \d+\\\.', s): add('불필요 이스케이프 후보', i, ln)
        if re.match(r'^<(table|br|colgroup)', s): add('HTML 잔여물', i, ln)
        if re.fullmatch(r'[ \t]+', ln): add('빈 줄 공백', i)
        if k in ('para', 'list', 'cont'):
            if HAEYO.search(ln + ' '): add('해요체(합니다체 대상)', i, ln)
            if any(is_plain(m) for m in PLAIN.finditer(ln)): add('평서체(합니다체 대상)', i, ln)
        if k == 'table':
            if not re.fullmatch(r'[|:\-\s]+', s):
                for c in s.strip('|').split('|'):
                    if len(rendered(c)) > MAX: add(f'{MAX}자 초과 셀', i, f'({len(rendered(c))}자) {c}')
        elif k and len(rendered(ln)) > MAX:
            add(f'{MAX}자 초과 줄', i, f'({len(rendered(ln))}자) {ln}')
        if k in ('para', 'list', 'cont') and MULTI.search(rendered(ln)):
            add('한 줄에 문장 여럿(문장 단위 줄 대상)', i, ln)
        for m in re.finditer(r'\*\*[^*]+\*\*', ln):
            pre = ln[:m.start()].rstrip()
            if pre not in ('', '*', '-') and not pre.endswith('|') and not re.fullmatch(r'\d+\.', pre):
                add('문장 중간 굵게', i, m.group())

    # 라벨 불릿·속성 반복 불릿이 3개 이상 이어지는 묶음 → 표 전환 대상
    for pat, key in ((LABEL, '라벨 불릿 묶음(표 대상)'), (ATTR, '속성 반복 목록(표 대상)')):
        run = []
        for i, ln in body + [(0, '#')]:
            if pat.match(ln):
                run.append(i)
            elif ln.strip() and kinds.get(i) != 'cont':
                if len(run) >= 3: add(key, run[0], f'{len(run)}개 L{run[0]}~L{run[-1]}')
                run = []

    for i in range(2, len(lines) + 1):
        ka, kb = kinds.get(i - 1, ''), kinds.get(i, '')
        if ka and kb and ka != kb and 'fence' not in (ka, kb) and not (ka in ('list', 'cont') and kb in ('list', 'cont')):
            add('블록 사이 빈 줄 없음', i, lines[i - 1])
        if ka in ('para', 'cont') and kb == ka and not lines[i - 2].endswith(('  ', '\\')):
            add('하드 줄바꿈 없는 개행(공백 2칸 추가 또는 합치기)', i - 1, lines[i - 2])
    if '\n\n\n' in text: add('연속 빈 줄', text[:text.index('\n\n\n')].count('\n') + 2)
    if not text.endswith('\n') or text.endswith('\n\n'): add('문서 끝 개행', len(lines))

    print(f'== {path}')
    for k, v in out.items():
        print(f'-- {k} ({len(v)})')
        for x in v[:8]:
            print('   ' + x)
        if len(v) > 8: print(f'   ... 외 {len(v) - 8}건')
    if not out: print('기계 검사 항목 없음')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        check(p)
