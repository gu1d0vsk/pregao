import streamlit as st

# Configuração da página
st.set_page_config(page_title="Guia de Compras - Finep", page_icon="🛒")

# CSS para dar uma melhorada no visual (opcional)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #004b8d;
        color: white;
    }
    .step-card {
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título e Cabeçalho
st.title("🛒 Guia de Compras - Áreas Demandantes")
st.markdown("Descubra o fluxo correto para sua contratação baseado no **RLCC v5**.")

# Inicializar estado da sessão para navegação
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'valor_compra' not in st.session_state:
    st.session_state.valor_compra = 0.0

# --- LÓGICA DE NAVEGAÇÃO ---

# Definição dos Limites (Conforme RLCC Art. 10 e atualizações anuais)
LIMITE_PEQUENAS_COMPRAS = 7500.00  # 10% do limite de dispensa (Art. 10 item 6)
LIMITE_DISPENSA = 75000.00         # Limite Art. 29 II Lei 13.303 (atualizado)

# PÁGINA 1: INPUT DO VALOR
if st.session_state.step == 1:
    st.markdown("### Passo 1: Qual o valor estimado da contratação?")
    
    val = st.number_input(
        "Insira o valor total (R$)", 
        min_value=0.0, 
        step=100.0, 
        format="%.2f"
    )
    
    st.info("ℹ️ Considere o valor global da contratação (ex: 12 meses de serviço ou total de bens).")

    if st.button("Verificar Procedimento ➡️"):
        if val > 0:
            st.session_state.valor_compra = val
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Por favor, insira um valor maior que zero.")

# PÁGINA 2: RESULTADO E CHECKLIST
elif st.session_state.step == 2:
    valor = st.session_state.valor_compra
    
    # Botão para voltar
    if st.button("⬅️ Voltar e simular outro valor"):
        st.session_state.step = 1
        st.rerun()
    
    st.divider()
    
    # --- CENÁRIO 1: DISPENSA DE DOCUMENTOS COMPLEXOS (< R$ 7.500) ---
    if valor <= LIMITE_PEQUENAS_COMPRAS:
        st.success(f"✅ **Faixa de Valor: Pequenas Compras (Até R$ {LIMITE_PEQUENAS_COMPRAS:,.2f})**")
        st.markdown("### 🚀 Rito Simplificado (Art. 10, Item 6 do RLCC)")
        st.write("Nesta faixa, o processo é desburocratizado para agilidade.")
        
        with st.expander("📄 Documentos Necessários (Checklist)", expanded=True):
            st.markdown("""
            * [ ] **Justificativa da Contratação**: Texto simples explicando a necessidade.
            * [ ] **Ficha Técnica**: Descrição do material/serviço (Substitui TR e ETP).
            * [ ] **Cotação Simplificada**: Preço de mercado (pode ser email, site, etc).
            * [ ] **Requisição de Compras**: No sistema interno.
            """)
            st.warning("⚠️ **Atenção:** Não é necessário elaborar Estudo Preliminar (EP) nem Termo de Referência (TR).")

    # --- CENÁRIO 2: DISPENSA DE LICITAÇÃO (Entre R$ 7.500 e R$ 75.000) ---
    elif valor <= LIMITE_DISPENSA:
        st.info(f"⚖️ **Faixa de Valor: Dispensa de Licitação (Até R$ {LIMITE_DISPENSA:,.2f})**")
        st.markdown("### 📋 Contratação Direta (Art. 10, Item 2 do RLCC)")
        st.write("Você não precisa fazer uma licitação pública, mas precisa formalizar o planejamento.")
        
        with st.expander("📄 Documentos Necessários (Checklist)", expanded=True):
            st.markdown("""
            * [ ] **Estudo Preliminar (EP)**: Análise da necessidade e viabilidade (Art. 18).
            * [ ] **Termo de Referência (TR)**: Detalhamento técnico e obrigações (Art. 18).
            * [ ] **Mapa de Preços**: Mínimo de 3 cotações válidas ou justificativa (Art. 10.2.d).
            * [ ] **Requisição de Compras**: Aprovada pelo gestor.
            * [ ] **Parecer Jurídico**: Pode ser dispensado se usar minuta padrão (Art. 10.2.k).
            """)
            
        st.markdown("#### Próximos Passos:")
        st.markdown("1. Elaborar documentos no SEI.\n2. Solicitar cotações aos fornecedores.\n3. Encaminhar ao DCAD com antecedência mínima de 10 dias úteis.")

    # --- CENÁRIO 3: LICITAÇÃO (> R$ 75.000) ---
    else:
        st.warning(f"🏛️ **Faixa de Valor: Licitação (Acima de R$ {LIMITE_DISPENSA:,.2f})**")
        st.markdown("### 📢 Processo Licitatório (Lei 13.303/16)")
        st.write("O valor exige ampla concorrência (geralmente Pregão). O planejamento deve ser rigoroso.")
        
        with st.expander("📄 Documentos Necessários (Checklist)", expanded=True):
            st.markdown("""
            * [ ] **Estudo Técnico Preliminar (ETP)**: Completo, com análise de mercado.
            * [ ] **Matriz de Risco**: Obrigatória para serviços complexos/TI (Art. 41).
            * [ ] **Termo de Referência (TR)**: Critérios de julgamento e habilitação claros.
            * [ ] **Orçamento Estimado**: Pesquisa de preços rigorosa (Art. 35).
            * [ ] **Aprovação da Autoridade Competente**: Conforme alçada (Art. 3).
            """)
            
        st.markdown("#### Próximos Passos:")
        st.markdown(f"1. Planejamento deve iniciar com **120 a 180 dias** de antecedência (Art. 18.1.e).\n2. Validação técnica conjunta se for TI (Art. 20).\n3. Envio ao DCAD para elaboração do Edital.")

# Rodapé
st.markdown("---")
st.caption("Baseado no Regulamento de Licitações e Contratos (RLCC) da Finep - Versão 05/2025.")
