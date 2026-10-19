# V5 temporal repeatability

## Status: partially complete; cloud temporal replication remains open

V4 established same-condition repeatability for six difficult variants with
three runs per pipeline: classification stability and normalized semantic
stability were 6/6 for LibreOffice, Google Docs, and supplementary Word;
byte identity was 0/6, 6/6, and 0/6 respectively. Those are same-session or
same-recorded-workflow repetitions, not time-separated cloud sessions.

The V5 protocol adds a required temporal Google arm with at least two
separated sessions, recording date, browser build, producer, workflow,
source/output hashes, normalized semantics, and classifications. No such new
authenticated session was available in the present automated run, so no
temporal stability claim is fabricated. The limitation is open and does not
alter the frozen V4 repeatability result.
