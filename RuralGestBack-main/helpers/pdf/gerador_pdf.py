from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors  
from datetime import datetime
import os

def gerar_pdf_solicitacao(solicitacao, tipo_doc, nome_arquivo):
    """
    Gera um ficheiro PDF físico para a Prefeitura de Pirpirituba.
    """
    output_folder = "documentos_gerados"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    caminho_completo = os.path.join(output_folder, nome_arquivo)
    
    c = canvas.Canvas(caminho_completo, pagesize=A4)
    width, height = A4
    
   
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)
    
    # --- CABEÇALHO ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 2*cm, "Prefeitura Municipal de Pirpirituba")
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, height - 2.8*cm, "Secretaria de Agricultura - RuralGest")
    
    c.line(2*cm, height - 3.2*cm, 19*cm, height - 3.2*cm)
    
    # --- TÍTULO ---
    c.setFont("Helvetica-Bold", 14)
    status_upper = solicitacao.status.upper()
    
    if status_upper == "CONCLUÍDA":
        titulo = "RELATÓRIO DE CONCLUSÃO DE SERVIÇO."
        # REMOVIDO QUALQUER CÓDIGO QUE MUDE PARA VERDE
    else:
        titulo = "PROTOCOLO DE SOLICITAÇÃO"

    # Reforçar preto antes de escrever o título
    c.setFillColor(colors.black) 
    c.drawCentredString(width / 2, height - 5*cm, titulo)
    
    # --- CORPO DO TEXTO ---
    c.setFont("Helvetica", 12)
    y = height - 7*cm
    
    def escrever_linha(label, valor, destaque=False):
        nonlocal y
        # Reforçar preto em cada linha
        c.setFillColor(colors.black)
        
        if destaque:
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 12)
        
        valor_str = str(valor) if valor is not None else "N/A"
        c.drawString(2.5*cm, y, f"{label}: {valor_str}")
        y -= 1*cm

    escrever_linha("Protocolo Nº", str(solicitacao.id), destaque=True)
    
    data_sol = solicitacao.data_solicitacao.strftime("%d/%m/%Y") if solicitacao.data_solicitacao else "-"
    escrever_linha("Data da Solicitação", data_sol)
    
    escrever_linha("Agricultor", solicitacao.agricultor.nome)
    escrever_linha("CPF", solicitacao.agricultor.cpf)
    escrever_linha("Propriedade", solicitacao.propriedade.terreno)
    escrever_linha("Serviço", solicitacao.servico.nome_servico)
    
    if status_upper == "CONCLUÍDA":
        y -= 0.5*cm
        c.line(2.5*cm, y + 0.5*cm, 18*cm, y + 0.5*cm)
        
        data_exec = solicitacao.data_execucao.strftime("%d/%m/%Y") if solicitacao.data_execucao else "N/A"
        escrever_linha("Executado em", data_exec, destaque=True)
        
        veiculo_nome = solicitacao.veiculo.nome if solicitacao.veiculo else "N/A"
        escrever_linha("Equipamento", veiculo_nome)
        
        y -= 1*cm
        c.setFont("Helvetica-Oblique", 11)
        c.drawString(2.5*cm, y, "O serviço foi atestado como concluído pelo técnico da secretaria.")
    else:
        escrever_linha("Status Atual", solicitacao.status, destaque=True)

    # --- RODAPÉ ---
    y -= 4*cm
    c.setStrokeColor(colors.black) # Linha preta
    c.line(5*cm, y, 16*cm, y)
    
    c.setFillColor(colors.black) # Texto preto
    c.drawCentredString(width / 2, y - 0.5*cm, "Assinatura do Agricultor")
    
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(2*cm, 2*cm, "Documento gerado pelo sistema RuralGest.")
    c.drawString(2*cm, 1.5*cm, f"Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    c.save()
    return caminho_completo