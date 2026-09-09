# Mechanism-point review (Bob only)

**Object:** [`REVIEW.pdf`](REVIEW.pdf), built from [`REVIEW.md`](REVIEW.md) by [`scripts/69_hogan_mechanism_review_pdf.py`](../../../scripts/69_hogan_mechanism_review_pdf.py).

**Audience:** Bob. **Not for Hogan.** He asked for bullets, then for DOIs. Do not send this PDF, and do not paste it into the live manuscript.

Opens with a one-page conversation map (keep / drop / refuse). Each of the seven points starts with a discussion card, then 500–1000 words of evidence. Figures are original schematics, the public HKO annual table already in git, or count ratios copied from live Table 2 / Table 3. Captions state the discussion point in plain English. No new health model. Gate 3 remains a human decision.

Rebuild:

```bash
python3 scripts/69_hogan_mechanism_review_pdf.py
```

`REVIEW.html` is generated and is not the sendable object.
