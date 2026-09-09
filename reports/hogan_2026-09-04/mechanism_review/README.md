# Mechanism discussion brief (Bob only)

**Object:** [`REVIEW.pdf`](REVIEW.pdf), built from [`REVIEW.md`](REVIEW.md) by [`scripts/69_hogan_mechanism_review_pdf.py`](../../../scripts/69_hogan_mechanism_review_pdf.py).

**Audience:** Bob. **Not for Hogan.** He asked for bullets, then for DOIs. Do not send this PDF, and do not paste it into the live manuscript.

Page 1 is the conversation: what is on the table, keep / drop / no, which paper. Each cited paper is then about 200 words under four headings: the question, what they found, what our file has, what we do. Three refusals that are not papers sit at the end (indoor temperature, five-as-spell, warning evaluation). Figures are original schematics or the public HKO annual table already in git. No new health model. Gate 3 remains a human decision.

Rebuild:

```bash
python3 scripts/69_hogan_mechanism_review_pdf.py
```

`REVIEW.html` is generated and is not the sendable object.
