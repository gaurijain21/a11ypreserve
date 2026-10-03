# Automated accessibility/AT proxy decision

## Decision

**No proxy added.** This limitation is **NOT NECESSARY TO RESOLVE** for the
paper's primary machine-verifiable semantic-preservation claim.

## Assessment

The available Windows Narrator executable and installed Adobe Acrobat do not
provide a stable, scriptable accessibility-tree extraction interface in the
current environment. Acrobat could provide a destination-side checker, but
that would answer a different question from source-to-destination preservation
and would add a proprietary, environment-dependent measurement path. Browser
or Windows UI Automation would expose the viewer application's accessibility
surface, not a reproducible PDF semantic oracle.

No screen-reader process was launched, no user interaction was simulated, and
no auxiliary result was added. The paper therefore continues to state that
structural semantic preservation does not establish equivalent end-user
accessibility or usability.
