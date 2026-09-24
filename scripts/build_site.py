from pathlib import Path
import html, re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/tutorial-source.md'
source = SOURCE.read_text(encoding='utf-8')

# Keep only the 20 lab units, in the order specified by the course design.
chunks = re.split(r'(?m)^# Lab (\d+): (.+)$', source)
labs = []
for i in range(1, len(chunks), 3):
    num = int(chunks[i]); title = chunks[i+1].strip(); body = chunks[i+2]
    if num > 20: continue
    if num == 20:
        body = re.split(r'(?m)^# 7\. Checkpoint Repository Design\s*$', body, maxsplit=1)[0]
    labs.append({'num':num, 'title':title, 'body':body.strip()})

assert len(labs) == 20, f'Expected 20 labs, got {len(labs)}'

def split_sections(md):
    lines=md.splitlines(); out=[]; current=('text',[]); in_fence=False
    for line in lines:
        if line.strip().startswith('```'):
            in_fence=not in_fence
            current[1].append(line)
            continue
        m=re.match(r'^## (.+)$', line) if not in_fence else None
        if m:
            out.append(current); current=(m.group(1).strip(),[])
        else: current[1].append(line)
    out.append(current)
    return out

def inline(s):
    s=html.escape(s, quote=False)
    s=re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s=re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s=re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s

def md_html(md):
    lines=md.splitlines(); out=[]; para=[]; in_code=False; code=[]; in_ul=False; in_ol=False; in_quote=False
    def flush_para():
        nonlocal para
        if para:
            out.append('<p>'+inline(' '.join(x.strip() for x in para))+'</p>'); para=[]
    def close_lists():
        nonlocal in_ul,in_ol
        if in_ul: out.append('</ul>'); in_ul=False
        if in_ol: out.append('</ol>'); in_ol=False
    def close_quote():
        nonlocal in_quote
        if in_quote: out.append('</blockquote>'); in_quote=False
    for line in lines:
        if line.strip().startswith('```'):
            flush_para(); close_lists(); close_quote()
            if not in_code: in_code=True; code=[]
            else: out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>'); in_code=False
            continue
        if in_code: code.append(line); continue
        if not line.strip(): flush_para(); close_lists(); close_quote(); continue
        hm=re.match(r'^(#{1,6})\s+(.+)$',line)
        if hm:
            flush_para(); close_lists(); close_quote(); level=len(hm.group(1)); out.append(f'<h{level}>{inline(hm.group(2))}</h{level}>'); continue
        if line.strip()=='---': flush_para(); close_lists(); close_quote(); out.append('<hr>'); continue
        if re.match(r'^\s*[-*]\s+',line):
            flush_para(); close_quote()
            if in_ol: out.append('</ol>'); in_ol=False
            if not in_ul: out.append('<ul>'); in_ul=True
            out.append('<li>'+inline(re.sub(r'^\s*[-*]\s+','',line))+'</li>'); continue
        if re.match(r'^\s*\d+\.\s+',line):
            flush_para(); close_quote()
            if in_ul: out.append('</ul>'); in_ul=False
            if not in_ol: out.append('<ol>'); in_ol=True
            out.append('<li>'+inline(re.sub(r'^\s*\d+\.\s+','',line))+'</li>'); continue
        if line.startswith('>'):
            flush_para(); close_lists()
            if not in_quote: out.append('<blockquote>'); in_quote=True
            out.append('<p>'+inline(line[1:].strip())+'</p>'); continue
        close_quote(); para.append(line)
    flush_para(); close_lists(); close_quote()
    if in_code: out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>')
    return '\n'.join(out)

checkpoint_for = {n:(f'lab-{n:02d}-start',f'Lab {n} start') for n in range(3,21)}

