"""Shared answer normalization for generator and independent verifier."""
import re, unicodedata

_ARTICLES = re.compile(r"^(a|an|the)\s+", re.I)
_PUNCT = re.compile(r"[^\w\s'-]", re.U)
_SPACE = re.compile(r"\s+")

def normalize(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s)).strip().lower()
    s = s.replace("'", "'").replace("'", "'").replace("–", "-").replace("—", "-")
    s = _PUNCT.sub(" ", s)
    s = _ARTICLES.sub("", s)
    s = _SPACE.sub(" ", s).strip()
    return s

def accept_forms(answer: str, extras=None):
    """Canonical answer plus common variants (with/without article, plural tweaks)."""
    forms = {normalize(answer)}
    raw = str(answer).strip()
    for a in ("a ", "an ", "the ", "A ", "An ", "The "):
        forms.add(normalize(a + raw))
        if raw.lower().startswith(a.lower()):
            forms.add(normalize(raw[len(a):]))
    if extras:
        for e in extras:
            forms.add(normalize(e))
    forms.discard("")
    return sorted(forms)
