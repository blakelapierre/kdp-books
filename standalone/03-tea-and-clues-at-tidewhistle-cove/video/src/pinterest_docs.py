"""Write pinterest/pins.csv and pins.md from the case list. Run from video/."""
import csv, glob, os, sys
sys.path.insert(0, "src"); from pinterest_pins import CASES
LINK = "AMAZON_URL_TBD"  # book not yet on Amazon; replace with https://www.amazon.com/dp/<ASIN>
BOARD = {1:"Cozy Mystery Puzzles",2:"Logic Puzzles for Kids",3:"Whodunit Riddles",4:"Cozy Mystery Puzzles",5:"Logic Puzzles for Kids",
         6:"Whodunit Riddles",7:"Cozy Mystery Puzzles",8:"Logic Puzzles for Kids",9:"Whodunit Riddles",10:"Cozy Mystery Puzzles"}
TEASE = {
1:"The Summer Show's best sponge has vanished from under its glass dome, and only a number card was left behind.",
2:"On the hottest afternoon of the summer, a silver locket disappears from a kitchen windowsill during a garden party.",
3:"A signed first edition vanishes from a seaside bookshop during a sudden summer downpour.",
4:"A brass ship's compass goes missing from the harbour office while the tide comes in.",
5:"Hedley's prize marrow has disappeared overnight. Four people, four statements, and one of them is a fib.",
6:"A hand-knitted puffin blanket vanishes on a quiet Sunday morning, and someone says they bought it at the post office.",
7:"The finest garden gnome in the Cove is gone, and the dog who barks at everyone never made a sound.",
8:"Twelve cinnamon buns vanish from the bakery's back door. Four suspects, and only one is telling the truth.",
9:"A watercolour disappears from its easel, and a visiting painter has a lovely story about the sunset.",
10:"The harbour benches have just been painted, and the lifeboat collection box is missing.",
}
KW = "cozy mystery puzzle, logic puzzle for kids, whodunit riddle, brain teaser, mystery riddles, can you solve it, family puzzles, Tea and Clues at Tidewhistle Cove"
rows, md = [], ["# Pinterest pins: Tea and Clues at Tidewhistle Cove (Cases 1-10)\n",
 f"Link for every pin: `{LINK}` (placeholder; the book is not on Amazon yet. Replace before posting.)\n",
 "Slots are relative to when the account is ready: T = first post. One case every 6 hours; the image pin goes up at the slot and the video pin 3 hours later.\n"]
for n,(slug,name,hook,*_ ) in CASES.items():
    img = f"images/pin-case-{n:02d}-{slug}.png"
    vid = os.path.basename([v for v in glob.glob(f"shorts/*case-{n:02d}-*short-part1.mp4") if "color" not in v][0])
    obj = hook[len("Who took the "):-1] if hook.startswith("Who took the ") else "it"
    t_img = f"Can You Solve It? Who Took the {obj.title()}? Cozy Mystery Puzzle | Case {n}"
    t_vid = f"Whodunit Riddle for Kids & Adults: {name} | Cozy Mystery Logic Puzzle"
    desc = (f"{TEASE[n]} Read Agnes's notebook clues and see if you can work out who did it. A gentle, cozy whodunit riddle "
            f"and logic puzzle for kids, families and grown-up mystery fans. No spoilers here: the answer is in the book. "
            f"Find 30 cozy mini-mysteries in Tea and Clues at Tidewhistle Cove. Tap to read the book!")
    alt_i = (f"Black-and-white ink illustration pin for Case {n}, {name}: the heading reads 'Can you solve it? {hook}', "
             f"with a scene from Tidewhistle Cove and Agnes's notebook listing three clues.")
    alt_v = f"Short animated cozy mystery video for Case {n}, {name}: the story and clues are read aloud, ending before the answer."
    for kind,t,media,thumb,alt,slot in (("Image",t_img,img,"",alt_i,f"T+{6*(n-1)}h"),("Video",t_vid,f"../shorts/{vid}",img,alt_v,f"T+{6*(n-1)+3}h")):
        assert len(t)<=100 and len(desc)<=500, (n,len(t),len(desc))
        rows.append({"Title":t,"Media URL":media,"Pinterest board":BOARD[n],"Thumbnail":thumb,"Description":desc,
                     "Link":LINK,"Publish date":slot,"Keywords":KW})
        md.append(f"## Case {n} {kind} pin ({slot})\n- **Title** ({len(t)} chars): {t}\n- **Media**: `{media}`" + (f" (cover/thumbnail: `{thumb}`)" if thumb else "") +
                  f"\n- **Board**: {BOARD[n]}\n- **Link**: {LINK}\n- **Alt text**: {alt}\n- **Description** ({len(desc)} chars): {desc}\n")
with open("pinterest/pins.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
open("pinterest/pins.md","w").write("\n".join(md)); print(len(rows),"pins")