notice_fallback = {
1:'Git is available in Git Bash, and the name and email settings appear in the global configuration list.',
2:'The support-tools folder is now a repository. The status output identifies the current branch and reports that there are no commits yet.',
3:'The new file is untracked. It exists in the working directory but is not included in repository history.',
4:'The file is staged for the next commit. Staging prepares the selected file version; it does not create a commit.',
5:'The commit creates the first saved point in repository history, and status reports a clean working tree.',
6:'Status reports a modified tracked file, and diff shows the added line as an unstaged change.',
7:'The added line is recorded in a new commit. The history now contains at least two commits.',
8:'The file can have staged content and newer unstaged content at the same time. The two diff commands show those states separately.',
9:'The README is a second tracked file after it is committed.',
10:'The log contains the commits from the fundamentals work. Commit identifiers differ between students.',
11:'A branch is another line of development in the same repository. The asterisk marks the branch currently checked out.',
12:'The new troubleshooting branch points to the same files and history as main until you make branch-specific commits.',
13:'Both new commits belong to troubleshooting because that was the current branch when you created them.',
14:'Switching branches changes the checked-out files. The troubleshooting additions remain saved on their branch.',
15:'The README commit is on main, while the checklist commits remain on troubleshooting.',
16:'The graph shows the branch histories diverging, and branch identifies the current branch.',
17:'After the merge, the troubleshooting additions are available on main.',
18:'Git reports a conflict because both branches changed the same line in different ways.',
19:'The conflict is resolved when you edit the final content, remove markers, stage the file, and commit the merge.',
20:'The graph shows branch work, merge history, and the completed conflict resolution.'}
check_fallback = {
1:'Both commands finish without an error, and the configuration list includes the values you entered.',
2:'Run git status. It should show a valid repository with no commits yet.',
3:'Run git status and confirm network-checklist.txt is listed as untracked.',
4:'Run git status and confirm network-checklist.txt is staged for commit.',
5:'Run git status and confirm a clean working tree. Run git log --oneline and confirm one commit appears.',
6:'Run git status and git diff. Confirm the new gateway line appears in the diff.',
7:'Run git log --oneline and confirm at least two commits appear.',
8:'Run git status, git diff, and git diff --staged. Confirm each shows the corresponding unstaged or staged line, then complete the commit.',
9:'Run git status and confirm a clean working tree after the README commit.',
10:'Run git log --oneline and git status. The log should show several commits and the working tree should be clean.',
11:'Run git branch and git status. Confirm the asterisk identifies the current branch.',
12:'Run git branch and git status. Confirm troubleshooting is the current branch.',
13:'Run git log --oneline and confirm your two troubleshooting commits appear.',
14:'Open the checklist on main and troubleshooting. The additional two lines should appear only on troubleshooting before the merge.',
15:'Run git branch and git log --oneline. Confirm each branch contains its own recent work.',
16:'Run git log --graph --oneline --all and confirm the output shows the branches diverging.',
17:'Open network-checklist.txt on main and confirm the troubleshooting additions are present.',
18:'Run git status and confirm Git identifies the unresolved path as a conflict.',
19:'Run git status and confirm the merge is complete with a clean working tree. Run git log --graph --oneline --all and confirm alternate-link-check remains visible with the resolved merge history.',
20:'Run git log --graph --oneline --all and save the output as Firstname_Lastname_M3_log.txt. Confirm that the graph shows the alternate-link-check branch, its divergence from main, and the completed merge.'}

# Explain the prepared conflict checkpoint clearly; all other recovery links are direct downloads.
checkpoint_notes={18:'This checkpoint starts with the clean, merged main branch at the end of Lab 17. Follow Lab 18 to create the alternate branch and make the two competing changes.',19:'This checkpoint contains the unresolved conflict produced by the normal Lab 18 sequence. Open network-checklist.txt, remove the conflict markers, and complete the merge.'}

def section_html(title, content, cls=''):
    return f'<section class="lesson-section {cls}"><h2>{title}</h2>{content}</section>'

