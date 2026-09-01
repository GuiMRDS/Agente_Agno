import pkgutil
import agno

for m in pkgutil.walk_packages(
    agno.__path__,
    agno.__name__ + "."
):
    if "embed" in m.name.lower():
        print(m.name)