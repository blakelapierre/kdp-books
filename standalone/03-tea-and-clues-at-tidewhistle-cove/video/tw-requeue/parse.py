import re,json
V='/workspace/kdp-books/standalone/03-tea-and-clues-at-tidewhistle-cove/video/'
L=open(V+'publish-log.md').read().split('\n')
yt={};tt={}  # id -> (case,slot,colourflag)
cur=None;plat=None;col=False
for ln in L:
    m=re.match(r'#+ .*?Cases? (\d+)(?:–(\d+))?.*?(YouTube|TikTok)',ln)
    if m: cur=int(m.group(1)); plat=m.group(3); col='olour' in ln
    m2=re.match(r'- Case (\d+)\b',ln)
    if m2 and 'https' not in ln: cur=int(m2.group(1)); col='olour' in ln
    if m2 and ('P1 ' in ln and 'wide' in ln): 
        c=int(m2.group(1)); 
        for s,i in re.findall(r'\b(P1|P2|wide) ([\w-]{11})\b',ln): yt[i]=(c,s,'colour' in ln or c>=25)
    if ln.startswith('Public:') and plat=='YouTube':
        for s,i in re.findall(r'\b(P1|P2|wide) ([\w-]{11})\b',ln.split('B&W')[0]):
            if i not in yt: yt[i]=(cur,s,col or cur>=25 or cur<=9)
    for c,s,i in re.findall(r'(?:Case (\d+) )?(P1|P2) https://www.tiktok.com/\S+/video/(\d+)',ln):
        cc=int(c) if c else cur
        if m2 and not c: cc=int(m2.group(1))
        tt[i]=(cc,s,col or cc>=25 or cc<=9)
yt['3ZB_lLqt52s']=(7,'P2',True);yt['JR8bOE0_KbU']=(7,'wide',True)
json.dump({'yt':yt,'tt':tt},open('/workspace/tw-requeue/map.json','w'))
yd=open('/workspace/tw-requeue/yt_delete.txt').read().split()
td=[l.split('\t') for l in open('/workspace/tw-requeue/tt_delete.tsv').read().strip().split('\n')]
print('yt unmapped',[i for i in yd if i not in yt])
print('tt unmapped',[(r[0],r[2]) for r in td if r[0] not in tt])
print(len(yt),len(tt))