for idx,lab in enumerate(labs):
    n=lab['num']; title=lab['title']; sections=split_sections(lab['body'])
    goal=''; notice=''; check=''; other=[]; all_commands=[]
    for name,lines in sections:
        raw='\n'.join(lines).strip()
        if name.lower()=='goal': goal=md_html(raw)
        elif name.lower() in ('what to notice','what just happened?','what just happened'):
            notice += md_html(raw)
        elif name.lower()=='check your work': check += md_html(raw)
        else:
            if raw: other.append((name,raw))
        
        for block in re.findall(r'```[^\n]*\n(.*?)```',raw,re.S):
            if re.search(r'(?m)^\s*(?:git|mkdir|cd)\b', block): all_commands.append(block)
    if n != 20 and not notice: notice=f'<p>{notice_fallback[n]}</p>'
    if n != 20 and not check: check=f'<p>{check_fallback[n]}</p>'
    instructions_parts=[]
    for name,raw in other:
        # Suppress the source's duplicate named checkpoint headings from being presented as top-level pages.
        instructions_parts.append((f'<h3>{inline(name)}</h3>' if name!='text' and name.lower()!='instructions' else '')+md_html(raw))
    instructions='\n'.join(instructions_parts) or '<p>Follow the steps in order and check the repository state as you work.</p>'
    commands=''.join(f'<div class="command-item"><pre><code>{html.escape(c.strip())}</code></pre><button class="copy-button" type="button">Copy</button></div>' for c in all_commands)
    if not commands: commands='<p>Use the commands shown in the instructions in the order presented.</p>'
    prev_url='../index.html' if n==1 else f'lab-{n-1:02d}.html'
    next_url='../index.html' if n==20 else f'lab-{n+1:02d}.html'
    prev_label='Course home' if n==1 else f'Lab {n-1}: {labs[n-2]["title"]}'
    next_label='Course home' if n==20 else f'Lab {n+1}: {labs[n]["title"]}'
    part='Part 1 · Git fundamentals' if n<=10 else 'Part 2 · Branching and merging'
    if n == 20:
        recovery=''
    elif n <= 2:
        message='There is no repository in this lab. Restart the setup steps if needed.' if n==1 else 'There is no repository checkpoint yet. Restart Lab 2 by creating a new practice folder.'
        recovery=f'<section class="recovery"><div class="recovery-icon" aria-hidden="true">↻</div><div><h2>Repository broken?</h2><p>{message}</p></div></section>'
    else:
        cp, cplabel=checkpoint_for[n]
        cpnote=checkpoint_notes.get(n,'If your repository is no longer in the expected state, download this checkpoint and continue from the files and history it contains.') + ' Extract the ZIP, then use Git Bash in the extracted support-tools folder.'
        recovery=f'<section class="recovery"><div class="recovery-icon" aria-hidden="true">↻</div><div><h2>Repository broken?</h2><p>{html.escape(cpnote)}</p></div><a class="button secondary" href="../checkpoints/{cp}.zip" download>Download Lab {n} checkpoint</a></section>'
    page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="CIS-1160 Git tutorial, Lab {n}: {html.escape(title)}"><title>Lab {n}: {html.escape(title)} | CIS-1160 Git</title><link rel="stylesheet" href="../assets/site.css"></head>
