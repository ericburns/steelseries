# steelseries

Design
------

I like to keep Views as simple as possible and push complexity on to Managers and Models. So, that's what I tried to do here.

One challenge of the database design is that the Tier data is on the Parent table. To make accessing only the rows with the current tiers easier, I created a custom Manager and QuerySet. Putting the code on the QuerySet allows us to adhere to DRY. We can reuse that code on the Manager, too, so we could chain the method calls.

(In this particular instance, since I had to use a Raw query, you would not be able to use a .filter on the results. But, on a Postgres stack, such as yours, you could. Django's ORM doesn't support distinct('field_name') for anything but Postgres. Since I'm using sqlite3, it wasn't as simple to use the ORM to solve the problem. On top of that, Django doesn't let you do straightforward Group By's. You have to use aggregation functions, which don't help much here. The result is a RawQuerySet instead of a QuerySet. But, I'd be able to do this same query with a Postgres backend using the ORM and return a QuerySet, making it chainable.)

I used Django's generic views, since they all seemed to work out here. It kept the code super short. I don't always get to use them, but I do when I can. I also prefer class based views over function based views when possible.

I didn't use a foreign key from the Parent's name to the Retailer's parent_name. Retailers had parents that didn't exist in the Parents table. In order to use the foreign key, I'd have to allow it to add those parents to the parent table or leave it null for those that don't exist. If I add data, I'd be changing the data. It seemed like the instructions hinted at this being against the rules. If I left it null, I'd have lost data about those retailers with parents not in the Parent table. I'll address this more in the DB bonus question.

A few concerns of mine: Retailers are repeated, but with/without periods in them. I went ahead and showed them here, but perhaps data cleanup is necessary? Also, there are Retailers that seem to have themselves listed as their parent. I don't know how that's interpreted. I took it to mean that a parent can also be a retailer and displayed it on the list of retailers. Those could be removed from being displayed by adding a RetailerManager that's base queryset excludes those rows where the name and parent_name are the same.

One restriction that I did impose was that updating a retailer's parent only allows you to choose from those in the Parent table, rather than all the parent options in the retailer table. I did this to prevent further disconnect from the tables. If you would want to add a parent that doesn't exist, you'd have to use a feature to add a new Parent first.

Bonus question
--------------
This is what I think I would have done.


Parent  | (i.e.)
------- | ------
id      | 1
name    | Comgame 576 Kft.
country | Hungary

Tier | (i.e.)
---- | ------
id   | 1
name | EUR Tier 1

Kickback | (i.e.)
-------- | ------
id       | 1
tier_id  | 1
start_date | 2013-05-01

Retailer | (i.e.)
-------- | ------
id       | 1
parent_id| 1
name     | Comgame 576 Kft.
country  | Hungary

If the Parent and Retailer are really just the same thing, like they are in this situation, you could get rid of the Parent table. Any Retailer with a parent_id, for example, has a parent.

Another thing I would want to do is clean up the data, so that there are not duplicates, retailers are not their own parents, and that there is an entry in the Parent table for each Retailer that references a Parent. That should be done to maintain the foreign key constraint on the Retailer.
