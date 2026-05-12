from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class CommandNode:
    """
    Rappresenta un nodo nell'albero dei comandi della Palette.
    Pu  essere una foglia (azione) o un ramo (menu).
    """

    label: str
    description: str = ""
    icon: str = "info"  # Default icon string
    shortcut: str = ""

    # Se definito, questo nodo  un'azione eseguibile
    action: Callable[[], Any] | None = None

    # Se definito, questo nodo  un menu con figli statici
    children: list["CommandNode"] = field(default_factory=list)

    # Se definito, questo nodo genera i figli dinamicamente
    # (es. lista file, lista account) al momento dell'apertura
    dynamic_provider: Callable[[], list["CommandNode"]] | None = None

    # Se True, la palette si chiude dopo l'azione.
    # Se False, rimane aperta (utile per toggle rapidi).
    close_on_execute: bool = True

    # --- INPUT MODE EXTENSION ---
    # Lista di prompt per richiedere input sequenziali (es. ["Inserisci OdA", "Inserisci Pos"])
    input_prompts: list[str] = field(default_factory=list)

    # Callback eseguita al termine degli input. Riceve una lista di valori str.
    on_input_complete: Callable[[list[str]], None] | None = None

    @property
    def is_leaf(self) -> bool:
        """Ritorna True se  un nodo finale eseguibile (azione o input)."""
        return self.action is not None or bool(self.input_prompts)

    def get_children(self) -> list["CommandNode"]:
        """Recupera i figli, gestendo anche i provider dinamici."""
        if self.dynamic_provider:
            return self.dynamic_provider()
        return self.children


class CommandRegistry:
    """
    Singleton per definire e recuperare l'albero dei comandi.
    """

    _instance: Optional["CommandRegistry"] = None
    _root: Optional["CommandNode"] = None

    @classmethod
    def instance(cls) -> "CommandRegistry":
        """Restituisce l'istanza singleton del registro comandi."""
        if cls._instance is None:
            cls._instance = CommandRegistry()
        return cls._instance

    def __init__(self) -> None:
        """Inizializza il registro con un nodo ROOT."""
        self._root = CommandNode("ROOT", children=[])

    def register_root(self, node: CommandNode) -> None:
        """Aggiunge un nodo alla radice dell'albero dei comandi."""
        if self._root:
            self._root.children.append(node)

    def get_root_nodes(self) -> list[CommandNode]:
        """Restituisce la lista dei nodi principali registrati."""
        return self._root.children if self._root else []
