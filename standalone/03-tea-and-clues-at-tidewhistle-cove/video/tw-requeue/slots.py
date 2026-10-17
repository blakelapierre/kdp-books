import json,re
m=json.load(open('map.json'));yt={k:tuple(v) for k,v in m['yt'].items()};tt={k:tuple(v) for k,v in m['tt'].items()}
for ln in open('/workspace/kdp-books/marketing/youtube-history.md'):
    r=re.match(r'\| C(\d+)\b([^|]*)\|([^|]*)\|',ln)
    if not r: continue
    c=int(r.group(1));lab=r.group(2);ids=[x.strip() for x in r.group(3).split('/')]
    parts=['P1','P2'] if 'P1 / P2' in lab else (['P1'] if 'P1' in lab else ['P2'] if 'P2' in lab else [])
    if len(parts)!=len(ids): continue
    for p,i in zip(parts,ids):
        d=tt if i.isdigit() else yt
        d.setdefault(i,(c,p,True))
yd=set(open('yt_delete.txt').read().split())
td=set(l.split('\t')[0] for l in open('tt_delete.tsv').read().strip().split('\n'))
print('unmapped yt',[i for i in yd if i not in yt],'tt',[i for i in td if i not in tt])
def miss(d,dl,slots):
    out=[]
    for c in range(1,31):
        for s in slots:
            allc=[i for i,v in d.items() if v[0]==c and v[1]==s]
            surv=[i for i in allc if i not in dl]
            if not surv: out.append((c,s,allc))
            elif c<=9 and not allc: pass
    return out
ym=miss(yt,yd,['P1','P2','wide']); tm=miss(tt,td,['P1','P2'])
# cases 1-9: slots with no known ids at all assumed surviving
ym=[x for x in ym if x[2]]; tm=[x for x in tm if x[2]]
print(len(ym),[(c,s) for c,s,_ in ym]);print(len(tm),[(c,s) for c,s,_ in tm])
json.dump({'yt':ym,'tt':tm},open('missing.json','w'))
