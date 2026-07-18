import importlib
import inspect
import pkgutil
import plugins


def load_all_plugins():
    """
    Scans the 'plugins' package, imports every module inside it,
    and collects all functions found in those modules.

    Returns a list of functions that can be handed to Gemini as tools.
    """
    tools = []

    # Go through every .py file inside the plugins folder
    for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
        if module_name == "loader":
            continue  # Don't load this file itself as a plugin

        module = importlib.import_module(f"plugins.{module_name}")

        # Grab every function defined in that file
        for _, func in inspect.getmembers(module, inspect.isfunction):
            tools.append(func)

    return tools