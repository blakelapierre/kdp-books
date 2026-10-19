"""Builds the word lists for Window Seat Codewords.
fill.txt   : friendly, common American-English words the grid filler may use (ENABLE dictionary words that are
             also common in wordfreq; no proper nouns, no British spellings, nothing violent or rude).
verify.txt : the full ENABLE word list (172,823 words). The uniqueness checks use this much bigger list, so a
             puzzle only counts as unique if no other answer exists even with obscure dictionary words.
Run from src/: python3 words.py"""
import os, re
from wordfreq import zipf_frequency
HERE = os.path.dirname(os.path.abspath(__file__))
enable = [w.strip() for w in open(os.path.join(HERE, "enable1.txt")) if w.strip()]
E = set(enable)
bad = set(w.strip().lower() for w in open(os.path.join(HERE, "badwords.txt")) if w.strip())
VIOLENT = """kill kills killed killer killers killing murder murders murdered murderer dead deadly death deaths die died dies dying
gun guns gunman gunfire gunshot shoot shoots shooting shot shots knife knives stab stabs stabbed blood bloody bleed bleeding bomb bombs bombed
war wars warfare weapon weapons rifle rifles bullet bullets slay slain gore gory corpse corpses grave graves coffin poison poisoned
hang hanged hanging assault attack attacks attacked fight fights fighting fought punch punched beat beaten battle battles sword swords
army armies soldier soldiers troops enemy enemies torture victim victims crime crimes criminal prison jail arrest arrested police cop cops
drug drugs cocaine heroin beer booze drunk vodka whiskey wine wines liquor rum gin cigar cigars cigarette smoke smoking tobacco
suicide wound wounded injury injured hurt pain cancer disease sick ill hell damn devil demon evil sin sins nazi hate hated hates
rape abuse cruel violent violence terror terrorist threat threats destroy destroyed riot riots fire fired explode explosion missile tank
hunt hunter hunting trap trapped prey cage slave slaves slavery ghost ghosts witch witches zombie skull skeleton bury buried tomb
sex sexy nude naked kiss kissing breast breasts lust bra bikini divorce widow widowed orphan funeral mourn mourning grief bitter
vengeance revenge ninja ninjas sniper raid raids bandit bandits pirate pirates thief thieves steal stole stolen rob robbed robbery hostage
gay fat ugly stupid idiot dumb fool moron crazy insane lunatic ass butt pee poop vomit puke spit toilet bum hoe""".split()
VIOLENT = set(VIOLENT)
SUB = ["kill", "murd", "blood", "bomb", "slaught", "corps", "suicid", "rape", "sex", "nazi", "terror", "weapon", "porn", "shit", "fuck", "damn", "bitch", "cunt", "dick", "cock", "piss", "whor", "slut", "nigg", "fag", "dyke", "tits", "boob", "anal", "anus", "penis", "vagin", "erot", "drunk", "dead", "gun", "stab"]
BRIT = set("""grey greys colour colours favour favours flavour flavours honour honours labour harbour harbours humour neighbour neighbours
rumour rumours odour vapour parlour parlours armour centre centres theatre theatres metre metres litre litres fibre calibre sombre
cheque cheques tyre tyres kerb kerbs programme programmes catalogue jewellery travelled travelling cancelled cancelling modelled
labelled fuelled marvellous woollen plough ploughs aluminium mum mums pyjamas manoeuvre storey storeys sceptic analyse paralyse
organise organised realise realised recognise apologise favourite favourites defence offence licence pretence""".split())


# proper nouns: words that the American hunspell dictionary (en_US.dic) lists only with a capital letter
_lower, _cap = set(), set()
for _l in open(os.path.join(HERE, "en_US.dic"), encoding="utf-8", errors="ignore"):
    _w = _l.split("/")[0].strip()
    if not _w.isalpha(): continue
    (_cap if _w[0].isupper() else _lower).add(_w.lower())
PROPER = _cap - _lower
ODD = set("""ain als ami bel bey bis cis col cor cos dis dom eff ems eta fil git hah heh hes hmm hon jin jun kat ken lac las lex lib mas mil mis mos nah nos obi ole ons ops pas pax pol rec reg res sec sen ser sha sic sim sri tae tel tho til tis umm var vis wat wen wha yah yeh yea yin roc raj taj pic dev bro god gods ale ales mead rum arse fart farts pimp thug thugs ammo dirk imam shri shes mina lulu baba gaga geez jeez ling ting lama raja amir jock jocks cosy japan swede swedes dutch""".split())


def ok_shape(w):
    return re.fullmatch(r"[a-z]+", w) is not None


def is_brit(w):
    if w in BRIT: return True
    if w.endswith("our") and len(w) >= 5 and w[:-3] + "or" in E: return True
    if w.endswith("ours") and len(w) >= 6 and w[:-4] + "ors" in E: return True
    for a, b in (("ise", "ize"), ("ised", "ized"), ("ises", "izes"), ("ising", "izing"), ("isation", "ization"), ("yse", "yze")):
        if w.endswith(a) and len(w) > len(a) + 2 and w[:-len(a)] + b in E: return True
    if w.endswith("re") and len(w) >= 5 and w[:-2] + "er" in E and zipf_frequency(w[:-2] + "er", "en") > zipf_frequency(w, "en") and zipf_frequency(w[:-2] + "er", "en") > 3.5: return True
    if "ll" in w and (w.endswith("lled") or w.endswith("lling") or w.endswith("ller")):
        alt = w.replace("lled", "led").replace("lling", "ling").replace("ller", "ler")
        if alt in E and zipf_frequency(alt, "en") >= zipf_frequency(w, "en"): return True
    return False


def clean(w):
    if w in bad or w in VIOLENT: return False
    if any(s in w for s in SUB): return False
    return True


def build(minz=3.3, minlen=3, maxlen=11):
    out = []
    for w in enable:
        if not (minlen <= len(w) <= maxlen) or not ok_shape(w): continue
        z = zipf_frequency(w, "en")
        if z < minz: continue
        if not clean(w) or is_brit(w) or w in PROPER or w in ODD: continue
        out.append((w, z))
    return out


if __name__ == "__main__":
    fill = build()
    open(os.path.join(HERE, "fill.txt"), "w").write("\n".join(f"{w}\t{z:.2f}" for w, z in fill) + "\n")
    print("fill words", len(fill))
    from collections import Counter
    print(sorted(Counter(len(w) for w, _ in fill).items()))
