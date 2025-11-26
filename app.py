import streamlit as st
from datetime import datetime, timedelta
import time
import pytz
# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Cockpit Pregoeiro Finep", layout="wide", page_icon="⚖️")

# --- CONSTANTES DO EDITAL 90019/2025 ---
VALOR_ESTIMADO = 3295260.58
MIN_PATRIMONIO_LIQUIDO = VALOR_ESTIMADO * 0.10  # 10% = R$ 329.526,06
ATIVO_MINIMO_BANCO = 14000000000.00  # R$ 14 Bilhões

st.title("⚖️ Cockpit do Pregoeiro - PE 90019/2025 (Finep)")
st.markdown(f"**Objeto:** Consultoria IFRS 9 / CMN 4.966 | **Valor Máx:** R$ {VALOR_ESTIMADO:,.2f}")

# Abas para separar as funcionalidades
tab1, tab2, tab3 = st.tabs(["✅ Checklist Habilitação", "⏱️ Cronômetro de Prazos", "💬 Gerador de Textos"])

# ==============================================================================
# ABA 1: CHECKLIST DE HABILITAÇÃO (O "PENTE FINO")
# ==============================================================================
with tab1:
    st.header("Validação de Habilitação")
    
    col_fin, col_tec = st.columns(2)
    
    with col_fin:
        st.subheader("1. Qualificação Econômico-Financeira")
        st.info("Insira os índices do SICAF ou Balanço (LG, LC, SG).")
        
        lg = st.number_input("Liquidez Geral (LG)", value=0.00, step=0.01, format="%.2f")
        lc = st.number_input("Liquidez Corrente (LC)", value=0.00, step=0.01, format="%.2f")
        sg = st.number_input("Solvência Geral (SG)", value=0.00, step=0.01, format="%.2f")
        
        # Lógica do Edital: Se índice <= 1, exige PL >= 10%
        indices_ok = (lg > 1) and (lc > 1) and (sg > 1)
        aprovado_financeiro = False
        
        if indices_ok:
            st.success("✅ Índices superiores a 1.0. HABILITADO financeiramente.")
            aprovado_financeiro = True
        else:
            st.warning("⚠️ Um ou mais índices são ≤ 1.0. Verificando Patrimônio Líquido...")
            pl_empresa = st.number_input(f"Patrimônio Líquido (R$)", value=0.00, step=1000.00)
            
            if pl_empresa >= MIN_PATRIMONIO_LIQUIDO:
                st.success(f"✅ PL (R$ {pl_empresa:,.2f}) supera o mínimo de R$ {MIN_PATRIMONIO_LIQUIDO:,.2f}. HABILITADO.")
                aprovado_financeiro = True
            else:
                st.error(f"❌ PL insuficiente. Mínimo exigido: R$ {MIN_PATRIMONIO_LIQUIDO:,.2f}. INABILITADO.")

    with col_tec:
        st.subheader("2. Qualificação Técnica (Atestados)")
        
        check_ativo = st.checkbox(f"Atestado emitido por Banco com Ativo Total ≥ R$ 14 Bilhões?")
        if check_ativo:
            st.caption("✔️ Confirmação de porte da instituição financeira atendida.")
        else:
            st.caption("❌ Atenção: Verificar valor do Ativo Total no atestado.")
            
        check_escopo = st.checkbox("Escopo cita IFRS 9 / Resolução CMN 4.966?")
        check_risco = st.checkbox("Escopo cita revisão de Risco de Crédito/Precificação?")
        
        st.subheader("3. Equipe Técnica (Vínculo + Exp)")
        perfil1 = st.checkbox("Especialista IFRS 9 (10 anos + 3 projetos pós-2014)")
        perfil2 = st.checkbox("Consultor Contábil (5 anos IFRS bancário)")
        perfil3 = st.checkbox("Consultor Tributário (5 anos + CRC)")
        perfil4 = st.checkbox("Consultor de Riscos (5 anos)")
        perfil5 = st.checkbox("Especialista Modelagem (5 anos)")
        
        aprovado_tecnico = check_ativo and check_escopo and check_risco and perfil1 and perfil2 and perfil3 and perfil4 and perfil5
        
        if aprovado_tecnico:
            st.success("✅ Qualificação Técnica APROVADA")
        else:
            st.error("❌ Pendências na Qualificação Técnica")

    st.divider()
    if aprovado_financeiro and aprovado_tecnico:
        st.balloons()
        st.success("🏆 LICITANTE HABILITADO COM SUCESSO! PODE ADJUDICAR.")
    else:
        st.warning("⚠️ Licitante com pendências. Não adjudicar ainda.")

