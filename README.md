# Django Postgres access control (DPAC)

DPAC provides very **granular row and column level role based access control** for your Django & Postgres applications.
In a nutshell, DPAC enable you to utilize the vast access control capabilities already built into PostgreSQL in a way which also feels comfortable from the Django side.

## What problem does it solve

Django has a built-in users and groups management system as part of the `django.contrib.auth` package.
However, there is no built-in solution for enforcing a rule such as "Users belonging into the `librerian` group can see the titles and ISBN codes of books in the library they are working for." There is not even a way to enforce the simpler rule "All users can see their own orders."

Of course you can write complex filtering functions in your views, but there is no way to enforce the same rules all across the application. And by to burdon yourself with enforcing the rules in an imperative way, if declerative rules are much easier to understand and maitain?

## How it works under to hood

PostgreSQL ships with a highly sophisticated set of access control features including both the standard SQL options like `GRANT` statements as well as its own additions like row level security.

The problem is that Django does not provide a convenient way to leverage these features. So you are faced with a hard dilemma: to give up the Django models and write custom SQL queries or to be cut off the valuable tools your database could offer you. And even if you would be all but happy with writting all SQL queryes by hand, most likly your co-workers could not keep up with you.

DPAC provides a bridge between Postgres And Django.

Both Postgres and Django think in terms of users and groups (or 'roles' in Postgres). However, for both of them the same terms means different things. For Django, its user is an instance of the `User` (`AUTH_USER_MODEL` to be precise) class, but for Postgres it is just a regular row in a regular table. The same goes with groups. A Postgres cluster might have many users belonging to multiple roles, but Django only has one user hardcoded into its settings and since it executes all the queries in the right of the same user, it does not benefit from what the database has to offer.

## Project status

DPAC is currently under active develpment and has not reached a stable version 1.0 yet.

