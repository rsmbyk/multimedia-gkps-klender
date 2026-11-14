from multimedia import retirement

# spec 194 — the three old docks and four old sources answer 302 to the live
# surface: docks to /obs/dock, sources to /obs/blank. This URLconf is the
# retirement alone; next release it and multimedia/retirement.py are deleted
# together, while the package's static and template files go with them.
urlpatterns = retirement.routes('obs')