# ==============================================================================
# ABA 2: CRONÔMETRO DE PRAZOS
# ==============================================================================
with tab2:
    st.header("Calculadora de Prazos (Horário de Brasília)")
    st.markdown("Defina o prazo no chat e use a calculadora para saber a hora exata de encerramento.")
    
    col_time1, col_time2 = st.columns(2)
    
    with col_time1:
        st.subheader("Definir Prazo")
        prazo_tipo = st.radio("Selecione o tipo de prazo:", 
                              ["Envio de Proposta (2h)", "Envio de Documentos (2h)", "Intenção de Recurso (Min. 10 min)", "Personalizado"])
        
        minutos = 0
        if prazo_tipo == "Envio de Proposta (2h)" or prazo_tipo == "Envio de Documentos (2h)":
            minutos = 120
        elif prazo_tipo == "Intenção de Recurso (Min. 10 min)":
            minutos = st.slider("Minutos para Recurso", min_value=10, max_value=60, value=20)
        else:
            minutos = st.number_input("Minutos Personalizados", min_value=1, value=30)
            
        if st.button("Calcular Horário Final"):
            # DEFININDO O FUSO HORÁRIO DE BRASÍLIA
            tz_brasilia = pytz.timezone('America/Sao_Paulo')
            agora = datetime.now(tz_brasilia)
            
            final = agora + timedelta(minutes=minutos)
            
            # Formatação para mostrar apenas Hora:Minuto
            hora_formatada = final.strftime("%H:%M")
            
            st.session_state['hora_final'] = hora_formatada
            st.session_state['msg_prazo'] = f"O prazo de {minutos} minutos encerra-se às {hora_formatada} (Horário de Brasília)."

    with col_time2:
        st.subheader("Resultado para o Chat")
        # Mostra o relógio atual só para você conferir se está certo
        tz_brasilia_check = pytz.timezone('America/Sao_Paulo')
        st.caption(f"Horário atual do sistema: {datetime.now(tz_brasilia_check).strftime('%H:%M:%S')}")
        
        if 'hora_final' in st.session_state:
            st.metric(label="Horário Limite (BSB)", value=st.session_state['hora_final'])
            st.code(st.session_state['msg_prazo'], language="text")
            st.info("Copie o texto acima e cole no chat do sistema.")

# ==============================================================================
# ABA 3: GERADOR DE TEXTOS (CHATBOT)
# ==============================================================================
with tab3:
    st.header("Gerador de Mensagens Padrão")
    
    situacao = st.selectbox("Selecione a situação atual:", 
                            ["Suspensão para Análise", 
                             "Solicitação de Planilha Ajustada",
                             "Solicitação de Habilitação",
                             "Abertura de Prazo Recursal",
                             "Recusa de Intenção de Recurso",
                             "Desclassificação (Preço Inexequível)"])
    
    texto_gerado = ""
    
    if situacao == "Suspensão para Análise":
        data_retorno = st.text_input("Data prevista de retorno (opcional)", "a ser informada via sistema")
        texto_gerado = f"Srs. Licitantes, a sessão será suspensa neste momento para análise detalhada da documentação técnica e contábil, com base no item 14.2 do Edital. A data de retomada será {data_retorno}. Acompanhem as mensagens pelo sistema."
        
    elif situacao == "Solicitação de Planilha Ajustada":
        texto_gerado = "Srs. Licitantes, convoco a empresa classificada provisoriamente em 1º lugar para o envio da Planilha de Preços readequada ao lance vencedor (Anexo II), no prazo de 2 (duas) horas, conforme Item 10.1 do Edital. Atentem-se para não ultrapassar duas casas decimais."
        
    elif situacao == "Solicitação de Habilitação":
        texto_gerado = "Srs. Licitantes, solicito o envio dos documentos de Habilitação (Jurídica, Fiscal, Econômica e Técnica) via sistema, no prazo de 2 (duas) horas, conforme Item 13.5 do Edital. Lembro que os atestados devem cumprir o requisito de Ativo Total (R$ 14 Bi) do item 13.7.4."
        
    elif situacao == "Abertura de Prazo Recursal":
        tempo = st.text_input("Tempo concedido (min)", "20")
        texto_gerado = f"Srs. Licitantes, declaro o vencedor do certame. Abro neste momento o prazo de {tempo} minutos para manifestação motivada de intenção de recurso, conforme Item 15.1 do Edital. A não manifestação imediata e motivada neste prazo implicará na decadência do direito de recurso."
        
    elif situacao == "Recusa de Intenção de Recurso":
        motivo = st.text_input("Motivo da recusa", "alegação genérica sobre preços, sem apontar vício específico")
        texto_gerado = f"Pregoeiro indefere a intenção de recurso registrada pela licitante, pois a manifestação não apresentou motivação concreta ou fática, tratando-se apenas de {motivo}. Conforme jurisprudência do TCU e item 15.1.1 do Edital, a falta de motivação imediata acarreta a perda do direito."

    elif situacao == "Desclassificação (Preço Inexequível)":
        texto_gerado = "A proposta foi desclassificada por apresentar preço manifestamente inexequível, inferior a 30% da média dos lances ofertados, conforme critério objetivo estabelecido no item 10.2.4.4 do Edital, não tendo a licitante demonstrado sua viabilidade."

    st.subheader("Texto para Copiar:")
    st.code(texto_gerado, language="text")
