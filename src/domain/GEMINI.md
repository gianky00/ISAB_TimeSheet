# 🧠 DOMAIN LAYER - AI ARCHITECT GUIDELINES

Sei all'interno di `src/domain/`, il cuore pulsante e immutabile di ISAB TimeSheet.
Questo layer contiene la Logica di Business Enterprise.

## 🚨 REGOLE DEL LAYER (STRICT)
1. **ZERO DIPENDENZE ESTERNE:** È assolutamente vietato importare `PySide6`, librerie di database (SQLAlchemy/SQLite), `requests`, o framework di automazione web. Solo Python puro, `typing`, `datetime` e `pydantic`.
2. **ENTITÀ E VALUE OBJECTS:** Usa `pydantic.BaseModel` (preferibile per la validazione automatica) o `@dataclass` (con `slots=True` per le performance) per definire i dati.
3. **INVERSION OF CONTROL (IoC):** Qui dentro si definiscono le interfacce (`typing.Protocol`). Non implementarle qui! L'implementazione va in `src/infrastructure/`.
4. **TIPING SEMANTICO:** Sfrutta `Annotated` per aggiungere significato di business ai tipi (es. `Annotated[str, Field(pattern="^[A-Z0-9]{16}$")]` per Codice Fiscale).
5. **ECCEZIONI DI DOMINIO:** Crea gerarchie di eccezioni custom (es. `class DomainError(Exception)`) per rappresentare fallimenti di business comprensibili, mai errori generici.
