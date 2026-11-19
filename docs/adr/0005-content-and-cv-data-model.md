# ADR-0005: Content and CV data model

Status: accepted
Date: 2026-11-19

## Context
The public pages are written by hand as HTML. That works for four
pages, but it cannot produce a CV, and every change to a skill or a
project means editing markup. The plan is to keep the content in a
database, render the public pages from it, and generate a CV for a
chosen role from the same records.

Storing the content in one place creates a disclosure risk that
hand-written pages did not have. The same record may be fine on a CV
and wrong on the site, or the other way round. Unfinished entries, such
as a skill still being learned, must not appear anywhere by accident.
Contact details are the sharpest case: some are meant to be on a CV and
none should reach a page or a file unless they were deliberately marked.
The earlier wording of ZT-11 covered only contact details, so it does
not describe this wider risk.

The database starts on a free Render Postgres instance. That plan
expires 30 days after creation, has no backups and may restart at any
time, so the content cannot live only in the database. A durable
Postgres provider is the next step after the first version works.

## Consequences
One table per kind of item keeps the data clean and lets the database
enforce its own links, at the price of repeating the status and flag
columns in every table. The shared filter and the test over every table
exist to keep that repetition from becoming a gap.

New items are hidden until someone publishes them, so a mistake in the
content shows up as something missing and not as something exposed. The
same rule makes a role cheap to add: it is a row, and an item joins it
through its link table.

The seed file holds public content only, so a rebuilt database has no
private contact details. Until the admin pages exist, those values are
entered by hand and are lost when the free database is recreated. This
is acceptable while the CV export is not built, and it is one reason the
move to a durable provider comes next.

ZT-11 is reworded to cover every kind of item and both flags, and
threat T-10 and abuse case AC-09 are updated to match. The database
engine, the connection settings and the migration tool are decided in
the next item, and the content tables are created there.