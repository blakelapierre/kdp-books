# Build scripts

These rebuild every marketing image and PDF from the books' own `interior.pdf` and `cover.pdf`. They use poppler's `pdftoppm`, Pillow, reportlab and pypdf.

```bash
cd marketing/src
python3 build_aplus.py     # a-plus/<book>/*.png and a-plus/comparison-chart/*.png
python3 build_pins.py      # social/pinterest/*.png (1000 x 1500)
python3 build_samples.py   # social/samples/*-sample.pdf (US Letter), needs pypdf
```

- `common.py`: book list, house palette and fonts, and page rendering and cropping helpers
- `content.py`: per-book copy, crop boxes and pin text
