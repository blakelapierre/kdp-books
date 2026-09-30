"""Master guest list for Frostwood Lodge: every guest has ONE fixed room, home, job and arrival day
for the whole book, so the same people reappear consistently from case to case."""
import random
FIRST = """Agatha Bernard Clara Desmond Eleanor Felix Greta Harold Iris Jasper Kitty Leopold Mabel Nigel Olive Percy
Queenie Rupert Sylvia Theo Ursula Victor Winnie Xavier Yvonne Zachary Beatrice Dorothy Edmund Florence Gilbert Hazel
Ivor June Kenneth Lillian Monty Nora Oscar Pearl Ralph Rosalind Stanley Tabitha Vera Walter Wilhelmina Arthur Constance
Douglas Estelle Frederick Gwendolyn Horace Imogen Lionel Marigold Otis Posy Albert Blanche Cecil Daphne Ernest Fern
Godfrey Harriet Ignatius Josephine Lavinia Maude Neville Ophelia Phineas Rhoda Silas Thea Una Vivian Wallace Adele
Basil Cordelia Duncan Edith Fergus Gideon Hattie Isadora Jonah Lottie Milo Nell Orla Piers Ruby Sebastian Tilly Ulric
Violet Wendell Alma Bertram Cressida Dexter Elsie Flora Gordon Honor Ida Jude Kit Linus Minnie Ned Opal Quentin Reggie
Sadie Toby Verity Wilfred Ada Barnaby Cora Dudley Effie Frank Gertie Hugo Ines Juno Lloyd Mavis Noel Odette Primrose
Roland Selma Tristan Viola Wynn Amos Birdie Clement Delphine Enid Fitz Gracie Humphrey Ivy Jem Lark Magnus""".split()
LAST = """Abernathy Blackwood Carrington Dunmore Ellsworth Fairweather Gallagher Hawthorne Ingram Jolliffe Kettering
Lockhart Merriweather Oakley Pennington Quimby Radcliffe Sterling Thistlewood Underhill Whitlock Yardley Ashby
Bramble Crumb Drummond Ember Finch Goodfellow Honeycutt Ivers Juniper Kingsley Larkspur Mulberry Norwood Oxley
Pickering Quill Rowntree Snowden Tuttle Upton Vickers Wren Young Zeller Parsley Tanner Wetherby Appleby Birch
Cobbold Dimsdale Everley Fenwick Greaves Hollis Iveson Jessop Kemble Loxley Marchbanks Nettles Orchard Pilbeam
Rushworth Starling Trelawney Umber Varley Winterbottom Aldridge Bellweather Chalk Dewberry Elphick Frost Gosling
Hargreaves Inchbald Jarvis Knightley Lumley Mottram Nuttall Ogilvy Peabody Ravenscroft Summerby Tregarth Valentine
Woolley Yelland Brightwell Cheeseman Foxley Hazelwood Merritt Pryce Sallow Tolliver""".split()
COLD = ["Anchorage","Boston","Buffalo","Chicago","Denver","Milwaukee","Minneapolis","Montreal","Quebec City","Toronto"]
WARM = ["Honolulu","Los Angeles","Miami","Phoenix","San Diego","Tampa"]
CITIES = sorted(COLD+WARM)
OCC = ["Accountant","Architect","Baker","Beekeeper","Botanist","Chef","Dentist","Doctor","Engineer","Florist",
       "Journalist","Lawyer","Librarian","Novelist","Nurse","Painter","Photographer","Pilot","Tailor","Teacher","Violinist"]
DAYS = ["Friday","Saturday","Sunday"]

def build(seed=20260930):
    r = random.Random(seed)
    firsts = [f for f in dict.fromkeys(FIRST) if f != "Cyril"]
    r.shuffle(firsts)
    lasts = [l for l in dict.fromkeys(LAST) if l != "Nightingale"]
    r.shuffle(lasts)
    rooms = [f*100+n for f in range(1,6) for n in range(1,21)]
    rooms.remove(216)                     # Cyril Nightingale's room (from the sample)
    r.shuffle(rooms)
    # 90 occupied rooms: 1 fixed (Cyril) + 39 single + 38 double + 12 triple = 152 guests; 10 rooms empty
    sizes = [1]*39 + [2]*38 + [3]*12
    r.shuffle(sizes)
    guests = [dict(first="Cyril", last="Nightingale", room=216, home="Honolulu", occ="Florist", arr="Saturday")]
    fi = 0
    for i, size in enumerate(sizes):
        room = rooms[i]
        family = size == 3 or r.random() < 0.75
        home = r.choice(COLD*2 + WARM*2)
        arr = r.choice(DAYS)
        sur = lasts.pop()
        for k in range(size):
            last = sur if (family or k == 0) else lasts.pop()
            occ = "Student" if (size == 3 and k == 2) else r.choice(OCC)
            guests.append(dict(first=firsts[fi], last=last, room=room, home=home, occ=occ, arr=arr))
            fi += 1
    # patch: one 5th-floor, even-numbered double room of Saturday arrivals from Tampa (keeps Case 3's
    # final clue meaningful: they satisfy every other Case 3 clue except the last two)
    from collections import Counter
    cnt = Counter(g["room"] for g in guests)
    room = min(rm for rm, k in cnt.items() if rm // 100 == 5 and rm % 2 == 0 and k == 2)
    for g in guests:
        if g["room"] == room:
            g.update(home="Tampa", arr="Saturday", last="Tolliver")
            if g["occ"] in ("Doctor", "Nurse"): g["occ"] = "Architect"
    for g in guests:
        g["floor"] = g["room"]//100; g["num"] = g["room"] % 100
        g["name"] = f"{g['first']} {g['last']}"
    assert len({g["name"] for g in guests}) == len(guests) == 152
    assert len({g["first"] for g in guests}) == 152
    guests.sort(key=lambda g: (g["last"], g["first"]))
    return guests

if __name__ == "__main__":
    G = build(); print(len(G), len({g['room'] for g in G}), len(FIRST), len(set(FIRST)), len(LAST))
