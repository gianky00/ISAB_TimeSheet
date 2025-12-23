    def _update_totals(self):
        total_row_idx = -1
        if self.table.rowCount() > 0:
            last_item = self.table.item(self.table.rowCount() - 1, 0)
            if last_item and last_item.text() == "TOTALI":
                total_row_idx = self.table.rowCount() - 1

        if total_row_idx == -1: return

        rows = total_row_idx
        count_prev = 0
        sum_totale_prev = 0.0
        sum_ore_sp = 0.0
        # Variabili per calcolo media (ora usate solo per compatibilità futura se richiesto)
        sum_resa = 0.0
        count_resa = 0

        for r in range(rows):
            if not self.table.isRowHidden(r):
                count_prev += 1
                is_excluded = False
                r_item = self.table.item(r, self.COL_RESA)
                if r_item:
                    resa_text = r_item.text().strip()
                    if "INS.ORE SP" in resa_text.upper():
                        is_excluded = True

                # Totale Prev (solo righe valide)
                if not is_excluded:
                    t_item = self.table.item(r, self.COL_TOTALE)
                    if t_item:
                        sum_totale_prev += self._parse_currency(t_item.text())

                # Ore Spese (TUTTE le righe, incluse INS.ORE SP per il costo totale)
                o_item = self.table.item(r, self.COL_ORE)
                if o_item:
                    sum_ore_sp += self._parse_float(o_item.text())

        self.table.item(total_row_idx, self.COL_N_PREV).setText(str(count_prev))
        self.table.item(total_row_idx, self.COL_TOTALE).setText(self._format_currency(sum_totale_prev))
        self.table.item(total_row_idx, self.COL_ORE).setText(self._format_number(sum_ore_sp))

        # Calcolo Resa Ponderata (Globale): Totale Preventivato / Ore Spese Totali
        # Sostituisce la media aritmetica precedente
        weighted_resa = 0.0
        if sum_ore_sp > 0:
            weighted_resa = sum_totale_prev / sum_ore_sp

        self.table.item(total_row_idx, self.COL_RESA).setText(self._format_number(weighted_resa))
