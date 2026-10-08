# TP : School hall reservation API

Author : Enow Eweh Mac Brenda

## Installation

python manage.py migrate
python manage.py seed
python manage.py runserver


## Endpoints

- /api/salles/ : GET and POST (write restricted to admin)
- /api/salles/{id}/ : GET, PUT, PATCH, DELETE (write restricted to admin)
- /api/reservations/ : GET and POST (create by an authenticated user)
- /api/reservations/{id}/ : GET, PUT, PATCH, DELETE (edit by the author only)
- /api/salles/{id}/occupation/?debut=...&fin=... : occupancy rate of the room (ISO 8601 format)

## Notes

Overlap : two reservations overlap if one of them starts before the end of the other
and ends after its start. Cancelled reservations don't count. For the occupancy rate
we only count the part of the reservations that is inside the requested period.