from pkgutil import iter_modules
from importlib import util, import_module
from django.apps import apps

def get_actions_from_apps():
    actions = []

    for app in apps.get_app_configs():
        modentry = f"{app.name}.case_actions"

        spec = util.find_spec(modentry)

        if spec:
            for (_, name, _) in iter_modules(spec.submodule_search_locations):
                modname = f"{modentry}.{name}"
                mod = import_module(modname)

                cls = getattr(mod, 'Action')
                instance = cls()
                actions.append((modname, instance.name))

    return actions
