# Build scripts

These rebuild every marketing image and PDF from the books' own `<prefix>-interior.pdf` and `<prefix>-cover.pdf` (the `pdf` prefix for each book is set in `common.py`, e.g. `frostwood-01-the-thief-stayed-the-night`). They use poppler's `pdftoppm`, Pillow, reportlab and pypdf.

```bash
cd marketing/src
python3 build_aplus.py     # a-plus/<book>/*.png and a-plus/comparison-chart/*.png
python3 build_pins.py      # social/pinterest/*.png (1000 x 1500)
python3 build_samples.py   # social/samples/<prefix>-sample.pdf (US Letter), needs pypdf
```

- `common.py`: book list, house palette and fonts, and page rendering and cropping helpers
- `content.py`: per-book copy, crop boxes and pin text
