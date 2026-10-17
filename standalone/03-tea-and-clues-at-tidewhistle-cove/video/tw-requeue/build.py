import json,re,os,glob
V='/workspace/kdp-books/standalone/03-tea-and-clues-at-tidewhistle-cove/video/'
M=json.load(open('missing.json'))
BOOKS="""📚 More cozy puzzles by Blake La Pierre:
• Bridges of Frostwood (logic puzzles): https://www.amazon.com/dp/B0HN6JKQQV
• Porch Swing Crosswords: https://www.amazon.com/dp/B0HN6QXPFG
• Stories We Keep (memory keepsake gift): https://www.amazon.com/dp/B0HN6TSN7T
• The Advent Clock (24-door puzzle countdown): https://www.amazon.com/dp/B0HMW1MR5T"""
PL="More cases in the Tidewhistle Cove Mysteries playlist."
def text(c):
    s=open(V+f'shorts/case-{c:02d}-youtube.md').read()
    secs={}
    for key,pat in [('P1',r'## Part 1'),('P2',r'## Part 2'),('wide',r'## Wide')]:
        m=re.search(pat+r'.*?(?=\n## |\Z)',s,re.S)
        if not m: continue
        b=m.group(0)
        t=re.search(r'\*\*Title\*\*[^\n]*\n```\n(.*?)\n```',b,re.S)
        d=re.search(r'\*\*Description\*\*[^\n]*\n```\n(.*?)\n```',b,re.S)
        secs[key]=(t.group(1).strip() if t else None, d.group(1).strip() if d else None)
    return secs
def clean(d):
    paras=[p for p in d.split('\n\n') if not re.match(r'(Next up|Next case|New case every)',p.strip())]
    d='\n\n'.join(paras)
    d=re.sub(r' ?New case every 6 hours\.','',d)
    return d
def files(c,s):
    if s=='wide':
        g=glob.glob(V+f'standalone-03-tidewhistle-case-{c:02d}-*-color-wide.mp4') or ([] if 10<=c<=24 else [f for f in glob.glob(V+f'standalone-03-tidewhistle-case-{c:02d}-*-wide.mp4') if '-bw' not in f])
    else:
        n=s[1]
        g=glob.glob(V+f'shorts/standalone-03-tidewhistle-case-{c:02d}-*-color-short-part{n}.mp4') or ([] if 10<=c<=24 else glob.glob(V+f'shorts/standalone-03-tidewhistle-case-{c:02d}-*-short-part{n}.mp4'))
    return g[0] if g else None
miss=[]
def esc(x): return x.replace('\t',' ').replace('\n','\\n')
for plat in ['yt','tt']:
    order={'P1':0,'P2':1,'wide':2}
    rows=[]
    for c,s,_ in sorted(M[plat],key=lambda x:(x[0],order[x[1]])):
        f=files(c,s)
        if not f or not os.path.exists(f): miss.append((plat,c,s)); f='MISSING'
        t,d=text(c).get(s,(None,None))
        if not t: miss.append((plat,c,s,'no text'))
        suf=' (Colour)' if 10<=c<=24 else ''
        d=clean(d or '')
        if plat=='yt':
            title=t.replace(' #shorts','')+suf+(' #shorts' if s!='wide' else '')
            if len(title)>100: title=title.replace(' (Colour)','')
            d=re.sub(r'(#whodunit\b)',r'\1 #whodunitpuzzle',d,1) if '#whodunit ' in d or d.endswith('#whodunit') else d+'\n\n#whodunitpuzzle'
            d=d.replace('Pause before Part 2','A whodunit puzzle for you: pause before Part 2',1) if 'Pause before Part 2' in d else d
            rel='Related video -> this case Part 2 (live copy; fill in at post time)' if s=='P1' else ''
            desc=d+'\n\n'+PL+'\n\n'+BOOKS
            rows.append([c,s,f,title,desc,rel])
        else:
            title=t.replace(' #shorts','')+suf
            first=d.split('\n\n')[0]
            tags='#whodunitpuzzle #whodunit #cozymystery #mysterypuzzle #canyousolveit #brainteaser #fyp'
            cap=f"{title}\n\nA cozy whodunit puzzle from Tidewhistle Cove. {first if s=='P1' else 'Did you solve it?'}\n\n{'Pause and drop your guess in the comments! Answer in Part 2.' if s=='P1' else 'Part 1 is on our profile.'} More Tidewhistle Cove cases on our profile.\n\n{tags}"
            rows.append([c,s,f,title,cap])
    fn='queue-youtube.tsv' if plat=='yt' else 'queue-tiktok.tsv'
    with open(fn,'w') as o:
        hdr=['seq','case','part_type','file','title','description' if plat=='yt' else 'caption']+(['related_video_note'] if plat=='yt' else [])+['status','posted_id']
        o.write('\t'.join(hdr)+'\n')
        for i,r in enumerate(rows,1):
            o.write('\t'.join([str(i),str(r[0]),r[1]]+[esc(x) for x in r[2:]]+['pending',''])+'\n')
    print(fn,len(rows))
print('missing',miss)
