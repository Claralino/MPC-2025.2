from __future__ import annotations
from pathlib import Path
from fpdf import FPDF
from .processing import Metrics


class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(left=30, top=30, right=20)
        self.set_auto_page_break(auto=True, margin=20)  # 20 mm from bottom

    def header(self):
        self.set_font("Times", "B", 14)  # title
        self.cell(0, 10, "Relatório - Análise de Comentários de PR", ln=True, align="C")
        self.ln(5)


    def footer(self):
        self.set_y(-20)  # 2 cm from bottom
        self.set_font("Times", size=10)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def _line(pdf: FPDF, label: str, value: str):
    pdf.set_font("Times", "B", 12)  # section title
    pdf.multi_cell(0, 8, label)
    pdf.set_font("Times", size=12) # body
    pdf.multi_cell(0, 8, value)
    pdf.ln(4)


def build_pdf(
    out_path: Path,
    repo_url: str,
    metrics: Metrics,
    group_number: str,
    participants: list[str],
):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()


    # (a) Grupo e participantes
    _line(pdf, "(a) Grupo e Participantes", f"Grupo: {group_number or '-'} | Participantes: {', '.join(participants) if participants else '-'}")
    # (b) Repositório
    _line(pdf, "(b) Repositório analisado", repo_url)
    # (c) Total de comentários
    _line(pdf, "(c) Total de comentários obtidos", str(metrics.total_comments))
    # (d) Média por PR
    _line(pdf, "(d) Nº médio de comentários por PR (amostra)", f"{metrics.avg_comments_per_pr:.2f}")
    # (e) Tamanho médio
    _line(pdf, "(e) Tamanho médio dos comentários", f"{metrics.avg_chars_per_comment:.2f} caracteres | {metrics.avg_words_per_comment:.2f} palavras")
    # (f) Obrigado/Thanks-like
    _line(pdf, "(f) Comentários contendo agradecimentos (case-insensitive)", str(metrics.thank_like_count))


    pdf.output(str(out_path))
