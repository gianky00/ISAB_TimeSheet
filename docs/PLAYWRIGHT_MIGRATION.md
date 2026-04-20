# Migrazione Selenium -> Playwright [AVVIO]

## Obiettivo
Migrare l'intera infrastruttura di automazione da Selenium a Playwright per migliorare affidabilità, velocità e manutenibilità.

## Piano di Migrazione

### 1. Infrastruttura Base
- [ ] Creazione di `PlaywrightBaseBot` in `src/bots/base/playwright_base_bot.py`.
- [ ] Implementazione del sistema di segnali compatibile con la GUI attuale.
- [ ] Gestione del ciclo di vita (Browser, Context, Page).

### 2. Mapping Comandi (Selenium vs Playwright)

| Selenium | Playwright (Sync API) | Note |
| :--- | :--- | :--- |
| `driver.find_element(By.ID, "id")` | `page.locator("#id")` | Playwright usa i selettori CSS/XPath direttamente. |
| `WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))` | `page.wait_for_selector(selector)` | Playwright ha l'auto-waiting integrato. |
| `element.click()` | `page.click(selector)` o `locator.click()` | Include controlli di visibilità e cliccabilità. |
| `element.send_keys("text")` | `page.fill(selector, "text")` | Più affidabile per i form. |
| `driver.execute_script("js")` | `page.evaluate("js")` | |
| `ActionChains(driver).move_to_element(el).click().perform()` | `page.hover(selector)` + `page.click(selector)` | |
| `EC.invisibility_of_element_located(locator)` | `page.wait_for_selector(selector, state="hidden")` | |

### 3. Strategia per i Bot
La migrazione avverrà in parallelo:
1.  **Coesistenza:** Selenium e Playwright coisteranno durante la transizione.
2.  **Bot per Bot:** Ogni bot verrà migrato e testato singolarmente.
3.  **Cleanup:** Rimozione di Selenium e `webdriver-manager` a migrazione completata.

## Dettagli Tecnici

### Gestione Download
Playwright gestisce i download tramite eventi:
```python
with page.expect_download() as download_info:
    page.click("button#download")
download = download_info.value
download.save_as(path)
```

### Headless & Anti-Detection
Useremo Playwright con parametri di evasione e profili persistenti per mantenere la compatibilità con i portali ISAB e SafeWork.

### Logging & Screenshot
La logica di `save_error_state` verrà portata in Playwright usando `page.screenshot()` e `page.content()`.

---
*Ultimo aggiornamento: 2026-04-02*
