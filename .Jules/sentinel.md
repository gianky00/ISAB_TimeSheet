## 2025-12-21 - Path Traversal in File Downloads
**Vulnerability:** A Path Traversal and File Overwrite vulnerability was identified in `ScaricaTSBot` and `DettagliOdABot`. The bots used unsanitized user input ("Numero OdA") to construct the destination filename for downloaded Excel files. This allowed a malicious input (e.g., `../../Important.xlsx`) to escape the download directory and overwrite arbitrary files on the system.

**Learning:** When automating file downloads based on user parameters, never assume the parameter is safe for use as a filename. Frameworks or libraries often don't sanitize paths automatically when you manually construct paths using `pathlib` or string formatting.

**Prevention:** Always sanitize any user input before using it in filesystem operations. Use a strict allowlist (e.g., alphanumeric only) for filenames. I implemented `src.utils.helpers.sanitize_filename` to enforce this across the application.

## 2025-12-21 - Plaintext Password Storage
**Vulnerability:** User credentials (ISAB Portal passwords) were stored in `config.json` in plaintext. This exposed credentials to any process or user with read access to the user's home directory configuration file.

**Learning:** Storing secrets in plaintext is a common convenience shortcut that becomes a significant liability. Even simple obfuscation or local encryption raises the bar significantly against automated malware or casual snooping.

**Prevention:** I implemented a `PasswordManager` that uses `cryptography.fernet` with a locally generated key (`~/.bot_ts/secret.key`) to encrypt passwords before saving them to disk. The application transparently handles decryption on load and encryption on save, maintaining backward compatibility with legacy plaintext configs.