<body><a class="skip-link" href="#main">Skip to lesson</a><header class="site-header"><a class="brand" href="../index.html"><span class="brand-mark">G</span><span>CIS-1160 <b>Git Practice</b></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Labs <span aria-hidden="true">☰</span></button><nav id="site-nav" class="site-nav"><a href="../index.html">Overview</a><a href="../index.html#part-1">Fundamentals</a><a href="../index.html#part-2">Branching &amp; merging</a></nav></header>
<div class="layout"><aside class="sidebar"><div class="side-label">Tutorial map</div><a class="part-link" href="../index.html#part-1">Part 1 · Fundamentals</a>{''.join(f'<a class="lab-link {"active" if x["num"]==n else ""}" href="lab-{x["num"]:02d}.html"><span>{x["num"]:02d}</span>{html.escape(x["title"])}</a>' for x in labs[:10])}<a class="part-link" href="../index.html#part-2">Part 2 · Branching &amp; merging</a>{''.join(f'<a class="lab-link {"active" if x["num"]==n else ""}" href="lab-{x["num"]:02d}.html"><span>{x["num"]:02d}</span>{html.escape(x["title"])}</a>' for x in labs[10:])}</aside>
<main id="main" class="lesson"><div class="crumb"><a href="../index.html">CIS-1160 Git Practice</a><span>/</span><span>Lab {n:02d}</span></div><div class="lesson-kicker">{part}</div><h1>Lab {n}: {html.escape(title)}</h1><div class="lesson-progress"><span>Lab {n} of 20</span><div class="progress-track"><span style="width:{n*5}%"></span></div></div>
{section_html('Goal',goal,'goal-section')}
{section_html('Instructions',instructions)}
{'' if n==20 else section_html('Commands',f'<p class="section-intro">Use these commands as you work through the instructions. Run them in Git Bash.</p>{commands}')}
{'' if n==20 else section_html('What to Notice',notice,'notice-section')}
{'' if n==20 else section_html('Check Your Work',check,'check-section')}
{recovery}
<nav class="lesson-nav" aria-label="Previous and next lessons"><a href="{prev_url}" class="nav-card"><span>← Previous</span><strong>{html.escape(prev_label)}</strong></a><a href="{next_url}" class="nav-card next"><span>Next →</span><strong>{html.escape(next_label)}</strong></a></nav><footer class="site-footer">CIS-1160 Introduction to Information Systems · Git fundamentals and branching</footer></main></div><script src="../assets/site.js"></script></body></html>'''
    (ROOT/'labs'/f'lab-{n:02d}.html').write_text(page,encoding='utf-8')

cards=''.join(f'<a class="overview-card" href="labs/lab-{x["num"]:02d}.html"><span class="card-number">{x["num"]:02d}</span><span class="card-copy"><b>{html.escape(x["title"])}</b><small>{"Git fundamentals" if x["num"]<=10 else "Branching and merging"}</small></span><span class="card-arrow">↗</span></a>' for x in labs)
index=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A beginner-friendly, task-focused Git tutorial for CIS-1160."><title>CIS-1160 Git Practice Tutorial</title><link rel="stylesheet" href="assets/site.css"></head><body><a class="skip-link" href="#main">Skip to tutorial</a><header class="site-header"><a class="brand" href="index.html"><span class="brand-mark">G</span><span>CIS-1160 <b>Git Practice</b></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">☰</span></button><nav id="site-nav" class="site-nav"><a href="#part-1">Fundamentals</a><a href="#part-2">Branching &amp; merging</a><a href="#getting-started">Getting started</a></nav></header><main id="main"><section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="eyebrow-dot"></span> CIS-1160 · Introduction to Information Systems</div><h1>Learn Git by working through the changes.</h1><p>Start with a local repository, make and inspect commits, then practise branches, merges, and conflict resolution using simple technical support files.</p><div class="hero-actions"><a class="button primary" href="labs/lab-01.html">Start with Lab 1 <span>→</span></a><a class="text-link" href="#part-1">Browse all 20 labs</a></div><div class="hero-meta"><span>20 short labs</span><span>Git Bash for Windows</span><span>No programming required</span></div></div><div class="hero-visual" aria-label="Illustration of a Git commit history branching and merging"><div class="visual-top"><span class="window-dot"></span><span class="window-dot"></span><span class="window-dot"></span><span class="visual-title">support-tools · history</span></div><div class="branch-lines"><div class="branch-label main-label">main</div><div class="branch-label work-label">troubleshooting</div><svg viewBox="0 0 440 206" role="img" aria-label="A simple branching and merge graph"><path class="line-main" d="M45 32 V174"/><path class="line-work" d="M45 86 C45 112 90 112 90 138 V174"/><path class="line-merge" d="M90 138 C90 164 45 148 45 174"/><circle cx="45" cy="32" r="7"/><circle cx="45" cy="82" r="7"/><circle cx="90" cy="132" r="7"/><circle cx="45" cy="174" r="7"/><text x="70" y="38">Add project README</text><text x="70" y="88">Clarify link status</text><text x="116" y="138">Add connectivity checks</text><text x="70" y="180">Merge troubleshooting</text></svg></div><div class="visual-caption"><span class="status-dot"></span> A visual history helps you see where work belongs.</div></div></section>
<section id="getting-started" class="start-strip"><div><span class="section-eyebrow">Before you begin</span><h2>Get Git ready in a few minutes.</h2><p>Install Git for Windows, open Git Bash, and complete Lab 1 to verify your setup and identify your commits.</p></div><a href="labs/lab-01.html" class="button secondary">Open setup instructions <span>→</span></a></section>
<section id="part-1" class="lab-group"><div class="group-heading"><div><div class="section-eyebrow">Part 1 · Labs 01–10</div><h2>Git fundamentals</h2><p>Create a repository, track changes, stage files, commit work, and inspect history.</p></div><a href="labs/lab-01.html" class="group-link">Begin Part 1 →</a></div><div class="lab-grid">{''.join(cards.split('</a>')[:10])}</div></section>
<section id="part-2" class="lab-group part-two"><div class="group-heading"><div><div class="section-eyebrow">Part 2 · Labs 11–20</div><h2>Branching and merging</h2><p>Build a second line of work, bring changes together, and resolve a conflict.</p></div><a href="labs/lab-11.html" class="group-link">Begin Part 2 →</a></div><div class="lab-grid">{''.join('</a>'.join(cards.split('</a>')[10:]))}</div></section>
<section class="outcomes"><div><div class="section-eyebrow">Your learning path</div><h2>From first commit to conflict resolution.</h2><p>Each lab adds one step. Check repository status and history often to see what Git has recorded and where your current work belongs.</p></div><ol class="path-list"><li><span>01</span>Create and manage a local repository</li><li><span>02</span>Stage, commit, and inspect changes</li><li><span>03</span>Create branches and develop separate work</li><li><span>04</span>Merge changes and resolve a conflict</li></ol></section></main><footer class="home-footer"><a class="brand" href="index.html"><span class="brand-mark">G</span><span>CIS-1160 <b>Git Practice</b></span></a><span>Course practice tutorial · Suitable for classroom and independent use</span></footer><script src="assets/site.js"></script></body></html>'''
(ROOT/'index.html').write_text(index,encoding='utf-8')

print(f'Built {len(labs)} lab pages and overview.')
