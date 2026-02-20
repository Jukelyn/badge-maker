"""Exploration and testing"""
# import time
from simplepycons import all_icons
# from simplepycons import _ICONS

lookup = all_icons.names()

# start = time.perf_counter()
# for icon in lookup:
#     _ = icon
# t1 = time.perf_counter() - start

# start = time.perf_counter()
# get_icon = _ICONS.__getitem__
# for icon in lookup:
#     _ = get_icon(icon)
# t2 = time.perf_counter() - start

# start = time.perf_counter()
# for icon in lookup:
#     factory = _ICONS.__dict__[f"get_{icon}_icon"]
#     _ = factory()
# t3 = time.perf_counter() - start

# start = time.perf_counter()
# for icon in lookup:
#     _ = all_icons[icon]

# t4 = time.perf_counter() - start

# start = time.perf_counter()

for icon in lookup:
    factory = all_icons.__dict__[f"get_{icon}_icon"]
    print(type(factory))
    print(factory)
    a = factory()
    print(type(a))
    print(a.name)
    print(a.__class__.mro())

# t5 = time.perf_counter() - start

# start = time.perf_counter()
# for icon in lookup:
#     _ = all_icons[icon]

# t6 = time.perf_counter() - start

# print(t1, t2, t3, t4, t5, t6)

# t1 7.958299829624593e-05
# t2 0.0013147089921403676
# t3 0.0006947089859750122
# t4 0.0012531249958556145
# t5 0.0006690410082228482
# t6 0.001229582994710654
# Fastest lookup is using all_icons.__dict__[f"get_{icon}_icon"]
# all_icons == _ICONS True but using all_icons.__dict__[f"get_{icon}_icon"] is
# just a tiny bit faster. Just using all_icons[icon] is about twice as slow but
# not that slow so it might be the better option due to readability.
