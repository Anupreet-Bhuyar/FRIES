import re
from typing import Dict, List


class MetricsExtractor:
    def __init__(self, pages: List[str]):
        self.text = " ".join(pages)

    def extract_metrics(self) -> Dict:
        metrics = {}

        metrics["revenue"] = self._extract_money(r"(Revenue|Total Revenue)[^\$]*\$?([\d,]+\.?\d*)")
        metrics["net_income"] = self._extract_money(r"(Net Income)[^\$]*\$?([\d,]+\.?\d*)")
        metrics["eps"] = self._extract_number(r"(EPS|Earnings per Share)[^\d]*([\d\.]+)")
        metrics["debt"] = self._extract_money(r"(Total Debt)[^\$]*\$?([\d,]+\.?\d*)")
        metrics["cash"] = self._extract_money(r"(Cash and Cash Equivalents)[^\$]*\$?([\d,]+\.?\d*)")
        metrics["operating_cash_flow"] = self._extract_money(r"(Operating Cash Flow)[^\$]*\$?([\d,]+\.?\d*)")
        metrics["revenue_yoy"] = self._extract_number(r"Revenue[^\%]*([\d\.]+)%")

        return metrics

    def _extract_money(self, pattern: str):
        match = re.search(pattern, self.text, re.IGNORECASE)
        if match:
            value = match.group(2).replace(",", "")
            return float(value)
        return None

    def _extract_number(self, pattern: str):
        match = re.search(pattern, self.text, re.IGNORECASE)
        if match:
            return float(match.group(2))
        return None
