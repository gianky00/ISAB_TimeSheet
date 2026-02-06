from dataclasses import dataclass, field
from typing import Callable, List, Optional

from src.core.constants import Icons


@dataclass
class CommandNode:
    """
    Rappresenta un nodo nell'albero dei comandi della Palette.
    Può essere una foglia (azione) o un ramo (menu).
    """

    label: str
    description: str = ""
    icon: str = Icons.INFO  # Default icon
    shortcut: str = ""

    # Se definito, questo nodo è un'azione eseguibile
    action: Optional[Callable] = None

    # Se definito, questo nodo è un menu con figli statici
    children: List["CommandNode"] = field(default_factory=list)

    # Se definito, questo nodo genera i figli dinamicamente
    # (es. lista file, lista account) al momento dell'apertura
    dynamic_provider: Optional[Callable[[], List["CommandNode"]]] = None

    # Se True, la palette si chiude dopo l'azione.
    # Se False, rimane aperta (utile per toggle rapidi).
    close_on_execute: bool = True

    # --- INPUT MODE EXTENSION ---
    # Lista di prompt per richiedere input sequenziali (es. ["Inserisci OdA", "Inserisci Pos"])
    input_prompts: List[str] = field(default_factory=list)

    # Callback eseguita al termine degli input. Riceve una lista di valori str.
    on_input_complete: Optional[Callable[[List[str]], None]] = None

    @property
    def is_leaf(self) -> bool:
        """Ritorna True se è un nodo finale eseguibile (azione o input)."""
        return self.action is not None or bool(self.input_prompts)

    def get_children(self) -> List["CommandNode"]:
        """Recupera i figli, gestendo anche i provider dinamici."""
        if self.dynamic_provider:
            return self.dynamic_provider()
        return self.children


class CommandRegistry:
    """
    Singleton per definire e recuperare l'albero dei comandi.
    """

    _instance = None
    _root: Optional["CommandNode"] = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = CommandRegistry()
        return cls._instance

    def __init__(self):
        self._root = CommandNode("ROOT", children=[])

    def register_root(self, node: CommandNode):
        if self._root:
            self._root.children.append(node)

    def get_root_nodes(self) -> List[CommandNode]:
        return self._root.children if self._root else []
